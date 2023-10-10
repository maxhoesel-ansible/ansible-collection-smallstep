#!/usr/bin/python

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: step_ca_bootstrap
author: Max Hösel (@maxhoesel)
short_description: Initialize C(step-cli) to trust a step-ca server
version_added: '0.3.0'
description: >
  Downloads the root certificate from the given cert authority and sets up the local environment to use it.
  This allows running other C(step-cli ca) commands without having to specify I(ca_url) or I(ca_config) every time.
notes:
  - Check mode is supported.
options:
  ca_url:
    description: URI of the targeted Step Certificate Authority
    type: str
    required: yes
  fingerprint:
    description: The fingerprint of the targeted root certificate
    type: str
    required: yes
  force:
    description: Force the overwrite of files without asking.
    type: bool
    default: no
  install:
    description: Install the root certificate into the system truststore. Make sure that the user has the required privileges.
    type: bool
    default: no
  redirect_url:
    description: Terminal OAuth redirect url.
    type: str

extends_documentation_fragment: maxhoesel.smallstep.cli_executable
"""

EXAMPLES = r"""
- name: Bootstrap using the CA url and a fingerprint
  maxhoesel.smallstep.step_ca_bootstrap:
    ca_url: https://ca.example.org
    fingerprint: d9d0978692f1c7cc791f5c343ce98771900721405e834cd27b9502cc719f5097

- name: Bootstrap and install the root certificate
  maxhoesel.smallstep.step_ca_bootstrap:
    ca_url: https://ca.example.org
    fingerprint: d9d0978692f1c7cc791f5c343ce98771900721405e834cd27b9502cc719f5097
    install: yes
"""

import json
import os
from typing import Dict, cast

from ansible.module_utils.basic import AnsibleModule
from ..module_utils.cli_wrapper import CLIWrapper

DEFAULTS_FILE = f"{os.environ.get('STEPPATH', os.environ['HOME'] + '/.step')}/config/defaults.json"


def run_module():
    argument_spec = dict(
        ca_url=dict(required=True),
        fingerprint=dict(required=True),
        force=dict(type="bool", default=False),
        install=dict(type="bool", default=False),
        redirect_url=dict(),
        step_cli_executable=dict(type="path", default="step-cli")
    )
    result = dict(changed=False, stdout="", stderr="", msg="")
    module = AnsibleModule(argument_spec, supports_check_mode=True)
    module_params = cast(Dict, module.params)

    cli = CLIWrapper(module, module_params["step_cli_executable"])

    if not module_params["force"]:  # type: ignore
        try:
            with open(DEFAULTS_FILE, "rb") as f:
                config = json.load(f)
        except OSError:
            # The file probably doesn't exist yet, continue for now
            config = {}
        current_fingerprint = config.get("fingerprint", "")
        if current_fingerprint != "":
            if current_fingerprint == module_params["fingerprint"]:
                result["msg"] = "Already bootstrapped and force not set."
            else:
                result["msg"] = "Already bootstrapped to a different CA, and force not set."
                result["failed"] = True
            module.exit_json(**result)

    cli_params = ["ca", "bootstrap"] + cli.build_params({
        "ca_url": "--ca-url",
        "fingerprint": "--fingerprint",
        "force": "--force",
        "install": "--install",
        "redirect_url": "--redirect-url",
    })
    result["stdout"], result["stderr"] = cli.run_command(cli_params)[1:3]
    result["changed"] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
