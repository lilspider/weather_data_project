#!/usr/bin/env bash
set -euo pipefail

HOST=${1:-localhost}
PORT=${2:-5432}
USER=${3:-admin}
DB=${4:-airflow_db}

until pg_isready -h "$HOST" -p "$PORT" -U "$USER" -d "$DB"; do
  echo "Waiting for Postgres at $HOST:$PORT..."
  sleep 2
done

echo "Postgres is ready"