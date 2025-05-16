import csv
import random
import os
import math

AIRPORTS_CSV = os.path.join(os.path.dirname(__file__), '..', 'airports.csv')

def load_airports():
    airports = []
    with open(AIRPORTS_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['type'] in ('large_airport', 'medium_airport'):
                try:
                    row['latitude_deg'] = float(row['latitude_deg'])
                    row['longitude_deg'] = float(row['longitude_deg'])
                    airports.append(row)
                except ValueError:
                    continue
    return airports

def haversine(lat1, lon1, lat2, lon2):
    R = 3440.065  # Nautical miles
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_random_destination(origin_icao, max_nm=None, min_nm=None):
    # Find origin airport
    origin = next((a for a in airports if a['ident'] == origin_icao), None)
    if not origin:
        return None

    lat1 = origin['latitude_deg']
    lon1 = origin['longitude_deg']

    # Filter airports by distance range
    eligible = []
    for a in airports:
        if a['ident'] == origin_icao:
            continue
        lat2 = a['latitude_deg']
        lon2 = a['longitude_deg']
        distance = haversine(lat1, lon1, lat2, lon2)
        if min_nm <= distance <= max_nm:
            eligible.append((a, distance))

    if not eligible:
        return None

    chosen, _ = random.choice(eligible)
    return chosen
