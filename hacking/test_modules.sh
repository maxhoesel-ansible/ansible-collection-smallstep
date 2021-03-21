#!/usr/bin/env bash

set -eu

cleanup() {
    ./hacking/cleanup.sh
}

trap cleanup err exit

./hacking/build.sh

ansible-galaxy collection install maxhoesel-smallstep-*.tar.gz -p .

(cd ansible_collections/maxhoesel/smallstep/ \
    && ansible-test sanity --docker --requirements -v --color --python 3.6 plugins/ \
    && ansible-test integration --docker --requirements -v --coverage --color --python 3.6 \
)
