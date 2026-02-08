#!/usr/bin/env bash
set -euo pipefail

# Use python3 explicitly; provide actionable hint if python3-venv is missing
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is not installed. On Debian/Ubuntu: sudo apt update && sudo apt install -y python3 python3-venv"
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "Virtualenv created and requirements installed. Activate with: source .venv/bin/activate"