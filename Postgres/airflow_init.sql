-- Idempotent initialization for airflow DB and user
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'airflow_db') THEN
        CREATE DATABASE airflow_db;
    END IF;
END$$;

-- Create role if not exists and set password
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'airflow_user') THEN
        CREATE ROLE airflow_user LOGIN PASSWORD 'airflow_password';
    ELSE
        ALTER ROLE airflow_user WITH PASSWORD 'airflow_password';
    END IF;
END$$;

GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
