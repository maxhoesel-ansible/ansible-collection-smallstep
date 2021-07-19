# maxhoesel.smallstep.step_bootstrap_host

Configure a host to trust your CA and install `step-cli` to access it.

This role is intended to be run on regular hosts in your network that you want to cooperate with your existing CA. It will:

1. Install `step-cli` if required
2. Install the CA root cert into the system trust store
3. Configure the root user to automatically connect to your CA when running `step-cli`.

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

##### `step_cli_steppath`
- Optionally set a custom `$STEPPATH` for bootstrapping.
  All step configuration will be saved in this path instead of the default `$HOME/.step/`
- **NOTE**: If set, you will have to supply your custom `$STEPPATH` in all future role/module/`step-cli` calls on this host that use the step config
- Example: `/etc/step-cli`
- Default: `/root/.step/`

##### `step_cli_version`
- Set the version of step to install
- Can be a version tag (e.g. `0.15.3`), or `latest` to always install the most recent version
- Note that the role will query the GitHub API if this value is set to `latest`. Try setting
  a specific version if you are running into rate limiting issues
- Default: `latest`

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
- If set to false, this role only installs `step-cli` and configures the root user to run `step-cli` against your CA
- Default: Yes

##### `step_bootstrap_force`
- Whether to force bootstrapping of the CA configuration.
- If true, will cause an overwrite of any existing CA configuration, including root certificate.  Useful to change the CA URL, or even change to a new CA entirely.
- Default: No

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
