import csv

def load_runway_data(filepath):
    runway_data = {}
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            icao = row["icao"]
            if icao not in runway_data:
                runway_data[icao] = []
            runway_data[icao].append({
                "runway": row["runway"],
                "length_ft": row["length_ft"],
                "surface": row["surface"],
                "lights": row.get("lights", "Unknown")
            })
    return runway_data

def get_runway_summary(icao, runway_data):
    runways = runway_data.get(icao.upper())
    if not runways:
        return f"No runway data available for {icao}"

    summary_lines = [f"Runways at {icao.upper()}:"]
    for rwy in runways:
        lights_info = rwy["lights"] if rwy["lights"] else "Unknown lighting"
        summary_lines.append(
            f"- {rwy['runway']}: {rwy['length_ft']} ft, {rwy['surface']} surface, {lights_info}"
        )
    return "\n".join(summary_lines)
