from flask import Flask, render_template, request
from data_utils import (
    get_airports_within_range,
    get_weather_data,
    get_runways_for_airport,
)
from openai_utils import generate_scenario

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        departure_icao = request.form.get("icao", "").upper()
        aircraft = request.form.get("aircraft")
        min_distance = int(request.form.get("min_distance", 0))
        max_distance = int(request.form.get("max_distance", 1000))
        min_runway_length = int(request.form.get("min_runway_length", 0))

        # Get all airports within range
        destinations = get_airports_within_range(
            departure_icao, min_distance, max_distance
        )

        if not destinations:
            return render_template("briefing.html", error="No nearby airports found.")

        # Select a destination (first one for now)
        selected = None
        for airport in destinations:
            runways = get_runways_for_airport(airport['ident'], min_runway_length)
            if runways:  # Ensure at least one suitable runway exists
                selected = airport
                break

        if not selected:
            return render_template("briefing.html", error="No destinations with valid runways found.")

        arrival_icao = selected["ident"]

        # Get scenario
        scenario = generate_scenario(departure_icao, arrival_icao, aircraft)

        # Get weather and runways
        departure_weather = get_weather_data(departure_icao)
        arrival_weather = get_weather_data(arrival_icao)

        departure_runways = get_runways_for_airport(departure_icao, min_runway_length)
        arrival_runways = get_runways_for_airport(arrival_icao, min_runway_length)

        return render_template(
            "briefing.html",
            aircraft=aircraft,
            departure_icao=departure_icao,
            arrival_icao=arrival_icao,
            scenario=scenario,
            departure_weather=departure_weather,
            arrival_weather=arrival_weather,
            departure_runways=departure_runways,
            arrival_runways=arrival_runways,
        )

    # GET request fallback – show empty form
    return render_template("briefing.html")
