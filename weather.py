import requests
import os
from datetime import datetime


def get_weather() -> str:
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    # Current conditions
    current_url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q=Bellevue,WA,US&appid={api_key}&units=imperial"
    )
    current = requests.get(current_url).json()
    description = current["weather"][0]["description"].capitalize()
    temp = round(current["main"]["temp"])

    # True daily high/low from the 5-day/3-hour forecast
    forecast_url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        f"?q=Bellevue,WA,US&appid={api_key}&units=imperial"
    )
    forecast = requests.get(forecast_url).json()
    today = datetime.now().date()
    # High = today's forecast entries; Low = today + overnight (next 30 hours) to catch the true overnight low
    from datetime import timedelta
    tomorrow_morning = datetime.now() + timedelta(hours=30)
    today_temps = [
        entry["main"]["temp"]
        for entry in forecast["list"]
        if datetime.fromtimestamp(entry["dt"]).date() == today
    ]
    overnight_temps = [
        entry["main"]["temp"]
        for entry in forecast["list"]
        if datetime.fromtimestamp(entry["dt"]) <= tomorrow_morning
    ]

    high = round(max(today_temps)) if today_temps else round(current["main"]["temp_max"])
    low = round(min(overnight_temps)) if overnight_temps else round(current["main"]["temp_min"])

    return f"{description}, {temp}°F (H:{high}° L:{low}°)"
