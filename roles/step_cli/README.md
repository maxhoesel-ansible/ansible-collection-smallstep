# maxhoesel.smallstep.step_cli

Install the `step` CLI tool on a host

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - CentOS 8 or newer
- Supported architectures: amd64, arm64
- This role requires root access. Make sure to run this role with `become: yes` or equivalent

## Role Variables

##### `step_cli_version`
- Set the version of step to install
- Can be a version tag (e.g. `0.15.3`), or `latest` to always install the most recent version
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
