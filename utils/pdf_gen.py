from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(departure, destination, aircraft, output_path, scenario):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Charter Operations Briefing")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Aircraft: {aircraft}")
    c.drawString(50, height - 120, f"Departure: {departure}")
    c.drawString(50, height - 140, f"Destination: {destination}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 180, "Scenario:")

    c.setFont("Helvetica", 12)
    text = c.beginText(50, height - 200)
    text.setLeading(16)

    for line in scenario.split('\n'):
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
