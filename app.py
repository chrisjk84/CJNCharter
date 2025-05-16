from flask import Flask, render_template, request, send_file
from utils.pdf_gen import generate_pdf
from utils.weather import get_weather_summary
from utils.airport_info import load_runway_data, get_runway_summary
from utils.scenario import generate_scenario
from utils.airport_picker import get_random_destination
import os

app = Flask(__name__)

# Load runway data on startup
runway_data = load_runway_data("data/runways.csv")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            icao = request.form['icao'].upper()
            aircraft = request.form['aircraft']
            min_distance = int(request.form['min_distance'])
            max_distance = int(request.form['max_distance'])

            # Optional destination field
            destination_icao = request.form.get('destination', '').upper()

            if not destination_icao:
                # Pick random destination if not manually specified
                destination_icao = get_random_destination(icao, min_distance, max_distance)

            # Get weather and runway data
            departure_weather = get_weather_summary(icao)
            arrival_weather = get_weather_summary(destination_icao)

            departure_runways = get_runway_summary(icao, runway_data)
            arrival_runways = get_runway_summary(destination_icao, runway_data)

            scenario = generate_scenario(icao, destination_icao, aircraft)

            pdf_path = generate_pdf(
                icao,
                destination_icao,
                aircraft,
                scenario,
                departure_weather,
                arrival_weather,
                departure_runways,
                arrival_runways
            )

            return send_file(pdf_path, as_attachment=True)

        except Exception as e:
            return f"Error: {e}", 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
