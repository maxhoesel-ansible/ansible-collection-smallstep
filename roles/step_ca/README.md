# maxhoesel.smallstep.step_ca

Install and initialize a Smallstep certificates server (`step-ca`).

This role performs the following actions:

1. Install `step-cli` (required to initialize the CA)
2. Install `step-ca`
3. Create a user to run the`step-ca`server, if it doesn't already exist
4. Initialize a fresh ca server with no provisioners using `step ca init`
5. Daemonize`step-ca`using a systemd service

---
**NOTE**

Please make sure that you have read the [considerations](https://smallstep.com/docs/step-ca/certificate-authority-server-production) for running a`step-ca`server in production.
`step_ca` follows these considerations where possible, but you should still be familiar with the basic operation of the `step-ca` server.

---

---
**ABOUT PRIVATE KEYS**

By default `step-ca` generates two keys when initialized - a root CA key and an intermediate key used to sign certificates. Both are present and encrypted on the ca host after this role exits,
with the `step-ca` server configured to read the intermediate key password from a protected file in `step_ca_path`. The root key can thus only be decrypted with the password set in `step_ca_root_password`.

It is thus **very** important that you **back up your root key and password** in a safe and secure location. The details of your backup scheme will depend on your environment and threat model.
---

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - Fedora 36 or newer
  - A CentOS-compatible distribution like RockyLinux/AlmaLinux 8 or newer. RockyLinux is used for testing
- Supported architectures: amd64, arm64
- This role requires root access. Make sure to run this role with `become: yes` or equivalent

## Role Variables

### Installation (step-ca)

##### `step_ca_version`
- Set the version of `step-ca` to install
- Can be a version tag (e.g. `0.15.3`), `latest-compatible` or `latest`.
- If set to `latest-compatible`, the most recent compatible release is installed, that is, the most recent minor release that matches the collection minor version.
  - For example, if the collection version is `0.24.x`, then the most recent release from the `0.24` series will be installed.
  - See the [versioning policy](https://github.com/maxhoesel-ansible/ansible-collection-smallstep/tree/main#versioning-policy) for more details.
- If set to `latest`, the most recent version of `step-cli` is installed, regardless of compatibility with the collection
    - This can be useful if you just want to install `step-ca`, but don't plan on using it with this collection (set `step_ca_init` to `false` in this case)
    - Using minor versions of `step-cli`/`step-ca` that don't match the collection minor version is not supported!
- Note that the role will query the GitHub API if this value is set to `latest-compatible` or `latest`. If you are getting rate limit errors, you can:
    - set `step_ca_version` to a specific value
    - set `step_ca_github_token` to a token with higher rate limits
- Default: `latest-compatible`

##### `step_ca_executable`
- Where to put the `step-ca` executable that will be installed by this role
- Must be an absolute path
- Default: `/usr/bin/step-ca`

##### `step_ca_user`
- User under which the`step-ca`server will run
- Default: `step-ca`

##### `step_ca_path`
- Directory under which to place`step-ca`configuration files
- Default: `/etc/step-ca`

### Installation (step-cli)

##### `step_cli_version`
- Set the version of `step-cli` to install
- Can be a version tag (e.g. `0.15.3`) or `latest-compatible`.
- If set to `latest-compatible`, the most recent compatible release is installed, that is, the most recent minor release that matches the collection minor version.
  - For example, if the collection version is `0.24.x`, then the most recent release from the `0.24` series will be installed.
  - See the [versioning policy](https://github.com/maxhoesel-ansible/ansible-collection-smallstep/tree/main#versioning-policy) for more details.
- Note that the role will query the GitHub API if this value is set to `latest-compatible`. If you are getting rate limit errors, you can:
  - Set `step_cli_version` to a specific value
  - Set `step_cli_github_token` to a token with higher rate limits
- Default: `latest-compatible`

##### `step_cli_executable`
- What to name and where to put the `step-cli` executable that will be installed by this role
- Can be an absolute path (make sure that the parent directory is in $PATH and has correct SELinux policies set, if applicable) or a filename
- If this executable is not found and `step_cli_executable` is a **path**, the executable will be installed there
- If this executable is not found and  `step_cli_executable` is a **name**, the executable will be installed at `step_cli_install_dir` with the given name
- Default: `step-cli`

##### `step_cli_install_dir`
- Used if `step_cli_executable` is a filename and not yet present
- Sets the directory to install `step_cli_executable` into
- The directory must already exist
- Ignored if `step_cli_executable` contains a path
- Default: `/usr/bin`

### CA Configuration

These variables correspond to the arguments passed to `step ca init`.
See the [step docs](https://smallstep.com/docs/step-cli/reference/ca/init) for more information.

#### `step_ca_configure`
- If `false`, this role will only install `step-ca` and skip CA creation, initialization and service installation
- This can be useful if you are only installing `step-ca` using this role but don't plan on using it with this collection.
- Default `true`

##### `step_ca_name`
- The name of the new PKI
- Required
- Default: Not set

##### `step_ca_root_password`
- Password used to encrypt the root key
- Required
- Default: Not set

##### `step_ca_intermediate_password`
- Password used to encrypt the intermediate key
- If unset, uses the root password will be used as the intermediate password
- Default: Not set

##### `step_ca_dns`
- The comma separated DNS names or IP addresses of the new CA
- Default: `{{ ansible_fqdn}},{{ ansible_default_ipv4.address }}`

##### `step_ca_address`
- The address that the new CA will listen at
- Default: `:443`

##### `step_ca_url`
- URI of the Step Certificate Authority to write in defaults.json
- Default: Not set

##### `step_ca_ssh`
- Create keys to sign SSH certificates
- Default: `false`


#### Existing Root Cert/Key

These variables can be used to import an existing certificate+key as your CA cert/key.

By default, this role will generate a new CA cert/key, only change these values if you want to import an existing certificate.

---
**⚠️ WARNING ⚠️**

If you want to use an existing root key, it is **highly** recommended that you use an encrypted keyfile and set
`step_ca_existing_key_password` from a secure source, such as Ansible Vault or Hashicorp Vault.

Storing your root key unencrypted (even just temporarily!) is strongly discouraged and poses a great security risk.
This role will only decrypt the root key for as long as strictly neccessary.

---

##### `step_ca_existing_<root/key>`
- Whether to use an existing root certificate/key and if so from where to import it from
- Choices:
    - `remote`: The root certificate/key is already present on the remote host
    - `local`: The root certificate/key is read from the controller
- Note that both cert and key need to be either imported, **or** generated.
  For example, you cannot import the key but generate the certificate
- Default: Not set.
    - If unset and `_root/key_file` is also unset, a new certificate will be generated
    - If unset and `_root/key_file` is set, the files are treated as `remote` to preserve backwards-compatibility to previous collection versions.
      This behavior may be removed in a future release

##### `step_ca_existing_<root/key>_file`
- The path of an existing PEM file to be used as the root certificate/key
- Depending on the value of `step_ca_existing_<root/key>`, the file must either be on the remote host or the controller

##### `step_ca_existing_key_password`
- Password to decrypt the existing key file
- Default: Not set

Example usage:

```yaml
# Select where to import the root certificate from. Can be `remote`, `local`, `false`
step_ca_existing_root: remote
step_ca_existing_root_file: /tmp/existing-ca-root.crt

# Same for the key, except that the key is read from the controller
step_ca_existing_key: local
step_ca_existing_key_file: /home/controller/secret-ca-key.pem
# If your keyfile is password-protected, you can set the decryption password like so:
step_ca_existing_key_password: Very-secret-password
```

#### RA Variables

Set these values if you are using a registration authority such as CloudCAS.
These variables need to be set as a group

##### `step_ca_ra`
- The registration authority name to use. Currently only "CloudCAS" is supported
- Default: Not set

##### `step_ca_ra_issuer`
- The registration authority issuer name to use
- Default: Not set

##### `step_ca_ra_credentials_file`
- The registration authority credentials file to use
- Default: Not set


## Example Playbooks

```
# Performs a basic step-ca installation with all default values.
# Please make sure that your passwords are provided by a secure mechanism,
# such as ansible-vault or via vars-prompt
- hosts: all
  roles:
    - role: maxhoesel.smallstep.step_ca
      become: yes
      vars:
        step_ca_name: Foo Bar Private CA
        step_ca_root_password: "very secret password"
        step_ca_intermediate_password: "also very secret password"
```
