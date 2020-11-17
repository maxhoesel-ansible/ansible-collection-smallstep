#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ca_claims
short_description: Manage default or provisioner claims on a step-ca server
version_added: '2.10.0'
description: |
    This module can add, update or remove claims (such as certificate duration) on a step-ca server.
    You can either modify the claims of an individual provisioner, or change the default claims.
requirements:
    - A initialized step-ca server with a C(ca.json) file
notes:
    - Check mode is supported.
options:
    ca_config:
        description: The path to the certificate authority configuration file. Defaults to the C(step) default of C($STEPPATH/config/ca.json).
        default: ~/.step/config/ca.json
    exclusive:
        description: Replace all existing claims for the selected scope with the ones defined in the module parameters.
        type: bool
        default: no
    scope:
        description: The scope for which the claims should be modified (either global defaults or a specific provisioner).
        default: provisioner
        choices:
        - 'global'
        - 'provisioner'
    name:
        description: >
            The name of the provisioner to modify. If multiple provisioners have the same name,
            all provisioners will be modified unless I(type) is set. Conflicts with I(scope=global)
    type:
        description: Modify the provisioner with the name I(provisioner) that has this type. Has no effect if I(scope=global). Case-sensitive
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
    min_tls_cert_duration:
        description: Do not allow certificates with a duration less than this value.
    max_tls_cert_duration:
        description: Do not allow certificates with a duration greater than this value.
    default_tls_cert_duration:
        description: If no certificate validity period is specified, use this value.
    disable_issued_at_check:
        description: >
            Disable a check verifying that provisioning tokens must be issued after the CA has booted.
            This claim is one prevention against token reuse. The default value is false.
            Do not change this unless you know what you are doing.
    disable_renewal:
        description: Disable renewals with this provisioner.
        type: bool
    enable_SSHCA:
        description: Enable this provisioner to generate SSH Certificates.
        type: bool
    min_host_ssh_duration:
        description: Do not allow certificates with a duration less than this value.
    max_host_ssh_duration:
        description: Do not allow certificates with a duration greater than this value.
    default_host_ssh_duration:
        description: If no certificate validity period is specified, use this value.
    min_user_ssh_duration:
        description: Do not allow certificates with a duration less than this value.
    max_user_ssh_duration:
        description: Do not allow certificates with a duration greater than this value.
    default_user_ssh_duration:
        description: If no certificate validity period is specified, use this value.
author:
    - Max Hösel (@maxhoesel)
"""

EXAMPLES = r"""
- name: Change the TLS cert duration of a provisioner
  maxhoesel.smallstep.ca_claims:
    name: webtokens-1
    type: JWK
    min_tls_cert_duration: 24h
    max_tls_cert_duration: 720h
    default_tls_cert_duration: 168h

- name: Change default (global) claims
  maxhoesel.smallstep.ca_claims:
    scope: global
    min_tls_cert_duration: 24h
    max_tls_cert_duration: 720h
    default_tls_cert_duration: 168h

- name: Overwrite the claims of a provisioner with the given parameters
  maxhoesel.smallstep.ca_claims:
    name: webtokens-1
    type: JWK
    exclusive: yes
    min_tls_cert_duration: 24h
    max_tls_cert_duration: 720h
    default_tls_cert_duration: 168h

"""

RETURN = r"""
claims:
  description: >
    Dictionary contianing the claims of the selected scope.
    Dict of dict if multiple provisioners were selected, with the provisioners type as key
  returned: always
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.validation import check_mutually_exclusive

import copy
import os
import json


def get_current_claims(module, config, result):
    """
    Get the current claims for the scope specified in the module params.
    Args:
        module: Module object for accessing module params
        config: dict cotaining the ca.json configuration to act on
        result: result dict for returning results
    Returns:
        A dict of claims if scope == global or the provisioner type is set.
        A dict of dicts, containing the claims for all provisioner where the provisioners name == name,
            keyed by their type
    """
    p_name = module.params["name"]
    p_type = module.params["type"]
    scope = module.params["scope"]

    if module.params["exclusive"]:
        current_claims = dict()
    elif scope == "global":
        current_claims = config["authority"].get("claims", dict())
    elif p_type:
        try:
            current_claims = [
                p.get("claims", dict())
                for p in config["authority"].get("provisioners", [])
                if p["name"] == p_name and p["type"] == p_type
            ][0]
        except IndexError:
            result["msg"] = "Could not find provisioner with name {} and type {}".format(
                p_name, p_type
            )
            module.fail_json(**result)
    else:
        # If type is not specified and multiple provisioners share the same name, we will
        # end up with multiple provisioners to update. We accordingly create a dict of dicts,
        # with the type of the provisioner being the key.
        current_claims = {
            p["type"]: p.get("claims", dict())
            for p in config["authority"].get("provisioners", [])
            if p["name"] == module.params["name"]
        }
        if not current_claims:
            result["msg"] = "Could not find any provisioner with name {}".format(p_name)
            module.fail_json(**result)
    return current_claims


