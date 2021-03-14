#!/usr/bin/env bash

./hacking/build.sh

ansible-galaxy collection install maxhoesel-smallstep-*.tar.gz -p .

(ansible-lint -v && \
    cd ansible_collections/maxhoesel/smallstep/ \
    && (cd roles/step_cli && molecule test) \
    && (cd roles/step_ca && molecule test) \
)

./hacking/cleanup.sh
