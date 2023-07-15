ARG STEP_CA_VERSION
ARG ANSIBLE_VERSION

FROM docker.io/smallstep/step-ca:${STEP_CA_VERSION} as ca

# This is only a target, the exact ansible version does not matter
# as long as that image has our required python lib
FROM quay.io/ansible/default-test-container:stable-2.15

# Get binaries from step-ca container
COPY --from=ca /usr/local/bin/step /usr/local/bin/step
COPY --from=ca /usr/local/bin/step-ca /usr/local/bin/step-ca

# Install and enable the systemd service
COPY step-ca.service /etc/systemd/system/step-ca.service
COPY step-ca.sh /usr/local/bin/step-ca.sh
RUN ln -s /etc/systemd/system/step-ca.service /etc/systemd/system/multi-user.target.wants/step-ca.service \
    && chmod 755 /usr/local/bin/step-ca.sh

# Recreate step environment
ENV STEP="/home/step"
ENV STEPPATH="/home/step"
RUN apt update && apt -y -qq install libcap2-bin sudo \
    && setcap CAP_NET_BIND_SERVICE=+eip /usr/local/bin/step-ca \
    && useradd -m step \
    && echo "step ALL=NOPASSWD: ALL" > /etc/sudoers.d/00_step \
    && rm -rf /var/lib/apt/lists/*
