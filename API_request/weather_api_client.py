"""
WeatherAPI.com client for bulk weather requests.
"""
import os
import logging
import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def fetch_bulk_weather():
    """Fetch weather data for all FIFA 2026 stadium locations."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise EnvironmentError("WEATHER_API_KEY not set")

    url = "https://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": "bulk"}
    
    # FIFA 2026 World Cup stadium coordinates
    payload = {
        "locations": [
            {"q": "40.8128,-74.0742"},   # MetLife Stadium, East Rutherford
            {"q": "33.9535,-118.3392"},  # SoFi Stadium, Inglewood
            {"q": "19.3029,-99.1505"},   # Estadio Azteca, Mexico City
            {"q": "43.6332,-79.4186"},   # BMO Field, Toronto
            {"q": "32.7473,-97.0945"},   # AT&T Stadium, Arlington
            {"q": "29.6847,-95.4107"},   # NRG Stadium, Houston
            {"q": "47.5952,-122.3316"},  # Lumen Field, Seattle
            {"q": "37.4033,-121.9694"},  # Levi's Stadium, Santa Clara
            {"q": "39.9008,-75.1675"},   # Lincoln Financial Field, Philadelphia
            {"q": "25.958,-80.2389"},    # Hard Rock Stadium, Miami Gardens
            {"q": "33.7554,-84.4010"},   # Mercedes-Benz Stadium, Atlanta
            {"q": "39.0489,-94.4839"},   # Arrowhead Stadium, Kansas City
            {"q": "42.0909,-71.2643"},   # Gillette Stadium, Foxborough
            {"q": "25.6701,-100.2440"},  # Estadio BBVA, Monterrey
            {"q": "20.6821,-103.4625"},  # Estadio Akron, Guadalajara
            {"q": "49.2768,-123.1120"},  # BC Place, Vancouver
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
