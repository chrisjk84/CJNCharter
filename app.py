from flask import Flask, request, send_file, render_template
from utils.weather import (
    get_metar,
    get_taf,
    get_metar_decoded,
    generate_weather_impact_summary
)
from utils.pdf_gen import generate_pdf
from utils.airport_info import load_runway_data
from utils.scenario_gen import generate_scenario
import tempfile
import os

app = Flask(__name__)

# Load runway data once
runway_data = load_runway_data("data/runways.csv")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        icao = request.form['icao'].upper()
        destination_icao = request.form['destination'].upper()
        aircraft = request.form['aircraft']

        # Get weather
        departure_metar = get_metar(icao)
        departure_taf = get_taf(icao)
        arrival_metar = get_metar(destination_icao)
        arrival_taf = get_taf(destination_icao)

        # Decoded weather
        departure_metar_decoded = get_metar_decoded(icao)
        arrival_metar_decoded = get_metar_decoded(destination_icao)

        # Weather summaries
        departure_summary = generate_weather_impact_summary(departure_metar_decoded)
        arrival_summary = generate_weather_impact_summary(arrival_metar_decoded)

        # Runway info
        departure_runways = runway_data.get(icao, [])
        arrival_runways = runway_data.get(destination_icao, [])

        # Scenario
        scenario = generate_scenario()

        # Generate PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            generate_pdf(
                icao,
                destination_icao,
                aircraft,
                temp_pdf.name,
                scenario,
                departure_metar,
                departure_taf,
                arrival_metar,
                arrival_taf,
                departure_metar_decoded,
                arrival_metar_decoded,
                departure_runways,
                arrival_runways,
                departure_summary,
                arrival_summary
            )
            return send_file(temp_pdf.name, as_attachment=True, download_name='charter_ops_pack.pdf')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
