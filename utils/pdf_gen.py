from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(origin, destination, aircraft, filepath):
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "CJN Charter Ops Pack")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Flight Briefing")
    c.drawString(50, height - 120, f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}Z")
    c.drawString(50, height - 140, f"Aircraft: {aircraft}")
    c.drawString(50, height - 160, f"Origin: {origin}")
    c.drawString(50, height - 180, f"Destination: {destination}")

    c.drawString(50, height - 220, "Passenger Manifest:")
    for i in range(1, 6):
        c.drawString(70, height - 220 - (i * 20), f"Passenger {i}: Name Placeholder")

    c.drawString(50, height - 360, "Weather and route will be added in future updates.")

    c.save()
