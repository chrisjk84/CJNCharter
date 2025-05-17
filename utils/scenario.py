import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_scenario(departure_icao, arrival_icao, aircraft):
    prompt = (
        f"Create a realistic charter flight mission scenario from {departure_icao} to {arrival_icao} "
        f"using a {aircraft}. Include weather considerations, passenger purpose, and any operational challenges. "
        f"Make it sound like a briefing paragraph."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a flight dispatcher writing charter flight briefings."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Unable to generate scenario: {str(e)}"
