# maxhoesel.smallstep.step_acme_cert

Get a certificate from a CA with ACME and setup automatic renewal using `step-cli renew`.

This role uses `step-cli` to request and save a certificate from the configured CA,
before setting up a renewal service using `step-cli ca renew`s `--daemon` mode.

Note that this is not the only way to use ACME with step-ca!
You can also configure a traditional ACME client such as certbot, Caddy or acme.sh to talk to step-ca.
[This post](https://smallstep.com/blog/private-acme-server/) shows some examples, you can use other Ansible content to automate this.
The advantage of the `step` method is that no additional tools are required.

## Requirements

- The following distributions are currently supported and tested:
  - Ubuntu: `22.04 LTS, 24.04 LTS`
  - Debian: `11, 12`
  - Fedora: `42`
  - RHEL(-compatible): `9` (RockyLinux is used for testing)
  - Other distributions may work as well, but are not tested
- Running this role requires root access. Make sure to run this role with `become: yes` or equivalent
- The host must be bootstrapped with `step_bootstrap_host` and at least one user must be able to access the CA.

## Role Variables

### General

##### `step_cli_executable`
- Path or name of the step-cli executable to use for executing commands in this role
- Can be an absolute path or a command (make sure the executable is in $PATH) for all users
- Default: `step-cli`

##### `step_acme_cert_user`
- The user account that will generate, own and renew the certificate
- This user must have been boostrapped with `step_bootstrap_host` before
- Default: `root`

##### `step_acme_cert_steppath`
- Set this if `step_acme_cert_user` requires a custom `$STEPPATH` from which to read the step config
- Example: `/etc/step-cli`
- Default: `$HOME/.step/`

### CA

##### `step_acme_cert_ca_provisioner`
- Name of the provisioner on the CA that will issue the ACME cert
- Required: Yes

##### `step_acme_cert_webroot_path`
- If set, this role will use `step-cli`s webroot mode to get a new certificate
- If empty, this role will use the standalone mode instead, causing `step-cli` to bind itself to port 80. Make sure that no other services are listening on this port
  Note that `step-cli` only needs to bind to this port when getting a *new* certificate. It does not need to bind if it is only *renewing* a certificate.
- Default: ""

### Certificate

##### `step_acme_cert_name`
- The subject name that the certificate will be issued for
- Default: `{{ ansible_fqdn }}`

##### `step_acme_cert_san`
- Subject Alternate Names to add to the cert
- Must be a list of valid SANs
- Default: `[]`

##### `step_acme_cert_duration`
- Valid duration of the certificate
- Default: undefined (uses the default for the given provisioner, typically 24h)

##### `step_acme_cert_contact`
- Contact email for the CA for important notifications
- Default: `root@localhost`

##### `step_acme_cert_certfile`/`step_acme_cert_keyfile`
- Details about the cert/key files on disk
- Is a dict with the following elements:
  - `path`: Absolute path to the cert/key file. Defaults to `/etc/ssl/step.crt|step.key`. The directory must already exist and the user must have write access
  - `mode`: File mode for the cert/key file. Defaults to `644` for the cert and `600` for the key
  - `owner`/`group`: Owner and group of the file. Defaults to `step_acme_cert_user`.

### Renewal

This role configures automatic cert renewal using a systemd service.
The service will monitor the certificate using `step-cli ca renew`s deamon mode and renew it when its expiry time approaches.
The daemon will run as the user defined in `step_acme_cert_user`.

##### `step_acme_cert_renewal_service`
- Name of the systemd service that will handle cert renewals
- If you have multiple cert/key pairs on one system, you will have to set a unique service name for each pair. If you only have one, then you can leave this as is.
- Default: `step-renew`

##### `step_acme_cert_renewal_when`
- Renew the cert when its remaining valid time crosses this threshold
- Default: undefined (uses the smallstep default: 1/3 of the certificates valid duration, i.e. 8 hours for a 24h cert)

##### `step_acme_cert_renewal_reload_services`
- Reload or restart these systemd services after a cert renewal
- Must be a list of systemd units
- If `step_acme_cert_user` is not root, a sudoers entry will be added to permit the user to reload-restart these service units.
  This sudoers policy is restricted to the single command needed to achieve this. Requires `sudo` to be installed
- Example: `["nginx", "mysqld"]`
- Default: `[]`

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
