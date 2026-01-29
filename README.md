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


Phase 2 - Database & Ingestion
1. Ensure `Postgres` init SQL files exist in `./Postgres` (created by this repo). They will run only on a fresh init.
2. Fix host permissions on the Postgres data folder before starting containers (example):

   # set owner to postgres-like uid/gid (defaults to 999:999 used by many images)
   chmod +x scripts/fix_postgres_perms.sh
   ./scripts/fix_postgres_perms.sh 999 999

3. Populate `.env` with real values (copy from `.env.example`).
4. Start services:
   docker compose up -d

Phase 3 - dbt
- Basic dbt project is scaffolded in `./dbt` with:
  - `dbt_project.yml`
  - `profiles.yml.example`
  - `models/staging/stg_weather_data.sql`
  - `models/marts/daily_average.sql`

Phase 4 - Visualization
- Placeholder config for Superset is in `docker/superset_config.py` and `docker/dockerinit.sh` to add init commands.

Notes:
- If you mount `/var/run/docker.sock` for the Airflow container, you may need to add group 101 (docker group) to Airflow's runtime user so it can access the socket. Example on host: `sudo usermod -aG docker $USER` and restart your shell or use proper container user mapping.
- Postgres initialization scripts under `./Postgres` are idempotent and safe to re-run on a fresh DB creation.

