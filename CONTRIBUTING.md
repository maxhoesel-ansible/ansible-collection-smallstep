# Contribution Guide

Below you will find the information needed to contribute to this project.

Note that by contributing to this collection, you agree with the code of conduct you can find [here.](/CODE_OF_CONDUCT.md)

## Requirements

To begin development on this collection, you need to have the following dependencies installed:

- Docker, accessible by your local user account
- Python 3.8 or newer (for running ansible-core 2.13+)

## Quick Start

1. Fork the repository and clone it to your local machine
2. Run `./scripts/setup.sh` to configure a local dev environment (virtualenv) with all required dependencies
3. Activate the virtualenv with `source .venv/bin/activate`
4. Make your changes and commit them to a new branch
5. Run the tests locally with `./scripts/test.sh`. This will run the full test suite that also runs in the CI
6. Once you're done, commit your changes (make sure that you are in the venv).
   Pre-commit will format your code and check for any obvious errors when you do so.

## Development Guide

### Module Development

The modules in this collection are mostly simple wrappers around the `step-cli` tool.
Feel free to add a new module if you would like to implement another subcommand.
Here are some general hints for module development:

- Read the [Ansible module conventions](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html)
- Use the pre-existing `doc_fragments` and `module_utils` python modules where applicable. Feel free to use an existing module as a base
- Name your module according to the `step-li` command that it wraps around (Example: `step-cli ca provisioner` -> `step_ca_provisioner`).
- Use the `CLIWrapper` class in [step_cli_wrapper.py](/plugins/module_utils/step_cli_wrapper.py) to run step-cli commands
- Try to make the calls idempotent where possible. Modules should always support check mode

You need to write tests to ensure that your module works and keeps working properly (see [here](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html) for the Ansible Integration testing guide). Notes:

- Typically, each module should have one integration test target (see [here for examples](/tests/integration/targets/)) that ensures that the module works as expected
- If your module interacts with a remote step CA (i.e. your module is part of the `step ca` subcommand), you can request creating one by adding the following to your targets `meta/main.yml`:

    ```yaml
    # In targets/<your_target>/meta/main.yml

    ---
    dependencies:
    - setup_remote_ca
    ```

    This will automatically configure your host to trust the remote CA. Then, use the variable names defined in `tests/integration/integration_config.yml.template` to access the remote CA. Use an existing target for guidance if needed.
- All targets are run sequentially on the same host. Make sure to clean up after yourself! You don't need to handle failures gracefully however,
  as the testing environment is destroyed on the first error.
- You can test your modules by running `tests/test-modules-sanity` and `tests/test-modules-integration`. These tests are also run as part of the CI.

### Role Development

General Notes:

- None so far

For testing, we use the `molecule` framework. Molecule scenarios are handled by `tox` and the [`tox-ansible` extension]( https://github.com/ansible-community/tox-ansible). Notes:

- To see all available scenarios, run `tox -l` and look for the scenarios starting with `ansible-py*`.
- To run all molecule scenarios, simply call `tests/test-roles`
    - Or pass a (partial) scenario name as a filter to limit execution (for example, `/tests/test-roles acme_cert` to limit molecule scenarios to the ACME role only)

## Information for maintainers

- To update the smallstep cli/ca versions that are used to run the tests, bump the values in `tests/constants.sh`
- This project uses sematic versioning. Version numbers and  releases/changelogs are automatically generated using [release-drafter](https://github.com/release-drafter/release-drafter), utilizing pull request labels.
- When merging a pull request, make sure to select an appropriate label (pr-bugfix, pr-feature, etc.).
  Release-drafter will automatically update the draft release changelog and the galaxy.yml version will be bumped if needed.
- Once a draft release is actually published, collection packages will be added to the release and ansible-galaxy automatically.
- If you need to manually bump the collection version, run the `update-version` script and adjust the test versions if required.
