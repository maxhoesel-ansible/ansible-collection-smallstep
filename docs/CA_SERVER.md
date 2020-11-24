maxhoesel.smallstep.ca_server
=========

Install a basic Smallstep Certificate server using `step-ca`.

This role performs the following actions:
1. Install `step` and `step-ca` on the remote hosts
2. Initialize a ca server with `step ca init` if none is found
3. Install a systemd service for the server
4. Print the root CA fingerprint for you to distribute to your clients

Note that this role does **not** manage the server once it has been created - you cannot use this role to add/remove provisioners for example. To do so, please see the `ca_` modules in the `maxhoesel.smallstep` collection.

Requirements
------------

A host running one of the below distributions with become privileges:

- Ubuntu 18.04 LTS or newer
- Debian 10 or newer
- CentOS 8 or newer

Other distributions based on Debian or RHEL may also work, but they are not officially supported.

The host must have the `expect` package installed. This package is installed form the OS repositories automatically when running this role.

Role Variables
--------------

### Installation

##### `stepca_version/step_version`
- Set the version of step(-ca) to install
- Can also be `latest` to always install the most recent version
- Default: `latest`

##### `stepca_user`
- Name of the user that will run the step-ca server
- Default: `step`

##### `stepca_home`
- Home directory of `stepca_user`
- The step-ca configuration can be found in `{{ stepca_home }}/.step`
- Default: `/opt/step`

##### `stepca_logdir`
- Directory under which logfiles will be saved
- Default: `/var/log/step-ca`

### CA Settings

**NOTE:** None of these values are changed if the configuration is already present on the remote system!

##### `stepca_name`
- User-Readable name of the CA
- Default: `Example Inc.`

##### `stepca_dns_names`
- Hostname(s) and/or IP address(es) of the CA as a comma-separated string
- Same Syntax as the one required by the `step ca init` command
- Default: `{{ ansible_fqdn }},{{ ansible_default_ipv4.address }}`

##### `stepca_address`
- Listen address of the CA server
- Default: `:443`

##### `stepca_ssh`
- Whether to enable the SSH CA
- Default: `no`

##### `stepca_provisioner_name`
- Name of the default provisioner generated during setup
- Default: `ansible-init`

##### `stepca_provisioner_remove`
- Whether to remove the default provisioner once setup is complete
- Default: `yes`

#### `stepca_root_cert/stepca_root_key`
- Optionally specify an existing CA key and cert for the new CA
- Cert and key must be in a format understood by `step ca init`
- Default: none

### Passwords

**NOTE:** Please ensure that these passwords are stored safely! You can use ansible-vault or a third-party tool to dynamically load the passwords at runtime.

**NOTE:** None of these values are changed if the configuration is already present on the remote system!

##### `stepca_root_password`
- Password used to encrypt the CA root key
- Default: none

##### `stepca_intermediate_password`
- Password used to encrypt the intermediate CA key
- Default: none

##### `stepca_provisioner_password`
- Password used to encrypt the key of the default provisioner
- As the default provisioner is deleted by default (`stepca_provisioner_remove`), the password for the intermediate CA is reused. Make sure to change this if you plan on keeping the default provisioner
- Default: `{{ stepca_provisioner_password }}`

Example Playbook
----------------

```
- hosts: all
  roles:
  - role: maxhoesel.smallstep.ca_server:
    stepca_name: Example-CA
    stepca_dns_names: ca.example.com
    stepca_root_password: 'super-secret-root-password'
    stepca_intermediate_password: 'super-secret-intermediate-password'
    # Enable SSH CA support
    stepca_ssh: yes
```

License
-------

GPL 3 or later
