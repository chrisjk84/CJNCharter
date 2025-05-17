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
    origin = next((a for a in airports if a['ident'].upper() == origin_icao.upper()), None)
    if not origin:
        print(f"Origin airport {origin_icao} not found.")
        return None

    try:
        lat1 = float(origin['latitude_deg'])
        lon1 = float(origin['longitude_deg'])
    except (ValueError, TypeError):
            print{f"Invalid coordinates for origin airport:{origin}")
            return None
            
    eligible = []
    for airport in airports:
        if airport['ident'].upper() == orgin_icao.upper():
            continue
        try:
            lat2 = float(airport['latitude_deg'])
            lon2 = float(airport['longitude_deg'])
            dist = haversine(lat1, lon1, lat2, lon2)
            if (min_nm is None or dist >= min_nm) and (max_nm is None or dist <= max_nm):
                eligible.append(airport)
        except (ValueError, TypeError):
            continue # Skip if data is invalid
    
    if not eligible:
        print ("No eligible destinations found within given parameters.")
        print (f"Found {len(eligible)} eligible destinations from {origin_icao}")
        return home

    return random.choice(eligible)['ident']
