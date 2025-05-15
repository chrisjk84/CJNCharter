import os
import requests

AVWX_API_KEY = os.getenv("AVWX_API_KEY")
AVWX_BASE_URL = "https://avwx.rest/api"

HEADERS = {
    "Authorization":sBJsDPqYkpnIr2bQzt3wgYx91nDZ-sAHavot1axXIbQ
}

def get_metar(icao):
    try:
        response = requests.get(f"{AVWX_BASE_URL}/metar/{icao}", headers=HEADERS, params={"format": "json"})
        if response.status_code == 200:
            return response.json().get("raw", "No METAR available")
        return f"METAR error ({response.status_code})"
    except Exception as e:
        return f"METAR error: {e}"

def get_taf(icao):
    try:
        response = requests.get(f"{AVWX_BASE_URL}/taf/{icao}", headers=HEADERS, params={"format": "json"})
        if response.status_code == 200:
            return response.json().get("raw", "No TAF available")
        return f"TAF error ({response.status_code})"
    except Exception as e:
        return f"TAF error: {e}"
