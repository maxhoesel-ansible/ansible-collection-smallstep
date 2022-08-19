# maxhoesel.smallstep.step_ca

Install and initialize a Smallstep certificates server (`step-ca`).

This role performs the following actions:

1. Install `step-cli` if required
2. Install `step-ca`
3. Create a user to run the step-ca server, if it doesn't already exist
4. Initialize a fresh ca server with no provisioners using `step ca init`
5. Daemonize step-ca using a systemd service

---
**NOTE**

Please make sure that you have read the [considerations](https://smallstep.com/docs/step-ca/certificate-authority-server-production) for running a step-ca server in production.
`step_ca` follows these considerations where possible, but you should still be familiar with the basic operation of the `step-ca` server.

---

---
**ABOUT PRIVATE KEYS**

By default `step-ca` generates two keys when initialized - a root CA key and an intermediate key used to sign certificates. Both are present and encrypted on the ca host after this role exits,
with the `step-ca` server configured to read the intermediate key password from a protected file in `step_ca_path`. The root key can thus only be decrypted with the password set in `step_ca_root_password`.

It is thus **very** important that you **back up your root key and password** in a safe and secure location. The details of your backup scheme will depend on your environment and threat model.
---

---
**⚠️ WARNING ABOUT USING EXISTING CERTIFICATES ⚠️**

If you want to use an existing root key, it is **highly** recommended that you use an encrypted keyfile and set
`step_ca_existing_key_password` from a secure source, such as Ansible Vault or Hashicorp Vault.

Storing your root key unencrypted (even just temporarily!) is strongly discouraged and poses a great security risk.
This role will only decrypt the root key for as long as strictly neccessary.

---

## Requirements and Variables

Please see the [online docs](https://ansible-collection-smallstep.readthedocs.io/en/latest/collections/maxhoesel/smallstep/step_ca_role.html) or [argument_spec](meta/argument_specs.yml) for more information.

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
