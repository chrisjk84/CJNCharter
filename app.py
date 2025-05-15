from flask import Flask, render_template, request, send_file
from utils.pdf_gen import generate_pdf
import os
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        icao = request.form['icao']
        aircraft = request.form['aircraft']

        # Generate random destination (placeholder for now)
        destination = "KPDK"

        # Create a temporary PDF file
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        generate_pdf(icao, destination, aircraft, temp_pdf.name)

        # Return it as a download
        return send_file(temp_pdf.name, as_attachment=True, download_name="Charter_Ops_Pack.pdf")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
