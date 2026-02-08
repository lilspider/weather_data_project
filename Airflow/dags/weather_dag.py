"""
Weather Data Pipeline DAG - WeatherAPI.com Bulk Request
Supports dual-mode: standard (55min) and live_match (5min)
"""
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/opt/airflow')

from API_request.insert_records import insert_bulk_weather_data
from API_request.weather_api_client import fetch_bulk_weather
from dbt_orchestrator import run_staging_models, run_mart_models, run_intermediate_models

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def _get_weather_mode():
    """Read weather mode at runtime, not parse time."""
    from airflow.models.variable import Variable
    return Variable.get("weather_mode", default_var="standard")

@task
def fetch_bulk_weather_task():
    """Fetch bulk weather data for all FIFA 2026 stadiums."""
    bulk_data = fetch_bulk_weather()
    if 'bulk' in bulk_data:
        locations = bulk_data['bulk']
        insert_bulk_weather_data(bulk_data)
        return f"Successfully processed {len(locations)} stadiums"
    else:
        raise ValueError("Unexpected response format from WeatherAPI.com")

@task
def run_staging():
    """Run staging models."""
    return run_staging_models()

@task
def run_intermediate():
    """Run intermediate models for FIFA athlete safety monitoring."""
    return run_intermediate_models()

@task
def run_marts():
    """Run mart models."""
    return run_mart_models()

# Use standard schedule — the match_mode_controller DAG handles switching
# by triggering this DAG more frequently during live matches
with DAG(
    dag_id='weather_ingestion_dag',
    default_args=default_args,
    description='FIFA 2026 World Cup Weather Pipeline',
    schedule_interval=timedelta(minutes=55),
    catchup=False,
    tags=['fifa', 'weather', 'worldcup'],
) as dag:

    bulk_fetch = fetch_bulk_weather_task()
    staging = run_staging()
    intermediate = run_intermediate()
    marts = run_marts()

    bulk_fetch >> staging >> intermediate >> marts
