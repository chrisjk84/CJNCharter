import requests
import os

AVWX_API_KEY = os.getenv('AVWX_API_KEY')

def fetch_metar(icao):
    url = f"https://avwx.rest/api/metar/{icao}"
    headers = {"Authorization": AVWX_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_taf(icao):
    url = f"https://avwx.rest/api/taf/{icao}"
    headers = {"Authorization": AVWX_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_weather_data(icao):
    try:
        metar = fetch_metar(icao)
        taf = fetch_taf(icao)
        summary = f"""METAR: {metar.get('raw', 'N/A')}\nTAF: {taf.get('raw', 'N/A')}"""
        return {"summary": summary}
    except Exception as e:
        return {"summary": f"Weather data unavailable for {icao} due to error: {str(e)}"}

def get_runways(icao):
    # Placeholder: Normally you'd fetch real runway data from your CSV or a service
    return f"Runway data for {icao} unavailable."
