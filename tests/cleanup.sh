#!/usr/bin/env bash

set -eu
set -o pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# Directory for the local testing dependencies
TESTENV_DIR="$SCRIPT_DIR/testenv"
# Directory in which to create the testing virtualenv
VENV_DIR="$TESTENV_DIR/venv"
# Path under which the collection will be installed for testing
COLLECTIONS_DIR="$TESTENV_DIR/ansible/"

# Destroy Docker/Molecule fragments
export TESTENV_COLLECTIONS="$COLLECTIONS_DIR"
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
molecule destroy
deactivate

rm -rf "$TESTENV_DIR"
