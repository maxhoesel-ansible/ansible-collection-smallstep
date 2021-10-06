# maxhoesel.smallstep.step_certificate

Get a certificate from a CA, using a specified provisioner, and setup automatic renewal using `step-cli renew`.

This role uses `step-cli` to request and save a certificate from the configured CA,
before setting up a renewal service using `step-cli ca renew`s `--daemon` mode.

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - CentOS 8 or newer
- This role requires root access. Make sure to run this role with `become: yes` or equivalent
- The host must be bootstrapped with `step_bootstrap_host` and the root user must be able to access the CA.

## Role Variables

### General

##### `step_cli_executable`
- Path or name of the step-cli executable to use for executing commands in this role
- Can be an absolute path or a command (make sure the executable is in $PATH) for all users
- Default: `step-cli`

##### `step_cli_steppath`
- Optionally set a custom `$STEPPATH` from which to read the step config
- Example: `/etc/step-cli`
- Default: `/root/.step/`

### CA

##### `step_cert_ca_provisioner_type`
- Type of provisioner on the CA that will issue the certificate
- Required: Yes

##### `step_cert_ca_provisioner_name`
- Name of the provisioner on the CA that will issue the certificate
- Required: Yes


### Provisioner

#### ACME

##### `step_cert_acme_webroot_path`
- If set, the ACME provisioner will use `step-cli`s webroot mode to get a new certificate.
- If empty, the ACME provisioner will use the standalone mode instead, causing `step-cli` to bind itself to port 80. Make sure that no other services are listening on this port.
  Note that `step-cli` only needs to bind to this port when getting a *new* certificate. It does not need to bind if it is only *renewing* a certificate.
- Default: ""

#### JWK

##### `step_cert_ca_jwk_password`
- The password used to decrypt the one-time token generating key from a JWK provisioner on the CA.
- Required: If using a JWK provisioner, either this or `step_cert_ca_jwk_password_file` is required.

##### `step_cert_ca_jwk_password_file`
- Path to the file on the client system containing the password used to decrypt the one-time token generating key from a JWK provisioner on the CA.
- Required: If using a JWK provisioner, either this or `step_cert_ca_jwk_password` is required.

### Certificate

##### `step_cert_name`
- The subject name that the certificate will be issued for
- Default: `{{ ansible_fqdn }}`

##### `step_cert_san`
- Subject Alternate Names to add to the cert
- Must be a list of valid SANs
- Default: `[]`

##### `step_cert_duration`
- Valid duration of the certificate
- Default: undefined (uses the default for the given provisioner, typically 24h)

##### `step_cert_contact`
- Contact email for the CA for important notifications
- Default: `root@localhost`

##### `step_cert_certfile`/`step_cert_keyfile`
- Details about the cert/key files on disk
- Is a dict with the following elements:
  - `path`: Absolute path to the cert/key file. Defaults to `/etc/ssl/step.crt|step.key`. The directory must already exist.
  - `mode`: File mode for the cert/key file. Defaults to `644` for the cert and `600` for the key
  - `owner`/`group`: Owner and group of the file. Defaults to root.

### Renewal

##### `step_cert_renewal_service`
- Name of the `systemd` service that will handle cert renewals
- If you have multiple cert/key pairs on one system, you will have to set a unique service name for each pair.
- Default: `step-renew`

##### `step_cert_renewal_when`
- Renew the cert when its remaining valid time crosses this threshold
- Default: undefined (uses the smallstep default: 1/3 of the certificates valid duration, e.g. 8 hours for a 24h cert)

##### `step_cert_renewal_reload_services`
- Reload or restart these `systemd` services after a cert renewal
- Must be a list of `systemd` units
- Example: `["nginx", "mysqld"]`
- Default: `[]`

## Example Playbooks

### ACME

Make sure that you are familiar with the way ACME certificate generation works.  Minimally, to make use of the ACME provisioners, you will need open network ports (e.g. `:80`) between the client and the server, and a functioning DNS environment.

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

# Create a certificate using an ACME provisioner
- hosts: step_clients
  tasks:
    # Bootstrap the host to trust the CA
    - role: maxhoesel.smallstep.step_bootstrap_host
      vars:
        step_bootstrap_ca_url: https://myca.localdomain
        step_bootstrap_fingerprint: your CAs fingerprint
      become: yes

    # Configure an ACME provisioned cert + renewal in /etc/step
    - role: maxhoesel.smallstep.step_certificate
      vars:
        step_cert_ca_provisioner_type: ACME
        step_cert_ca_provisioner_name: ACME
      become: yes
```

### JWK

When using a JWK provisioner, you will need a shared secret between the CA server and the CA clients.  This file must be placed on the system before you attempt to generate a certificate.

```yaml
# Configure your CA to include a JWK provisioner
- hosts: step_ca
  become: yes
  tasks:
    - name: step-ca | deploy CA JWK provisioner password
      copy:
        dest: "{{ step_ca_jwk_provisioner_password_file }}"
        content: "SUPER SECRET JWK Provisioner Password"
        owner: step-ca
        group: step-ca
        mode: 0600

    - name: step-ca | configure JWK provisioner on the CA
      maxhoesel.smallstep.step_ca_provisioner:
        type: JWK
        name: "JWK@{{ ansible_domain }}"
        jwk_password_file: "{{ step_ca_jwk_provisioner_password_file }}"
      become_user: step-ca
      notify: reload step-ca

  handlers:
    - name: reload step-ca
      systemd:
        name: step-ca
        state: reloaded

# Create a certificate using a JWK provisioner
- hosts: step_clients
  tasks:
    # Bootstrap the host to trust the CA
    - role: maxhoesel.smallstep.step_bootstrap_host
      vars:
        step_bootstrap_ca_url: https://myca.localdomain
        step_bootstrap_fingerprint: your CAs fingerprint
      become: yes

    # Configure a JWK provisioned cert + renewal in /etc/step
    - role: maxhoesel.smallstep.step_certificate
      vars:
        step_cert_ca_provisioner_type: JWK
        step_cert_ca_provisioner_name: "JWK@{{ ansible_domain }}"
        step_cert_ca_jwk_password: "SUPER SECRET JWK Provisioner Password"
        # or:
        # step_cert_ca_jwk_password_file: "/path/to/file/containing/jwk/provisioner/password/on/step/client/host"
```
