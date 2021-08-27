#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: step_ca_provisioner
author: Max Hösel (@maxhoesel)
short_description: Manage provisioners on a C(step-ca) server
version_added: '0.3.0'
description: Use this module to create and remove provisioners from a Smallstep CA server.
notes:
  - This module does B(not) modify existing provisioners - it will only add or remove them.
  - It is currently not possible to add JWK provisioners based on existing keys. Only the C(--create) option is supported.
  - Most of the options correspond to the command-line parameters for the C(step ca provisioner) command.
    See the documentation for mode information (U(https://smallstep.com/docs/step-cli/reference/ca/provisioner)).
  - The C(_file(s)) parameters must point to already existing files on the B(remote) host
  - Check mode is supported.
options:
  aws_account:
    description: The AWS account ids used to validate the identity documents. Must be a list.
    type: list
    elements: str
  aws_iid_roots_file:
    description: The path to the file containing the certificates used to validate the instance identity documents in AWS.
    type: path
  azure_tenant:
    description: The Microsoft Azure tenant id used to validate the identity tokens.
    type: str
  azure_resource_group:
    description: The Microsoft Azure resource group name used to validate the identity tokens. Must be a list.
    type: list
    elements: str
  disable_custom_sans:
    description: On cloud provisioners, if enabled only the internal DNS and IP will be added as a SAN. By default it will accept any SAN in the CSR.
    type: bool
    default: no
  disable_trust_on_first_use:
    description: >
      On cloud provisioners, if enabled multiple sign request for this provisioner with the same instance will be accepted.
      By default only the first request will be accepted.
    type: bool
    default: no
  gcp_service_account:
    description: The Google service account email or id used to validate the identity tokens. Must be a list.
    type: list
    elements: str
  gcp_project:
    description: The Google project id used to validate the identity tokens. Must be a list.
    type: list
    elements: str
  instance_age:
    description: >
      The maximum duration to grant a certificate in AWS and GCP provisioners. A duration is sequence of decimal numbers,
      each with optional fraction and a unit suffix, such as '300ms', '-1.5h' or '2h45m'.
      Valid time units are 'ns', 'us' (or 'µs'), 'ms', 's', 'm', 'h'.
    type: str
  k8s_pem_keys_file:
    description: >
      Public key file for validating signatures on K8s Service Account Tokens.
      PEM formatted bundle (can have multiple PEM blocks in the same file) of public keys and x509 Certificates.
    type: path
  jwk_password_file:
    description: The path to the file containing the password to encrypt or decrypt the private key
    type: path
  name:
    description: The name of the provisioner to add/remove.
    required: yes
    type: str
  oidc_client_id:
    description: The id used to validate the audience in an OpenID Connect token.
    type: str
  oidc_client_secret:
    description: The secret used to obtain the OpenID Connect Tokens.
    type: str
  oidc_listen_address:
    description: The callback address used in the OpenID Connect flow (e.g. ':10000').
    type: str
  oidc_configuration_endpoint:
    description: OpenID Connect configuration url.
    type: str
  oidc_admin_email:
    description: >
      The email of an admin user in an OpenID Connect provisioner, this user will not have restrictions in the certificates to sign. Must be a list.
    type: list
    elements: str
  oidc_domain:
    description: The domain used to validate the email claim in an OpenID Connect provisioner. Must be a list.
    type: list
    elements: str
  ssh:
    description: Whether to enable SSH on the new provisioners.
    type: bool
    default: no
  state:
    description: Whether the provisioner should be present or absent.
    choices:
      - 'present'
      - 'absent'
    default: 'present'
    type: str
  type:
    description: The type of provisioner to create or remove (case-sensitive).
    required: True
    choices:
      - 'JWK'
      - 'OIDC'
      - 'AWS'
      - 'GCP'
      - 'Azure'
      - 'ACME'
      - 'X5C'
      - 'K8sSA'
      - 'SSHPOP'
    type: str
  x5c_root_file:
    description: Root certificate (chain) file used to validate the signature on X5C provisioning tokens.
    type: path

extends_documentation_fragment:
  - maxhoesel.smallstep.step_cli
  - maxhoesel.smallstep.ca_connection_local_only
"""

EXAMPLES = r"""
# NOTE: All examples assume that the module is executed as a user with STEPPATH set to
# the step-ca config directory. If this is not the case, you can always specify the required
# parameters with ca_config

- name: Add a single JWK provisioner using an auto-generated asymmetric key pair
  maxhoesel.smallstep.ca_provisioner:
    name: max@smallstep.com
    type: JWK
    # Password file must already exist on the remote host
    jwk_password_file: /tmp/step-ca/max-laptop.pass
    state: present

- name: Add a single OIDC provisioner
  maxhoesel.smallstep.ca_provisioner:
    name: Google
    type: OIDC
    oidc_client_id: 1087160488420-8qt7bavg3qesdhs6it824mhnfgcfe8il.apps.googleusercontent.com
    oidc_configuration_endpoint: https://accounts.google.com/.well-known/openid-configuration

- name: Add an OIDC provisioner with two administrators
  maxhoesel.smallstep.ca_provisioner:
    name: Google
    type: OIDC
    oidc_client_id: 1087160488420-8qt7bavg3qesdhs6it824mhnfgcfe8il.apps.googleusercontent.com
    oidc_configuration_endpoint: https://accounts.google.com/.well-known/openid-configuration
    oidc_admin_email:
      - mariano@smallstep.com
      - max@smallstep.com
    oidc_domain: smallstep.com

- name: Add an AWS provisioner on one account with a one hour of instance age
  maxhoesel.smallstep.ca_provisioner:
    name: Amazon
    type: AWS
    aws_account: 123456789
    instance_age: 1h

- name: Add an GCP provisioner with two service accounts and two project ids
  maxhoesel.smallstep.ca_provisioner:
    name: Google
    type: GCP
    gcp_service_account:
      - 1234567890-compute@developer.gserviceaccount.com
      - 9876543210-compute@developer.gserviceaccount.com
    gcp_project:
      - identity
      - accounting

- name: Add an Azure provisioner with two service groups
  maxhoesel.smallstep.ca_provisioner:
    name: Azure
    type: Azure
    azure_tenant: bc9043e2-b645-4c1c-a87a-78f8644bfe57
    azure_resource_group:
      - identity
      - accounting

- name: Add an GCP provisioner that will only accept the SANs provided in the identity token
  maxhoesel.smallstep.ca_provisioner:
    name: Google
    type: GCP
    disable_custom_sans: yes
    gcp_project: internal

- name: Add an ACME provisioner
  maxhoesel.smallstep.ca_provisioner:
    name: acme-smallstep
    type: ACME

- name: Add an X5C provisioner.
  maxhoesel.smallstep.ca_provisioner:
    name: x5c-smallstep
    type: X5C
    # Key file must already exist on the remote host
    x5c_root_file: /tmp/x5c_root.crt

- name: Add a K8s Service Account provisioner
  maxhoesel.smallstep.ca_provisioner:
    name: my-kube-provisioner
    type: K8sSA
    # Key file must already exist on the remote host
    k8s_pem_keys_file: /tmp/keys.pub

- name: Add an SSH-POP provisioner
  maxhoesel.smallstep.ca_provisioner:
    name: sshpop-smallstep
    type: SSHPOP

- name: Remove a JWK provisioner
  maxhoesel.smallstep.ca_provisioner:
    name: my-jwk-provisioner
    type: JWK
    state: absent
"""

from ..module_utils.ca_connection_local_only import connection_argspec, connection_run_args
from ..module_utils.run import run_step_cli_command
from ..module_utils.validation import check_step_cli_install
from ansible.module_utils.basic import AnsibleModule
import os
import json


def add_provisioner(module, result):
    args = {
        "aws_account": "--aws-account",
        "aws_iid_roots_file": "--iid-roots",
        "azure_tenant": "--azure-tenant",
        "azure_resource_group": "--azure-resource-group",
        "disable_custom_sans": "--disable-custom-sans",
        "disable_trust_on_first_use": "--disable-trust-on-first-use",
        "gcp_service_account": "--gcp-service-account",
        "gcp_project": "--gcp-project",
        "instance_age": "--instance-age",
        "jwk_password_file": "--password-file",
        "k8s_pem_keys_file": "--pem-keys",
        "oidc_client_id": "--client-id",
        "oidc_client_secret": "--client-secret",
        "oidc_admin_email": "--admin",
        "oidc_domain": "--domain",
        "oidc_listen_address": "--listen-address",
        "oidc_configuration_endpoint": "--configuration-endpoint",
        "ssh": "--ssh",
        "type": "--type",
        "x5c_root_file": "--x5c-root",
    }
    command = ["ca", "provisioner", "add", module.params["name"]]
    # We only support creation of JWK provisioners with new keys right now
    if module.params["type"] == "JWK":
        command.append("--create")

    result = run_step_cli_command(
        module.params["step_cli_executable"], command,
        module, result, {**args, **connection_run_args}
    )
    result["changed"] = True
    return result


def remove_provisioner(module, result):
    result = run_step_cli_command(
        module.params["step_cli_executable"],
        ["ca", "provisioner", "remove", module.params["name"],
            "--type", module.params["type"]],
        module, result, connection_run_args
    )
    result["changed"] = True
    return result


def run_module():
    module_args = dict(
        aws_account=dict(type="list", elements="str"),
        aws_iid_roots_file=dict(type="path"),
        azure_tenant=dict(),
        azure_resource_group=dict(type="list", elements="str"),
        disable_custom_sans=dict(type="bool", default=False),
        disable_trust_on_first_use=dict(type="bool", default=False),
        gcp_service_account=dict(type="list", elements="str"),
        gcp_project=dict(type="list", elements="str"),
        instance_age=dict(),
        k8s_pem_keys_file=dict(type="path"),
        jwk_password_file=dict(type="path", no_log=False),
        name=dict(required=True),
        oidc_client_id=dict(),
        oidc_client_secret=dict(no_log=True),
        oidc_admin_email=dict(type="list", elements="str"),
        oidc_listen_address=dict(),
        oidc_domain=dict(type="list", elements="str"),
        oidc_configuration_endpoint=dict(),
        ssh=dict(type="bool", default=False),
        state=dict(choices=["present", "absent"], default="present"),
        step_cli_executable=dict(type="path", default="step-cli"),
        type=dict(
            choices=["JWK", "OIDC", "AWS", "GCP", "Azure",
                     "ACME", "X5C", "K8sSA", "SSHPOP"],
            required=True,
        ),
        x5c_root_file=dict(type="path"),
    )
    result = dict(changed=False, stdout="", stderr="", msg="")
    module = AnsibleModule(argument_spec={**module_args, **connection_argspec}, supports_check_mode=True)

    check_step_cli_install(
        module, module.params["step_cli_executable"], result)

    name = module.params["name"]
    state = module.params["state"]
    p_type = module.params["type"]

    # Need to read the config file directly as `step ca provisioner list` queries the CA server instead
    # of just loading from file. This means we'd have to include ca_url and handle failures, which we don't want.
    try:
        with open(module.params["ca_config"], "rb") as f:
            provisioners = json.load(f).get("authority", {}).get("provisioners", [])
    except Exception as e:
        result["msg"] = "Error reading ca.json config: {err}".format(err=e)
        module.fail_json(**result)

    for p in provisioners:
        if p["type"] == p_type and p["name"] == name:
            # Found a matching provisioner, now we need to decide what to do with it
            if state == "present":
                result["msg"] = "Provisioner found in CA config - not modified"
            elif state == "absent":
                result = remove_provisioner(module, result)
            module.exit_json(**result)

    # No matching provisioner found
    if state == "present":
        result = add_provisioner(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
