import csv

def load_runway_data(filepath):
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_runway_summary(icao, runways):
    matching = [r for r in runways if r.get("ident") == icao]
    summary = []
    for r in matching:
        summary.append(f"{r.get('surface', 'UNK')} {r.get('length_ft', '???')}ft Runway {r.get('le_ident', '')}/{r.get('he_ident', '')}")
    return "\n".join(summary) or "No runway data available."

def filter_airports_by_runway_length(airports, runways, min_length):
    longest_by_ident = {}
    for r in runways:
        ident = r.get("ident")
        try:
            length = int(r.get("length_ft") or 0)
            if ident and (ident not in longest_by_ident or length > longest_by_ident[ident]):
                longest_by_ident[ident] = length
        except:
            continue
    return [a for a in airports if longest_by_ident.get(a["ident"], 0) >= min_length]
