#!/usr/bin/env bash
set -eu
set -o pipefail

# Sanity checks for our modules
# We explicitly only support Python 3.6, so the boilerplate isn't required and is automatically removed by pyupgrade
tox -e sanity -- --docker --color -v --python 3.6 --skip-test metaclass-boilerplate --skip-test future-import-boilerplate

# Integration tests for modules
tox -e integration -- --color -v --controller docker:default --target docker:default,python=3.6

# Molecule tests - this grabs all molecule scenarios and executes them.
# Note that to run this command, you need to have
# - run and tox command at least once (tox -l is fine)
# - have the collection built and installed locally.
#   Running the module tests will do that for you
tox -e "$(tox -l | grep ansible | grep -v "lint" | tr '\n' ',')"
