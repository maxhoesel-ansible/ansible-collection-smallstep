# maxhoesel.smallstep.step_cli

Install the `step` CLI tool on a host

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - A CentOS 8-compatible distribution like RockyLinux or AlmaLinux. RockyLinux is used for testing
- Supported architectures: amd64, arm64
- This role requires root access. Make sure to run this role with `become: yes` or equivalent

## Role Variables

##### `step_cli_version`
- Set the version of step to install
- Can be a version tag (e.g. `0.15.3`), or `latest` to always install the most recent version
- It is **highly** recommended that your cli version matches the collection version
  (e.g. if you are using the collection version 0.20.x you should be installing step-cli version 0.20.x as well)
- Note that the role will query the GitHub API if this value is set to `latest`. Try setting
  a specific version if you are running into rate limiting issues
- Default: `latest`

## Example Playbook

```
- hosts: all
  roles:
  - role: maxhoesel.smallstep.step_cli
    become: yes
```
