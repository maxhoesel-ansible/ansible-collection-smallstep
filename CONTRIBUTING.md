# Contribution Guide

So you want to contribute something to this collection? Awesome! This guide should give you all the information needed to get started.

## Project Overview

The collections directory layout follows the standard collection structure, as documented [here](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html). There are a few additional directories:

- `.chlog`: Automatic changelog generation
- `.github/`: GitHub Actions CI configuration
- `molecule/`: Molecule testing framework
    - `files/`: Static files used during testing
    - `tests/`: Test cases for individual components
- tests: Local testing tools


## Contribution Workflow

The basic workflow for making a contribution to this collection looks like this:

0. (Prequesite: Make sure that you agree with the [Code of Conduct.](https://github.com/maxhoesel/ansible-collection-smallstep/blob/devel/CODE_OF_CONDUCT.yml))
1. Fork the main repo.
2. Make your changes.
2. Update tests and documentation.
3. Test your changes locally.
4. Commit your changes locally
5. Push your changes to your repo.
6. Create a pull request.

### Creating a Fork and Making Changes

1. Fork the repository in GitHub.
2. Clone our fork to your machine and create a new branch.
3. Make all the changes you need to on your branch.

### Updating Tests and Documentation

- If you added/modified a feature to/of an existing component, make sure that the appropriate `verify_` file has appropriate test cases.
- If you added a new component, you will need to create a new `verify_` file and populate it with test cases. Make sure to include the tests in the main `verify.yml` as well.

Additionally, please make sure that the documentation ins `docs/` and the `README.md` are up-to-date.

### Testing Locally

You can test the changes you made locally with the testing scripts located in `tests/`. These will run the molecule tests on your local host using docker.

Steps to test locally:

1. Install docker and make sure that your user can access the docker socket.
2. Run `tets/test_local.sh`. The script will create a temporary testing environment in `testing/testenv` and install all requirements there, before running molecule..
3. Make changes as needed until all tests succeed.
4. Run `tests/cleanup.sh` to remove the local testing environment.

#### Hints for Testing

- You can optionally pass a molecule command to `test_local.sh` to limit the scope of the molecule run (e.g. `converge` to create and configure the hosts).
- You can use a few environment variables to make testing easier, especially when debugging modules. The following envvars are available:
    - `TESTENV_KEEP_REMOTE` (false): Set to true to keep remote Ansible files on hosts. Useful for module debugging.
    - `TESTENV_VERBOSE` (false): Set to true to change Ansibles output verbosity to `-vvv
    - To debug modules, you can use this command: `TESTENV_VERBOSE=True TESTENV_KEEP_REMOTE=True ./tests/test_local.sh`

### Submitting your Changes

#### Commit style

Before you make your changes public, please make sure that your commit messages are clean and understandable

Commits **MUST** follow the [conventional-commits standard](https://www.conventionalcommits.org/en/v1.0.0/):

`<type>[optional scope]: <description>`

- Valid types can be found in `.chlog/config.yml`
- Valid scopes are all components of this collection, such as modules or roles
- The description must be lower-case

Example: `fix(ca_server): not cleaning up files on EL8`

Remember: As long as you are working on a private branch, it's okay to rewrite history with `git-rebase`.
What matters is that the final pull contains one commit following the spec above for each functional change.

#### Submission workflow

1. Create local commits
2. Push your branch to your local repo
3. Create a pull request from your branch onto the `devel` branch of the main repository
4. The CI tests will run automatically and inform you if any more changes need to be made
5. Wait for feedback or approval
