-- Idempotent initialization for superset DB and user
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'superset_db') THEN
        CREATE DATABASE superset_db;
    END IF;
END$$;

-- Create role if not exists and set password
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'superset_user') THEN
        CREATE ROLE superset_user LOGIN PASSWORD 'superset_password';
    ELSE
        ALTER ROLE superset_user WITH PASSWORD 'superset_password';
    END IF;
END$$;

GRANT ALL PRIVILEGES ON DATABASE superset_db TO superset_user;
