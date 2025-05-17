import os
import requests

AVWX_API_KEY = os.getenv("AVWX_API_KEY")

def fetch_metar(icao):
    url = f"https://avwx.rest/api/metar/{icao}"
    headers = {"Authorization": AVWX_API_KEY}
    return requests.get(url, headers=headers).json()

def fetch_taf(icao):
    url = f"https://avwx.rest/api/taf/{icao}"
    headers = {"Authorization": AVWX_API_KEY}
    return requests.get(url, headers=headers).json()

def get_weather_summary(icao):
    try:
        metar = fetch_metar(icao)
        taf = fetch_taf(icao)

        return {
            "summary": f"{icao} METAR: {metar.get('raw', 'N/A')}\nTAF: {taf.get('raw', 'N/A')}",
            "taf": taf.get('raw', 'N/A'),
            "metar": metar.get('raw', 'N/A')
        }
    except Exception as e:
        return {
            "summary": f"Weather data unavailable for {icao}: {str(e)}",
            "taf": "N/A",
            "metar": "N/A"
        }
