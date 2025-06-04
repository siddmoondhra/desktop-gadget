import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = os.getenv("CITY")

def get_weather():
    if not API_KEY or not CITY:
        return "Weather config missing"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        description = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]

        return f"{CITY}: {description}, {temp*(9/5)+32}°F"

    except requests.RequestException as e:
        return f"Error: {e}"
