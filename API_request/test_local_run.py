"""
Local test runner for weather data pipeline.
"""
import os
import sys

if __package__ is None:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from API_request.API_request import fetch_weather
from API_request.insert_records import init_raw_table, insert_raw_weather
from API_request.constants import SAMPLE_PAYLOAD, is_mock_mode

def main():
    """Run local test."""
    mock = is_mock_mode()
    
    if mock:
        data = SAMPLE_PAYLOAD
    else:
        data = fetch_weather('London')

    print(f'Fetched: {data.get("city")} {data.get("temperature")}°C')
    
    try:
        init_raw_table()
        insert_raw_weather(data.get('city'), data.get('temperature'), str(data.get('weather_descriptions')))
        print('Data inserted successfully')
    except Exception as e:
        print(f'DB operation failed: {e}')

if __name__ == '__main__':
    main()
