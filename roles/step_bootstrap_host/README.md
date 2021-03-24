# maxhoesel.smallstep.step_bootstrap_host

Configure a host to trust your CA and setup a service user to perform certificate jobs and renewals.

This role is intended to be run on regular hosts in your network that you want to cooperate with your existing CA. It will:

1. Install `step-cli` if required
2. Create a service user to CA by running `step-cli` commands/collection modules as that user
3. Install the CA root cert into the system trust store

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - CentOS 8 or newer
- This role requires root access. Make sure to run this role with `become: yes` or equivalent
- `step-cli` will be automatically installed, if not already present

## Role Variables

##### `step_cli_executable`
- Path or name of the step-cli executable to use for executing commands in this role
- Can be an absolute path or a command (make sure the executable is in $PATH) for all users
- Default: `step-cli`

##### `step_cli_version`
- Set the version of step to install
- Can be a version tag (e.g. `0.15.3`), or `latest` to always install the most recent version
- Note that the role will query the GitHub API if this value is set to `latest`. Try setting
  a specific version if you are running into rate limiting issues
- Default: `latest`

##### `step_cli_user`
- Name of the service user that will be able to communicate with the CA
- Default: `step`

##### `step_cli_user_path`
- Configuration directory for the service user. Used to store `step-cli` configuration
- Default: `/etc/step`

##### `step_bootstrap_ca_url`
- URL of the `step-ca` CA
- Example: https://myca.localdomain
- Required: Yes

##### `step_bootstrap_fingerprint`
- Fingerprint of the CA root cert
- This is used to verify the authenticity of the remote CA
- Required: Yes

##### `step_bootstrap_install_cert`
- Whether to install the CA cert into the system root trust store(s)
- Default: Yes


## Example Playbook

```
- name: Configure the host to trust the CA and setup the step service user
  hosts: all
  roles:
    - role: maxhoesel.smallstep.step_bootstrap_host
      vars:
        step_bootstrap_ca_url: https://myca.localdomain
        step_bootstrap_fingerprint: 6e1419b2a5086e961dc503cb2994f479968ed10b73c973705ed8a2d12a337b99
      become: yes
```
