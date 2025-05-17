import csv
import random

AIRPORTS_CSV = "airports.csv"

def get_weather_data(icao):
    # Placeholder: Replace with real weather API calls if available
    # For demo, generate random weather conditions
    conditions = ["Clear skies", "Partly cloudy", "Overcast", "Light rain", "Thunderstorms", "Foggy"]
    temp_c = random.randint(-5, 30)
    condition = random.choice(conditions)
    return {
        "summary": f"{condition}, temperature {temp_c}°C at {icao}"
    }

def get_runways(icao, min_length_ft=3000):
    runways = []
    try:
        with open(AIRPORTS_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get("ident", "").upper() == icao.upper():
                    # Adjust these column names to your actual CSV schema
                    length_str = row.get("length_ft") or row.get("runway_length_ft") or ""
                    surface = row.get("surface_type", "").lower()

                    if not length_str or not length_str.isdigit():
                        continue
                    length = int(length_str)

                    # Filter out short runways and unwanted surfaces
                    if length >= min_length_ft and surface not in ["turf", "grass", "dirt", "water", "gravel", "snow"]:
                        le_ident = row.get("le_ident", "")
                        he_ident = row.get("he_ident", "")
                        runways.append(f"{le_ident} / {he_ident}: {length} ft, surface: {surface}")
    except Exception as e:
        return [f"Error reading runway data: {str(e)}"]

    return runways if runways else ["No suitable runways found."]
