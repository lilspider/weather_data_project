"""
Weather Data Pipeline DAG - WeatherAPI.com Bulk Request
"""
from airflow import DAG
from airflow.decorators import task
from airflow.models.variable import Variable
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/opt/airflow')

from API_request.insert_records import insert_bulk_weather_data
from API_request.weather_api_client import fetch_bulk_weather
from dbt_orchestrator import run_staging_models, run_mart_models, run_intermediate_models

# Read weather mode from Airflow Variables
WEATHER_MODE = Variable.get("weather_mode", default_var="standard")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@task
def fetch_bulk_weather_task():
    """Fetch bulk weather data for all cities using WeatherAPI.com."""
    bulk_data = fetch_bulk_weather()
    
    # Extract the bulk locations array from the response
    if 'bulk' in bulk_data:
        locations = bulk_data['bulk']
        insert_bulk_weather_data(bulk_data)
        return f"Successfully processed {len(locations)} cities"
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

@dag(
    dag_id='weather_ingestion_dag',
    default_args=default_args,
    description=f'FIFA World Cup Weather Pipeline - Current mode: {WEATHER_MODE}',
    schedule_interval=timedelta(minutes=5) if WEATHER_MODE == "live_match" else timedelta(minutes=55),
    catchup=False,
    tags=['fifa', 'weather', 'worldcup'],
) as dag:

    # Single bulk weather fetch task
    bulk_fetch = fetch_bulk_weather_task()
    
    # dbt transformation tasks
    staging = run_staging()
    intermediate = run_intermediate()
    marts = run_marts()

    # Set dependencies: bulk fetch -> staging -> intermediate -> marts
    bulk_fetch >> staging >> intermediate >> marts
