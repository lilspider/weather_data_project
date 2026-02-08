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

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@task
def get_weather_mode():
    """Get current weather mode from Airflow Variables."""
    return Variable.get("weather_mode", default_var="standard")

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
    description='FIFA World Cup Weather Pipeline - Dynamic scheduling based on match periods',
    schedule_interval='@hourly',  # Default schedule, will be updated by controller
    catchup=False,
    tags=['fifa', 'weather', 'worldcup'],
) as dag:

    # Get weather mode dynamically
    weather_mode = get_weather_mode()
    
    # Single bulk weather fetch task
    bulk_fetch = fetch_bulk_weather_task()
    
    # dbt transformation tasks
    staging = run_staging()
    intermediate = run_intermediate()
    marts = run_marts()

    # Set dependencies: weather_mode -> bulk fetch -> staging -> intermediate -> marts
    weather_mode >> bulk_fetch >> staging >> intermediate >> marts
