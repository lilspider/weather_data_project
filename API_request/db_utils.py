"""
Database utilities for the weather data project.
"""
import psycopg2
from contextlib import contextmanager
from .constants import get_db_config

@contextmanager
def get_connection():
    """Get a database connection."""
    config = get_db_config()
    conn = psycopg2.connect(
        dbname=config['dbname'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port'],
    )
    try:
        yield conn
    finally:
        conn.close()

def init_schema(schema_name='dev'):
    """Initialize a database schema."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
            conn.commit()
