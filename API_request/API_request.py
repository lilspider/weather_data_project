"""
Weather API client.
"""
import os
import logging
import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def fetch_weather(city="London"):
    """Fetch weather data from Weatherstack API."""
    api_key = os.getenv("WEATHERSTACK_API_KEY")
    if not api_key:
        raise EnvironmentError("WEATHERSTACK_API_KEY not set")

    url = "https://api.weatherstack.com/current"
    params = {"access_key": api_key, "query": city}

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if "error" in data:
            raise ValueError(f"Weatherstack API error: {data.get('error', {}).get('info')}")

        return {
            "city": data.get("location", {}).get("name"),
            "temperature": data.get("current", {}).get("temperature"),
            "weather_descriptions": data.get("current", {}).get("weather_descriptions"),
            "raw": data,
        }

    except RequestException:
        logger.exception(f"Network error fetching weather for {city}")
        raise
