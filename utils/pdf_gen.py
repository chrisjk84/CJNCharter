from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap

def generate_pdf(departure, destination, aircraft, output_path, scenario):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Charter Operations Briefing")

    # Flight Info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Aircraft: {aircraft}")
    c.drawString(50, height - 120, f"Departure: {departure}")
    c.drawString(50, height - 140, f"Destination: {destination}")

    # Scenario Heading
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 180, "Scenario:")

    # Scenario Text (Word Wrapped)
    c.setFont("Helvetica", 12)
    y = height - 200
    wrapped_lines = wrap(scenario, width=85)  # Approx. line width in characters

    for line in wrapped_lines:
        c.drawString(50, y, line)
        y -= 16  # Line height

        # If near bottom of page, start a new one
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50

    c.showPage()
    c.save()
