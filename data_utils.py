import pandas as pd
from geopy.distance import geodesic
import requests

# Load your CSV data once when module loads
airports_df = pd.read_csv("/data/airports.csv")
runways_df = pd.read_csv("/data/runways.csv")

# Ensure runway lengths are numeric (in case of bad or missing data)
runways_df['length_ft'] = pd.to_numeric(runways_df['length_ft'], errors='coerce')

def get_airports_within_range(origin_icao, min_distance_nm=0, max_distance_nm=300):
    # Find origin airport lat/lon
    origin_row = airports_df[airports_df['ident'] == origin_icao]
    if origin_row.empty:
        return []  # Origin ICAO not found
    
    origin_lat = float(origin_row.iloc[0]['latitude_deg'])
    origin_lon = float(origin_row.iloc[0]['longitude_deg'])

    airports = []

    for _, row in airports_df.iterrows():
        lat, lon = float(row['latitude_deg']), float(row['longitude_deg'])
        distance_nm = geodesic((origin_lat, origin_lon), (lat, lon)).nautical

        if min_distance_nm <= distance_nm <= max_distance_nm:
            airport = row.to_dict()
            airport['distance_nm'] = round(distance_nm, 1)
            airports.append(airport)

    return sorted(airports, key=lambda x: x['distance_nm'])

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

def get_runways_for_airport(icao_code, min_runway_length_ft=0):
    """
    Get runways for an airport filtered by minimum runway length in feet.
    """
    airport_runways = runways_df[runways_df['airport_ident'] == icao_code]
    if airport_runways.empty:
        return []
    
    filtered_runways = airport_runways[airport_runways['length_ft'] >= min_runway_length_ft]

    # Convert to list of dicts for easier templating
    runways_list = filtered_runways.to_dict(orient='records')

    return runways_list
