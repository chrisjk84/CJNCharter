from flask import Flask, request, render_template
from utils.pdf_gen import generate_pdf
from utils.weather import get_weather_summary
from utils.airport_info import load_airports, load_runways, get_random_destination, filter_airports_by_runway_length

app = Flask(__name__)

# Load data once on startup
airports = load_airports()
runways = load_runways()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            icao = request.form['icao'].upper()
            aircraft = request.form['aircraft']
            destination_icao = request.form.get('destination', '').upper()
            min_distance = int(request.form.get('min_distance') or 0)
            max_distance = int(request.form.get('max_distance') or 9999)
            min_runway_length = int(request.form.get('min_runway_length') or 0)

            # Filter airports by runway length
            eligible_airports = filter_airports_by_runway_length(airports, runways, min_runway_length)

            # Choose a destination if not provided
            if not destination_icao:
                destination_icao = get_random_destination(icao, eligible_airports, max_distance, min_distance)
                if not destination_icao:
                    return "<h2>No eligible destination found with given parameters.</h2>", 400

            # Weather summaries
            departure_weather = get_weather_summary(icao)
            arrival_weather = get_weather_summary(destination_icao)

            # Generate the charter briefing summary (no PDF for now)
            summary = f"""
                <h2>Charter Briefing</h2>
                <strong>Aircraft:</strong> {aircraft}<br>
                <strong>From:</strong> {icao}<br>
                <strong>To:</strong> {destination_icao}<br><br>
                
                <h3>Departure Weather:</h3>
                <pre>{departure_weather}</pre>
                
                <h3>Arrival Weather:</h3>
                <pre>{arrival_weather}</pre>
            """
            return summary

        except Exception as e:
            return f"<h2>Error: {str(e)}</h2>", 500

    return render_template("index.html")
