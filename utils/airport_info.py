import csv
from collections import defaultdict

def load_runway_data(filepath="data/runways.csv"):
    data = defaultdict(list)

    light_map = {
        'H': 'High Intensity',
        'M': 'Medium Intensity',
        'L': 'Low Intensity',
        '': 'None'
    }

    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lights = light_map.get(row.get("edge_lights", "").strip(), "Unknown")
            data[row['airport_ident']].append({
                "runway_ident": row.get("runway_ident"),
                "length_ft": row.get("length_ft"),
                "surface": row.get("surface"),
                "lights": lights
            })
    return data
