import random
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    R = 3440.065  # nautical miles
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def get_random_destination(origin_icao, airports, max_nm=None, min_nm=None):
    origin = next((a for a in airports if a['ident'] == origin_icao), None)
    if not origin:
        return None
    lat1, lon1 = origin['latitude_deg'], origin['longitude_deg']
    eligible = []
    for a in airports:
        if a['ident'] == origin_icao:
            continue
        lat2, lon2 = a['latitude_deg'], a['longitude_deg']
        dist = haversine(lat1, lon1, lat2, lon2)
        if (not min_nm or dist >= min_nm) and (not max_nm or dist <= max_nm):
            eligible.append(a)
    return random.choice(eligible)['ident'] if eligible else None
