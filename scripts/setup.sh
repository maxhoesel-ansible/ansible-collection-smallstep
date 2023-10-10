#!/usr/bin/env bash
set -eu
set -e pipefail

printf "Creating project-specific virtualenv in .venv..."
python3 -m venv .venv
printf "OK\n"

source .venv/bin/activate

printf "Installing development requirements..."
python3 -m pip install --upgrade pip --quiet
python3 -m pip install --quiet -r requirements.txt --upgrade
# Also install the scenario requirements so we can run them directly
python3 -m pip install --quiet -r tests/roles/requirements.txt --upgrade
printf "OK\n"

printf "Installing pre-commit hook..."
pre-commit install > /dev/null
printf "OK\n"

printf "Development venv initialized!\n"
printf "To activate it, run:\n\n"
printf "source .venv/bin/activate\n"
