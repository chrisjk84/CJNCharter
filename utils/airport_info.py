import csv

def load_runway_data(filepath="data/runways.csv"):
    runways = {}
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            airport_ident = row['airport_ident']
            if airport_ident not in runways:
                runways[airport_ident] = []
            runways[airport_ident].append({
                "runway_ident": row["le_ident"],
                "length_ft": row["length_ft"],
                "surface": row["surface"],
                "lights": row["edge_lights"]
            })
    return runways
