# Contribution Guide

This document contains the information needed to contribute to this project.
In here you will find the basic steps for getting started, as well as an overview over our testing system.

Note that by contributing to this collection, you agree with the code of conduct you can find [here.](/CODE_OF_CONDUCT.md)

## Getting Started

Prerequisites:

- A recent version of Python supported by `ansible-core` (see [here](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements))
- For role tests: `podman` 4 or newer set up as shown [below](#setting-up-podman) (note that Docker will *not* work for role tests!)
- For plugin tests: A recent version of Docker

Steps:

1. Clone the repository (or your fork) to your local machine
2. Run `./scripts/setup.sh`. This will set up a virtual environment with all required dependencies for development
3. Activate the virtualenv with `source .venv/bin/activate`
4. Make your changes
5. Run the relevant tests using the instructions in [here](#testing-changes)
6. Once you're done, commit your changes and open a PR

## Developing Content

### Plugins (and Modules)

The plugins in this collection are mostly simple wrappers around the `step-cli` tool.
Feel free to add a new plugin if you would like to implement another functionality.
Here are some general hints for plugin development:

- All plugins should target Python 3.6 as the minimum supported version
- Read the [Ansible module conventions](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html)
- Use the pre-existing `doc_fragments` and `module_utils` python modules where applicable. Feel free to use an existing plugin/module as a base
- Name your module according to the `step-li` command that it wraps around (Example: `step-cli ca provisioner` -> `step_ca_provisioner`).
- Use the `CLIWrapper` class in [step_cli_wrapper.py](/plugins/module_utils/step_cli_wrapper.py) to run step-cli commands
- Try to make the calls idempotent where possible.
- Modules should always support check mode

### Roles

Each role in this collection performs a complex task to bring a remote host into a desired state.
If you want to write a new role, look to the existing ones for inspiration.

Some general guidelines:

- Try to support most common Linux distributions (including Ubuntu, Debian, Fedora and Rockylinux)
    - You should test every supported distro in your `molecule.yml` see [here](#roles-2)
- Keep the configuration for the user simple and try to provide sensible defaults where possible
- Try to avoid using complex data structures as role variables/parameters, use simple values that can be composed easily instead.
- Make sure to document any role variables in both the `README.md` and in the `meta/argument_specs.yml` file.
  Te latter is used to generate role documentation programmatically.

## Testing Changes

We aim to test all of the components in this collection as thoroughly as possible.
We currently test all components using the following testing matrix:

- Ansible version: The three most recent major releases (such as 6,7,8), with a compatible host Python
- Node Python: The minimum supported Python version (see `tox.ini`)
- Step-CLI/CA version: The most recent minor release corresponding to the collections version (e.g. collection version `0.24.X` is teated with `step-cli/ca` `0.24.y`)
- For each entry in this matrix, we test all roles on all of their supported platforms, as well as all modules/plugins

To make testing all these permutations easier, we use `tox`to manage test scenarios.
If you set up the test environment as described in [the Getting Started guide](#getting-started), you should be able to run `tox -l` from the collection root:

This should print a list of test environments (scenarios) that you can run.
To run a specific environment, just use `tox -e {environment}`.
You can also use substitution syntax to run multiple environments at once:

```bash
# Will run the py3-ansible7-roles-step_cli environment
tox -e py3-ansible7-roles-step_cli

# Will run XXX-roles-step_cli environment with ansible versions 6,7 and 8
# Note the single quotes around the string!
tox -e 'py3-ansible{6,7,8}-roles-step_cli'
```

### Plugins (and Modules)

Modules (and plugins in general) are verified using `ansible-test`, specifically sanity, unit (TBD) and integration tests, all run from tox.
Since many plugins in this collection need access to a step-ca server, the `tox` environments spin up additional docker containers as needed -
see [`tox.ini`](./tox.ini) and the `docker-compose.yml` files in `tests/{integration/sanity}` for details.

You should always run the plugin tests after making changes to one (sanity, unit (TBD), integration):

```bash
tox -e 'py3-ansible215-test-{sanity,integration,#add other environments here}'
```

### Roles

We use the `tox-ansible` plugin (v1) to integrate molecule scenarios into tox.
You can run these scenarios using `tox -e`, just like for module tests.

Molecule itself runs the subject role against several containers to verify its functionality across target systems.
Since some roles involve the management of systemd services, we need a container runtime with good systemd support,
something which `docker` sadly doesn't offer on [modern linux distros](https://gist.github.com/pinkeen/bba0a6790fec96d6c8de84bd824ad933).

Instead, we use `podman`, a daemonless, rootless container runtime developed by RedHat to be (mostly) compatible to docker, but with better support for certain features such as systemd.
See below for setup instructions.
Once podman is installed and running, you can use `tox` to run the molecule scenarios.

#### Setting up Podman

1. Ensure that you have the following packages installed:
    - `podman` version 4+ (as it comes with the new netvark networking stack)
    - `aardvark-dns`, a plugin for netvark which provides DNS between containers in the same network
    - **NOTE:** If you previously used an older (`<=3.x`) version of `podman`, you will have to migrate to the new networking stack fist. This can be done with `podman system reset`
2. Ensure that your user has a subuid/subguid configuration associated with them so that you can run rootless containers
    - Check the `/etc/subuid` and `/etc/subgid` files for entries corresponding to your username.
    - If there is nothing, you can add them like so: `sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 <USERNAME>` (make sure that the range is not  already taken by another user in `/etc/subuid`/`/etc/subgid`).
3. Once you have applied your changes, run `podman system migrate` to force `podman` to pick up the new configuration.

That's it! Podman should now be working! To test it, you can run a container just like with docker: `podman run --rm -it ubuntu bash`

## Writing Tests

Any new new component or change to an existing one should be covered by tests to ensure that the code works, and that it keeps working into the future.
This section will help you in adding your own tests to this collection.

#### Plugins

Unit tests are currently not used in this collection, this section will be filled once the need for them arises.

For integration tests, you can get started by either copying an existing target such as [`step_ca_certificate`](./tests/integration/targets/step_ca_certificate/), or starting out from scratch.
Each target is an ansible role containing tasks that verify the functionality of a plugin.
Your targets directory structure should look like this:

```
meta/
  main.yml
tasks/
  main.yml
```

Since many plugins need to connect to a CA to verify functionality, you can set up your target to connect to either a remote (network) or a local CA:

```yaml
# in meta/main.yml:
dependencies:
  # Setup the target role for accessing a CA over the network, this is the default
  - setup_remote_ca
  # Setup the target role for accessing a CA that is installed locally.
  # This is needed for certain plugins/modules such as step_ca_provisioner.
  # Mutually exclusive with setup_remote_ca
  #- setup_local_ca
```

Your target will then be set up for accessing the selected CA.
For more details, see the integration config templates for the [remote]() and the [local]() CA.

```yaml
# in tasks/main.yml:
- name: Get a certificate from the remote CA
  maxhoesel.smallstep.step_ca_certificate:
    # parameters go here
```

#### Roles

There are tons of good guides online for how to write tests using molecule.
Alternatively, you can always look at the existing molecule scenarios in this collection

When creating a new molecule scenario, your directory structure should look like this:

```
some_role/
  defaults/
  meta/
  molecule/
    default/
      converge.yml
      molecule.yml
      prepare.yml
      requirements.txt # --> symlink to /tests/roles/requirements.txt
      verify.yml
    another-scenario/
      ...
  tasks
  ...
```

The `requirements.txt` symlink is used by `tox-ansible` when running tests via `tox` to install a specific, known-good version of `molecule` and the `molecule-podman` driver.
That way, all roles and scenarios in this collection can use the same version of `molecule`.

The [root molecule config](./.config/molecule/config.yml) contains the basic settings for molecule, such as driver setup and the step utility versions.
In addition, your roles molecule scenario must define a set of platforms to test on, as well as any inventory configuration that you may need.
To get started you can copy the `molecule.yml` configuration from an existing role, then adjust it to suit your needs.

## Collection Docs

In addition to the `README.md`s, we use `antsibull-docs` to generate sphinx documentation for both plugins and roles (from the `meta/argument_specs.yml` file).
See [here](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_documenting.html) for more information about the build process.

The CI also builds the docs to ensure they don't break silently.

## Maintainer information

### Updating Tested Versions

- Smallstep CLI/CA and Node Python: Bump the values in `tox.ini` (`consts` section)
- ansible-core (for plugins): Add the new core version to the following places in `tox.ini`:
    - The `envlist` in `tox.ini`
    - each `testenv:xxx` section header that deals with plugin tests
    - Set the correct environment variable in the main `testenv` section
- ansible (for roles): Change the version string in the `ansible` section in `tox.ini`

### Versioning and Releases

- This project uses sematic versioning. the collection version stays in sync with the `step-cli`` utility version to ensure compatibility.
  This means that any breaking changes can only be shipped when updates to the `step-cli` utility are released.
  Version numbers and releases/changelogs are automatically generated using [release-drafter](https://github.com/release-drafter/release-drafter), utilizing pull request labels.
- When merging a pull request, make sure to select an appropriate label (pr-bugfix, pr-feature, etc.).
  Release-drafter will automatically update the draft release changelog and the galaxy.yml version will be bumped if needed.
- Once a draft release is actually published, collection packages will be added to the release and ansible-galaxy automatically.
- If you need to manually bump the collection version, run the `update-version` script and adjust the test versions if required.
