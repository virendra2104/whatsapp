from datetime import datetime
import pytz,requests
from langchain.tools import tool
import os
@tool
def get_current_datetime():
    """Returns the current date and time in IST"""
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    return now.strftime("%Y-%m-%d %H:%M:%S IST")
"for the weather"

@tool
def get_current_weather(location: str):
    """Get current weather using WeatherAPI"""

    api_key = os.getenv("WEATHER_API_KEY")

    url = "http://api.weatherapi.com/v1/current.json"

    params = {
        "key": api_key,
        "q": location,
        "aqi": "yes"
    }

    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()

    loc = data["location"]
    current = data["current"]

    resolved = f"{loc['name']}, {loc['region']}, {loc['country']}"

    temp = current["temp_c"]
    feels = current["feelslike_c"]
    condition = current["condition"]["text"]
    humidity = current["humidity"]
    wind = current["wind_kph"]
    aqi = current.get("air_quality", {}).get("us-epa-index", "N/A")

    return (
        f"Weather in {resolved}:\n"
        f"Temperature: {temp}°C\n"
        f"Feels like: {feels}°C\n"
        f"Condition: {condition}\n"
        f"Humidity: {humidity}%\n"
        f"Wind: {wind} km/h\n"
        f"AQI: {aqi}"
    )
"for forecasting" 
@tool
def get_weather(location: str, days: int = 1):
    """Get current + forecast weather"""

    api_key = os.getenv("WEATHER_API_KEY")

    url = "http://api.weatherapi.com/v1/forecast.json"

    params = {
        "key": api_key,
        "q": location,
        "days": days,
        "aqi": "yes",
        "alerts": "no"
    }

    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()

    loc = data["location"]
    current = data["current"]

    output = (
        f"Weather in {loc['name']}, {loc['country']}:\n"
        f"Temp: {current['temp_c']}°C\n"
        f"Condition: {current['condition']['text']}\n\n"
        f"Forecast:\n"
    )

    for day in data["forecast"]["forecastday"]:
        output += (
            f"{day['date']} → "
            f"{day['day']['avgtemp_c']}°C, "
            f"{day['day']['condition']['text']}\n"
        )

    return output