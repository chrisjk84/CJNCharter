import csv
import random
from math import radians, cos, sin, asin, sqrt

def load_airports(filepath='data/airports.csv'):
    with open(filepath, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def load_runways(filepath='data/runways.csv'):
    with open(filepath, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def filter_airports_by_runway_length(airports, runways, min_length):
    runway_lengths = {}
    for rwy in runways:
        ident = rwy['airport_ident']
        try:
            length = int(rwy.get('length_ft', 0) or 0)
            if ident not in runway_lengths or length > runway_lengths[ident]:
                runway_lengths[ident] = length
        except:
            continue
    return [a for a in airports if runway_lengths.get(a['ident'], 0) >= min_length]

def haversine(lat1, lon1, lat2, lon2):
    # Radius of earth in nautical miles
    R = 3440.065
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def get_random_destination(origin_icao, airports, max_nm=None, min_nm=None):
    origin = next((a for a in airports if a['ident'] == origin_icao), None)
    if not origin:
        return None

    lat1 = origin['latitude_deg']
    lon1 = origin['longitude_deg']

    eligible = []
    for airport in airports:
        if airport['ident'] == origin_icao:
            continue
        lat2 = airport['latitude_deg']
        lon2 = airport['longitude_deg']
        dist = haversine(lat1, lon1, lat2, lon2)
        if (min_nm is None or dist >= min_nm) and (max_nm is None or dist <= max_nm):
            eligible.append(airport)

    if not eligible:
        return None

    return random.choice(eligible)['ident']
