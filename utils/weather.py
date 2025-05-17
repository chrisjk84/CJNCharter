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

def get_weather_summary(icao):
    try:
        metar = fetch_metar(icao)
        taf = fetch_taf(icao)

        return {
            "taf": taf.get('raw', 'N/A'),
            "decode_metar": metar.get('sanitized', 'N/A'),
            "summary": f"""Weather at {icao}:

METAR:
{metar.get('raw', 'N/A')}

TAF:
{taf.get('raw', 'N/A')}
"""
        }
    except Exception as e:
        return {
            "taf": "N/A",
            "decoded_metar": "N/A",
            "summary": f"Weather data unavailable for {icao} due to error: {str(e)}"
        }