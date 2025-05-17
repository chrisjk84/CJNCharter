from flask import Flask, render_template, request
from data_utils import get_weather_data, get_runways
import openai

app = Flask(__name__)

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_scenario(icao, aircraft):
    prompt = f"Generate a professional flight briefing scenario for a flight departing {icao} with aircraft {aircraft}."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating scenario: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        icao = request.form.get("icao", "").upper()
        aircraft = request.form.get("aircraft", "")
        min_length = int(request.form.get("min_runway_length", 3000))

        weather_data = get_weather_data(icao)
        runways = get_runways(icao, min_length)
        scenario = generate_scenario(icao, aircraft)

        return render_template(
            "briefing.html",
            icao=icao,
            aircraft=aircraft,
            weather_summary=weather_data["summary"],
            runways=runways,
            scenario=scenario,
            min_runway_length=min_length
        )
    return render_template("briefing.html")

if __name__ == "__main__":
    app.run(debug=True)
