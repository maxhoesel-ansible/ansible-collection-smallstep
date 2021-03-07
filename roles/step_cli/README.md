maxhoesel.smallstep.step_client
=========

Install the `step` CLI tool on a host

Requirements
------------

A host running one of the below distributions with `become` privileges:

- Ubuntu 18.04 LTS or newer
- Debian 10 or newer
- CentOS 8 or newer

Role Variables
--------------

##### `step_cli_version`
- Set the version of step to install
- Can be a version tag (e.g. `0.15.3`), or `latest` to always install the most recent version
- Default: `latest`


Example Playbook
----------------

```
- hosts: all
  roles:
  - role: maxhoesel.smallstep.step_cli
    become: yes
```
