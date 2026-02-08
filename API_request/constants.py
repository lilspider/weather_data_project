"""
Shared constants for the weather data project.
"""
import os

CITIES = ['New York', 'London', 'Tokyo', 'Paris', 'Sydney']

SAMPLE_PAYLOAD = {
    'city': 'CITY_PLACEHOLDER',
    'temperature': 25.3,
    'weather_descriptions': ['Sunny'],
    'raw': {}
}

DB_DEFAULTS = {
    'host': 'postgres',
    'port': '5432',
    'dbname': 'airflow_db',
    'user': 'airflow_user',
    'password': 'airflow_password'
}

def get_db_config():
    """Get database configuration from environment variables."""
    return {
        'host': os.getenv('POSTGRES_HOST', DB_DEFAULTS['host']),
        'port': os.getenv('POSTGRES_PORT', DB_DEFAULTS['port']),
        'dbname': os.getenv('POSTGRES_DB', DB_DEFAULTS['dbname']),
        'user': os.getenv('POSTGRES_USER', DB_DEFAULTS['user']),
        'password': os.getenv('POSTGRES_PASSWORD', DB_DEFAULTS['password']),
    }

def is_mock_mode():
    """Check if mock mode is enabled."""
    return os.getenv('MOCK_WEATHER', '0') in ('1', 'true', 'True')
