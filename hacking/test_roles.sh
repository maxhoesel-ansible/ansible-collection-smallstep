#!/usr/bin/env bash

set -eu

cleanup() {
    ./hacking/cleanup.sh
}

trap cleanup err exit

ansible-lint -v

for role in roles/*; do
    (cd "$role" && molecule test)
done
