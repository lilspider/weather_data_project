# Weather Data Project

This project contains an automated pipeline using Airflow, Postgres, dbt, and Superset to ingest and visualize weather data.

Phase 1 - Setup
1. Copy `.env.example` to `.env` and add your `WEATHERSTACK_API_KEY`.
2. Initialize git and create a virtual environment:

   git init
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

3. Run tests or quick local scripts (e.g., `API_request/test_local_run.py`) after setting env vars.

Stop after you commit these initial files and confirm to proceed to Phase 2.
