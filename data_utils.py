import csv
import math
import requests
import os

AIRPORTS_CSV = "data/airports.csv"  # Path to your CSV file with airport data

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_airport_info(icao_code):
    with open(AIRPORTS_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ident'].upper() == icao_code.upper():
                return {
                    'ident': row['ident'],
                    'name': row['name'],
                    'latitude': float(row['latitude_deg']),
                    'longitude': float(row['longitude_deg']),
                    'elevation': row.get('elevation_ft', ''),
                }
    return None

def get_nearby_airports(lat, lon, min_dist_km=0, max_dist_km=1000):
    nearby = []
    with open(AIRPORTS_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['type'] not in ['small_airport', 'medium_airport', 'large_airport']:
                # skip helipads, closed airports, etc.
                continue
            try:
                air_lat = float(row['latitude_deg'])
                air_lon = float(row['longitude_deg'])
            except (ValueError, KeyError):
                continue
            dist = haversine(lat, lon, air_lat, air_lon)
            if min_dist_km <= dist <= max_dist_km:
                nearby.append({
                    'ident': row['ident'],
                    'name': row['name'],
                    'distance_km': round(dist, 1)
                })
    nearby.sort(key=lambda x: x['distance_km'])
    return nearby

def get_weather_data(icao_code):
    # Placeholder for weather data fetching
    # Return dict with keys like 'metar', 'taf', etc.
    # Implement as needed or use your existing code.
    return {
        'metar': f"METAR data for {icao_code}",
        'taf': f"TAF data for {icao_code}"
    }

def get_runways(icao_code):
    # Placeholder for runway info fetching
    # Return list of runways with lengths and surface types
    return [
        {'id': '09/27', 'length_ft': 5000, 'surface': 'asphalt'},
        {'id': '18/36', 'length_ft': 3000, 'surface': 'grass'},
    ]
