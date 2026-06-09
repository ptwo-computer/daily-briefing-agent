import requests
import os


def get_weather() -> str:
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q=Bellevue,WA,US&appid={api_key}&units=imperial"
    )
    data = requests.get(url).json()

    description = data["weather"][0]["description"].capitalize()
    temp = round(data["main"]["temp"])
    high = round(data["main"]["temp_max"])
    low = round(data["main"]["temp_min"])

    return f"{description}, {temp}°F (H:{high}° L:{low}°)"
