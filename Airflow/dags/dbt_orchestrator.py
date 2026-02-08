"""
dbt Orchestrator for FIFA 2026 Weather Data Project
"""
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

DBT_DIR = '/opt/airflow/dbt'

def _get_dbt_env():
    """Get dbt environment with correct paths."""
    env = os.environ.copy()
    env.update({
        'DBT_LOG_PATH': '/tmp/dbt_logs',
        'DBT_TARGET_PATH': '/tmp/dbt_target'
    })
    return env

def _run_dbt(select_target):
    """Run dbt for a given target (staging, intermediate, marts, etc.)."""
    env = _get_dbt_env()
    command = [
        'dbt', 'run',
        '--profiles-dir', DBT_DIR,
        '--project-dir', '.',
        '--select', select_target
    ]

    result = subprocess.run(
        command,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        cwd=DBT_DIR
    )

    if result.returncode != 0:
        raise Exception(f"dbt {select_target} failed: {result.stderr}")

    logger.info(f"dbt {select_target} completed: {result.stdout}")
    return result.stdout

def run_staging_models():
    """Run staging models."""
    return _run_dbt('staging')

def run_intermediate_models():
    """Run intermediate models."""
    return _run_dbt('intermediate')

def run_mart_models():
    """Run mart models."""
    return _run_dbt('marts')

def run_full_pipeline():
    """Run complete dbt pipeline: deps -> staging -> intermediate -> marts."""
    env = _get_dbt_env()
    result = subprocess.run(
        ['dbt', 'deps', '--profiles-dir', DBT_DIR, '--project-dir', '.'],
        env=env, capture_output=True, text=True, timeout=300, cwd=DBT_DIR
    )
    if result.returncode != 0:
        raise Exception(f"dbt deps failed: {result.stderr}")

    _run_dbt('staging')
    _run_dbt('intermediate')
    _run_dbt('marts')
