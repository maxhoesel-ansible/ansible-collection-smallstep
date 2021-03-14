# Contribution Guide

So you want to contribute something to this collection? Awesome! This guide should give you all the information needed to get started.

Note that by contributing to this collection, you agree with the code of conduct you can find [here.](https://github.com/maxhoesel/ansible-collection-smallstep/blob/devel/CODE_OF_CONDUCT.md)

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

To begin development on this collection, perform the following steps:

1. Fork the repo
2. Clone your fork to your machine
3. Install the following depdencies:
    - Docker: Must be running for tests and be manageable by the current user.
      You must also have the `docker` pip package installed.
    - Ansible: This collection always supports the latest and second-latest release
    - pip: `molecule molecule-docker` for testing roles

### Make your changes

Please make sure that each change is contained in a single, independent commit.
Follow best practices when it comes to creating and naming commits.
All commits **must** follow the [conventional-commits standard](https://www.conventionalcommits.org/en/v1.0.0/):

`<type>(optional scope): <description>`

- Valid types can be found in `.chlog/config.yml`
- Valid scopes are all components of this collection, such as modules or roles
- The description must be lower-case

Example: `fix(step_ca): also clean up on EL8`

#### Hints for module development

- Make sure that you have read the [Ansible module conventions](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html)
- Each module should typically wrap around one step-cli command or a set of closely related commands.
  The modules name should reflect this. For example, step_ca_provisioner performs the same functionality as "step ca provisioner add/remove".
- Make sure to use the doc fragment and utils already present.
  You can also add additional utils if they can be used in multiple modules.
- If you need to call `step-cli`, do so via `run_step_cli_command()` in `run.py`.
  This function automatically assembles command-line arguments for you - all you
  need to do is provide it with a simple mapping dict. It also handles errors and check mode for you
- If you are using the `ca_config` parameter, make sure to initialize it like so:
  ```
  CA_CONFIG = "{steppath}/config/ca.json".format(steppath=os.environ.get("STEPPATH", os.environ["HOME"] + "/.step"))
  ...
  module_args = dict(
    ca_config=dict(type="path", default=CA_CONFIG),
    ...
  )
  ```
  This ensures that the config file is read from the correct path, regardless of whether STEPPATH is set or not.
  If ansible-test complains about the doc spec and argspec not matching, add this line to all the `ignore` files in `tests/sanity`:
  `plugins/modules/your_module_name.py validate-modules:doc-default-does-not-match-spec # Can't always rely on $STEPPATH being set`


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
- You can run modules from this collection with `environment: {"STEPPATH": "{{ STEP_CA_PATH }}"}` if you don't want to specify ca_config for every call

### Submitting your Changes

The "Before-opening-a-PR-Checklist":

- Your commit history is clean and follows the conventional commits standard
- All local tests succeed (both roles and modules)
- The documentation is up-to-date
- (Rebasing against the current devel is always a good idea)

## Release Workflow

This project uses sematic versioning. Name versions accordingly.

0. Install [git-chlog](https://github.com/git-chglog/git-chglog) to generate the changelog
1. Create a new branch named "vX.Y.Z" and check it out
2. Bump the version number in `galaxy.yml` and commit the change
3. Run `git-chlog --next-tag vX.Y.Z` to update the changelog. Make sure to remove any mentions of "unreleased", then commit it
4. Push the branch and create a pull request onto `main`
5. Wait for all tests to complete, then merge it.
6. Create a release referencing main, with a link to the changelog and add a collection.tar.gz archive
7. Merge main back into devel
