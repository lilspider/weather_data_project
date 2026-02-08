-- Unified database initialization for both Airflow and Grafana
-- This script creates databases, users, and tables for the entire weather data project

-- Create Airflow database and user
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'airflow_db') THEN
        CREATE DATABASE airflow_db;
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'airflow_user') THEN
        CREATE ROLE airflow_user LOGIN PASSWORD 'airflow_password';
    ELSE
        ALTER ROLE airflow_user WITH PASSWORD 'airflow_password';
    END IF;
END$$;

GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;

-- Create Grafana reader user
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'grafana_reader') THEN
        CREATE ROLE grafana_reader LOGIN PASSWORD 'grafana_password';
    ELSE
        ALTER ROLE grafana_reader WITH PASSWORD 'grafana_password';
    END IF;
END$$;

-- Create dev schema and raw weather data table with idempotency
\c airflow_db;

CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    temperature NUMERIC,
    weather_descriptions TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(city, recorded_at)
);

-- Grant SELECT permissions on dev schema to grafana_reader for dashboard access
GRANT USAGE ON SCHEMA dev TO grafana_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA dev TO grafana_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA dev GRANT SELECT ON TABLES TO grafana_reader;
