#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ca_provisioner
short_description: Manage provisioners for a Smallstep CA server
version_added: '2.10.0'
description: Use this module to create and remove provisioners from a Smallstep CA server.
requirements:
    - C(step) tool and C(step-ca) server installed on remote host
    - C(pexpect) module on remote host
    - This module must be executed as a user with write permissions on the config file specified in I(ca_config) (or the default step-ca config in ~/.step)
notes:
    - This module will B(not) modify existing provisioners - it can only add or remove them.
    - Most of the options correspond to the command-line parameters for the C(step ca provisioner) command. See the documentation for mode information (U(https://smallstep.com/docs/step-cli/reference/ca/provisioner)).
    - The C(_file(s)) parameters must point to already existing files on the B(remote) host
    - Check mode is supported.
options:
    aws_account:
        description: The AWS account id used to validate the identity documents. Also accepts a list for passing multiple ids.
    aws_iid_roots_file:
        description: The path to the file containing the certificates used to validate the instance identity documents in AWS.
    azure_tenant:
        description: The Microsoft Azure tenant id used to validate the identity tokens.
    azure_resource_group:
        description: The Microsoft Azure resource group name used to validate the identity tokens. Also accepts a list for passing multiple names.
    ca_config:
        description: The path to the certificate authority configuration file. Defaults to the C(step) default of C($STEPPATH/config/ca.json).
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
        description: The Google service account email or id used to validate the identity tokens. Also accepts a list for passing multiple ids.
    gcp_project:
        description: The Google project id used to validate the identity tokens. Also accepts a list for passing multiple ids.
    instance_age:
        description: >
            The maximum duration to grant a certificate in AWS and GCP provisioners. A duration is sequence of decimal numbers,
            each with optional fraction and a unit suffix, such as '300ms', '-1.5h' or '2h45m'.
            Valid time units are 'ns', 'us' (or 'µs'), 'ms', 's', 'm', 'h'.
    k8s_pem_keys_file:
        description: >
            Public key file for validating signatures on K8s Service Account Tokens.
            PEM formatted bundle (can have multiple PEM blocks in the same file) of public keys and x509 Certificates.
    jwk_create:
        description: Create a new ECDSA key pair using curve P-256 and populate a new JWK provisioner with it.
        type: bool
        default: no
    jwk_encrypt_password:
        description: Password used to encrypt the JWK provisioner key. Required when creating a JWK provisioner
        no_log: yes
    jwk_key_files:
        description: List of private (or public) keys in JWK or PEM format to be added to the provisioner.
    jwk_password_file:
        description: The path to the file containing the password to encrypt or decrypt the private key
    name:
        description: The name of the provisioner to add/remove.
        required: yes
    oidc_client_id:
        description: The id used to validate the audience in an OpenID Connect token.
    oidc_client_secret:
        description: The secret used to obtain the OpenID Connect Tokens.
    oidc_listen_address:
        description: The callback address used in the OpenID Connect flow (e.g. ':10000').
    oidc_configuration_endpoint:
        description: OpenID Connect configuration url.
    oidc_admin_email:
        description: >
            The email of an admin user in an OpenID Connect provisioner, this user will not have restrictions in the certificates to sign.
            Also accepts a list for multiple administrators.
    oidc_domain:
        description: The domain used to validate the email claim in an OpenID Connect provisioner. Also accepts a list for multiple domains.
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
    step_executable:
        description: Path or name of the step tool used to manage the step-ca server
        default: step
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
    x5c_root_file:
        description: Root certificate (chain) file used to validate the signature on X5C provisioning tokens.
author:
    - Max Hösel (@maxhoesel)
"""

EXAMPLES = r"""
- name: Add a single JWK provisioner
  maxhoesel.smallstep.ca_provisioner:
    name: max@smallstep.com
    type: JWK
    # Key and password files must already exist on the remote host
    jwk_key_files: /tmp/step-ca/max-laptop.jwk
    jwk_password_file: /tmp/step-ca/max-laptop.pass
    jwk_encrypt_password: a-secret-password
    state: present

- name: Add a single JWK provisioner using an auto-generated asymmetric key pair
  maxhoesel.smallstep.ca_provisioner:
    name: max@smallstep.com
    type: JWK
    # Password file must already exist on the remote host
    jwk_password_file: /tmp/step-ca/max-laptop.pass
    jwk_encrypt_password: a-secret-password
    jwk_create: yes
    state: present

- name: Add a list of provisioners for a single name
  maxhoesel.smallstep.ca_provisioner:
    name: max@smallstep.com
    type: JWK
    # Key and password files must already exist on the remote host
    jwk_key_files:
      - /tmp/step-ca/max-laptop.jwk
      - /tmp/max-phone.pem
      - /tmp/max-work.pem
    jwk_password_file: /tmp/step-ca/max-laptop.pass
    jwk_encrypt_password: a-secret-password
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
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
from ansible.module_utils.common.validation import check_type_list

import json
import os

try:
    import pexpect

    HAS_PEXPECT = True
except ImportError:
    HAS_PEXPECT = False


def validate_params(module, result):
    """
    Basic input parameter validation to ensure that the module will run properly.
    Does not guarantee that the parameters for a given provisioners actually make sense.
    Args:
        module: Module object for accessing module params
        result: result dict for returning results
    """
    if module.params["type"] == "JWK" and module.params["state"] == "present" and not HAS_PEXPECT:
        result["msg"] = "Please make sure that pexpect is installed for creating JWK provisioners"
        module.fail_json(**result)

    if module.params["type"] == "SSHPOP" and module.params["state"] == "absent":
        result["msg"] = "Cannot remove SSHPOP provisioners"
        module.fail_json(**result)

    rc, step_stdout, step_stderr = module.run_command([module.params["step_executable"]])
    if rc != 0:
        result["msg"] = (
            "Could not run step binary on remote host. "
            "Please make sure that it is installed and in $PATH."
        )
        result["stdout"] = step_stdout
        result["stderr"] = step_stderr
        module.fail_json(**result)
    return result


def get_provisioners(module, result):
    """
    Get a list of provisioners from step-ca.
    Args:
        module: Module object for accessing module params
        result: result dict for returning results
    Returns:
        list of provisioner dicts
    """
    with open(module.params["ca_config"], "rb") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as e:
            module.fail_json(msg="Error when loading ca.json config: {}".format(e), **result)
    return config["authority"]["provisioners"]


def add_provisioner(module, result):
    """
    Create a new provisioner of the type given in the module parameters.
    Args:
        module: Module object for accessing module params
        result: result dict for returning results
    """
    arg_map = {
        "aws_account": "--aws-account",
        "aws_iid_roots_file": "--iid-roots",
        "azure_tenant": "--azure-tenant",
        "azure_resource_group": "--azure-resource-group",
        "disable_custom_sans": "--disable-custom-sans",
        "disable_trust_on_first_use": "--disable-trust-on-first-use",
        "gcp_service_account": "--gcp-service-account",
        "gcp_project": "--gcp-project",
        "instance_age": "--instance-age",
        "k8s_pem_keys_file": "--pem-keys",
        "oidc_client_id": "--client-id",
        "oidc_client_secret": "--client-secret",
        "oidc_admin_email": "--admin",
        "oidc_domain": "--domain",
        "oidc_configuration_endpoint": "--configuration-endpoint",
        "ssh": "--ssh",
        "x5c_root_file": "--x5c-root",
    }
    bool_args = ["disable_custom_sans", "disable_trust_on_first_use", "jwk_create", "ssh"]

    # These args are always required
    args = ["add", module.params["name"], "--type=" + module.params["type"]]

    # step automatically truncates invalid parameters for us, so we can be
    # lazy and just pass through all user-supplied parameters for provisioners,
    # even if their type doesn't match (e.g. Azure params for a GCP provisioner).
    # We do however handle the jwk keys separately as they are positional parameters
    # instead of flags
    for arg in arg_map:
        if module.params[arg]:
            if isinstance(module.params[arg], list):
                # Step can accept some parameters multiple times. To use this,
                # we first need to convert the user-supplied lists into steps format:
                # --arg-name=val1 --arg-name=val2
                args.extend([arg_map[arg] + "=" + a for a in module.params[arg]])
            elif arg in bool_args:
                args.append(arg_map[arg])
            else:
                args.append(arg_map[arg] + "=" + module.params[arg])

    else:
        result = run_step_ca_command(
            module, result, args, errmsg="Error when trying to add provisioner"
        )
    result["changed"] = True
    return result


def add_jwk_provisioner(module, result):
    """
    Add a JWK provisioner using the options given in the module params.
    JWK provisioners need special treatment because they require an
    interactive password input and use positional parameters instead of
    options.
    Args:
        module: Module object for accessing module params
        result: result dict for returning results
    """
    if not module.params["jwk_encrypt_password"]:
        result["msg"] = "jwk_encrypt_password is required when creating a JWK provisioner"
        module.fail_json(**result)

    args = ["ca", "provisioner", "add", module.params["name"]]
    if module.params["jwk_create"]:
        args.append("--create")
    else:
        args.extend(module.params["jwk_key_files"])
        if module.params["jwk_password_file"]:
            args.extend(["--password-file", module.params["jwk_password_file"]])

    try:
        child = pexpect.spawn(module.params["step_executable"], args)
        child.expect("Please enter the password to encrypt the private JWK:")
        child.sendline(module.params["jwk_encrypt_password"])
        child.read()
        child.close()
    except (OSError, pexpect.ExceptionPexpect):
        result["msg"] = "Could not create JWK provisioner"
        module.fail_json(**result)
    return result


def remove_provisioner(module, result):
    """
    Remove an existing provisioner of the type given in the module parameters.
    Args:
        module: Module object for accessing module params
        result: result dict for returning results
    """
    args = ["remove", module.params["name"], "--type", module.params["type"]]
    result = run_step_ca_command(
        module, result, args, errmsg="Error when trying to remove provisioner"
    )
    result["changed"] = True
    return result


def run_step_ca_command(module, result, args, errmsg):
    """
    Run a step-ca command with args and the defaults passed to the module.
    Args:
        module: Module object for accessing module params
        result: result dict for returning results
        args: arguments of the command to run, as passed to module.run_command()
        errmsg: Error message to return if execution fails
    """
    base_args = [module.params["step_executable"], "ca", "provisioner"]
    args = base_args + args
    if module.params["ca_config"]:
        args.append("--ca-config=" + module.params["ca_config"])

    rc, result["stdout"], result["stderr"] = module.run_command(args)
    if rc != 0:
        result["msg"] = errmsg
        module.fail_json(**result)
    return result


def run_module():
    module_args = dict(
        aws_account=dict(type="list"),
        aws_iid_roots_file=dict(),
        azure_tenant=dict(),
        azure_resource_group=dict(type="list"),
        ca_config=dict(default="{}/.step/config/ca.json".format(os.path.expanduser("~"))),
        disable_custom_sans=dict(type="bool", default=False),
        disable_trust_on_first_use=dict(type="bool", default=False),
        gcp_service_account=dict(type="list"),
        gcp_project=dict(type="list"),
        instance_age=dict(),
        k8s_pem_keys_file=dict(),
        jwk_create=dict(type="bool", default=False),
        jwk_key_files=dict(type="list"),
        jwk_password_file=dict(no_log=False),
        jwk_encrypt_password=dict(no_log=True),
        name=dict(required=True),
        oidc_client_id=dict(),
        oidc_client_secret=dict(no_log=True),
        oidc_admin_email=dict(type="list"),
        oidc_domain=dict(type="list"),
        oidc_configuration_endpoint=dict(),
        ssh=dict(type="bool", default=False),
        state=dict(choices=["present", "absent"], default="present"),
        step_executable=dict(default="step"),
        type=dict(
            choices=["JWK", "OIDC", "AWS", "GCP", "Azure", "ACME", "X5C", "K8sSA", "SSHPOP"],
            required=True,
        ),
        x5c_root_file=dict(),
    )
    result = dict(changed=False, stdout="", stderr="", msg="")
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    result = validate_params(module, result)

    name = module.params["name"]
    state = module.params["state"]
    p_type = module.params["type"]

    provisioners = get_provisioners(module, result)
    # Ensure that we can always iterate over something
    if not provisioners:
        provisioners = []
    for p in provisioners:
        if p["type"] == p_type and p["name"] == name:
            # Found a matching provisioner, now we need to decide what to do with it
            if state == "present":
                result["msg"] = "Provisioner found in CA config - not modified"
            else:
                if not module.check_mode:
                    result = remove_provisioner(module, result)
                result["changed"] = True
            module.exit_json(**result)

    # No matching provisioner found
    if state == "present":
        if not module.check_mode and p_type == "JWK":
            result = add_jwk_provisioner(module, result)
        elif not module.check_mode:
            result = add_provisioner(module, result)
        result["changed"] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
