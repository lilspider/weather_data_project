#!/usr/bin/env bash
set -euo pipefail

# Boot the stack
docker compose up -d

# Show basic statuses
sleep 2
docker compose ps
