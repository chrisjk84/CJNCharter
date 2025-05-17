import csv
import math
import os
from flask import Flask, render_template, request

app = Flask(__name__)

AIRPORTS_CSV = os.path.join("data", "airports.csv")
RUNWAYS_CSV = os.path.join("data", "runways.csv")


def haversine(lat1, lon1, lat2, lon2):
    # Calculate great-circle distance between two points (in NM)
    R = 3440.065  # Radius of Earth in nautical miles
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    dphi = math.radians(float(lat2) - float(lat1))
    dlambda = math.radians(float(lon2) - float(lon1))
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))


def load_airports():
    with open(AIRPORTS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def load_runways():
    with open(RUNWAYS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def get_airport_by_icao(airports, icao):
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

    # Filter airports
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

        # Output ICAO, Name, Location (Municipality, State/Region)
        icao_out = airport.get("icao_code") or airport.get("gps_code") or airport.get("iata_code") or ""
        results.append({
            "icao": icao_out,
            "name": airport.get("name", ""),
            "location": f"{airport.get('municipality','')}, {airport.get('iso_region','')}"
        })
    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    error = ""
    user_input = {
        "departure_icao": "",
        "min_distance": "50",
        "max_distance": "500",
        "min_runway_length": "2000",
        "surface": ["turf", "asph", "grvl", "concrete", "dirt"],
        "max_passengers": "6"
    }
    if request.method == 'POST':
        try:
            dep_icao = request.form['departure_icao'].strip().upper()
            min_dist = float(request.form['min_distance'])
            max_dist = float(request.form['max_distance'])
            min_rwy_len = int(request.form['min_runway_length'])
            surfaces = [s.lower() for s in request.form.getlist('surface')]
            max_pax = int(request.form['max_passengers'])
            user_input.update({
                "departure_icao": dep_icao,
                "min_distance": str(min_dist),
                "max_distance": str(max_dist),
                "min_runway_length": str(min_rwy_len),
                "surface": surfaces,
                "max_passengers": str(max_pax)
            })
            if not dep_icao:
                error = "Departure ICAO is required."
            elif not surfaces:
                error = "Please select at least one runway surface type."
            else:
                results = find_destinations(dep_icao, min_dist, max_dist, min_rwy_len, surfaces, max_pax)
                if not results:
                    error = "No results found with the current filters."
        except Exception as e:
            error = f"Error: {e}"
    return render_template('index.html', results=results, error=error, user_input=user_input)


if __name__ == '__main__':
    app.run(debug=True)