import requests
import os

AVWX_API_KEY = os.getenv('sBJsDPqYkpnIr2bQzt3wgYx91nDZ-sAHavot1axXIbQ')
AVWX_BASE_URL = "https://avwx.rest/api"
HEADERS = {"Authorization": AVWX_API_KEY}

def get_metar(icao):
    response = requests.get(f"{AVWX_BASE_URL}/metar/{icao}?format=raw", headers=HEADERS)
    return response.text if response.status_code == 200 else "METAR unavailable"

def get_taf(icao):
    response = requests.get(f"{AVWX_BASE_URL}/taf/{icao}?format=raw", headers=HEADERS)
    return response.text if response.status_code == 200 else "TAF unavailable"

def get_metar_decoded(icao):
    try:
        response = requests.get(f"{AVWX_BASE_URL}/metar/{icao}", headers=HEADERS, params={"format": "json"})
        if response.status_code == 200:
            data = response.json()
            return {
                "flight_rules": data.get("flight_rules", "N/A"),
                "winds": f"{data.get('wind_direction', {}).get('repr', '---')}\u00b0 at {data.get('wind_speed', {}).get('repr', '---')}kt",
                "visibility": data.get("visibility", {}).get("repr", "N/A"),
                "clouds": ", ".join(cloud.get("repr", "") for cloud in data.get("clouds", [])) or "None reported",
                "altimeter": data.get("altimeter", {}).get("value", "N/A"),
                "temperature": f"{data.get('temperature', {}).get('repr', 'N/A')}\u00b0C",
                "dewpoint": f"{data.get('dewpoint', {}).get('repr', 'N/A')}\u00b0C",
            }
        return {"error": f"METAR decode error ({response.status_code})"}
    except Exception as e:
        return {"error": f"METAR decode error: {e}"}

def generate_weather_impact_summary(decoded_metar):
    try:
        summary = []
        rules = decoded_metar.get("flight_rules", "N/A")
        wind = decoded_metar.get("winds", "")
        visibility = decoded_metar.get("visibility", "N/A")

        if rules == "VFR":
            summary.append("Visual flight conditions expected.")
        elif rules == "MVFR":
            summary.append("Marginal visual flight \u2014 exercise caution.")
        elif rules == "IFR":
            summary.append("Instrument flight rules required.")
        elif rules == "LIFR":
            summary.append("Low IFR \u2014 expect approach minima and poor visibility.")

        if "gust" in wind.lower() or "20" in wind:
            summary.append("Gusty winds possible.")

        if "less" in visibility.lower() or visibility == "N/A":
            summary.append("Reduced visibility reported.")

        return " ".join(summary) if summary else "No significant weather impacts expected."
    except Exception:
        return "Unable to assess weather impact."


# utils/airport_info.py
import csv

def load_runway_data(filepath="data/runways.csv"):
    runways = {}
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            airport_ident = row['airport_ident']
            if airport_ident not in runways:
                runways[airport_ident] = []
            runways[airport_ident].append({
                "runway_ident": row["le_ident"],
                "length_ft": row["length_ft"],
                "surface": row["surface"],
                "lights": row["edge_lights"]
            })
    return runways
