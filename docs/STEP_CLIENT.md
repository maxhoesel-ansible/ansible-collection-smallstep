maxhoesel.smallstep.step_client
=========

## WARNING

This role has been deprecated and replaced by `step_cli` role and the `step_ca_bootstrap` module.
This role will be removed in a future release of this collection.

Install the `step` command-line tool on a system

Requirements
------------

A host running one of the below distributions with become privileges:

- Ubuntu 18.04 LTS or newer
- Debian 10 or newer
- CentOS 8 or newer

Other distributions based on Debian or RHEL may also work, but they are not officially supported.

Role Variables
--------------

##### `stepclient_version`
- Set the version of step to install
- Can also be `latest` to always install the most recent version
- Default: `latest`

##### `stepclient_ca_servers`
- List of step-ca servers whose certificates will be installed into the system trust store
- Each list element must have the keys `url` and `fp`, containing the URL of the server and fingerprint of the cert respectively
- Default: `[]`

Example Playbook
----------------

```
- hosts: all
  roles:
  - role: maxhoesel.smallstep.step_client
```

License
-------

GPL 3 or later
