#!/usr/bin/env bash

# Remove previous test installs
rm -r ansible_collections

# Remove old built versions
rm maxhoesel-smallstep-*.tar.gz

ansible-galaxy collection build --force .

ansible-galaxy collection install maxhoesel-smallstep-*.tar.gz -p .
