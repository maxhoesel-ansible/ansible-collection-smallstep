Some modules, such as `step_ca_provisioner` need to be run on the same host as the `step-ca` server.
To enable this in ansible integration tests, we use a custom Docker image based on the official ansible test image that also runs `step-ca`.

This dockerfile is built automatically by pytest when module tests are executed
