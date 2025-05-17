import pandas as pd
import os
import requests
from geopy.distance import geodesic
from xml.etree import ElementTree as ET

# Paths to CSVs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AIRPORTS_FILE = os.path.join(BASE_DIR, "data", "airports.csv")
RUNWAYS_FILE = os.path.join(BASE_DIR, "data", "runways.csv")

# Load CSVs
airports_df = pd.read_csv(AIRPORTS_FILE)
runways_df = pd.read_csv(RUNWAYS_FILE)

def get_airports_within_range(origin_lat, origin_lon, min_distance_nm=0, max_distance_nm=300):
    airports = []

    for _, row in airports_df.iterrows():
        lat, lon = row['latitude_deg'], row['longitude_deg']
        distance_nm = geodesic((origin_lat, origin_lon), (lat, lon)).nautical

        if min_distance_nm <= distance_nm <= max_distance_nm:
            airport = row.to_dict()
            airport['distance_nm'] = round(distance_nm, 1)
            airports.append(airport)

    return sorted(airports, key=lambda x: x['distance_nm'])


def get_runways_for_airport(ident, min_runway_length_ft=3000):
    runways = runways_df[runways_df['airport_ident'] == ident]
    filtered = runways[runways['length_ft'] >= min_runway_length_ft]
    return filtered.to_dict(orient='records')


def get_metar(icao_code):
    url = f"https://aviationweather.gov/adds/dataserver_current/httpparam?" \
          f"dataSource=metars&requestType=retrieve&format=xml&stationString={icao_code}&hoursBeforeNow=1"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            metar = root.find(".//raw_text")
            return metar.text if metar is not None else "No METAR found"
        else:
            return f"Failed to fetch METAR: HTTP {response.status_code}"
    except Exception as e:
        return f"Error fetching METAR: {e}"


def get_weather_data(icao_code):
    url = f"https://aviationweather.gov/api/data/metar?ids={icao_code}&format=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            return data[0].get("raw_text", "No METAR available.")
        return "No METAR found."
    except Exception as e:
        return f"Weather fetch error: {e}"