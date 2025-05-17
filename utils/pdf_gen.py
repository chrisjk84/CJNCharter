from fpdf import FPDF
import os
from datetime import datetime

# Ensure the output directory exists
os.makedirs("output", exist_ok=True)

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

    try:
        pdf = PDF()
        pdf.add_page()

        # Charter Overview
        pdf.section_title("Charter Overview")
        pdf.section_body(
            f"Aircraft: {aircraft}\n"
            f"Departure: {departure_icao}\n"
            f"Arrival: {arrival_icao}\n"
            f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%MZ')}"
        )

        # Scenario
        pdf.section_title("Scenario")
        pdf.section_body(scenario)

        # Departure Weather Summary
        pdf.section_title("Departure Weather Summary")
        pdf.section_body(departure_summary)

        # Arrival Weather Summary
        pdf.section_title("Arrival Weather Summary")
        pdf.section_body(arrival_summary)

        # TAF
        pdf.section_title("TAF (Arrival)")
        pdf.section_body(arrival_taf)

        # Runway Summaries
        pdf.section_title("Runways (Departure)")
        pdf.section_body(departure_runways)

        pdf.section_title("Runways (Arrival)")
        pdf.section_body(arrival_runways)

        output_path = "output/charter.pdf"
        pdf.output(output_path)
        return output_path

    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return None
