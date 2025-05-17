from flask import Flask, render_template, request
from data_utils import get_airport_info, get_weather_data, get_runways, get_nearby_airports
from openai_utils import generate_scenario

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        departure_icao = request.form.get("icao", "").upper()
        aircraft = request.form.get("aircraft", "")
        min_distance = float(request.form.get("min_distance", 0))
        max_distance = float(request.form.get("max_distance", 1000))
        destination = request.form.get("destination", "").upper()

        print(f"Form received: departure={departure_icao}, aircraft={aircraft}, min_dist={min_distance}, max_dist={max_distance}, destination={destination}")

        # Get departure airport info
        departure_info = get_airport_info(departure_icao)
        if not departure_info:
            error = f"Departure airport {departure_icao} not found."
            return render_template("briefing.html", error=error)

        # Get nearby airports filtered by min/max distance
        nearby_airports = get_nearby_airports(departure_info['latitude'], departure_info['longitude'], min_distance, max_distance)

        # If destination not specified, pick first from filtered nearby airports
        if not destination:
            if nearby_airports:
                destination = nearby_airports[0]['ident']
            else:
                error = "No nearby airports found within specified distance range."
                return render_template("briefing.html", error=error)

        # Get arrival airport info
        arrival_info = get_airport_info(destination)
        if not arrival_info:
            error = f"Arrival airport {destination} not found."
            return render_template("briefing.html", error=error)

        # Get weather and runways
        departure_weather = get_weather_data(departure_icao)
        arrival_weather = get_weather_data(destination)
        departure_runways = get_runways(departure_icao)
        arrival_runways = get_runways(destination)

        # Generate scenario text using OpenAI
        scenario_text = generate_scenario(departure_icao, destination, aircraft)

        return render_template(
            "briefing.html",
            aircraft=aircraft,
            departure_icao=departure_icao,
            arrival_icao=destination,
            min_distance=min_distance,
            max_distance=max_distance,
            nearby_airports=nearby_airports,
            departure_weather=departure_weather,
            arrival_weather=arrival_weather,
            departure_runways=departure_runways,
            arrival_runways=arrival_runways,
            scenario=scenario_text
        )

    # GET request
    return render_template("briefing.html", nearby_airports=[])

if __name__ == "__main__":
    app.run(debug=True)
