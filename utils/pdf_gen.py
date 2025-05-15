def generate_pdf(departure, destination, aircraft, output_path, scenario,
                 departure_metar, departure_taf, arrival_metar, arrival_taf):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from textwrap import wrap

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

    y = height - 200
    for line in wrap(scenario, width=85):
        c.drawString(50, y, line)
        y -= 16

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Weather")

    c.setFont("Helvetica", 12)
    y -= 20
    c.drawString(50, y, f"{departure} METAR:")
    y -= 16
    for line in wrap(departure_metar, 85):
        c.drawString(50, y, line)
        y -= 16

    y -= 8
    c.drawString(50, y, f"{departure} TAF:")
    y -= 16
    for line in wrap(departure_taf, 85):
        c.drawString(50, y, line)
        y -= 16

    y -= 8
    c.drawString(50, y, f"{destination} METAR:")
    y -= 16
    for line in wrap(arrival_metar, 85):
        c.drawString(50, y, line)
        y -= 16

    y -= 8
    c.drawString(50, y, f"{destination} TAF:")
    y -= 16
    for line in wrap(arrival_taf, 85):
        c.drawString(50, y, line)
        y -= 16

    c.showPage()
    c.save()
