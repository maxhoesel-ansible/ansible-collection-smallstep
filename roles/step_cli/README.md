# maxhoesel.smallstep.step_cli

Install the `step-cli`  tool on a host.

This role is used by `step_bootstrap_host` and `step_ca`, but can also be used standalone to install the cli tool and then do nothing else.


## Requirements and Variables

Please see the [online docs](https://ansible-collection-smallstep.readthedocs.io/en/latest/collections/maxhoesel/smallstep/step_cli_role.html) or [argument_spec](meta/argument_specs.yml) for more information.

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
