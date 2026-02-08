"""
Database operations for weather data.
"""
from .db_utils import get_connection
import json
import logging

logger = logging.getLogger(__name__)

def insert_bulk_weather_data(bulk_data):
    """Insert bulk weather data from WeatherAPI.com response."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # WeatherAPI.com returns a dict with a 'bulk' array
            if 'bulk' in bulk_data:
                locations = bulk_data['bulk']
                for location_data in locations:
                    try:
                        # The data is nested under a 'query' key
                        query_data = location_data.get('query', {})
                        location = query_data.get('location', {})
                        current = query_data.get('current', {})
                        
                        city_name = location.get('name')
                        temperature = float(current.get('temp_c', 0))
                        humidity = float(current.get('humidity', 0))
                        wind_speed = float(current.get('wind_kph', 0))
                        weather_description = current.get('condition', {}).get('text', '')
                        
                        # Store the complete JSON response
                        json_data = json.dumps(location_data)
                        
                        cur.execute(
                            """
                            INSERT INTO dev.raw_weather_data 
                            (city, temperature, weather_descriptions, recorded_at, json_data)
                            VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s)
                            ON CONFLICT (city, recorded_at) DO NOTHING
                            """,
                            (city_name, temperature, weather_description, json_data),
                        )
                    except Exception as e:
                        logger.error(f"Error processing city data: {e}")
                        continue
            conn.commit()
