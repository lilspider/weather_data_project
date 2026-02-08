"""
Production-ready dbt Orchestrator for Weather Data Project
"""
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def _get_dbt_env():
    """Get dbt environment from Docker container."""
    env = os.environ.copy()
    env.update({
        'DBT_LOG_PATH': '/tmp/dbt_logs',
        'DBT_TARGET_PATH': '/tmp/dbt_target'
    })
    return env

def run_intermediate_models():
    """Run intermediate models."""
    env = _get_dbt_env()
    command = ['dbt', 'run', '--profiles-dir', '/opt/airflow/dbt', '--project-dir', '.', '--select', 'intermediate']
    
    result = subprocess.run(
        command,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        cwd='/opt/airflow/dbt'
    )
    
    if result.returncode != 0:
        raise Exception(f"dbt failed: {result.stderr}")
    
    return result.stdout

def run_mart_models():
    """Run mart models."""
    env = _get_dbt_env()
    command = ['dbt', 'run', '--profiles-dir', '/opt/airflow/dbt', '--project-dir', '.', '--select', 'marts']
    
    result = subprocess.run(
        command,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        cwd='/opt/airflow/dbt'
    )
    
    if result.returncode != 0:
        raise Exception(f"dbt failed: {result.stderr}")
    
    return result.stdout

def run_full_pipeline():
    """Run complete dbt pipeline: staging -> intermediate -> marts."""
    env = _get_dbt_env()
    
    subprocess.run(['dbt', 'deps', '--profiles-dir', '/opt/airflow/dbt', '--project-dir', '.'], env=env, timeout=300, cwd='/opt/airflow/dbt')
    subprocess.run(['dbt', 'run', '--profiles-dir', '/opt/airflow/dbt', '--project-dir', '.', '--select', 'staging'], env=env, timeout=300, cwd='/opt/airflow/dbt')
    subprocess.run(['dbt', 'run', '--profiles-dir', '/opt/airflow/dbt', '--project-dir', '.', '--select', 'intermediate'], env=env, timeout=300, cwd='/opt/airflow/dbt')
    subprocess.run(['dbt', 'run', '--profiles-dir', '/opt/airflow/dbt', '--project-dir', '.', '--select', 'marts'], env=env, timeout=300, cwd='/opt/airflow/dbt')
