# maxhoesel.smallstep

![Release](https://img.shields.io/github/v/release/maxhoesel/ansible-collection-smallstep)
![CI Status (Roles)](https://img.shields.io/github/workflow/status/maxhoesel/ansible-collection-smallstep/CI%20Roles/main)
![CI Status (Modules)](https://img.shields.io/github/workflow/status/maxhoesel/ansible-collection-smallstep/CI%20Modules/main)
![License](https://img.shields.io/github/license/maxhoesel/ansible-collection-smallstep)

---
**NOTE**

This collection (and the upstream `step-cli`/`step-ca` packages) are still under active development and do not have an official stable release yet.
Breaking changes may occur between minor releases (e.g. 0.2 -> 0.3) if they are needed to keep up with upstream changes.

---

An Ansible collection for managing Smallstep CLI and CA applications.

This collection contains role and modules to help you install, configure, and maintain both the step-cli client and the CA server using Ansible.

## Installation

### Dependencies

- A recent version of ansible. We test against the current and previous major release
- Python 3.6 or newer

Individual roles and modules may have additional dependencies, please check their respective documentation.

### Install via ansible-galaxy

Install this role via ansible-galaxy:

`ansible-galaxy collection install maxhoesel.smallstep`

You can also install the most recent version of this collection by referencing this repository:

`ansible-galaxy collection install git+https://github.com/maxhoesel/ansible-collection-smallstep`

## Overview

This collection contains several roles that run common tasks related to `step-cli` and `step-ca`. They are:

- `step_ca`: Install and initialize a step certificate authority on a host
- `step_bootstrap_host`: Initialize a host to trust an existing step CA and create a service user for communicating with the CA via `step-cli`
- `step_acme_cert`: Generate and install and ACME certificate for a host from an existing step CA. Also sets up automatic renewal.

The `step_cli` role is used by the other roles to install the step client tool. While you can run it on its own, this will not initialize your host to trust your CA.

Additionally, this collection contains several modules that you can use to configure your CA, get certificates and perform various other tasks.
These generally required the `step-cli` tool to be present and the host to trust the remote CA. You can do this with `step_bootstrap_host`.

If you'd like to know more about an individual module, you can view its documentation using `ansible-doc maxhoesel.smallstep.<step_module_name>`.

## Getting started

Let's say you have a set of hosts and a separate CA that you want these hosts to trust. To achieve this, you can follow the steps below

```
all:
  children:
    step_ca:
      my-ca.localdomain
    clients:
      hosta.localdomain
      hostb.localdomain
      hostc.localdomain
```

### Create a CA

If you are starting from scratch, you will need to create a new step CA first.
Luckily, this collection has a role just for that - `step_ca`. This role will install and initialize a CA for you,
which you can then configure however you want. It also installs the `step-cli` tool, allowing you to manage your CA via the modules in this collection.
Below is a simple example for how to do so. If you want to know more, check out the documentation for `step_ca` and the `step_ca_provisioner(_claims)` modules.

---
**NOTE**

Please make sure that you have read the [considerations](https://smallstep.com/docs/step-ca/certificate-authority-server-production) for running a step-ca server in production.
`step_ca` follows these considerations where possible, but you should still be familiar with the basic operation of the `step-ca` server.
See the `step_ca` documentation for more details on how private keys are handled.

---

`ca.yml`:

```yaml
- hosts: step_ca
  become: yes
  tasks:
    # Install and initialize the CA server.
    # There are a lot of configuration options, see the step_ca README for details
    - name: Install step-ca
      include_role:
        name: maxhoesel.smallstep.step_ca
      vars:
        step_ca_name: Foobar Internal CA
        step_ca_root_password: "incredibly secret password"
        step_ca_intermediate_password: "very secret password"

    # The CA root cert fingerprint is used by clients to verify the authenticity of your CA.
    # You can save the output of this task and then pass it on to any client that you want to trust the CA.
    - name: Get root CA fingerprint
      command: `step-cli certificate fingerprint /etc/step-ca/certs/root_ca.crt`
      register: root_ca_fp
    - name: Show root CA fingerprint
      debug:
        msg: "Fingerprint of root cert: {{ root_ca_fp.stdout }}"
```


### Bootstrap the clients

To establish trust between your clients and the CA, you will need the fingerprint of the CA root cert - see the [Create a CA](#create-a-ca) section for more details.
This fingerprint identifies your CA to your clients and allows them to verify the CA cert.

To actually initialize the clients, you can use `step_bootstrap_host`. This role will install `step-cli` and configure the host to trust your CA.

`clients.yml`:

```yaml
- hosts: clients
  become: yes
  tasks:
    - name: Bootstrap the hosts to trust the CA
      include_role:
        name: maxhoesel.smallstep.step_bootstrap_host
      vars:
        # These values point the hosts to your newly created CA
        step_bootstrap_ca_url: https://my-ca.localdomain
        step_bootstrap_fingerprint: "your root CA certs fingerprint"

    - name: Verify that everything is working
      command: step-cli ca health
      changed_when: no
      become: yes
```

---
**NOTE**

If you want to access the CA from your clients CLI at a later point, you need to either run `step-cli` as root or specify the CA url and cert with the `--ca-url` and `--root` flags.
This is because `step_bootstrap_host` can automatically configure the root user to trust your CA, but it can't do so for other users on the system.

---

At this point, your CA is up and running and your hosts are configured to trust it. You're ready to go!
You can take a look at the available modules to further configure your CA and hosts if you whish to do so.

### Using Modules

Most of the modules in this collection wrap around the `step-cli` tool. Note that there are two kinds of modules - those dealing with a CA, remote or local (named `step_ca_<action>`)
and those dealing with local, standalone actions (named `step_<action>`, TBD).

To run the CA modules, you need to provide them with information about your CA. There's several options to do this:

- Use the root user on a host bootstrapped with `step_bootstrap_host`. This role configures the root user to trust your CA, so you can run `step-cli` commands/modules as root without issues
- Use the `ca_config` and `root` module parameters to specify the CA url and root certificate.
- Point them to your CAs config file with `ca_config` (and potentially also the `offline` flag). This obviously only works on your CA host and requires that you run the module as the CA user (`step-ca` if installed using this collection)

---
**NOTE**

Most CA modules can be run both remotely via the client and directly on the CA (e.g. `step_ca_certificate`), but others are remote/local-only
(e.g. `step_ca_bootstrap` is remote-only, while `step_ca_provisioner` is local-only). See the module documentation for details.

---

```yaml
- hosts: ca
  tasks:
    - name: Run a module by specifying the CA URL and CA cert
      maxhoesel.smallstep.step_ca_certificate:
        root: /etc/ssl/myca.crt
        ca_url: https://my-ca.localdomain
        #params go here

    # This will only work if you ran step_bootstrap_host on this host first!
    - name: Run a module as root to use the CA configured during bootstrapping
      maxhoesel.smallstep.step_ca_certificate:
        #params go here
      become: yes

    - name: Run a module against a locally installed CA
      maxhoesel.smallstep.step_ca_provisioner:
        ca_config: /etc/step-ca/config/ca.json
        #params go here
      # You should run modules acting on a local CA as the user that the CA runs as.
      # If you configured your CA with `step_ca`, the default user name is `step-ca`.
      become_user: step-ca
```

### Getting ACME certs from the CA

One possible use case for a internal CA is to issue short-lived host certificates via the ACME protocol.
This collection has a role specifically for that - `step_acme_cert`. Below is a simple example for setting
up an ACME workflow.

---
**NOTE**

Make sure that you are familiar with the way ACME works. You will need a functioning DNS environment at the very least
to make use of ACME certs.

---

`acme.yml`:

```yaml
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
  tasks:
    # This will download a certificate to /etc/step/ that you can then use in other applications.
    # See the step_acme_cert README for more options
    - name: Configure an ACME cert + renewal
      include_role:
        name: maxhoesel.smallstep.step_acme_cert
        vars:
          step_acme_cert_ca_provisioner: ACME
      become: yes

```

## License & Author

Created & Maintained by Max Hösel (@maxhoesel)

Licensed under the GPL 3.0 or later
