import pandas as pd
from geopy.distance import geodesic
import requests

# Load your CSV data once when module loads
airports_df = pd.read_csv("airports.csv")
runways_df = pd.read_csv("runways.csv")

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
    Fetch METAR or weather data for the airport.
    Here, as an example, using AVWX API or any public METAR service.
    Replace API call with your real API key and URL.
    """
    try:
        # Example URL for a public METAR API (replace with real one or your preferred source)
        url = f"https://avwx.rest/api/metar/{icao_code}?options=summary"
        headers = {
            "Authorization": "AVWX_API_KEY"
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Example: return a simple dictionary with main weather info
        weather = {
            "raw": data.get("raw", ""),
            "summary": data.get("summary", ""),
            "temperature_c": data.get("temperature", {}).get("value"),
            "wind_direction": data.get("wind_direction", {}).get("value"),
            "wind_speed_kt": data.get("wind_speed", {}).get("value"),
            "visibility": data.get("visibility", {}).get("value"),
            "clouds": data.get("clouds", [])
        }
        return weather
    except Exception as e:
        # On error, return a placeholder or empty info
        return {"error": str(e), "message": f"Could not fetch weather for {icao_code}"}


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
