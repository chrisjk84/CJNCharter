from flask import Flask, render_template, request, send_file
from utils.pdf_gen import generate_pdf
from utils.emailer import send_email
import os
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        icao = request.form['icao']
        aircraft = request.form['aircraft']
        email = request.form['email']

        # Generate random destination and dummy manifest (you'll expand this)
        destination = "KPDK"

        # Generate PDF file
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        generate_pdf(icao, destination, aircraft, temp_pdf.name)

        # Email the PDF
        send_email(email, temp_pdf.name)

        return "🛫 Charter Pack Sent to Your Email!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)