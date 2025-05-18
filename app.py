<!DOCTYPE html>
<html lang="en">
<head>
    <title>CJX Aviation Network - Pilot Portal</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root {
            --cjx-black: #141414;
            --cjx-darkgray: #23272a;
            --cjx-lightgray: #e0e0e0;
            --cjx-white: #ffffff;
            --cjx-accent: #6c757d;
            --cjx-blue: #4682b4;
        }
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            background: var(--cjx-black);
            color: var(--cjx-lightgray);
            font-family: 'Segoe UI', 'Arial', 'Helvetica Neue', sans-serif;
        }
        .cjx-header {
            background: var(--cjx-darkgray);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 2rem 2rem 1rem 2rem;
            border-bottom: 2px solid var(--cjx-accent);
            position: relative;
        }
        .cjx-header-center {
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .cjx-logo-img {
            height: 56px;
            display: block;
            margin: 0 auto 0.6rem auto;
        }
        .cjx-tagline {
            font-size: 1.2rem;
            color: var(--cjx-lightgray);
            font-style: italic;
            opacity: 0.8;
        }
        .cjx-version {
            position: absolute;
            top: 1.2rem;
            right: 2rem;
            background: var(--cjx-accent);
            color: var(--cjx-white);
            font-size: 1.0rem;
            font-weight: 600;
            padding: 0.35em 0.9em;
            border-radius: 14px;
            letter-spacing: 1.5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.13);
            z-index: 2;
            pointer-events: none;
        }
        .cjx-content {
            max-width: 700px;
            margin: 2rem auto;
            background: var(--cjx-darkgray);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.32);
            padding: 2.5rem 2rem;
        }
        .cjx-section-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1.2rem;
            color: var(--cjx-white);
            letter-spacing: 0.5px;
            text-align: center;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        label {
            font-weight: 600;
            display: block;
            margin-bottom: 0.3rem;
            color: var(--cjx-lightgray);
            text-align: center;
        }
        .cjx-row {
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
            margin-bottom: 1.5rem;
            justify-content: center;
            width: 100%;
        }
        .cjx-row > div {
            flex: 1 1 213px;
            min-width: 213px;
            max-width: 213px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .cjx-input {
            width: 100%;
            max-width: 220px;
            padding: 0.87rem 1.12rem;
            border: 1px solid var(--cjx-accent);
            border-radius: 6px;
            background: var(--cjx-black);
            color: var(--cjx-lightgray);
            font-size: 1.15rem;
            margin-top: 0.2rem;
            box-sizing: border-box;
            font-weight: bold;
            letter-spacing: 0.09em;
            text-align: center;
        }
        .cjx-input:focus {
            border-color: var(--cjx-white);
            background: #18191a;
        }
        input[type="checkbox"] {
            accent-color: var(--cjx-accent);
            margin-right: 0.4em;
        }
        .cjx-checkbox-group label {
            display: inline-block;
            margin-right: 1.2rem;
            font-weight: normal;
        }
        button[type="submit"] {
            margin-top: 1.5rem;
            padding: 0.9rem 0;
            background: linear-gradient(90deg, var(--cjx-accent) 0%, var(--cjx-darkgray) 100%);
            color: var(--cjx-white);
            border: none;
            border-radius: 6px;
            font-size: 1.2rem;
            font-weight: bold;
            letter-spacing: 0.1em;
            cursor: pointer;
            transition: background 0.2s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        }
        button[type="submit"]:hover {
            background: linear-gradient(90deg, var(--cjx-white) 0%, var(--cjx-accent) 100%);
            color: var(--cjx-black);
        }
        .error {
            color: #ff6b6b;
            background: rgba(255,107,107,0.06);
            padding: 0.7em;
            border-radius: 6px;
            margin-top: 0.5em;
            font-weight: 600;
            text-align: center;
        }
        .cjx-dispatch-sheet {
            margin-top: 2.5rem;
            background: var(--cjx-black);
            border: 1.5px solid var(--cjx-accent);
            border-radius: 10px;
            padding: 2rem 1.5rem;
            color: var(--cjx-white);
            box-shadow: 0 4px 24px rgba(0,0,0,0.22);
        }
        .cjx-dispatch-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1.2rem;
            color: var(--cjx-lightgray);
            letter-spacing: 1px;
            text-align: center;
        }
        .cjx-info-block {
            flex: 1 1 220px;
            background: var(--cjx-darkgray);
            margin-bottom: 0.7rem;
            padding: 1rem 1rem 0.7rem 1rem;
            border-radius: 7px;
            border: 1px solid var(--cjx-accent);
        }
        .cjx-info-block b {
            color: var(--cjx-lightgray);
        }
        .cjx-weather, .cjx-scenario {
            margin-top: 1.2rem;
        }
        .cjx-weather pre,
        .cjx-scenario pre {
            background: var(--cjx-darkgray);
            color: var(--cjx-white);
            border-radius: 6px;
            padding: 1rem;
            font-family: 'Fira Mono', 'Consolas', monospace;
            font-size: 1.05rem;
            white-space: pre-wrap;
        }
        .simbrief-btn {
            display: inline-block;
            background: #6c757d;
            color: #fff;
            font-weight: bold;
            padding: 0.7em 1.8em;
            border-radius: 8px;
            text-decoration: none;
            font-size: 1.12rem;
            margin: 1.5rem 0;
            transition: background 0.16s;
        }
        .simbrief-btn:hover, .simbrief-btn:focus {
            background: #4682b4;
            color: #fff;
        }
        .cjx-footer {
            text-align: center;
            color: var(--cjx-lightgray);
            opacity: 0.85;
            font-size: 1.05rem;
            margin-top: 2.3rem;
            margin-bottom: 1.7rem;
            letter-spacing: 0.05em;
        }
        .cjx-changelog-link {
            display: inline-block;
            margin-top: 0.5em;
            color: var(--cjx-white);
            font-size: 1.1rem;
            background: var(--cjx-accent);
            padding: 0.4em 1.2em;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: background 0.16s;
        }
        .cjx-changelog-link:hover,
        .cjx-changelog-link:focus {
            background: var(--cjx-blue);
            color: var(--cjx-white);
            text-decoration: underline;
        }
        .cjx-helper-text {
            font-size: 0.98em;
            color: #bbbbbb;
            margin-bottom: 1.2em;
            margin-top: 1.3em;
            text-align: center;
            font-weight: bold;
        }
        @media (max-width: 700px) {
            .cjx-header {
                flex-direction: column;
                align-items: flex-start;
                padding: 1.2rem 0.7rem 0.8rem 0.7rem;
            }
            .cjx-version {
                position: static;
                align-self: flex-end;
                margin-bottom: 0.5rem;
                margin-top: -1.2rem;
            }
            .cjx-content, .cjx-dispatch-sheet {
                padding: 1.1rem 0.8rem;
            }
            .cjx-row {
                flex-direction: column;
                gap: 1rem;
                align-items: center;
            }
            .cjx-row > div {
                max-width: 100%;
                min-width: 0;
            }
            .cjx-logo-img {
                height: 44px;
            }
        }
    </style>
