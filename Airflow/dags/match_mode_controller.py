"""
Match Mode Controller DAG - Manages weather mode switching for live match periods
"""
from airflow import DAG
from airflow.decorators import task
from airflow.models.variable import Variable
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger(__name__)

# Sample match schedule for FIFA 2026 (will be connected to dim_match_schedule later)
SAMPLE_MATCHES = [
    {"match_id": 1, "kickoff_utc": "2026-06-11T23:00:00Z", "stadium": "MetLife Stadium"},
    {"match_id": 2, "kickoff_utc": "2026-06-12T01:00:00Z", "stadium": "Estadio Azteca"},
    {"match_id": 3, "kickoff_utc": "2026-06-15T20:00:00Z", "stadium": "BMO Field"},
    {"match_id": 4, "kickoff_utc": "2026-06-20T19:00:00Z", "stadium": "SoFi Stadium"},
]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@task
def check_match_periods():
    """Check if current time is within live match periods and set weather mode accordingly."""
    from datetime import datetime as dt
    
    current_utc = dt.now(timezone.utc)
    logger.info(f"Current UTC time: {current_utc}")
    
    # Check if we're within 2 hours before or 1 hour after any match kickoff
    in_live_period = False
    for match in SAMPLE_MATCHES:
        kickoff_time = dt.fromisoformat(match['kickoff_utc'].replace('Z', '+00:00'))
        
        # Live period: 2 hours before kickoff to 1 hour after kickoff
        live_start = kickoff_time - timedelta(hours=2)
        live_end = kickoff_time + timedelta(hours=1)
        
        if live_start <= current_utc <= live_end:
            in_live_period = True
            logger.info(f"Live match period detected for {match['stadium']} (Match {match['match_id']})")
            break
    
    # Set weather mode based on match periods
    if in_live_period:
        Variable.set("weather_mode", "live_match")
        logger.info("Weather mode set to: live_match (5-minute intervals)")
        return "Switched to live_match mode"
    else:
        Variable.set("weather_mode", "standard")
        logger.info("Weather mode set to: standard (55-minute intervals)")
        return "Switched to standard mode"

@dag(
    dag_id='match_mode_controller',
    default_args=default_args,
    description='FIFA 2026 Match Mode Controller - Switches weather mode during live matches',
    schedule_interval=timedelta(minutes=30),
    catchup=False,
    tags=['fifa', 'controller', 'weather'],
) as dag:
    
    # Single task to check match periods and update weather mode
    mode_check = check_match_periods()
