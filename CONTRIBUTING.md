# Contribution Guide

So you want to contribute something to this collection? Awesome! This guide should give you all the information needed to get started.

Note that by contributing to this collection, you agree with the code of conduct you can find [here.](https://github.com/maxhoesel/ansible-collection-smallstep/blob/main/CODE_OF_CONDUCT.md)

## Contribution Workflow

To successfully submit your changes to this collection, please make sure to follow the steps below:

1. Open an issue and discuss your proposal
2. Fork and setup your local environment
3. Make your changes
4. Update tests and documentation.
5. Test your changes locally.
6. Push and open a PR
7. Respond to any feedback/CI failures

### Suggesting your changes

Start off any major contribution by opening an issue. Not only is it a good idea to bounce off your ideas against other people first,
it also leaves a trail in the repo for other people to follow in the future.

### Fork and setup your local environment

To begin development on this collection, you need the following dependencies installed:

- Docker, accessible by your local user account
- Python 3.6 or higher

Fork the repo and clone it to your local machine, then run `hacking/env_setup.sh`.
This script will set up a local dev environment for you. In particular, it will:

- Create a virtualenv in hacking/venv/
- Install all the dev dependencies in it
- Install and activate commit hooks to lint commit messages and catch common errors

To begin, activate the venv with `. hacking/venv/bin/activate`

If you need to clear the environment for whatever reason, just run
`deactivate && rm -rf ./venv`

### Make your changes

Please make sure that each change is contained in a single, independent commit.
Follow best practices when it comes to creating and naming commits.
All commits **must** follow the [conventional-commits standard](https://www.conventionalcommits.org/en/v1.0.0/):

`<type>(optional scope): <description>`

- Valid scopes are all components of this collection, such as modules or roles
- The description must be lower-case

Example: `fix(step_ca): clean up files on EL8`

#### Hints for module development

- Make sure that you have read the [Ansible module conventions](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html)
- Each module should typically wrap around one step-cli command or a set of closely related commands.
  The modules name should reflect this. For example, step_ca_provisioner performs the same functionality as "step ca provisioner add/remove".
- Make sure to use the doc fragment and utils already present.
  You can also add additional utils if they can be used in multiple modules.
- If you need to call `step-cli`, do so via `run_step_cli_command()` in `run.py`.
  This function automatically assembles command-line arguments for you - all you
  need to do is provide it with a simple mapping dict. It also handles errors and check mode for you
- If you need to troubleshoot inside the ansible-test container, add `--docker-terminate never` to the
  call inside the hacking script. The container will then persist even on failure, and you can debug it

#### Hints for role development

None so far

### Update Tests and Documentation

We use `molecule` to test all roles and the `ansible-test` suite to rest modules. In addition to local tests,
CI jobs are also run on every push/PR against one of the main branches.

To test your changes locally, follow the steps above and then run either `hacking/test_modules.sh` or `hacking/test_roles.sh`, depending
on what you changed. These scripts will run a subset of the CI tests in an isolated environment via docker and report any obvious errors back
to you.

#### Creating new module tests

We currently only run integration tests for our modules via `ansible-test`. If you added a new module (or added new functionality to an already existing module),
you will need to write new tests for it. Each module has its own integration target in `tests/integration/targets`. To start, copy an existing targets directory
and adjust the test tasks for your module.

Some additional hints:

- All targets are run sequentially on the same host. Make sure to clean up after yourself! You don't need to handle failures gracefully however,
  as the testing environment is destroyed on the first error anyways.
- All targets call the `setup_smallstep` target via the dependency declared in `meta/main.yml`. This target performs basic setup
  of both step-cli and step-ca using, so you don't need to install them in your target
- See `targets/setup_smallstep/defaults/main.yml` for some variables you can use in your tests
- You can run modules from this collection with `environment: {"STEPPATH": "{{ STEP_CA_PATH }}"}` if you don't want to specify ca_config/ca_url for every module call

### Submitting your Changes

The "Before-opening-a-PR-Checklist":

- Your commit history is clean
- The documentation is up-to-date
- All local tests and commit hooks succeed
- (Rebasing against the current main before pushing is always a good idea)

## Release Workflow

This project uses sematic versioning. Name versions accordingly.

For now, releases are simply tags on the main branch, with no separate release branch currently in use.

---
**NOTE**

This still needs to be implemented

---

To create a release, simply run the "Create Release" GitHub Action with the desired version number (e.g. "0.3.0").
This action will:

1. Bump the version number in `galaxy.yml`
2. Update the changelog
3. Commit the changes in a "Release" commit and push it
4. Create a GitHub release (which will also create a tag at that commit)
5. Build the collection and publish the new release on galaxy
