#!/usr/bin/env bash

set -eu
set -o pipefail

python3 -m venv hacking/venv

# shellcheck disable=SC1091
. hacking/venv/bin/activate

pip3 install -r hacking/requirements.txt
ansible-galaxy collection install -r hacking/collections/requirements.yml

pre-commit install
pre-commit install --hook-type commit-msg
