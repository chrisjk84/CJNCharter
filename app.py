from flask import Flask, render_template, request, send_file
from utils.pdf_gen import generate_pdf
from utils.weather import get_weather_summary
from utils.airport_info import load_runway_data, get_runway_summary
from utils.scenario import generate_scenario
from utils.airport_picker import get_random_destination
import os
import traceback

app = Flask(__name__)

# Load runway data once at startup
runway_data = load_runway_data("data/runways.csv")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            print("Form received:", request.form)

            # Collect form data
            icao = request.form['icao'].upper()
            aircraft = request.form['aircraft']

            # Get min and max distance if provided, else None
            min_distance_str = request.form.get('min_distance')
            max_distance_str = request.form.get('max_distance')

            min_distance = int(min_distance_str) if min_distance_str else None
            max_distance = int(max_distance_str) if max_distance_str else None

            # Optional destination override
            destination_icao = request.form.get('destination', '').upper()

            if not destination_icao:
                # Call get_random_destination with optional distances
                if max_distance is not None and min_distance is not None:
                    destination_icao = get_random_destination(icao, max_nm=max_distance, min_nm=min_distance)
                elif max_distance is not None:
                    destination_icao = get_random_destination(icao, max_nm=max_distance)
                else:
                    destination_icao = get_random_destination(icao)

            print(f"Generating charter from {icao} to {destination_icao} using {aircraft}")

            # Get weather info
            departure_weather = get_weather_summary(icao)
            arrival_weather = get_weather_summary(destination_icao)

            # Runway summaries
            departure_runways = get_runway_summary(icao, runway_data)
            arrival_runways = get_runway_summary(destination_icao, runway_data)

            # Generate scenario narrative
            scenario = generate_scenario(icao, destination_icao, aircraft)

            # Generate PDF
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

            # Return generated PDF
            return send_file(pdf_path, as_attachment=True)

        except Exception as e:
            traceback.print_exc()
            return f"<h2>Error: {e}</h2><p>Check the logs for more details.</p>", 400

    return render_template('index.html')
