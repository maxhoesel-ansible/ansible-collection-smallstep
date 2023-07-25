# maxhoesel.smallstep - Ansible Collection for Smallstep CA/CLI

![Release](https://img.shields.io/github/v/release/maxhoesel-ansible/ansible-collection-smallstep?style=flat-square)
![Build Status](https://img.shields.io/circleci/build/github/maxhoesel-ansible/ansible-collection-smallstep/main?style=flat-square)
![License](https://img.shields.io/github/license/maxhoesel-ansible/ansible-collection-smallstep?style=flat-square)

An Ansible collection containing roles/modules to install, configure and interact with the [Smallstep certificate server](https://github.com/smallstep/certificates)
and the [CLI tool](https://github.com/smallstep/cli). Possible uses for this collection include:

- Managing your `step-ca` server install (installation, configuration, provisioners)
- Automated bootstrapping of hosts to trust your CA
- Token or certificate creation from within your Ansible playbooks
- [Complete configuration of client certificates via ACME, including automatic renewal](roles/step_acme_cert/README.md)

## Components

---
**📘 Documentation**

- For role documentation, see their `README.md`s or the online docs [here](https://ansible-collection-smallstep.readthedocs.io)
- For modules documentation, see the online docs [here](https://ansible-collection-smallstep.readthedocs.io)

---

### Roles

| Role | Description |
|------|-------------|
| [`step_ca`](roles/step_ca/README.md) | Install step-ca as an internal CA.
| [`step_bootstrap_host`](roles/step_bootstrap_host/README.md) | Configure a client host to trust your CA using step-cli.
| [`step_acme_cert`](roles/step_acme_cert/README.md) | Set up a Let's Encrypt-style certificate on a host using your ca, including automatic renewal.
| [`step_cli`](roles/step_cli/README.md) | Install step-cli and nothing else. Used by bootstrap_host and step_ca under the hood.

### Modules

| Module  | Description | Remote (Online mode) | Local (Offline mode) |
|---------|-------------|--------|---------------|
| [`step_ca_bootstrap`](https://ansible-collection-smallstep.readthedocs.io/en/latest/collections/maxhoesel/smallstep/step_ca_bootstrap_module.html) | Initialize `step-cli` to trust a step-ca server | ✅ | ❌ |
| [`step_ca_certificate`](https://ansible-collection-smallstep.readthedocs.io/en/latest/collections/maxhoesel/smallstep/step_ca_certificate_module.html) | Generate a new private key and certificate signed by the CA root certificate | ✅ | `offline` parameter |
| [`step_ca_provisioner`](https://ansible-collection-smallstep.readthedocs.io/en/latest/collections/maxhoesel/smallstep/step_ca_provisioner_module.html) | Manage provisioners on a `step-ca` server | `admin` parameters, [if configured](https://smallstep.com/docs/step-ca/provisioners/#remote-provisioner-management) | ✅ |
| [`step_ca_renew`](https://ansible-collection-smallstep.readthedocs.io/en/latest/collections/maxhoesel/smallstep/step_ca_renew_module.html) | Renew a valid certificate | ✅ | `offline` parameter |
| [`step_ca_revoke`](https://ansible-collection-smallstep.readthedocs.io/en/latest/collections/maxhoesel/smallstep/step_ca_revoke_module.html) | Revoke a Certificate | ✅ | `offline` parameter |
| [`step_ca_token`](https://ansible-collection-smallstep.readthedocs.io/en/latest/collections/maxhoesel/smallstep/step_ca_token_module.html) | Generate an OTT granting access to the CA | ✅ | `offline` parameter |

## Installation

### Dependencies

- A recent release of Ansible. This collection is tested against the 3 most recent Ansible releases.
  Older versions might still work, but are not supported
- Python 3.6 or newer on the target nodes

Individual roles or modules may have additional dependencies, please check their respective documentation.

### Versioning Policy and Node Requirements

Each minor version of this collection designed to be compatible with the corresponding minor release of the `step-cli` utility.
For example, The collection releases with version `0.24.x` are compatible with the `step-cli` utility versions `0.24.x`.
This coupling is needed as newer minor versions of the `step-cli` tool may introduce breaking changes and affect this collection.

To install the correct collection version, check your `step-cli` version (`step-cli --version`), then use that value when installing the collection.

**For step-cli versions `<0.20`:** Use the collection version `>=0.4,<0.5`.

### Install

Via ansible-galaxy (recommended):

`ansible-galaxy collection install maxhoesel.smallstep>=your-step-cli-version,<next-major-version`

Alternatively, you can download a collection archive from a [previous release](hhttps://github.com/maxhoesel-ansible/ansible-collection-smallstep/releases).

## Module Usage

This collection contains several modules for managing your smallstep environment.
Most of them wrap around `step-cli` commands, so they usually support all the features of the respective command.

If you'd like to know more about an individual module, you can view its documentation using `ansible-doc maxhoesel.smallstep.<step_module_name>` (or use the [online docs](https://ansible-collection-smallstep.readthedocs.io)).

The `step-cli` tool has two sets of commands - standalone and CA.

- Standalone commands are executed by  `step-cli` directly with no external CA required. Example: `step-cli certificate create`
- CA commands require the usage of an external step CA (Example: `step-cli ca certificate`). Depending on the module, there are two modes:
  - Online mode: `step-cli` communicates with the CA over HTTPS and requests the data it needs.
  - Offline/Local mode: `step-cli` accesses the CA files (certificates, config) directly. This only works on the CA host itself.

Most CA modules can use either online or offline mode using the `offline` parameter, but there are some exceptions.
For example, the `step_ca_provisioner_(claims)` modules(s) need to run in offline mode as they directly write to the CA config.
See [this table](#ca-modules) for details.

In order to talk to your CA in online mode, `step-cli` needs to already trust it. You can achieve this by:
- Running the module on a host that was configured with `step_bootstrap_host` as root (recommended).
- Pasing the `ca_url` and `root` parameters to the module.

For offline mode, you need to:
  - Provide `step-cli` with the path to your CA config (`$STEPPATH/config/ca.json` by default).
    You can override this with the `ca_config` parameter if required.
  - Run the module as the user the CA is running as to prevent permission issues

Below are some examples to showcase the different options. These examples assume that a CA is already set up on the local host.

```yaml
- hosts: ca
  tasks:
    - name: Run a module in online mode by specifying the CA URL and CA cert
      maxhoesel.smallstep.step_ca_certificate:
        root: /etc/ssl/myca.crt
        ca_url: https://my-ca.localdomain
        #params go here

    # This will only work if you ran step_bootstrap_host on this host first!
    - name: Run a module as root to use the CA configured during bootstrapping
      maxhoesel.smallstep.step_ca_certificate:
        #params go here
      become: yes

    - name: Run a module in offline mode
      maxhoesel.smallstep.step_ca_certificate:
        offline: yes
        # params go here
      become: yes
      # You should run modules acting on a local CA as the user that the CA runs as.
      # If you configured your CA with `step_ca`, the default user name is `step-ca`.
      become_user: step-ca

    - name: Run a offline-only module and manually supply the ca_config
      maxhoesel.smallstep.step_ca_provisioner:
        ca_config: /etc/step-ca/config/ca.json
        #params go here
      become: yes
      become_user: step-ca
```

All modules in this collection respect the `$STEPPATH` environment variable used to customize the step-cli config directory:

```yaml
  - name: Use the custom $STEPPATH in a module
    maxhoesel.smallstep.step_ca_certificate:
      # params go here
    environment:
      STEPPATH: /etc/step-cli
```

## Getting started (Step-By-Step)

This section will show you how to install a step-ca server and configure clients to trust that CA using this collection.
This guide will give you a good overview of how to use the tools in this collection.

Let's start with our inventory: In this example, we have a single server that we want to use as a step CA and three clients that we
want to trust the server:

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

To create a CA server from scratch, this role contains the [`step_ca`](roles/step_ca/README.md) role.
It will install and initialize a step-ca server for you, which you can then configure however you want.
Below is a simple example for how to do so. If you want to know more, check out the documentation for `step_ca`.

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
      command: 'step-cli certificate fingerprint /etc/step-ca/certs/root_ca.crt'
      register: root_ca_fp
    - name: Show root CA fingerprint
      debug:
        msg: "Fingerprint of root cert: {{ root_ca_fp.stdout }}"
```

### Bootstrap the clients

To establish trust between your clients and the CA, you will need the fingerprint of the CA root cert - see the [Create a CA](#create-a-ca) section for more details.
This fingerprint identifies your CA to your clients and allows them to verify the CA cert.

To actually initialize the clients, you can use [`step_bootstrap_host`](roles/step_bootstrap_host/README.md). This role will install `step-cli` and configure the host to trust your CA.

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
```

At this point, your CA is up and running and your hosts are configured to trust it. You're ready to go!
You can take a look at the available modules to further configure your CA and hosts if you wish to do so.


## License & Author

Created & Maintained by Max Hösel (@maxhoesel) and Contributors

Licensed under the GPL 3.0 or later
