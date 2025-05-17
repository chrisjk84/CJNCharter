import csv
from geopy.distance import geodesic
import requests

def get_airports_within_range(origin_icao, min_distance_nm=0, max_distance_nm=300):
    # First, find the origin airport's coordinates
    origin_lat = origin_lon = None
    with open("data/airports.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ident'] == origin_icao:
                try:
                    origin_lat = float(row['latitude_deg'])
                    origin_lon = float(row['longitude_deg'])
                except (TypeError, ValueError):
                    return []
                break
    if origin_lat is None or origin_lon is None:
        return []

    # Now process airports line by line to find those within range
    results = []
    with open("data/airports.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                lat = float(row['latitude_deg'])
                lon = float(row['longitude_deg'])
            except (TypeError, ValueError):
                continue
            distance_nm = geodesic((origin_lat, origin_lon), (lat, lon)).nautical
            if min_distance_nm <= distance_nm <= max_distance_nm:
                row_copy = dict(row)
                row_copy['distance_nm'] = round(distance_nm, 1)
                results.append(row_copy)
    return sorted(results, key=lambda x: x['distance_nm'])

def get_runways_for_airport(icao_code, min_runway_length_ft=0):
    runways = []
    with open("data/runways.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ident'] == icao_code:
                try:
                    length = float(row['length_ft'])
                except (TypeError, ValueError):
                    continue
                if length >= min_runway_length_ft:
                    runways.append(dict(row))
    return runways

def get_weather_data(icao_code):
    """
    Fetch METAR weather data from aviationweather.gov.
    """
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