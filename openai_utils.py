import openai
import os

# Load your OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_scenario(departure_icao, destination_icao, aircraft):
    prompt = (
        f"You are a dispatcher planning a charter flight for a {aircraft} from {departure_icao} to {destination_icao}. "
        "Generate a professional flight scenario including the purpose of the trip, passenger profile, and any special considerations. "
        "Keep it under 300 words and formatted for inclusion in a flight briefing."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Scenario generation failed: {e}"
