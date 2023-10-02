# maxhoesel.smallstep.step_cli

Install the `step-cli`  tool on a host.

This role is used by `step_bootstrap_host` and `step_ca`, but can also be used standalone to install the cli tool and then do nothing else.

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - Fedora 36 or newer
  - A CentOS-compatible distribution like RockyLinux/AlmaLinux 8 or newer. RockyLinux is used for testing
- Supported architectures: amd64, arm64
- This role requires root access. Make sure to run this role with `become: yes` or equivalent

## Role Variables

##### `step_cli_version`
- Set the version of`step-cli`to install
- Can be a version tag (e.g. `0.15.3`), `latest-compatible`, or `latest`.
- If set to `latest-compatible`, the most recent compatible release is installed, that is, the most recent minor release that matches the collection minor version.
  - For example, if the collection version is `0.24.x`, then the most recent release from the `0.24` series will be installed.
  - See the [versioning policy](https://github.com/maxhoesel-ansible/ansible-collection-smallstep/tree/main#versioning-policy) for more details.
- If set to `latest`, the most recent version of`step-cli`is installed, regardless of compatibility with the collection
    - This can be useful if you just want to install `step-cli`, but don't plan on using it with this collection
    - Using collection modules with mismatched minor versions of `step-cli`/`step-ca` is not supported!
- Note that the role will query the GitHub API if this value is set to `latest`. If you are getting rate limit errors, you can:
    - set `step_cli_version` to a specific value
    - set `step_cli_github_token` to a token with higher rate limits
- Default: `latest-compatible`

##### `step_cli_executable`
- What to name and where to put the `step-cli` executable that will be installed by this role
- Can be an absolute path (make sure that the parent directory is in $PATH and has correct SELinux policies set, if applicable) or a filename
- If this executable is not found and `step_cli_executable` is a **path**, the executable will be installed there
- If this executable is not found and  `step_cli_executable` is a **name**, the executable will be installed at `step_cli_install_dir` with the given name
- Default: `step-cli`

##### `step_cli_install_dir`
- Used if `step_cli_executable` is a filename and not yet present
- Sets the directory to install `step_cli_executable` into
- The directory must already exist
- Ignored if `step_cli_executable` contains a path
- Default: `/usr/bin`

## Example Playbook

```yaml
# Install step-cli into the default path
- hosts: all
  roles:
  - role: maxhoesel.smallstep.step_cli
    become: yes

# Install a specific step-cli version to a custom path
- hosts: all
  roles:
  - role: maxhoesel.smallstep.step_cli
    become: yes
    vars:
      step_cli_version: "0.21.0"
      # This will install step-cli to `/opt/step-cli`
      # make sure that this directory is in $PATH, or the role will fail to find `step-cli`
      # alternatively, you can also set `step_cli_executable` like so:
      #step_cli_executable: /opt/step-cli
      step_cli_install_dir: /opt
```
