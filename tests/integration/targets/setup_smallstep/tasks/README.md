# setup target

This integration target performs basic setup and initialization of the testing container(s).

To test the various modules, we need to make the following modifications to the container used by ansible-test:

1. Install step-cli and step-ca via our roles
2. Install several required packages
