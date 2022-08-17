#!/usr/bin/env bash

set -e

/usr/sbin/sshd

su-exec step bash /entrypoint.sh "${@}"
