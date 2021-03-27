#!/usr/bin/env bash

rm -rf ansible_collections
# Need to install the collection in ~/.ansible to test roles, see test_roles.sh
rm -rf ~/.ansible/collections/ansible_collections/maxhoesel/smallstep

rm -rf .cache
