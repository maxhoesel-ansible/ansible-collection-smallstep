#!/usr/bin/env bash

set -eu
set -o pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# Directory for the local testing dependencies
TESTENV_DIR="$SCRIPT_DIR/testenv"

rm -rf "$TESTENV_DIR"
