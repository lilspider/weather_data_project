#!/usr/bin/env bash
set -euo pipefail


HOST_UID=${1:-999}
HOST_GID=${2:-999}

TARGET_DIR="${PWD}/postgres_data"

if [ ! -d "$TARGET_DIR" ]; then
  echo "Directory $TARGET_DIR does not exist. Creating..."
  mkdir -p "$TARGET_DIR"
fi

echo "Setting ownership of $TARGET_DIR to $HOST_UID:$HOST_GID and mode 700"
chown -R ${HOST_UID}:${HOST_GID} "$TARGET_DIR"
chmod -R 700 "$TARGET_DIR"

echo "Done. You can now run: docker compose up -d"