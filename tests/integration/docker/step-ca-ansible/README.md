To test module functionality, we need a ready-to-go docker image serving the smallstep CA to out target container in a docker network.
For most tests, we can simply use the upstream image for this (see the testenv:integration section in [tox.ini](/tox.ini)).

However, there are modules that need direct access to the CA resources (like, on the same host) and the upstream image does not work as an ansible target by default (big surprise).

The Dockerfile in this directory modifies the upstream image to support Ansible connections made from ansible-test, so that our local-only targets can be run on the container directly.
Note that this container is launched by ansible-test, so a lot of typical `docker run` options aren't available, hence the hardcoded values in the Dockerfile.
