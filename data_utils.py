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
    # Unchanged from previous version
    try:
        url = f"https://aviationweather.gov/api/data/metar?ids={icao_code}&format=json"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if not data:
            return {"message": f"No METAR data found for {icao_code}"}
        metar = data[0]
        return {
            "raw": metar.get("raw_text", ""),
            "station": metar.get("station_id", icao_code),
            "observation_time": metar.get("observation_time", ""),
            "temperature_c": metar.get("temp_c", None),
            "dewpoint_c": metar.get("dewpoint_c", None),
            "wind_direction": metar.get("wind_dir_degrees", None),
            "wind_speed_kt": metar.get("wind_speed_kt", None),
            "visibility_statute_mi": metar.get("visibility_statute_mi", None),
            "altim_in_hg": metar.get("altim_in_hg", None),
            "flight_category": metar.get("flight_category", None),
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": f"Could not fetch weather for {icao_code}"
        }