# Contribution Guide

Below you will find the information needed to contribute to this project.

Note that by contributing to this collection, you agree with the code of conduct you can find [here.](https://github.com/maxhoesel/ansible-collection-smallstep/blob/main/CODE_OF_CONDUCT.md)

## Requirements

To begin development on this collection, you need to have the following dependencies installed:

- Docker, accessible by your local user account
- Python 3.6 or higher. CI tets run specifically against 3.6, but to make things easier we just use whatever version is available locally
- [Tox](https://tox.readthedocs.io/en/latest/)

## Quick Start

1. Fork the repository and clone it to your local machine
2. Run `./scripts/setup.sh` to configure a local dev environment (virtualenv) with a commit hook
3. Make your changes and commit them to a new branch
4. Run the tests locally with `./scripts/test.sh`. This will run the full test suite that also runs in the CI
5. Once you're done, push your changes and open a PR



## About commit messages and structure

Follow the guidelines below when committing your changes

- All commits **must** follow the [conventional-commits standard](https://www.conventionalcommits.org/en/v1.0.0/):
  `<type>(optional scope): <description>`
  - Valid scopes are all components of this collection, such as modules or roles
- Structure your changes so that they are separated into logical and independent commits whenever possible.
- The commit message should clearly state **what** your change does. The "why" and "how" belong into the commit body.

Some good examples:
- `fix(step_ca): don't install unneeded packages`
- `feat(step_ca_certificate): add support for RA flags`

Don't be afraid to rename/amend/rewrite your branch history to achieve these goals!
Take a look at the `git rebase -i` and `git commit --amend` commands if you are not sure how to do so.
As long as your make these changes on your feature branch, there is no harm in doing so.



## Hints for Development

For Modules:
- Make sure that you have read the [Ansible module conventions](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html)
- Each module should typically wrap around one step-cli command or a set of closely related commands.
  The modules name should reflect this. For example, step_ca_provisioner performs the same functionality as "step ca provisioner add/remove".
- Make sure to use the doc fragment and utils already present, specifically the connection fragments used for parameters like --ca-url and --offline.
- If you need to call `step-cli`, do so via `run_step_cli_command()` in `run.py`.
  This function automatically assembles command-line arguments for you - all you
  need to do is provide it with a simple dict of module parameters mapped to their CLI equivalent. It also handles errors and check mode for you
- If you need to troubleshoot inside the ansible-test container, add `--docker-terminate never` to the
  call inside the hacking script. The container will then persist even on failure, and you can debug it

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

## Release Workflow

This project uses sematic versioning. Name versions accordingly.

For now, releases are simply tags on the main branch, with no separate release branch currently in use.

To create a release, simply run the "Create Release" GitHub Action with the desired version number (e.g. "0.3.0").
This action will:

1. Bump the version number in `galaxy.yml`
2. Update the changelog
3. Commit the changes in a "Release" commit and push it
4. Create a GitHub release (which will also create a tag at that commit)
5. Build the collection and publish the new release on galaxy
