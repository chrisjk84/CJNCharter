import os
import random
from flask import Flask, request, render_template
from math import radians, cos, sin, asin, sqrt
import csv
import openai
from weather import get_weather_data, get_runways

app = Flask(__name__)

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load airport data
def load_airports():
    with open("airports.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

airports = load_airports()

# Haversine distance (in nautical miles)
def haversine(lat1, lon1, lat2, lon2):
    R = 3440.1  # nautical miles
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c

# Get a valid destination airport
def get_random_destination(origin_icao, airports, max_nm=None, min_nm=None, min_runway_length=None):
    origin = next((a for a in airports if a['ident'] == origin_icao), None)
    if not origin:
        return None

    lat1 = float(origin['latitude_deg'])
    lon1 = float(origin['longitude_deg'])

    eligible = []
    for airport in airports:
        if airport['ident'] == origin_icao:
            continue
        if airport['type'] not in ['large_airport', 'medium_airport']:
            continue
        if min_runway_length and airport.get('longest_runway') and int(airport['longest_runway']) < min_runway_length:
            continue

        lat2 = float(airport['latitude_deg'])
        lon2 = float(airport['longitude_deg'])
        dist = haversine(lat1, lon1, lat2, lon2)

        if (min_nm is None or dist >= min_nm) and (max_nm is None or dist <= max_nm):
            eligible.append(airport)

    return random.choice(eligible)['ident'] if eligible else None

# Generate a scenario using OpenAI
def generate_scenario(departure, arrival, aircraft):
    prompt = f"Generate a realistic charter flight mission scenario for a {aircraft} from {departure} to {arrival}."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            icao = request.form["icao"].upper()
            aircraft = request.form["aircraft"]
            min_distance = request.form.get("min_distance", type=int)
            max_distance = request.form.get("max_distance", type=int)
            min_runway_length = request.form.get("min_runway_length", type=int)
            destination_icao = request.form.get("destination", "").upper()

            if not destination_icao:
                destination_icao = get_random_destination(
                    icao, airports, max_distance, min_distance, min_runway_length
                )
                if not destination_icao:
                    return "<h2>No eligible destination found with given parameters.</h2>", 400

            scenario = generate_scenario(icao, destination_icao, aircraft)
            departure_weather = get_weather_data(icao)
            arrival_weather = get_weather_data(destination_icao)

            departure_runways = get_runways(icao)
            arrival_runways = get_runways(destination_icao)

            return render_template(
                "briefing.html",
                aircraft=aircraft,
                departure=icao,
                arrival=destination_icao,
                scenario=scenario,
                departure_weather=departure_weather["summary"],
                arrival_weather=arrival_weather["summary"],
                departure_runways=departure_runways,
                arrival_runways=arrival_runways
            )
        except Exception as e:
            return f"<h2>Error occurred: {e}</h2>", 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
