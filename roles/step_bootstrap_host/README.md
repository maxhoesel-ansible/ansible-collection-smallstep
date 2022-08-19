# maxhoesel.smallstep.step_bootstrap_host

Install `step-cli` on a host and configure it to trust your CA.
This is intended as a one-stop role that sets up all the components neccessary for using `step-cli` on a given host.
It will:

1. Install `step-cli` if required (using the `step_cli` role)
2. Install the CA root cert into the system trust store
3. Configure the root user to automatically connect to your CA when running `step-cli`.

## Requirements and Variables

Please see the [online docs](https://ansible-collection-smallstep.readthedocs.io/en/latest/collections/maxhoesel/smallstep/step_bootstrap_host_role.html) or [argument_spec](meta/argument_specs.yml) for more information.

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
