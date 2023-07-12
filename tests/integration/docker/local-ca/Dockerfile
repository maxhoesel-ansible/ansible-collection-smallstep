# Dockerfile for a python-capable step-ca container that can be accessed by ansible
# Heavily modified and *highly* cursed variant of the step-ca dockerfile
# https://github.com/smallstep/certificates/blob/master/docker/Dockerfile.step-ca

ARG STEP_CA_VERSION=latest
ARG PYTHON_VERSION=3.6

FROM docker.io/smallstep/step-ca:${STEP_CA_VERSION} as ca

FROM python:${PYTHON_VERSION}-alpine

ARG STEP_CA_USER=step

# Get binaries from step-ca container
COPY --from=ca /usr/local/bin/step /usr/local/bin/step
COPY --from=ca /usr/local/bin/step-ca /usr/local/bin/step-ca

# Recreate step environment
ENV STEP="/home/${STEP_CA_USER}"
ENV STEPPATH="/home/${STEP_CA_USER}"
ARG STEPUID=1000
ARG STEPGID=1000
# Ansible-test still connects to the container via SSH, so let's also install a server
# ipruote2 is needed for ansible_default_ipv4/6 facts
# sudo is needed for become: in ansible, su-exec is used to start step-ca, shadow to unlock the root user for ssh login
RUN apk update \
    && apk upgrade \
    && apk add --no-cache bash curl tzdata libcap openssh iproute2 sudo su-exec shadow procps\
    && setcap CAP_NET_BIND_SERVICE=+eip /usr/local/bin/step-ca \
    && addgroup -g ${STEPGID} step \
    && adduser -D -u ${STEPUID} -G step ${STEP_CA_USER} \
    && chown ${STEP_CA_USER}:step /home/${STEP_CA_USER}

# SSH setup, generate keys, permit root login, allow step to start it
RUN cd /etc/ssh \
    && ssh-keygen -A \
    && echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config \
    && usermod -p $1$pBxtBT.3$T4Vx/azTzrgdpJzAP/O121 root \
    && usermod -U root

ENV CONFIGPATH="/home/${STEP_CA_USER}/config/ca.json"
ENV PWDPATH="/home/${STEP_CA_USER}/secrets/password"

VOLUME ["/home/${STEP_CA_USER}"]
STOPSIGNAL SIGTERM
HEALTHCHECK CMD step ca health 2>/dev/null | grep "^ok" >/dev/null

COPY --from=ca /entrypoint.sh /entrypoint.sh
COPY pre-entry.sh /pre-entry.sh

# Start the container as root then switch to step for the actual
ENTRYPOINT ["/bin/bash", "/pre-entry.sh"]
CMD exec /usr/local/bin/step-ca --password-file $PWDPATH $CONFIGPATH

# Custom overrides for our local tests, this allows the container to initialize on its own
ENV DOCKER_STEPCA_INIT_NAME=Ansible-Test
ENV DOCKER_STEPCA_INIT_DNS_NAMES=localhost,step-ca
