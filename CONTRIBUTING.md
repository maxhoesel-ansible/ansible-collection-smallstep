# Contribution Guide

Below you will find the information needed to contribute to this project.

Note that by contributing to this collection, you agree with the code of conduct you can find [here.](CODE_OF_CONDUCT.md)

## Quick-start using the devcontainer

Requirements:

- Docker

This repository comes with a `devcontainer.json` file that compatible editors (like VSCode) can use to quickly run a development container with all the required dependencies needed to work on this collection.

To use the devcontainer, either click on the automatic prompt that should pop up when opening this repository,
or manually open the repository inside the devcontainer by selecting that option in the bottom left remote menu inside VSCode.

You should now have a fully functional dev environment with all the tools you will need to work on this collection.

## Manual setup

To begin development on this collection, you need to have the following dependencies installed:

- Docker, accessible by your local user account
- Python 3.8 or newer (for running ansible-core 2.13+)

Then, run the following steps

1. Clone the repository to your local machine
2. Run `./scripts/setup.sh` to configure a local dev environment (virtualenv) with all required dependencies
3. Activate the virtualenv with `source .venv/bin/activate`
4. Make your changes and commit them to a new branch
5. Run the tests locally with `./scripts/test.sh`. This will run the full test suite that also runs in the CI
6. Once you're done, commit your changes (make sure that you are in the venv).
   Pre-commit will format your code and check for any obvious errors when you do so.

## Hints for Development

For Modules:
- Make sure that you have read the [Ansible module conventions](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html)
- Make sure to use the doc fragment and utils already present when possible.
- Each module should typically wrap around one step-cli command or a set of closely related commands.
  The modules name should reflect this. For example, step_ca_provisioner performs the same functionality as "step ca provisioner add/remove".
- Make sure to use the doc fragment and utils already present, specifically the connection fragments used for parameters like --ca-url and --offline.
- If you need to call `step-cli`, do so via `run_step_cli_command()` in `run.py`.
  This function automatically assembles command-line arguments for you - all you
  need to do is provide it with a simple dict of module parameters mapped to their CLI equivalent. It also handles errors and check mode for you
- If you need to troubleshoot inside the ansible-test container, add `--docker-terminate never` to the
  call inside the hacking script. The container will then persist even on failure, and you can debug it

For Roles:
- None so far

In general:
- Don't be afraid to rewrite your local branch history to clean up your commit messages!
  You should familiarize yourself with `git rebase -i` if you haven't done so already.

## Testing Framework

We use `molecule` to test all roles and the `ansible-test` suite to test modules. Calls to these are handled by `tox` and the [`tox-ansible` extension]( https://github.com/ansible-community/tox-ansible).
You can run all the required tests for this project with `./scripts/test.sh`. You can also open that file to view the individual test stages.

Note that you **can't** just run `tox`, as the `sanity` and `integration` environments need extra parameters passed to
`ansible-test`. Without these, they will fail. In addition, the `tox-ansible` plugin (which automatically generate scenario envs)
also adds a few unneeded environments to the list, such as `env`.

#### Creating new module tests

We currently only run integration tests for our modules via `ansible-test`. If you added a new module (or added new functionality to an already existing module),
you will need to write new tests for it. Each module has its own integration target in `tests/integration/targets`. To start, copy an existing targets directory
and adjust the test tasks for your module.

Some additional hints:

- All targets are run sequentially on the same host. Make sure to clean up after yourself! You don't need to handle failures gracefully however,
  as the testing environment is destroyed on the first error.
- All targets call the `setup_smallstep` target via the dependency declared in `meta/main.yml`. This target performs basic setup
  of both step-cli and step-ca, so you don't need to install them in your target
- See `targets/setup_smallstep/defaults/main.yml` for some variables you can use in your tests
- You can run modules from this collection with `environment: {"STEPPATH": "{{ STEP_CA_PATH }}"}` if you don't want to specify ca_config/ca_url for every module call

### Updating test versions

To update the smallstep cli/ca versions that are used to run the tests, the following files need to be modified:

- `tests/integration/targets/setup_smallstep/vars/versions.yml`: Versions for module integration test
- `tests/molecule/group_vars/all/versions.yml`: Versions for molecule tests

## Information for maintainers

This project uses sematic versioning. Version numbers and  releases/changelogs are automatically generated using [release-drafter](https://github.com/release-drafter/release-drafter), utilizing pull request labels.

When merging a pull request, make sure to select an appropriate label (pr-bugfix, pr-feature, etc.).
release-drafter will automatically update the draft release changelog and the galaxy.yml version will be bumped if needed.

Once a draft release is published, collection packages will be added to the release and ansible-galaxy automatically.

If you need to manually bump the collection version, run the `update-version` script and adjust the test versions if required.