</head>
<body>
    <div class="cjx-header">
        <div class="cjx-header-center">
            <img src="{{ url_for('static', filename='CJX-Aviation-Network-logo.png') }}" alt="CJX Aviation Network Logo" class="cjx-logo-img">
            <span class="cjx-tagline">Pilot Dispatch Portal &mdash; Homebase: New Orleans, Worldwide Service</span>
        </div>
        <div class="cjx-version">V0.2.4b</div>
    </div>
    <div class="cjx-content">
        <div class="cjx-section-title">Flight Request Form</div>
        <form method="POST" id="dispatch-form">
            <label for="aircraft_select">Select Aircraft:</label>
            <select id="aircraft_select" class="cjx-input" name="aircraft_selected" style="max-width:350px;">
                <option value="">-- Select Aircraft --</option>
                {% for a in aircraft_list %}
                  <option value="{{ a.name }}"
                          data-max_passengers="{{ a.max_passengers }}"
                          data-min_landing_distance="{{ a.min_landing_distance }}"
                          data-max_range="{{ a.max_range }}">
                    {{ a.name }}
                  </option>
                {% endfor %}
            </select>
            <div class="cjx-helper-text">
                <b>Selecting aircraft auto populates fields below, but they can be changed if needed.</b>
            </div>
            <div class="cjx-row">
                <div>
                    <label>Departure ICAO:</label>
                    <input type="text" name="departure_icao" maxlength="4" required
                        value="{{ user_input.departure_icao }}"
                        style="text-transform:uppercase;"
                        class="cjx-input">
                </div>
                <div>
                    <label>Min Distance (nm):</label>
                    <input type="number" name="min_distance" value="{{ user_input.min_distance }}" min="0" required class="cjx-input">
                </div>
                <div>
                    <label>Max Distance (nm):</label>
                    <input type="number" name="max_distance" value="{{ user_input.max_distance }}" min="1" required class="cjx-input">
                </div>
                <div>
                    <label>Min Runway Length (ft):</label>
                    <input type="number" name="min_runway_length" value="{{ user_input.min_runway_length }}" min="0" required class="cjx-input">
                </div>
                <div>
                    <label>Max Passengers:</label>
                    <input type="number" name="max_passengers" value="{{ user_input.max_passengers }}" min="1" max="300" required class="cjx-input">
                </div>
                <div>
                    <label>Max Range (nm):</label>
                    <input type="number" name="max_range" value="{{ user_input.max_range if user_input.max_range is defined else '' }}" min="1" class="cjx-input" readonly>
                </div>
            </div>
            <div class="cjx-checkbox-group" style="text-align:center;">
                <label>Runway Surface:</label><br>
                <label><input type="checkbox" name="surface" value="turf" {% if 'turf' in user_input.surface %}checked{% endif %}>Grass/Turf</label>
                <label><input type="checkbox" name="surface" value="asph" {% if 'asph' in user_input.surface %}checked{% endif %}>Asphalt</label>
                <label><input type="checkbox" name="surface" value="grvl" {% if 'grvl' in user_input.surface %}checked{% endif %}>Gravel</label>
                <label><input type="checkbox" name="surface" value="concrete" {% if 'concrete' in user_input.surface %}checked{% endif %}>Concrete</label>
                <label><input type="checkbox" name="surface" value="dirt" {% if 'dirt' in user_input.surface %}checked{% endif %}>Dirt</label>
            </div>
            <button type="submit">Generate Dispatch Sheet</button>
        </form>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if random_scenario %}
            <div class="cjx-dispatch-sheet">
                {% if airport_info and user_input.departure_icao and airport_info.icao %}
                <div style="text-align:center;">
                  <a href="https://www.simbrief.com/system/dispatch.php?orig={{ user_input.departure_icao|upper }}&dest={{ airport_info.icao|upper }}" 
                     target="_blank" 
                     class="simbrief-btn">
                    Go to SimBrief Dispatch
                  </a>
                </div>
                {% endif %}
                <div class="cjx-dispatch-title">CJX Dispatch Sheet</div>
                <div class="cjx-row">
                    <div class="cjx-info-block">
                        <b>Destination:</b><br>
                        {{ airport_info.icao }} - {{ airport_info.name }}<br>
                        <span style="color:var(--cjx-accent);font-size:0.98em;">{{ airport_info.location }}</span>
                    </div>
                    <div class="cjx-info-block">
                        <b>Field Elevation:</b> {{ airport_info.elevation }} ft<br>
                        <b>Primary Runway:</b><br> {{ airport_info.runway }}
                    </div>
                </div>
                <div class="cjx-weather">
                    <b>Weather Briefing (Departure):</b>
                    <pre>{{ weather_brief_dep }}</pre>
                </div>
                <div class="cjx-weather">
                    <b>Weather Briefing (Destination):</b>
                    <pre>{{ weather_brief_dest }}</pre>
                </div>
                <div class="cjx-scenario">
                    <b>Flight Scenario:</b>
                    <pre>{{ random_scenario }}</pre>
                </div>
            </div>
        {% endif %}
    </div>
    <div class="cjx-footer">
        &copy; 2025 Chris Keever 2025
        <br>
        <a href="{{ url_for('changelog') }}" class="cjx-changelog-link">View Change Log</a>
    </div>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const aircraftSelect = document.getElementById('aircraft_select');
        const maxPassengersInput = document.querySelector('input[name="max_passengers"]');
        const minRunwayInput = document.querySelector('input[name="min_runway_length"]');
        const maxRangeInput = document.querySelector('input[name="max_range"]');
        const maxDistInput = document.querySelector('input[name="max_distance"]');

