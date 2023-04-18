#!/usr/bin/python

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: step_ca_provisioner
author: Max Hösel (@maxhoesel)
short_description: Manage provisioners on a C(step-ca) server
version_added: '0.3.0'
description: Use this module to create and remove provisioners from a Smallstep CA server.
notes:
  - Existing provisioners will B(not) be modified by default, use the I(update) flag to force provisioner updates
  - Most of the options correspond to the command-line parameters for the C(step ca provisioner) command.
    See the documentation for mode information (U(https://smallstep.com/docs/step-cli/reference/ca/provisioner)).
  - Any files used to create the provisioner (e.g. root certificate chains) must already be present on the remote host.
  - Check mode is supported.
options:
  allow_renewal_after_expiry:
    description: Allow renewals for expired certificates generated by this provisioner.
    type: bool
    version_added: 0.20.0
  aws_accounts:
    description: The AWS account ids used to validate the identity documents. Must be a list
    type: list
    elements: str
    aliases:
      - aws_account
  azure_audience:
    description: The Microsoft Azure audience name used to validate the identity tokens.
    type: str
    version_added: 0.20.0
  azure_object_ids:
    description: The Microsoft Azure AD object ids used to validate the identity tokens. Must be a list
    type: list
    elements: str
    version_added: 0.20.0
    aliases:
      - azure_object_id
  azure_resource_groups:
    description: The Microsoft Azure resource group names used to validate the identity tokens. Must be a list
    type: list
    elements: str
    aliases:
      - azure_resource_group
  azure_subscription_ids:
    description: The Microsoft Azure subscription ids used to validate the identity tokens. Must be a list
    type: list
    elements: str
    version_added: 0.20.0
    aliases:
      - azure_subscription_id
  azure_tenant:
    description: The Microsoft Azure tenant id used to validate the identity tokens.
    type: str
  ca_config:
    description: The path to the certificate authority configuration file on the host if managing provisioners locally.
    type: path
    default: CI($STEPPATH)/config/ca.json
  ca_url:
    description: URI of the targeted Step Certificate Authority
    version_added: 0.20.0
    type: str
  disable_custom_sans:
    description: >
      On cloud provisioners, if enabled only the internal DNS and IP will be added as a SAN.
      By default it will accept any SAN in the CSR.
    type: bool
  disable_renewal:
    description: Disable renewal for all certificates generated by this provisioner.
    type: bool
    version_added: 0.20.0
  disable_trust_on_first_use:
    description: >
      On cloud provisioners, if enabled multiple sign request for this provisioner with the same instance will be accepted.
      By default only the first request will be accepted.
    type: bool
  force_cn:
    description: Always set the common name in provisioned certificates.
    type: bool
    version_added: 0.20.0
  gcp_projects:
    description: The Google project ids used to validate the identity tokens. Must be a list
    type: list
    elements: str
    aliases:
      - gcp_project
  gcp_service_accounts:
    description: The Google service account emails or ids used to validate the identity tokens. Must be a list
    type: list
    elements: str
    aliases:
      - gcp_service_account
  instance_age:
    description: >
        The maximum duration to grant a certificate in AWS and GCP provisioners.
        A duration is sequence of decimal numbers, each with optional fraction and a unit suffix,
        such as "300ms", "-1.5h" or "2h45m".
        Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
  jwk_create:
    description: Create the JWK key pair for the provisioner.
    type: bool
    version_added: 0.20.0
    aliases:
      - create
  jwk_private_key:
    description: The file containing the JWK private key.
    type: path
    version_added: 0.20.0
    aliases:
      - private_key
  name:
    description: The name of the provisioner to add/remove.
    required: yes
    type: str
  nebula_root:
    description: Root certificate (chain) file used to validate the signature on Nebula provisioning tokens.
    type: path
    version_added: 0.20.0
  oidc_admins:
    description: >
        The emails of admin users in an OpenID Connect provisioner,
        these users will not have restrictions in the certificates to sign.
        Must be a list
    type: list
    elements: str
    aliases:
      - admin
      - oidc_admin
      - oidc_admin_email
  oidc_client_id:
    description: The id used to validate the audience in an OpenID Connect token.
    type: str
    aliases:
      - client_id
  oidc_client_secret:
    description: The secret used to obtain the OpenID Connect tokens.
    type: str
    aliases:
      - client_secret
  oidc_configuration_endpoint:
    description: OpenID Connect configuration url.
    type: str
    aliases:
      - configuration_endpoint
  oidc_groups:
    description: The group list used to validate the groups extenstion in an OpenID Connect token. Must be a list
    type: list
    elements: str
    aliases:
      - oidc_group
      - group
  oidc_listen_address:
    description: The callback address used in the OpenID Connect flow (e.g. ":10000").
    type: str
    aliases:
      - listen_address
      - oidc_client_address
  oidc_tenant_id:
    description: The tenant-id used to replace the templatized {tenantid} in the OpenID Configuration.
    type: str
    version_added: 0.20.0
    aliases:
      - tenant_id
  password_file:
    description: The path to the file containing the password to encrypt or decrypt the private key.
    type: path
    aliases:
      - jwk_password_file
  public_key:
    description: >
        The file containing the JWK public key.
        Or, a file containing one or more PEM formatted keys, if used with the K8SSA provisioner.
    type: path
    aliases:
      - jwk_public_key
      - k8ssa_public_key
      - k8s_pem_keys_file
  require_eab:
    description: >
        Require (and enable) External Account Binding (EAB) for Account creation.
        If this flag is set to false, then disable EAB.
    type: bool
    version_added: 0.20.0
  root:
    description:  The path to the PEM file used as the root certificate authority.
    type: path
    version_added: 0.20.0
  scep_capabilities:
    description: The SCEP capabilities to advertise
    type: str
    aliases:
      - capabilities
    version_added: 0.20.0
  scep_challenge:
    description: The SCEP challenge to use as a shared secret between a client and the CA
    type: str
    aliases:
      - challenge
    version_added: 0.20.0
  scep_encryption_algorithm_identifier:
    description: >
        The id for the SCEP encryption algorithm to use.
        Valid values are 0 - 4, inclusive. The values correspond to:
        0: DES-CBC, 1: AES-128-CBC, 2: AES-256-CBC, 3: AES-128-GCM, 4: AES-256-GCM.
        Defaults to DES-CBC (0) for legacy clients.
    type: int
    aliases:
      - encryption_algorithm_identifier
    version_added: 0.20.0
  scep_include_root:
    description: Include the CA root certificate in the SCEP CA certificate chain.
    type: bool
    aliases:
      - include_root
    version_added: 0.20.0
  scep_min_public_key_length:
    description: The minimum public key length of the SCEP RSA encryption key
    type: str
    aliases:
      - min_public_key_length
    version_added: 0.20.0
  ssh:
    description: Enable provisioning of ssh certificates. The default value is true. To disable ssh use '--ssh=false'.
    type: bool
    default: true
  ssh_host_min_dur:
    description: >
      The minimum duration for an ssh host certificate generated by this provisioner.
      Value must be a sequence of decimal numbers, each with optional fraction,
      and a unit suffix, such as "300ms", "-1.5h" or "2h45m".
      Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
    version_added: 0.20.0
  ssh_host_max_dur:
    description: >
      The maximum duration for an ssh host certificate generated by this provisioner.
      Value must be a sequence of decimal numbers, each with optional fraction,
      and a unit suffix, such as "300ms", "-1.5h" or "2h45m".
      Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
    version_added: 0.20.0
  ssh_host_default_dur:
    description: >
      The default duration for an ssh host certificate generated by this provisioner.
      Value must be a sequence of decimal numbers, each with optional fraction,
      and a unit suffix, such as "300ms", "-1.5h" or "2h45m".
      Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
    version_added: 0.20.0
  ssh_user_min_dur:
    description: >
      The minimum duration for an ssh user certificate generated by this provisioner.
      Value must be a sequence of decimal numbers, each with optional fraction,
      and a unit suffix, such as "300ms", "-1.5h" or "2h45m".
      Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
    version_added: 0.20.0
  ssh_user_max_dur:
    description: >
      The maximum duration for an ssh user certificate generated by this provisioner.
      Value must be a sequence of decimal numbers, each with optional fraction,
      and a unit suffix, such as "300ms", "-1.5h" or "2h45m".
      Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
    version_added: 0.20.0
  ssh_user_default_dur:
    description: >
      The default duration for an ssh user certificate generated by this provisioner.
      Value must be a sequence of decimal numbers, each with optional fraction,
      and a unit suffix, such as "300ms", "-1.5h" or "2h45m".
      Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
    version_added: 0.20.0
  ssh_template:
    description: The ssh certificate template file, a JSON representation of the certificate to create.
    type: path
    version_added: 0.20.0
  ssh_template_data:
    description: The ssh certificate template data file, a JSON map of data that can be used by the certificate template.
    type: path
    version_added: 0.20.0
  state:
    description: >
        Whether the provisioner should be present or absent.
        Note that C(present) does not update existing provisioners.
        C(updated) will attempt to update the provisioner regardless of whether it has changed or not.
        Note that this will always report the task as changed.
    choices:
      - 'present'
      - 'updated'
      - 'absent'
    default: 'present'
    type: str
  type:
    description: >
        The type of provisioner to create (case-sensitive).
        Ignored when state == absent or updated.
        Required if state == present
    choices:
      - 'JWK'
      - 'OIDC'
      - 'AWS'
      - 'GCP'
      - 'Azure'
      - 'ACME'
      - 'X5C'
      - 'K8SSA'
      - 'SSHPOP'
      - 'SCEP'
      - 'Nebula'
    type: str
  x509_template:
    description: The x509 certificate template file, a JSON representation of the certificate to create.
    type: path
    version_added: 0.20.0
  x509_template_data:
    description:  The x509 certificate template data file, a JSON map of data that can be used by the certificate template.
    type: path
    version_added: 0.20.0
  x509_min_dur:
    description: >
      The minimum duration for an x509 certificate generated by this provisioner.
      Value must be a sequence of decimal numbers, each with optional fraction,
      and a unit suffix, such as "300ms", "-1.5h" or "2h45m".
      Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
    version_added: 0.20.0
  x509_max_dur:
    description: >
      The maximum duration for an x509 certificate generated by this provisioner.
      Value must be a sequence of decimal numbers, each with optional fraction,
      and a unit suffix, such as "300ms", "-1.5h" or "2h45m".
      Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
    version_added: 0.20.0
  x509_default_dur:
    description: >
      The default duration for an x509 certificate generated by this provisioner.
      Value must be a sequence of decimal numbers, each with optional fraction,
      and a unit suffix, such as "300ms", "-1.5h" or "2h45m".
      Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
    version_added: 0.20.0
  x5c_root:
    description: Root certificate (chain) file used to validate the signature on X5C provisioning tokens.
    type: path
    aliases:
      - x5c_root_file

extends_documentation_fragment:
  - maxhoesel.smallstep.step_cli
  - maxhoesel.smallstep.admin
"""

EXAMPLES = r"""
# NOTE: All examples assume that the module is executed as a user with STEPPATH set to
# the step-ca config directory. If this is not the case, you can always specify the required
# parameters with ca_config

- name: Create a JWK provisioner with newly generated keys and a template for x509 certificates
  maxhoesel.smallstep.step_ca_provisioner:
    name: cicd
    type: JWK
    jwk_create: yes
    x509_template: ./templates/example.tpl

- name: Create a JWK provisioner with duration claims
  maxhoesel.smallstep.step_ca_provisioner:
    name: cicd
    type: JWK
    create: yes
    x509_min_dur: 20m
    x509_default_dur: 20m
    x509_max_dur: 24h

- name: Create a JWK provisioner with existing keys
  maxhoesel.smallstep.step_ca_provisioner:
    name: jane@doe.com
    type: JWK
    public_key: jwk.pub
    private_key: jwk.priv

- name: Create an OIDC provisioner
  maxhoesel.smallstep.step_ca_provisioner:
    name: Google
    type: OIDC
    client_id: 1087160488420-8qt7bavg3qesdhs6it824mhnfgcfe8il.apps.googleusercontent.com
    client_secret: udTrOT3gzrO7W9fDPgZQLfYJ
    configuration_endpoint: https://accounts.google.com/.well-known/openid-configuration

- name: Create an X5C provisioner
  maxhoesel.smallstep.step_ca_provisioner:
    name: x5c
    type: X5C
    x5c_root: x5c_ca.crt

- name: Create an ACME provisioner, forcing a CN and requiring EAB
  maxhoesel.smallstep.step_ca_provisioner:
    name: acme
    type: ACME
    force_cn: yes
    require_eab: yes

- name: Crate an K8SSA provisioner
  maxhoesel.smallstep.step_ca_provisioner:
    name: kube
    type: K8SSA
    ssh: true
    public_key: key.pub

- name: Create an SSHPOP provisioner
  maxhoesel.smallstep.step_ca_provisioner:
    name: sshpop
    type: SSHPOP

- name: Create a SCEP provisioner
  maxhoesel.smallstep.step_ca_provisioner:
    name: scep_provisioner
    type: SCEP
    scep_challenge: secret
    scep_encryption_algorithm_identifier: 2

- name: Create a complexAzure provisioner
  maxhoesel.smallstep.step_ca_provisioner:
    name: Azure
    type: Azure
    azure_tenant: bc9043e2-b645-4c1c-a87a-78f8644bfe57
    azure_resource_groups:
      - identity
      - accounting
    azure_subscription_ids:
      - dc760a01-2886-4a84-9abc-f3508e0f87d9
    azure_object_ids:
      - f50926c7-abbf-4c28-87dc-9adc7eaf3ba7
"""

import json
import os

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import admin
from ..module_utils.step_cli_wrapper import CLIWrapper

# We cannot use the default connection module util, as that one includes the --offline flag,
# which is not valid for the provisioner API call
CONNECTION_PARAM_SPEC = {
    "ca_config": "--ca-config",
    "ca_url": "--ca-url",
    "root": "--root"
}

CREATE_UPDATE_PARAM_SPEC = {
    "allow_renewal_after_expiry": "--allow-renewal-after-expiry",
    "aws_accounts": "--aws-account",
    "azure_audience": "--azure-audience",
    "azure_object_ids": "--azure-object-id",
    "azure_resource_groups": "--azure-resource-group",
    "azure_subscription_ids": "--azure-subscription-id",
    "azure_tenant": "--azure-tenant",
    "disable_custom_sans": "--disable-custom-sans",
    "disable_renewal": "--disable-renewal",
    "disable_trust_on_first_use": "--disable-trust-on-first-use",
    "force_cn": "--force-cn",
    "gcp_projects": "--gcp-project",
    "gcp_service_accounts": "--gcp-service-account",
    "instance_age": "--instance-age",
    "jwk_create": "--create",
    "jwk_private_key": "--private-key",
    "nebula_root": "--nebula-root",
    "oidc_admins": "--admin",
    "oidc_client_id": "--client-id",
    "oidc_client_secret": "--client-secret",
    "oidc_configuration_endpoint": "--configuration-endpoint",
    "oidc_groups": "--group",
    "oidc_listen_address": "--listen-address",
    "oidc_tenant_id": "--tenant-id",
    "password_file": "--password-file",
    "public_key": "--public-key",
    "require_eab": "--require-eab",
    "scep_capabilities": "--capabilities",
    "scep_challenge": "--challenge",
    "scep_encryption_algorithm_identifier": "--encryption-algorithm-identifier",
    "scep_include_root": "--include-root",
    "scep_min_public_key_length": "--min-public-key-length",
    "ssh": "--ssh",
    "ssh_host_min_dur": "--ssh-host-min-dur",
    "ssh_host_max_dur": "--ssh-host-max-dur",
    "ssh_host_default_dur": "--ssh-host-default-dur",
    "ssh_user_min_dur": "--ssh-user-min-dur",
    "ssh_user_max_dur": "--ssh-user-max-dur",
    "ssh_user_default_dur": "--ssh-user-default-dur",
    "ssh_template": "--ssh-template",
    "ssh_template_data": "--ssh-template-data",
    "x509_template": "--x509-template",
    "x509_template_data": "--x509-template-data",
    "x509_min_dur": "--x509-min-dur",
    "x509_max_dur": "--x509-max-dur",
    "x509_default_dur": "--x509-default-dur",
    "x5c_root": "--x5c-root",
}


def add_provisioner(module, cli, result):
    command = ["ca", "provisioner", "add", module.params["name"], "--type", module.params["type"]]
    params = {**CREATE_UPDATE_PARAM_SPEC, **CONNECTION_PARAM_SPEC, **admin.param_spec}
    result["stdout"], result["stderr"] = cli.run_command(command, params)[1:3]
    result["changed"] = True
    return result


def update_provisioner(module, cli, result):
    command = ["ca", "provisioner", "update", module.params["name"]]
    params = {**CREATE_UPDATE_PARAM_SPEC, **CONNECTION_PARAM_SPEC, **admin.param_spec}
    result["stdout"], result["stderr"] = cli.run_command(command, params)[1:3]
    result["changed"] = True
    return result


def remove_provisioner(module, cli, result):
    command = ["ca", "provisioner", "remove", module.params["name"]]
    params = {**CONNECTION_PARAM_SPEC, **admin.param_spec}
    result["stdout"], result["stderr"] = cli.run_command(command, params)[1:3]
    result["changed"] = True
    return result


def run_module():
    # name, state, type
    module_args = dict(
        allow_renewal_after_expiry=dict(type="bool"),
        aws_accounts=dict(type="list", elements="str", aliases=["aws_account"]),
        azure_audience=dict(type="str"),
        azure_object_ids=dict(type="list", elements="str", aliases=["azure_object_id"]),
        azure_resource_groups=dict(type="list", elements="str", aliases=["azure_resource_group"]),
        azure_subscription_ids=dict(type="list", elements="str", aliases=["azure_subscription_id"]),
        azure_tenant=dict(type="str"),
        ca_config=dict(
            type="path", default=f"{os.environ.get('STEPPATH', os.environ['HOME'] + '/.step')}/config/ca.json"),
        ca_url=dict(type="str"),
        disable_custom_sans=dict(type="bool"),
        disable_renewal=dict(type="bool"),
        disable_trust_on_first_use=dict(type="bool"),
        force_cn=dict(type="bool"),
        gcp_projects=dict(type="list", elements="str", aliases=["gcp_project"]),
        gcp_service_accounts=dict(type="list", elements="str", aliases=["gcp_service_account"]),
        instance_age=dict(type="str"),
        jwk_create=dict(type="bool", aliases=["create"]),
        jwk_private_key=dict(type="path", aliases=["private_key"]),
        name=dict(type="str", required=True),
        nebula_root=dict(type="path"),
        oidc_admins=dict(type="list", elements="str", aliases=["oidc_admin", "admin", "oidc_admin_email"]),
        oidc_client_id=dict(type="str", aliases=["client_id"]),
        oidc_client_secret=dict(type="str", no_log=True, aliases=["client_secret"]),
        oidc_configuration_endpoint=dict(type="str", aliases=["configuration_endpoint"]),
        oidc_groups=dict(type="list", elements="str", aliases=["group", "oidc_group"]),
        oidc_listen_address=dict(type="str", aliases=["listen_address", "oidc_client_address"]),
        oidc_tenant_id=dict(type="str", aliases=["tenant_id"]),
        # This is already specified in admin.py, but apparently also used in JWK provisioning?
        # Seems like a source of conflict - for now we override it here
        password_file=dict(type="path", no_log=False),
        public_key=dict(type="path", aliases=["jwk_public_key", "k8ssa_public_key", "k8s_pem_keys_file"]),
        require_eab=dict(type="bool"),
        root=dict(type="path"),
        scep_capabilities=dict(type="str", aliases=["capabilities"]),
        scep_challenge=dict(type="str", no_log=True, aliases=["challenge"]),
        scep_encryption_algorithm_identifier=dict(type="int", aliases=["encryption_algorithm_identifier"]),
        scep_include_root=dict(type="bool", aliases=["include_root"]),
        scep_min_public_key_length=dict(type="str", aliases=["min_public_key_length"]),
        ssh=dict(type="bool", default=True),
        ssh_host_min_dur=dict(type="str"),
        ssh_host_max_dur=dict(type="str"),
        ssh_host_default_dur=dict(type="str"),
        ssh_user_min_dur=dict(type="str"),
        ssh_user_max_dur=dict(type="str"),
        ssh_user_default_dur=dict(type="str"),
        ssh_template=dict(type="path"),
        ssh_template_data=dict(type="path"),
        state=dict(type="str", default="present", choices=["present", "updated", "absent"]),
        type=dict(type="str", choices=[
            "JWK", "OIDC", "AWS", "GCP", "Azure", "ACME", "X5C", "K8SSA", "SSHPOP", "SCEP", "Nebula"]),
        x509_template=dict(type="path"),
        x509_template_data=dict(type="path"),
        x509_min_dur=dict(type="str"),
        x509_max_dur=dict(type="str"),
        x509_default_dur=dict(type="str"),
        x5c_root=dict(type="path", aliases=["x5c_root_file"]),
        step_cli_executable=dict(type="path", default="step-cli"),
    )
    result = dict(changed=False, stdout="", stderr="", msg="")
    module = AnsibleModule(
        argument_spec={**admin.args, **module_args},
        supports_check_mode=True
    )

    admin.check_argspec(module, result)

    cli = CLIWrapper(module, result, module.params["step_cli_executable"])

    name = module.params["name"]
    state = module.params["state"]
    p_type = module.params["type"]

    if state == "present" and not p_type:
        result["msg"] = "Provisioner type is required when state == present."
        module.fail_json(**result)

    rc, stdout = cli.run_command(["ca", "provisioner", "list"], CONNECTION_PARAM_SPEC,
                                 check_mode_safe=True, exit_on_error=False)[0:2]
    # Offline provisioner management is possible even if the CA is down.
    # ca provisioner list does depend on the CA being available however, so we need some backup strategies.
    if rc == 0:
        try:
            provisioners = json.loads(stdout)
        except (json.JSONDecodeError, OSError) as e:
            result["msg"] = f"Error reading provisioner config: {e}"
            module.fail_json(**result)
    elif admin.is_present(module):
        # Admin credentials means that the provisioners are managed remotely and are stored in the DB.
        # Combined with a connection failure, this means that we are unable to continue
        result["msg"] = "Unable to contact CA to retrieve provisioner list remotely, and admin args are set."
        module.fail_json(**result)
    else:
        # Without admin, provisioners are always managed locally, so we can just read them as a fallback
        with open(module.params["ca_config"], "rb") as f:
            try:
                provisioners = json.load(f).get("authority", {}).get("provisioners", [])
            except (json.JSONDecodeError, OSError) as e:
                result["msg"] = f"Error reading provisioner config: {e}"
                module.fail_json(**result)

    for p in provisioners:
        if p["name"] == name:
            if state == "present" and p["type"] == p_type:
                result["msg"] = "Provisioner found in CA config - not modified"
                module.exit_json(**result)
            elif state == "updated":
                result = update_provisioner(module, cli, result)
            elif state == "absent":
                result = remove_provisioner(module, cli, result)
                module.exit_json(**result)

    # No matching provisioner found
    if state == "present":
        result = add_provisioner(module, cli, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
