from flask import Flask, render_template, request, send_file
from utils.pdf_gen import generate_pdf
from utils.airport_picker import load_airports, get_random_destination
import tempfile

app = Flask(__name__)

# Load airports once on app start
airports = load_airports()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        icao = request.form['icao']
        aircraft = request.form['aircraft']
        min_distance = int(request.form['min_distance'])
        max_distance = int(request.form['max_distance'])
        
        destination_airport = get_random_destination(airports, icao, min_distance, max_distance)
        if not destination_airport:
            return "No destination found within that range. Try adjusting distance."

        destination_icao = destination_airport['ident']

        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        generate_pdf(icao, destination_icao, aircraft, temp_pdf.name)

        return send_file(temp_pdf.name, as_attachment=True, download_name="Charter_Ops_Pack.pdf")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
