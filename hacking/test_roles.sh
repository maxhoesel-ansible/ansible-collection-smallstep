#!/usr/bin/env bash

(ansible-lint -v \
    && (cd roles/step_cli && molecule test) \
    && (cd roles/step_ca && molecule test) \
)

./hacking/cleanup.sh
