"""
WeatherAPI.com client for bulk weather requests.
FIFA 2026 World Cup stadium weather monitoring.
"""
import os
import logging
import requests
from requests.exceptions import RequestException
from .constants import STADIUM_COORDINATES

logger = logging.getLogger(__name__)

def fetch_bulk_weather():
    """Fetch weather data for all FIFA 2026 stadium locations."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise EnvironmentError("WEATHER_API_KEY not set")

    url = "https://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": "bulk"}

    payload = {
        "locations": [{"q": s["q"]} for s in STADIUM_COORDINATES]
    }

    try:
        resp = requests.post(url, params=params, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if "error" in data:
            raise ValueError(f"WeatherAPI error: {data.get('error', {}).get('message')}")

        if 'bulk' in data:
            return data
        else:
            raise ValueError("Unexpected response format from WeatherAPI.com")

    except RequestException:
        logger.exception("Network error fetching bulk weather data")
        raise