def write_config(module, config, result):
    """
    Write the config object to the ca.json file specified in the module params.
    Args:
        module: Module object for accessing module params
        config: dict cotaining the ca.json configuration to write
        result: result dict for returning results
    """
    tmpfile = module.params["ca_config"] + ".ansible-tmp"
    try:
        with open(tmpfile, "w") as f:
            json.dump(config, f)
            module.atomic_move(tmpfile, module.params["ca_config"])
    except Exception as e:
        result["msg"] = "Could not write ca.json file. Exception: {}".format(e)
        module.fail_json(**result)
    return result


def update_claims(module, current_config, result):
    """
    Update the claims for the scope specified in the module args.
    Args:
        module: Module object for accessing module params
        config: dict cotaining the ca.json configuration to act on
        result: result dict for returning results
    Returns:
        An updated configuration dict to be written to ca.json
    """
    claims = {
        "min_tls_cert_duration": "minTLSCertDuration",
        "max_tls_cert_duration": "maxTLSCertDuration",
        "default_tls_cert_duration": "defaultTLSCertDuration",
        "disable_issued_at_check": "disableIssuedAtCheck",
        "disable_renewal": "disableRenewal",
        "enable_SSHCA": "enableSSHCA",
        "min_host_ssh_duration": "minHostSSHDuration",
        "max_host_ssh_duration": "maxHostSSHDuration",
        "default_host_ssh_duration": "defaultHostSSHDuration",
        "min_user_ssh_duration": "minUserSSHDuration",
        "max_user_ssh_duration": "maxUserSSHDuration",
        "default_user_ssh_duration": "defaultUserSSHDuration",
    }
    current_claims = get_current_claims(module, current_config, result)
    module_claims = {claims[c]: module.params[c] for c in claims.keys() if module.params[c]}
    # We need a truly separate dict for the new config so that we
    # can compare both to set changed= appropriately when we're done.
    new_config = copy.deepcopy(current_config)

    # When creating our new claims, we might have to update multiple provisioners if
    # type is not specified and at least 2 provisioners share the same name.
    # We use their type as a key for identification in this case
    if module.params["type"] or module.params["scope"] == "global":
        new_claims = copy.deepcopy(current_claims)
        new_claims.update(module_claims)
    else:
        new_claims = dict()
        for p in current_claims:
            new_claims[p] = copy.deepcopy(current_claims[p])
            new_claims[p].update(module_claims)

    if module.params["scope"] == "global":
        new_config["authority"]["claims"] = new_claims
        result["claims"] = new_claims
    else:
        # To update existing provisioners, we generate a new list of provisioners from the old config,
        # updating claims as needed.
        new_provisioners = []
        for p in new_config["authority"].get("provisioners", []):
            if (
                module.params["type"]
                and p["name"] == module.params["name"]
                and p["type"] == module.params["type"]
            ):
                new_p = p
                new_p["claims"] = new_claims
                new_provisioners.append(new_p)
                result["claims"] = new_p["claims"]
            elif not module.params["type"] and p["name"] == module.params["name"]:
                new_p = p
                new_p["claims"] = new_claims[new_p["type"]]
                new_provisioners.append(new_p)
                result["claims"][new_p["type"]] = new_p["claims"]
            else:
                new_provisioners.append(p)
        new_config["authority"]["provisioners"] = new_provisioners

    if not module.check_mode:
        write_config(module, new_config, result)

    if current_config != new_config:
        result["changed"] = True
    return result


def validate_params(module, result):
    """
    Ensure that the module parameters make sense.
    Args:
        module: Module object for accessing module params
        result: result dict for returning results
    """
    try:
        check_mutually_exclusive([["set_global", "name"], ["set_global", "type"]], module.params)
    except TypeError:
        result["msg"] = "set_global cannot be used with 'name' or 'type"
        module.fail_json(**result)
    return result


def run_module():
    module_args = dict(
        ca_config=dict(default="{}/.step/config/ca.json".format(os.path.expanduser("~"))),
        exclusive=dict(type="bool", default=False),
        scope=dict(choices=["global", "provisioner"], default="provisioner"),
        min_tls_cert_duration=dict(),
        max_tls_cert_duration=dict(),
        default_tls_cert_duration=dict(),
        disable_issued_at_check=dict(type="bool"),
        disable_renewal=dict(type="bool"),
        enable_SSHCA=dict(type="bool"),
        min_host_ssh_duration=dict(),
        max_host_ssh_duration=dict(),
        default_host_ssh_duration=dict(),
        min_user_ssh_duration=dict(),
        max_user_ssh_duration=dict(),
        default_user_ssh_duration=dict(),
        name=dict(),
        type=dict(
            choices=["JWK", "OIDC", "AWS", "GCP", "Azure", "ACME", "X5C", "K8sSA", "SSHPOP"],
        ),
    )
    result = dict(changed=False, msg="", claims=dict())
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    result = validate_params(module, result)

    try:
        with open(module.params["ca_config"]) as f:
            config = json.load(f)
    except Exception as e:
        result["msg"] = "Error when loading ca.json config: {}".format(e)
        module.fail_json(**result)

    result = update_claims(module, config, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