<<<<<<< HEAD
        aircraftSelect.addEventListener('change', function() {
            const selected = aircraftSelect.selectedOptions[0];
            if(selected && selected.value !== "") {
                maxPassengersInput.value = selected.dataset.max_passengers;
                minRunwayInput.value = selected.dataset.min_landing_distance;
                maxRangeInput.value = selected.dataset.max_range;
                if (maxDistInput) {
                    maxDistInput.max = selected.dataset.max_range;
                    if (parseInt(maxDistInput.value) > parseInt(selected.dataset.max_range)) {
                        maxDistInput.value = selected.dataset.max_range;
=======
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
        f"Write a short realistic scenario for a charter flight. "
        f"from {dep['name']} ({dep['icao']}) to {dest['name']} ({dest['icao']}). The distance is {int(distance_nm)} nautical miles. "
        f"Departure airport METAR: {dep_metar}. Destination airport METAR: {dest_metar}. Destination TAF: {dest_taf}. You have {pax} passengers. "
        "Focus on the reason for the trip and the passenger background. "
        "Only mention weather at departure or destination if it is notable or will directly affect the flight. "
        "Do NOT invent in-flight emergencies, do NOT discuss enroute weather unless the real METAR/TAF suggests it. "
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
>>>>>>> parent of e24b737 (Update app.py)
                    }
                }
            } else {
                maxRangeInput.value = "";
                maxDistInput.max = "";
            }
        });
    });
    </script>
</body>
</html>