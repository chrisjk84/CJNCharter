from flask import Flask, render_template, request, send_file
from utils.pdf_gen import generate_pdf
from utils.weather import get_weather_summary
from utils.airport_info import load_runway_data, get_runway_summary
from utils.scenario_gen import generate_scenario
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
            min_distance = int(request.form['min_distance'])
            max_distance = int(request.form['max_distance'])

            # Optional destination override
            destination_icao = request.form.get('destination', '').upper()
            if not destination_icao:
                destination_icao = get_random_destination(icao, min_distance, max_distance)

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
            import traceback
            traceback.print_exc()
            return f"<h2>Error: {e}</h2><p>Check the logs for more details.</p>", 400

    return render_template('index.html')