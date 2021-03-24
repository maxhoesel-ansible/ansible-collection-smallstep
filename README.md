# maxhoesel.smallstep

![Release](https://img.shields.io/github/v/release/maxhoesel/ansible-collection-smallstep)
![CI Status (Roles)](https://img.shields.io/github/workflow/status/maxhoesel/ansible-collection-smallstep/CI%20Roles/devel)
![CI Status (Modules)](https://img.shields.io/github/workflow/status/maxhoesel/ansible-collection-smallstep/CI%20Modules/devel)
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

- ansible-base, either the most recent release or the release before
- Python 3.6 or newer

Individual roles and modules may have additional dependencies, please check their respective documentation.

### Install via ansible-galaxy

Install this role via ansible-galaxy:

`ansible-galaxy collection install maxhoesel.smallstep`

You can also install the most recent version of this collection by referencing this repository:

`ansible-galaxy collection install git+https://github.com/maxhoesel/ansible-collection-smallstep`

## Usage

In addition to a set of modules that wrap around `step-cli` commands, allowing to perform typical `step-cli`/`ca` operations,
this collection also contains several roles that perform typical tasks related to `step-cli` and `step-ca`. They are:

- `step_ca`: Install and initialize a step certificate authority on a host
- `step_bootstrap_host`: Initialize a host to trust an existing step CA and create a service user for communicating with the CA via `step-cli`
- `step_acme_cert`: Generate and install and ACME certificate for a host from an existing step CA. Also sets up automatic renewal.
- `step_cli`: Install the `step-cli` client on a host. This role is used by `step_ca` and `step_bootstrap_host` and
              it is recommended that you use these roles unless you really only want `step-cli` for some reason


### Basic setup

In this scenario you want to create an internal CA for a group of hosts to trust and get TLS certs from.
Your inventory will probably look a little like the one below:

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

First, you will need to create a step CA on the CA host.
Below is a simple example for how to do so (check the `step_ca` docs for more details):

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

Now that your CA is up and running, it's time to configure the clients to trust the CA:

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

    # `step` is the default service user created by step_bootstrap_host. This user
    # is configured to access the CA and can be used to get certs, check the CA status and so on.
    - name: Verify that everything is working
      command: step-cli ca health
      changed_when: no
      become_user: step
```

At this point, your CA is up and running and your hosts are configured to trust it. You're ready to go!
You can take a look at the available modules to further configure your CA and hosts if you whish to do so.

### About step-cli config and service users

Most of the modules in this collection wrap around the `step-cli` command, which reads its configuration from
$STEPPATH (~/.step) by default. Alternatively, it is possible to pass required configuration parameters via command-line args.

This collection makes things easy for you by installing a cli and ca user with the `step_bootstrap_host` and `step_ca` roles respectively
These users are named `step` and `step-ca` and can access the CA remotely/locally without any further configuration required.

You can also pass the required parameters via module args (e.g. `ca_url` for remote access or `ca_config` if the CA is local), but
this is not recommended.

---
**NOTE**

Some modules can be run both remotely via the client and directly on the CA (e.g. `step_ca_certificate`), while others are remote/local-only
(e.g. `step_ca_bootstrap` is remote-only, while `step_ca_provisioner` is local-only). See the module documentation for details.
---

```yaml
- hosts: all
  become: yes
  tasks:
    - name: Run a step-cli command
      command: step-cli ca health
      become_user: step
    - name: Run a module instead
      maxhoesel.smallstep.step_ca_certificate:
        # module args
      become_user: step

    - name: run a module against a local CA
      maxhoesel.smallstep.step_ca_provisioner:
        # module args
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
  become: yes
  tasks:
    # This will download a certificate to /etc/step/ that you can then use in other applications.
    # See the step_acme_cert README for more options
    - name: Configure an ACME cert + renewal
      include_tasks:
        name: maxhoesel.smallstep.step_acme_cert
        vars:
          step_acme_cert_ca_provisioner: ACME
      become_user: step

```

## License & Author

Created & Maintained by Max Hösel (@maxhoesel)

Licensed under the GPL 3.0 or later
