import random
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    # Calculate great-circle distance in nautical miles
    R = 3440.065  # Earth radius in nautical miles
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
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
