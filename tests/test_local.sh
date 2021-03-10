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

show_help() {
    printf "Usage: ./test_local.sh (-hkv?) command\n"
    printf "Parameters:\n"
    printf "    command: The molecule command to execute (e.g. \"converge\"). Default: \"test\"\n"
    printf "Arguments:\n"
    printf "    -h: This help screen\n"
}

test_role() {
    printf "Testing role %s with molecule..\n" "$1"
    cd "$1"
    molecule "$MOLECULE_COMMAND"
    cd ..
}

run() {
    # Go into root directory of project
    cd "$SCRIPT_DIR/../"

    # Create venv and install requirements
    printf "Creating testing virtualenv...\n\n"
    python3 -m venv "$VENV_DIR"
    # shellcheck disable=SC1090
    source "$VENV_DIR/bin/activate"
    pip3 install --upgrade pip
    pip3 install ansible docker molecule molecule-docker yamllint ansible-lint --upgrade
    # Build and install our collection
    printf "\nBuilding and installing collection...\n\n"
    mkdir -p "$COLLECTIONS_DIR"
    ansible-galaxy collection build --force --output-path "$COLLECTIONS_DIR"
    ansible-galaxy collection install --force -p "$COLLECTIONS_DIR" "$COLLECTIONS_DIR"/maxhoesel-smallstep-*.tar.gz

    printf "\nRunning Linters...\n\n"
    export ANSIBLE_COLLECTIONS_PATH="$COLLECTIONS_DIR"
    ansible-lint 

    printf "\nRunning molecule tests for roles\n\n"
    export TESTENV_COLLECTIONS="$COLLECTIONS_DIR"
    cd roles
    test_role step_cli
    test_role step_ca
    cd ..

}

set +u
if [ "$1" == "-h" ]; then
    show_help
    exit 0
fi
if [ -z "$1" ]; then
    MOLECULE_COMMAND="test"
else
    MOLECULE_COMMAND="$1"
fi
set -u

if ! command -v docker &> /dev/null; then
    echo "Please install docker on your system and ensure this account can access the docker command"
    exit 1
fi

run
