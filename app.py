import os
import csv
import math
import random
import requests # type: ignore
import openai
from flask import Flask, render_template, request # type: ignore

app = Flask(__name__)

AIRPORTS_CSV = os.path.join("data", "airports.csv")
RUNWAYS_CSV = os.path.join("data", "runways.csv")
AIRCRAFT_CSV = os.path.join("data", "aircraft.csv")  # Updated to match your file location

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
AVWX_API_KEY = os.getenv("AVWX_API_KEY")

def haversine(lat1, lon1, lat2, lon2):
    R = 3440.065  # Radius of Earth in nautical miles
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    dphi = math.radians(float(lat2) - float(lat1))
    dlambda = math.radians(float(lon2) - float(lon1))
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

def load_aircraft():
    aircraft = []
    if os.path.exists(AIRCRAFT_CSV):
        try:
            with open(AIRCRAFT_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Compose display name from Make, Model, ICAO Code
                    name = f"{row['Make']} {row['Model']} ({row['ICAO Code']})"
                    aircraft.append({
                        'name': name,
                        'icao_code': row['ICAO Code'],
                        'max_passengers': int(row['Max Passengers']),
                        'min_landing_distance': int(row['Min Takeoff Distance (ft)']),
                        'max_range': int(row['Max Range (nm)'])
                    })
        except Exception as e:
            print(f"Error loading aircraft.csv: {e}")
    return aircraft

def load_airports():
    with open(AIRPORTS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def load_runways():
    with open(RUNWAYS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def get_airport_by_icao(airports, icao):
    icao = icao.upper()
    for a in airports:
        if ((a.get("icao_code") and a["icao_code"].upper() == icao) or
            (a.get("gps_code") and a["gps_code"].upper() == icao) or
            (a.get("iata_code") and a["iata_code"].upper() == icao)):
            return a
    return None

def runways_for_airport_id(runways, airport_id):
    return [r for r in runways if r["airport_ref"] == airport_id]

def find_destinations(dep_icao, min_dist, max_dist, min_rwy_len, surfaces, max_pax):
    airports = load_airports()
    runways = load_runways()
    dep_airport = get_airport_by_icao(airports, dep_icao)
    if not dep_airport:
        return []

    dep_lat = float(dep_airport["latitude_deg"])
    dep_lon = float(dep_airport["longitude_deg"])

    # Build runway info: {airport_ref: [runways]}
    rwys_by_airport = {}
    for rwy in runways:
        rwys_by_airport.setdefault(rwy["airport_ref"], []).append(rwy)

    results = []
    for airport in airports:
        # Skip departure airport itself
        if ((airport.get("icao_code") and airport["icao_code"].upper() == dep_icao) or
            (airport.get("gps_code") and airport["gps_code"].upper() == dep_icao) or
            (airport.get("iata_code") and airport["iata_code"].upper() == dep_icao)):
            continue

        # Find at least one runway meeting length and surface requirements
        airport_runways = rwys_by_airport.get(airport["id"], [])
        valid_rwy = False
        for rwy in airport_runways:
            try:
                length = int(rwy["length_ft"] or 0)
                surface = (rwy["surface"] or "").lower()
                if length >= min_rwy_len and any(s in surface for s in surfaces):
                    valid_rwy = True
                    break
            except Exception:
                continue
        if not valid_rwy:
            continue

        # Calculate distance
        try:
            dist = haversine(dep_lat, dep_lon, float(airport["latitude_deg"]), float(airport["longitude_deg"]))
        except Exception:
            continue
        if not (min_dist <= dist <= max_dist):
            continue

        icao_out = airport.get("icao_code") or airport.get("gps_code") or airport.get("iata_code") or ""
        results.append({
            "icao": icao_out,
            "name": airport.get("name", ""),
            "location": f"{airport.get('municipality','')}, {airport.get('iso_region','')}"
        })
    return results

def fetch_avwx_metar(icao):
    key = AVWX_API_KEY
    if not key or not icao or len(icao) != 4 or not icao.isalpha():
        return "No API key or valid ICAO code."
    url = f"https://avwx.rest/api/metar/{icao}"
    headers = {
        "Authorization": key,
        "Accept": "application/json"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.ok:
            if not resp.text.strip():
                return "No METAR available (empty response)."
            try:
                data = resp.json()
            except Exception as e:
                return f"AVWX METAR error: Invalid JSON ({resp.text[:200]})"
            return data.get("raw", "No METAR found.")
        else:
            return f"AVWX METAR error: HTTP {resp.status_code} ({resp.text[:200]})"
    except Exception as e:
        return f"AVWX METAR error: {e}"

def fetch_avwx_taf(icao):
    key = AVWX_API_KEY
    if not key or not icao or len(icao) != 4 or not icao.isalpha():
        return ""
    url = f"https://avwx.rest/api/taf/{icao}"
    headers = {
        "Authorization": key,
        "Accept": "application/json"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.ok:
            if not resp.text.strip():
                return ""
            try:
                data = resp.json()
            except Exception as e:
                return ""
            return data.get("raw", "")
        else:
            return ""
    except Exception:
        return ""

def add_icao_field(airport):
    airport["icao"] = airport.get("icao_code") or airport.get("gps_code") or airport.get("iata_code") or ""

def generate_openai_scenario(dep, dest, distance_nm, dep_metar, dest_metar, dest_taf, pax):
    prompt = (
        f"Write a single-paragraph, immersive, and realistic scenario for a virtual charter flight "
        f"from {dep['name']} ({dep['icao']}) to {dest['name']} ({dest['icao']}). The distance is {int(distance_nm)} nautical miles. "
        f"Departure airport METAR: {dep_metar}. Destination airport METAR: {dest_metar}. Destination TAF: {dest_taf}. You have {pax} passengers. "
        "Focus on the reason for the trip and the passenger background. "
        "Only mention weather at departure or destination if it is notable or will directly affect the flight. "
        "Do NOT invent in-flight emergencies, do NOT discuss enroute weather unless the real METAR/TAF suggests it, and do NOT continue past the first paragraph."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip().split('\n\n')[0]  # Only the first paragraph
    except Exception as e:
        return f"OpenAI error: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    error = ""
    random_scenario = None
    weather_brief_dep = None
    weather_brief_dest = None
    airport_info = None
    results = []
    aircraft_list = load_aircraft()
    user_input = {
        "departure_icao": "",
        "min_distance": "50",
        "max_distance": "500",
        "min_runway_length": "2000",
        "surface": ["turf", "asph", "grvl", "concrete", "dirt"],
        "max_passengers": "6",
        "max_range": "",
        "aircraft_selected": ""
    }
    if request.method == 'POST':
        try:
            dep_icao = request.form['departure_icao'].strip().upper()
            min_dist = float(request.form['min_distance'])
            max_dist = float(request.form['max_distance'])
            min_rwy_len = int(request.form['min_runway_length'])
            surfaces = [s.lower() for s in request.form.getlist('surface')]
            max_pax = int(request.form['max_passengers'])
            max_range = request.form.get('max_range', '').strip()
            aircraft_selected = request.form.get('aircraft_selected', '').strip()
            user_input.update({
                "departure_icao": dep_icao,
                "min_distance": str(min_dist),
                "max_distance": str(max_dist),
                "min_runway_length": str(min_rwy_len),
                "surface": surfaces,
                "max_passengers": str(max_pax),
                "max_range": max_range,
                "aircraft_selected": aircraft_selected
            })
            # Restrict max_distance by aircraft max_range if selected
            if max_range:
                try:
                    max_range_val = int(max_range)
                    if max_dist > max_range_val:
                        error = f"Selected aircraft range is {max_range_val} nm. Max distance cannot exceed this."
                        max_dist = max_range_val
                        user_input["max_distance"] = str(max_range_val)
                except Exception:
                    error = "Invalid aircraft max range."

            if not dep_icao:
                error = "Departure ICAO is required."
            elif not surfaces:
                error = "Please select at least one runway surface type."
            else:
                results = find_destinations(dep_icao, min_dist, max_dist, min_rwy_len, surfaces, max_pax)
                if not results:
                    error = "No results found with the current filters."
                else:
                    dep_airport = get_airport_by_icao(load_airports(), dep_icao)
                    dest = random.choice(results)
                    airports = load_airports()
                    dest_full = None
                    for a in airports:
                        if a.get("icao_code") == dest["icao"] or a.get("gps_code") == dest["icao"]:
                            dest_full = a
                            break
                    distance = haversine(
                        float(dep_airport["latitude_deg"]), float(dep_airport["longitude_deg"]),
                        float(dest_full["latitude_deg"]), float(dest_full["longitude_deg"])
                    )
                    add_icao_field(dep_airport)
                    add_icao_field(dest_full)
                    dep_metar = fetch_avwx_metar(dep_airport["icao"])
                    dest_metar = fetch_avwx_metar(dest_full["icao"])
                    dest_taf = fetch_avwx_taf(dest_full["icao"])
                    weather_brief_dep = dep_metar
                    weather_brief_dest = f"METAR: {dest_metar}\nTAF: {dest_taf}"
                    scenario = generate_openai_scenario(dep_airport, dest_full, distance, dep_metar, dest_metar, dest_taf, max_pax)
                    random_scenario = scenario
                    airport_info = {
                        "icao": dest_full["icao"],
                        "name": dest_full["name"],
                        "location": f"{dest_full.get('municipality','')}, {dest_full.get('iso_region','')}",
                        "elevation": dest_full.get("elevation_ft", ""),
                        "runway": "See below"
                    }
                    runways = load_runways()
                    rwylist = [r for r in runways if r["airport_ref"] == dest_full["id"] and
                               int(r["length_ft"] or 0) >= min_rwy_len and
                               any(s in (r["surface"] or "").lower() for s in surfaces)]
                    if rwylist:
                        best_rwy = sorted(rwylist, key=lambda x: -int(x["length_ft"] or 0))[0]
                        airport_info["runway"] = (
                            f"{best_rwy['ident']}: {best_rwy['length_ft']} ft, {best_rwy['surface']}"
                        )
                    else:
                        airport_info["runway"] = "No suitable runway found."
        except Exception as e:
            error = f"Error: {e}"
    return render_template(
        'index.html',
        error=error,
        user_input=user_input,
        random_scenario=random_scenario,
        weather_brief_dep=weather_brief_dep,
        weather_brief_dest=weather_brief_dest,
        airport_info=airport_info,
        aircraft_list=aircraft_list
    )

@app.route('/changelog')
def changelog():
    return render_template('changelog.html')

if __name__ == '__main__':
    app.run(debug=True)