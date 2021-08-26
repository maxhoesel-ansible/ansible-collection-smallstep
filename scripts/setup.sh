#!/usr/bin/env bash
set -eu
set -e pipefail

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install 'gitlint>=0.15.0,<0.16.0'

gitlint install-hook

# Initialize tox venvs
tox -l > /dev/null
