# maxhoesel.smallstep

![Release](https://img.shields.io/github/v/release/maxhoesel/ansible-collection-smallstep)
![Build Status](https://img.shields.io/github/workflow/status/maxhoesel/ansible-collection-smallstep/CI/devel)
![License](https://img.shields.io/github/license/maxhoesel/ansible-collection-smallstep)

An Ansible collection for managing Smallstep CLI and CA applications.

This collection contains role and modules to help you install, configure, and maintain both the step client and the CA server from Ansible.

## Components

Currently, the following components are available:

#### Modules

- ca_provisioner: Add and remove provisioners on a step-ca server

#### Roles

- ca_server: Install and initialize a step-ca server
- (TODO) ca_cli: Install and initialize the step-cli client

## Installation

Before installing the collection, make sure that the following dependencies are met on the controller:

- Ansible 2.9 or newer
- Python 3.6 or newer

NOTE: Individual roles/modules may have additional requirements. Please see the role/module documentation for more details.

#### From Ansible-Galaxy

Installation via the official ansible-galaxy repository is currently not possible, due to [this issue](https://github.com/ansible/galaxy/issues/2519).

#### Repo install

To install the collection directly from this repository, run:

```ansible-galaxy install https://github.com/maxhoesel/ansible-collection-smallstep```

#### Tarball install

You can also install a specific version of this collection manually by downloading a tarball from the [releases](https://github.com/maxhoesel/ansible-collection-smallstep/releases).
