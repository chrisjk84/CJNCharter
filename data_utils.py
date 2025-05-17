import sqlite3
from geopy.distance import geodesic
import requests

def get_connection():
    return sqlite3.connect("data/aviation.db")

def get_airports_within_range(origin_icao, min_distance_nm=0, max_distance_nm=300):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT latitude_deg, longitude_deg FROM airports WHERE ident=?", (origin_icao,))
    row = c.fetchone()
    if not row:
        conn.close()
        return []
    origin_lat, origin_lon = float(row[0]), float(row[1])

    # You can optimize this query further by restricting latitude/longitude bounds if needed.
    c.execute("SELECT * FROM airports")
    columns = [desc[0] for desc in c.description]
    results = []
    for airport in c.fetchall():
        airport_dict = dict(zip(columns, airport))
        try:
            lat = float(airport_dict['latitude_deg'])
            lon = float(airport_dict['longitude_deg'])
        except (TypeError, ValueError):
            continue
        distance_nm = geodesic((origin_lat, origin_lon), (lat, lon)).nautical
        if min_distance_nm <= distance_nm <= max_distance_nm:
            airport_dict['distance_nm'] = round(distance_nm, 1)
            results.append(airport_dict)
    conn.close()
    return sorted(results, key=lambda x: x['distance_nm'])

def get_runways_for_airport(icao_code, min_runway_length_ft=0):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM runways WHERE ident=? AND length_ft>=?",
        (icao_code, min_runway_length_ft)
    )
    columns = [desc[0] for desc in c.description]
    runways = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return runways

def get_weather_data(icao_code):
    """
    Fetch METAR weather data from AVWX API.
    """
    api_key = os.environ.get("AVWX_API_KEY")
    if not api_key:
        return {"error": "AVWX_API_KEY not set in environment"}

    url = f"https://avwx.rest/api/metar/{icao_code}"
    headers = {
        "Authorization": api_key,
        "Accept": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        # AVWX returns a lot; here’s a simple mapping that you can customize:
        return {
            "raw": data.get("raw", ""),
            "station": data.get("station", icao_code),
            "observation_time": data.get("time", {}).get("dt", ""),
            "temperature_c": data.get("temperature", {}).get("value", None),
            "dewpoint_c": data.get("dewpoint", {}).get("value", None),
            "wind_direction": data.get("wind_direction", {}).get("value", None),
            "wind_speed_kt": data.get("wind_speed", {}).get("value", None),
            "visibility_statute_mi": data.get("visibility", {}).get("repr", None),
            "altim_in_hg": data.get("altimeter", {}).get("value", None),
            "flight_category": data.get("flight_rules", None),
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": f"Could not fetch weather for {icao_code} from AVWX"
        }