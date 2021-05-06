# maxhoesel.smallstep.step_acme_cert

Get a certificate from a CA with ACME and setup automatic renewal using `step-cli renew`.

This role uses `step-cli` to request and save a certificate from the configured CA,
before setting up a renewal service using `step-cli ca renew`s `--daemon` mode.

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - CentOS 8 or newer
- This role requires root access. Make sure to run this role with `become: yes` or equivalent
- `step-cli` must be installed.
- The host must be bootstrapped with `step_bootstrap_host`.
  In particular, `step_service_user` must have a functional `step-cli` environment.

## Role Variables

### General

##### `step_cli_executable`
- Path or name of the step-cli executable to use for executing commands in this role
- Can be an absolute path or a command (make sure the executable is in $PATH) for all users
- Default: `step-cli`

##### `step_service_user`
- User that will perform the ACME request and run the renewal job
- The user must already exist
- Use the `step_bootstrap_host` role to create and initialize the service user
- Default: `step`

### CA

##### `step_acme_cert_ca_provisioner`
- Name of the provisioner on the CA that will issue the ACME cert
- Required: Yes

##### `step_acme_cert_webroot_path`
- If set, this role will use `step-cli`s webroot mode to get a new certificate. You need to make sure that `step_service_user` has write permissions in this directory.
- If empty, this role will use the standalone mode instead, causing `step-cli` to bind itself to port 80. The `step-cli` binary installed via the `step_cli` role already has the required capabilities to do so regardless of the user running it. If you installed `step-cli` yourself, you will need to make sure that the executable can bind to port 80 via some other means.
- Default: ""

### Certificate

##### `step_acme_cert_name`
- The subject name that the certificate will be issued for
- Default: `{{ ansible_fqdn }}`

##### `step_acme_cert_san`
- Subject Alternate Names to add to the cert
- Must be a list of valid SANs
- Default: `[ {{ ansible_default_ipv4.address }} ]`

##### `step_acme_cert_duration`
- Valid duration of the certificate
- Default: undefined (uses the default for the given provisioner)

##### `step_acme_cert_contact`
- Contact email for the CA for important notifications
- Default: `root@localhost`

##### `step_acme_cert_certfile`/`step_acme_cert_keyfile`
- Details about the cert/key files on disk
- Is a dict with the following elements:
  - `path`: Absolute path to the cert/key file. Defaults to `/etc/step/step.crt|step.key`, which is created by `step_bootstrap_host`.
            The directories must already exist.
  - `mode`: File mode for the cert/key file. Defaults to `644` for the cert and `600` for the key
  - `owner`/`group`: Owner and group of the file. Defaults to `{{ step_service_user }}`.
- Make sure that `{{ step_service_user }}` can write still write to the cert/key file if you decide to change the `mode`/`owner`/`group` parameters,
  or renewal might fail.

### Renewal

##### `step_acme_cert_renewal_service`
- Name of the systemd service that will handle cert renewals
- If you have multiple cert/key pairs on one system, you will have to set a unique service name for each pair. If you only have one, then you can leave this as is.
- Default: `step-renew`

##### `step_acme_cert_renewal_when`
- Renew the cert when it expires in this amount of time
- Default: undefined (uses the smallstep default: 1/3 of the certificates valid duration, i.e. 8 hours for a 24h cert)

##### `step_acme_cert_renewal_reload_services`
- Reload or restart these systemd services upon a cert renewal
- Must be a list of services
- Example: `["nginx", "mysqld"]`
- Default: `[]`

## Example Playbooks

```
- hosts: all
  roles:
    # Bootstrap the host to create the service user
    - role: maxhoesel.smallstep.step_bootstrap_host
      vars:
        step_bootstrap_ca_url: https://myca.localdomain
        step_bootstrap_fingerprint: 6e1419b2a5086e961dc503cb2994f479968ed10b73c973705ed8a2d12a337b99
      become: yes

    - role: maxhoesel.smallstep.step_acme_cert
      vars:
        step_acme_cert_ca_provisioner: ACME
        # Use webroot instead of standalone, as that requires binding to port 80 -> root. Make sure that the user has write permissions to the webroot
        step_acme_cert_webroot_path: /var/www/html
      become: yes
```
