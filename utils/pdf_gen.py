from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf(
    departure_icao,
    arrival_icao,
    aircraft,
    scenario,
    arrival_taf,
    departure_runways,
    arrival_runways,
    departure_summary,
    arrival_summary
):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "Charter Briefing", ln=True, align="C")
            self.ln(10)

        def section_title(self, title):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, title, ln=True)
            self.ln(4)

        def section_body(self, body):
            self.set_font("Arial", "", 11)
            self.multi_cell(0, 10, body)
            self.ln()

    pdf = PDF()
    pdf.add_page()

    # Charter Overview
    pdf.section_title("Charter Overview")
    pdf.section_body(
        f"Aircraft: {aircraft}\n"
        f"Departure: {departure_icao}\n"
        f"Arrival: {arrival_icao}\n"
        f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%MZ')}")
