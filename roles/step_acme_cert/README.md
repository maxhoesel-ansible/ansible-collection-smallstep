# maxhoesel.smallstep.step_acme_cert

Get a certificate from a CA with ACME and setup automatic renewal using `step-cli renew`.

This role uses `step-cli` to request and save a certificate from the configured CA,
before setting up a renewal service using `step-cli ca renew`s `--daemon` mode.

## Requirements and Variables

Please see the [online docs](https://ansible-collection-smallstep.readthedocs.io/en/latest/collections/maxhoesel/smallstep/step_acme_cert_role.html) or [argument_spec](meta/argument_specs.yml) for more information.
## Example Playbooks

---
**NOTE**

Make sure that you are familiar with the way ACME works. You will need a functioning DNS environment at the very least
to make use of ACME certs.

---

```yaml
# Configure your CA to include an ACME provisioner
- hosts: step_ca
  become: yes
  tasks:
    - name: Add an ACME provisioner to the CA
      maxhoesel.smallstep.step_ca_provisioner:
        name: ACME
        type: ACME
      become_user: step-ca
      notify: reload step-ca
  handlers:
    - name: reload step-ca
      systemd:
        name: step-ca
        state: reloaded

- hosts: clients
  become: yes
  tasks:
    # Bootstrap the host to trust the CA
    - include_role:
        name: maxhoesel.smallstep.step_bootstrap_host
      vars:
        step_bootstrap_ca_url: https://myca.localdomain
        step_bootstrap_fingerprint: your CAs fingerprint

    # This will download a certificate to /etc/step/ that you can then use in other applications.
    # See the step_acme_cert README for more options
    - name: Configure an ACME cert + renewal
      include_role:
        name: maxhoesel.smallstep.step_acme_cert
      vars:
        step_acme_cert_ca_provisioner: ACME

```
