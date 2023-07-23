#!/bin/bash
set -euo pipefail

if [ ! -f "${STEPPATH}/config/ca.json" ]; then
    # Generate password
    set +o pipefail
    < /dev/urandom tr -dc A-Za-z0-9 | head -c40 > "$STEPPATH/password"
    echo
    set -o pipefail

    DOCKER_STEPCA_INIT_PROVISIONER_NAME="${DOCKER_STEPCA_INIT_PROVISIONER_NAME:-admin}"
    DOCKER_STEPCA_INIT_ADMIN_SUBJECT="${DOCKER_STEPCA_INIT_ADMIN_SUBJECT:-step}"
    DOCKER_STEPCA_INIT_ADDRESS="${DOCKER_STEPCA_INIT_ADDRESS:-127.0.0.1:9000}"

    step ca init --name "${DOCKER_STEPCA_INIT_NAME}" \
        --dns "${DOCKER_STEPCA_INIT_DNS_NAMES}" \
        --provisioner "${DOCKER_STEPCA_INIT_PROVISIONER_NAME}" \
        --password-file "${STEPPATH}/password" \
        --provisioner-password-file "${STEPPATH}/password" \
        --address "${DOCKER_STEPCA_INIT_ADDRESS}"
fi

/usr/local/bin/step-ca --password-file "$STEPPATH/password" "$STEPPATH/config/ca.json"
