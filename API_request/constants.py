"""
Shared constants for the weather data project.
"""
import os

STADIUM_COORDINATES = [
    {"q": "40.8128,-74.0742", "name": "MetLife Stadium"},
    {"q": "33.9535,-118.3392", "name": "SoFi Stadium"},
    {"q": "19.3029,-99.1505", "name": "Estadio Azteca"},
    {"q": "43.6332,-79.4186", "name": "BMO Field"},
    {"q": "32.7473,-97.0945", "name": "AT&T Stadium"},
    {"q": "29.6847,-95.4107", "name": "NRG Stadium"},
    {"q": "47.5952,-122.3316", "name": "Lumen Field"},
    {"q": "37.4033,-121.9694", "name": "Levi's Stadium"},
    {"q": "39.9008,-75.1675", "name": "Lincoln Financial Field"},
    {"q": "25.958,-80.2389", "name": "Hard Rock Stadium"},
    {"q": "33.7554,-84.4010", "name": "Mercedes-Benz Stadium"},
    {"q": "39.0489,-94.4839", "name": "Arrowhead Stadium"},
    {"q": "42.0909,-71.2643", "name": "Gillette Stadium"},
    {"q": "25.6701,-100.2440", "name": "Estadio BBVA"},
    {"q": "20.6821,-103.4625", "name": "Estadio Akron"},
    {"q": "49.2768,-123.1120", "name": "BC Place"},
]

DB_DEFAULTS = {
    'host': 'postgres',
    'port': '5432',
    'dbname': 'airflow_db',
    'user': 'admin',
    'password': 'admin_password'
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
