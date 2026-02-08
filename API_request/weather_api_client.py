"""
WeatherAPI.com client for bulk weather requests.
"""
import os
import logging
import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def fetch_bulk_weather():
    """Fetch weather data for multiple cities using WeatherAPI.com bulk endpoint."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise EnvironmentError("WEATHER_API_KEY not set")

    url = "https://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": "bulk"}
    
    payload = {
        "locations": [
            {"q": "New York"},
            {"q": "London"}, 
            {"q": "Tokyo"},
            {"q": "Paris"},
            {"q": "Sydney"}
        ]
    }

    try:
        resp = requests.post(url, params=params, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if "error" in data:
            raise ValueError(f"WeatherAPI error: {data.get('error', {}).get('message')}")

        # Extract the actual location data from the bulk structure
        if 'bulk' in data:
            # The bulk array already contains the properly structured data
            # No need to extract from nested query structure
            return data
        else:
            raise ValueError("Unexpected response format from WeatherAPI.com")

    except RequestException:
        logger.exception("Network error fetching bulk weather data")
        raise
