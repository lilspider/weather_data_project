#!/usr/bin/env python3
"""
Unified database initialization script for the weather data project.
Creates databases and users for both Airflow and Superset.
"""
import sys
import os

# Add the API_request directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'API_request'))

from db_utils import create_database_if_not_exists, create_user_if_not_exists, grant_privileges


def init_airflow_db():
    """Initialize Airflow database and user."""
    print("Initializing Airflow database...")
    create_database_if_not_exists('airflow_db')
    create_user_if_not_exists('airflow_user', 'airflow_password')
    grant_privileges('airflow_db', 'airflow_user')
    print("Airflow database initialization complete.")


def init_superset_db():
    """Initialize Superset database and user."""
    print("Initializing Superset database...")
    create_database_if_not_exists('superset_db')
    create_user_if_not_exists('superset_user', 'superset_password')
    grant_privileges('superset_db', 'superset_user')
    print("Superset database initialization complete.")


def main():
    """Main initialization function."""
    try:
        init_airflow_db()
        init_superset_db()
        print("All database initialization completed successfully!")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
