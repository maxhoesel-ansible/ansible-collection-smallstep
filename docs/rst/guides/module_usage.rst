Module Usage
============

The modules in this collection allow you to perform actions exposed by the :code:`step-cli` CLI tool, such as generating certificates or provisioners.
Since they are wrappers for :code:`step-cli` commands, some it is a good idea to first familiarize yourself with how :code:`step-cli` works:

First, :code:`step-cli` has two sets of commands - Standalone and CA commands:

* Standalone commands are run on the local host and do not involve a CA at all. Examples include :code:`step-cli certificate create` to create a certificate or all :code:`step-cli crypto` commands.

* CA commands communicate with a smallstep CA and can be identified by the :code:`ca` subcommand (e.g. :code:`step-cli ca certificate create`). :code:`step-cli` can talk to the CA in two different ways:

  * Online mode: :code:`step-cli` talks to the CA over HTTPS and uses the CAs API.

  * Offline mode: :code:`step-cli` accesses the CA files (certificates, config) directly, bypassing the API. This only works on the CA host itself.

Currently, this collection only includes CA modules.

CA Module Usage
---------------

Since the CA modules require access to a smallstep CA, you need to provide them with the parameters to access your CA.
There are a few ways to accomplish this and most modules can use any of these methods (see :ref:`Connection Method Exceptions` for exceptions).

Bootstrapping (Online, recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The easiest way is to first :code:`bootstrap` the host from which you are executing the CA modules.
This sets up the :code:`step-cli` utility to trust the smallstep CA, letting you connect to it without any further configuration.

You can use the :code:`step_bootstrap_host` role to install and bootstrap :code:`step-cli` for you:

..  code-block:: yaml

    - hosts: all
      become: true # step_bootstrap_host needs to be run as root
      tasks:
        - name: Install step-cli and bootstrap the root user to trust the CA
          ansible.builtin.include_role:
            name: maxhoesel.smallstep.step_bootstrap_host
          vars:
            # These values point the host to your smallstep CA
            step_bootstrap_ca_url: https://my-ca.localdomain
            step_bootstrap_fingerprint: "your root CA certs fingerprint"
            # You can configure the users that should trust the CA with this variable
            step_bootstrap_users:
                - name: root
                - name: your-ansible-service-user

        - name: Get a certificate from the CA
          maxhoesel.smallstep.step_ca_certificate:
            provisioner: "certificate-provisioner"
            contact: "email@example.com"
            crt_file: "/etc/ssl/my_cert.pem"
            key_file: "/etc/ssl/my_key.pem"
            name: "{{ ansible_fqdn }}"
            not_after: "24h"
            san: "{{ ansible_fqdn }}"
            standalone: true

Alternatively, you can install :code:`step-cli` yourself and then use the :code:`step_ca_bootstrap` module to bootstrap your host.

.. note::
    The bootstrapping process is done on a **per-user** basis, so any users not included in :code:`step_bootstrap_users` will **not** trust the CA and thus cannot run CA modules.

Manual CA parameters (Online)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There may be cases where you do not want to setup :code:`step-cli` to trust your CA permanently.
If find yourself in such a situation, you can use the :code:`ca_url` and :code:`root` parameters to make :code:`step-cli` trust your CA for one operation:

..  code-block:: yaml

    - hosts: all
      tasks:
        - name: Get a certificate from a CA in offline mode
          maxhoesel.smallstep.step_ca_certificate:
            provisioner: "certificate-provisioner"
            contact: "email@example.com"
            crt_file: "/etc/ssl/my_cert.pem"
            key_file: "/etc/ssl/my_key.pem"
            name: "{{ ansible_fqdn }}"
            not_after: "24h"
            san: "{{ ansible_fqdn }}"
            standalone: true
            # These parameters tell step-cli to trust the CA
            ca_url: https://my-ca.localdomain
            root: "/path/to/ca/root/cert.pem"

CA Config (Offline)
^^^^^^^^^^^^^^^^^^^

If you are running on the CA host itself, you can also use the existing CA config directly, bypassing the CA API:

..  code-block:: yaml

    - hosts: all
      tasks:
        - name: Get a certificate from a CA without bootstrapping
          maxhoesel.smallstep.step_ca_certificate:
            provisioner: "certificate-provisioner"
            contact: "email@example.com"
            crt_file: "/etc/ssl/my_cert.pem"
            key_file: "/etc/ssl/my_key.pem"
            name: "{{ ansible_fqdn }}"
            not_after: "24h"
            san: "{{ ansible_fqdn }}"
            standalone: true
            # Don't use the CA API, directly access the config file
            offline: true
            ca_config: /etc/step-ca/config/ca.json
          # run this module as the CA user so that we can read the config file
          become: true
          become_user: step-ca

.. _Connection Method Exceptions:

Connection Method Exceptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most modules can use any of the above connection methods, but there are a few exceptions:

* The `step_ca_bootstrap<ansible_collections.maxhoesel.smallstep.step_ca_bootstrap_module>` module is used to bootstrap the CA and doesn't use any of the above methods.

* The :ref:`step_ca_provisioner<ansible_collections.maxhoesel.smallstep.step_ca_provisioner_module>` module controls provisioners and *requires* offline mode.

  * Recent versions of the smallstep tools support remote provisioner management using the :code:`admin` facility and parameters.
    Support for these is a WIP - see `this issue <https://github.com/maxhoesel-ansible/ansible-collection-smallstep/issues/141>`_ for details.

STEPPATH Usage
--------------

All modules in this collection respect the :code:`$STEPPATH` environment variable used to customize the step-cli config directory:

..  code-block:: yaml

  - name: Use the custom $STEPPATH in a module
    maxhoesel.smallstep.step_ca_certificate:
      # params go here
    environment:
      STEPPATH: /etc/step-cli
