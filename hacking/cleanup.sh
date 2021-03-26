#!/usr/bin/env bash

rm -rf ansible_collections
rm -rf hacking/venv
# Need to install the collection in ~/.ansible to test roles, see test_roles.sh
rm -rf ~/.ansible/collections/ansible_collections/maxhoesel/smallstep

rm -rf .cache
