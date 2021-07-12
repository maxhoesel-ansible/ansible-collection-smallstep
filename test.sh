#!/usr/bin/env bash
set -eu
set -o pipefail

# Lint ansible roles and git commits
tox -e lint

# Sanity checks for our modules
tox -e sanity -- --docker --color -v --python 3.6

# Integration tests for modules - we don't have an unit tests as of now
tox -e integration -- --docker --color -v --python 3.6 --docker-terminate success

# Molecule tests - this grabs all molecule scenarios and executes them.
# Note that to run this command, you need to have
# - run and tox command at least once (tox -l is fine)
# - have the collection built and installed locally.
#   Running the module tests will do that for you
tox -e "$(tox -l | grep ansible | grep -v "lint" | tr '\n' ',')"
