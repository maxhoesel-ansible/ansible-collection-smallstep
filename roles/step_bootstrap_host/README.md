# maxhoesel.smallstep.step_bootstrap_host

Install `step-cli` on a host and configure it to trust your CA.
This is intended as a one-stop role that sets up all the components neccessary for using `step-cli` on a given host.
It will:

1. Install `step-cli` if required (using the `step_cli` role)
2. Install the CA root cert into the system trust store
3. Configure the root user to automatically connect to your CA when running `step-cli`.

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - Fedora 36 or newer
  - A CentOS-compatible distribution like RockyLinux/AlmaLinux 8 or newer. RockyLinux is used for testing
- This role requires root access. Make sure to run this role with `become: yes` or equivalent
- `step-cli` will be automatically installed, if not already present

## Role Variables

### Install

##### `step_cli_executable`
- What to name and where to put the `step-cli` executable that will be installed by this role
- Can be an absolute path (make sure that the parent directory is in $PATH) or a filename
- If this executable is not found and `step_cli_executable` is a **path**, the executable will be installed there
- If this executable is not found and  `step_cli_executable` is a **name**, the executable will be installed at `step_cli_install_dir` with the given name
- Default: `step-cli`

##### `step_cli_version`
- Set the version of step to install
- Can be a version tag (e.g. `0.15.3`), or `latest` to always install the most recent version
- It is **highly** recommended that your cli version matches the collection version
  (e.g. if you are using the collection version 0.20.x you should be installing step-cli version 0.20.x as well)
- Note that the role will query the GitHub API if this value is set to `latest`. Try setting
  a specific version if you are running into rate limiting issues
- Default: `latest`

##### `step_cli_install_dir`
- Used if the binary defined by `step_cli_executable` is not found on the system and `step_cli_executable` contains a executable name
- Sets the directory to install `step_cli_executable` into
- The directory must already exist
- Ignored if `step_cli_executable` contains a directory already
- Default: `/usr/bin`

### Bootstrap

##### `step_cli_steppath`
- Optionally set a custom `$STEPPATH` for bootstrapping.
  All step configuration will be saved in this path instead of the default `$HOME/.step/`
- **NOTE**: If set, you will have to supply your custom `$STEPPATH` in all future role/module/`step-cli` calls on this host that use the step config
- Example: `/etc/step-cli`
- Default: `$HOME/.step/`

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
- If set to false, this role only installs `step-cli` and configures the root user to run `step-cli` against your CA.
  Other applications on your system will **not** trust the CA, as the certificate won't be in the system trust store.
- Default: Yes

##### `step_bootstrap_force`
- Whether to force bootstrapping of the CA configuration.
- If true, will cause an overwrite of any existing CA configuration, including root certificate. Useful to change the CA URL, or even change to a new CA entirely.
- Default: No

## Example Playbook

See the [step-cli role docs](/roles/step_cli/README.md) for more details on the install options

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
