import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_scenario(departure, destination, aircraft):
    prompt = f"""
    You are a charter dispatcher. Generate a realistic short backstory for a charter flight using a {aircraft} departing {departure} and flying to {destination}.
    Include the purpose of the trip, passenger profile, and any urgency or special instructions.
    Keep it under 100 words.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Scenario unavailable (error: {e})"
