from flask import Flask, render_template, request, send_file
from utils.weather import get_weather_summary
from utils.airport_info import load_runway_data, get_runway_summary
from utils.scenario import generate_scenario
from utils.airport_picker import get_random_destination
from utils.airport_data import load_airports
from utils.pdf_gen import generate_pdf
import traceback
import os

app = Flask(__name__)

# Load data on startup
airports = load_airports("data/airports.csv")
runway_data = load_runway_data("data/runways.csv")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            print("Form received:", request.form)

            icao = request.form['icao'].upper()
            aircraft = request.form['aircraft']

            # Optional distance filters
            min_distance = int(request.form.get('min_distance') or 0)
            max_distance = int(request.form.get('max_distance') or 9999)

            destination_icao = request.form.get('destination', '').upper()
            if not destination_icao:
                destination_icao = get_random_destination(icao, airports, max_distance, min_distance)
                if not destination_icao:
                    return "<h2>No eligible destination found with given parameters.</h2>", 400

            print(f"Generating charter from {icao} to {destination_icao} using {aircraft}")

            departure_weather = get_weather_summary(icao)
            arrival_weather = get_weather_summary(destination_icao)

            departure_runways = get_runway_summary(icao, runway_data)
            arrival_runways = get_runway_summary(destination_icao, runway_data)

            scenario = generate_scenario(icao, destination_icao, aircraft)

            # Generate PDF (may fail)
            try:
                pdf_path = generate_pdf(
                    icao,
                    destination_icao,
                    aircraft,
                    scenario,
                    arrival_taf=arrival_weather["taf"],
                    departure_runways=departure_runways,
                    arrival_runways=arrival_runways,
                    departure_summary=departure_weather["summary"],
                    arrival_summary=arrival_weather["summary"]
                )
                if pdf_path:
                    return send_file(pdf_path, as_attachment=True, download_name="charter_briefing.pdf", mimetype="application/pdf")
            except Exception as pdf_error:
                print("PDF generation failed:", pdf_error)

            # If PDF fails or is skipped, show the briefing in browser
            return render_template(
                'briefing.html',
                departure_icao=icao,
                destination_icao=destination_icao,
                aircraft=aircraft,
                scenario=scenario,
                departure_weather=departure_weather["summary"],
                arrival_weather=arrival_weather["summary"],
                departure_runways=departure_runways,
                arrival_runways=arrival_runways
            )

        except Exception as e:
            traceback.print_exc()
            return f"<h2>Error: {e}</h2><p>Check the logs for more details.</p>", 400

    return render_template('index.html')
