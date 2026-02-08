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
            if 'bulk' not in bulk_data:
                raise ValueError("Expected 'bulk' key in response data")

            locations = bulk_data['bulk']
            success_count = 0
            fail_count = 0

            for location_data in locations:
                try:
                    query_data = location_data.get('query', {})
                    location = query_data.get('location', {})
                    current = query_data.get('current', {})

                    city_name = location.get('name')
                    if not city_name:
                        logger.warning("Skipping location with no city name")
                        fail_count += 1
                        continue

                    temperature = float(current.get('temp_c', 0))
                    weather_description = current.get('condition', {}).get('text', '')
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
                    success_count += 1
                except Exception as e:
                    logger.error(f"Error processing location: {e}")
                    fail_count += 1
                    continue

            conn.commit()
            logger.info(f"Bulk insert complete: {success_count} succeeded, {fail_count} failed out of {len(locations)}")

            if fail_count > len(locations) // 2:
                raise Exception(f"Too many failures: {fail_count}/{len(locations)} locations failed to insert")
