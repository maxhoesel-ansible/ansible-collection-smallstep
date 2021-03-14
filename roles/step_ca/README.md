# maxhoesel.smallstep.step_ca

Install and initialize a Smallstep certificates server (`step-ca`).

This role performs the following actions:
1. Install `step-ca`
2. Create a user to run the step-ca server, if it doesn't already exist
3. Initialize a fresh ca server with no provisioners using `step ca init`
4. Daemonize step-ca using a systemd service

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - CentOS 8 or newer
- This role requires root access. Make sure to run this role with `become: yes` or equivalent
- The host must already have `step-cli` installed. Use the `step_cli` role to do so
- This role requires `expect` to answer some interactive prompts. It will automatically install
  `expect` if it is not present

## Role Variables

### Installation

##### `step_ca_version`
- Set the version of step-ca to install
- Can be a version tag (e.g. `0.15.3`), or `latest` to always install the most recent version
- Default: `latest`

##### `step_ca_user`
- User under which the step-ca server will run
- Default: `step`

##### `step_ca_path`
- Directory under which to place step-ca configuration files
- Default: `/etc/step-ca`


### CA Initialization

These variables correspond to the arguments passed to `step ca init`.
See the [step docs](https://smallstep.com/docs/step-cli/reference/ca/init) for more information.

##### `step_ca_name`
- The name of the new PKI
- Required
- Default: Not set

##### `step_ca_root_password`
- Password used to encrypt the root key
- Required
- Default: Not set

##### `step_ca_intermediate_password`
- Password used to encrypt the intermediate key
- If unset, uses the root password for both
- Default: Not set

##### `step_ca_dns`
- The comma separated DNS names or IP addresses of the new CA
- Default: `{{ ansible_fqdn}},{{ ansible_default_ipv4.address }}`

##### `step_ca_address`
- The address that the new CA will listen at
- Default: `:443`

##### `step_ca_url`
- URI of the Step Certificate Authority to write in defaults.json
- Default: `""`

##### `step_ca_ssh`
- Create keys to sign SSH certificates
- Default: `false`


#### Existing Root Cert/Key

Set these values if you want to use an existing cert/key.
These variables need to be set as a group.

##### `step_ca_existing_root_file`
- The path of an existing PEM file to be used as the root certificate authority
- The file must already exist on the remote host
- Default: `""`

##### `step_ca_existing_key_file`
- The path of an existing key file of the root certificate authority
- The key file must not be password-protected
- The file must already exist on the remote host
- Default: `""`


#### RA Variables

Set these values if you are using a registration authority such as CloudCAS.
These variables need to be set as a group

##### `step_ca_ra`
- The registration authority name to use. Currently only "CloudCAS" is supported
- Default: `""`

##### `step_ca_ra_issuer`
- The registration authority issuer name to use
- Default: `""`

##### `step_ca_ra_credentials_file`
- The registration authority credentials file to use
- Default: `""`


### step-cli 

##### `step_cli_executable`
- Path or name of the step-cli executable to use for executing commands in this role
- Can be an absolute path or a command (make sure the executable is in $PATH) for all users
- Default: `step-cli`


## Example Playbooks

```
# Performs a basic step-ca installation with all default values.
# Please make sure that your passwords are provided by a secure mechanism,
# such as ansible-vault or via vars-prompt
- hosts: all
  roles:
    - role: maxhoesel.smallstep.step_ca
      vars:
        step_ca_name: Foo Bar Private CA
        step_ca_root_password: "very secret password"
        step_ca_intermediate_password: "also very secret password"
```