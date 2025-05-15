from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(departure, destination, aircraft, output_path, scenario,
                 departure_metar, departure_taf, arrival_metar, arrival_taf,
                 departure_metar_decoded, arrival_metar_decoded,
                 departure_runways, arrival_runways,
                 departure_summary, arrival_summary):

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Charter Flight Briefing")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Aircraft: {aircraft}")
    y -= 20
    c.drawString(50, y, f"From: {departure} To: {destination}")
    y -= 20

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Scenario:")
    y -= 16
    c.setFont("Helvetica", 10)
    for line in scenario.split('\n'):
        c.drawString(60, y, line)
        y -= 14

    y -= 10
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Weather Impact Summary")
    y -= 16
    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"{departure}: {departure_summary}")
    y -= 14
    c.drawString(60, y, f"{destination}: {arrival_summary}")

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "METAR/TAF")
    y -= 16
    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"{departure} METAR: {departure_metar}")
    y -= 14
    c.drawString(60, y, f"{departure} TAF: {departure_taf}")
    y -= 14
    c.drawString(60, y, f"{destination} METAR: {arrival_metar}")
    y -= 14
    c.drawString(60, y, f"{destination} TAF: {arrival_taf}")

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Decoded METAR")
    y -= 16
    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"{departure}:")
    y -= 14
    for k, v in departure_metar_decoded.items():
        c.drawString(70, y, f"{k.capitalize()}: {v}")
        y -= 14

    y -= 10
    c.drawString(60, y, f"{destination}:")
    y -= 14
    for k, v in arrival_metar_decoded.items():
        c.drawString(70, y, f"{k.capitalize()}: {v}")
        y -= 14

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Runway Information")
    y -= 16
    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"{departure}:")
    y -= 14
    for rwy in departure_runways:
        rwy_str = f"RWY {rwy['runway_ident']} - {rwy['length_ft']} ft - {rwy['surface']} - Lights: {rwy['lights']}"
        c.drawString(70, y, rwy_str)
        y -= 14

    y -= 10
    c.drawString(60, y, f"{destination}:")
    y -= 14
    for rwy in arrival_runways:
        rwy_str = f"RWY {rwy['runway_ident']} - {rwy['length_ft']} ft - {rwy['surface']} - Lights: {rwy['lights']}"
        c.drawString(70, y, rwy_str)
        y -= 14

    c.save()
