#!/usr/bin/python

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: step_ca_revoke
author: Max Hösel (@maxhoesel)
short_description: Revoke a Certificate
version_added: '0.3.0'
description: Revoke a Certificate
notes:
  - Check mode is supported.
options:
  cert:
    description: The path to the cert that should be revoked. Can be let empty if I(serial_number) is defined.
    type: path
  key:
    description: The path to the key corresponding to the cert that should be revoked. Can be let empty if I(serial_number) is defined.
    type: path
  reason:
    description: The string representing the reason for which the cert is being revoked.
    type: str
  reason_code:
    description: >
      The reasonCode specifies the reason for revocation - chose from a list of common revocation reasons.
      If unset, the default is Unspecified. See https://smallstep.com/docs/step-cli/reference/ca/revoke for more details
    type: int
  serial_number:
    description: >
      The serial number of the certificate that should be revoked.
      Can be left blank when using I(cert) and I(key) params for revocation over mTLS.
    type: int
  token:
    description: The one-time token used to authenticate with the CA in order to revoke the certificate.
    type: str
    ##no_log

extends_documentation_fragment:
  - maxhoesel.smallstep.cli_executable
  - maxhoesel.smallstep.ca_connection
"""

EXAMPLES = r"""
# See https://smallstep.com/docs/step-cli/reference/ca/revoke for more examples

- name: Revoke a local certificate
  maxhoesel.smallstep.step_ca_revoke:
    cert: internal.crt
    key: internal.key
    ca_url: https://ca.smallstep.com:9000

- name: Revoke a certificate via serial number
  maxhoesel.smallstep.step_ca_revoke:
    serial_number: 308893286343609293989051180431574390766
    ca_url: https://ca.smallstep.com:9000
    token: "{{ ca_token }}"
"""

from typing import Dict, cast

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.cli_wrapper import CLIWrapper
from ..module_utils.params.ca_connection import CaConnectionParams
from ..module_utils.constants import DEFAULT_STEP_CLI_EXECUTABLE


def run_module():
    argument_spec = dict(
        cert=dict(type="path"),
        key=dict(type="path"),
        reason=dict(type="str"),
        reason_code=dict(type="int"),
        serial_number=dict(type="int"),
        token=dict(type="str", no_log=True),
        step_cli_executable=dict(type="path", default=DEFAULT_STEP_CLI_EXECUTABLE),
    )
    result = dict(changed=False, stdout="", stderr="", msg="")
    module = AnsibleModule(argument_spec={
        **CaConnectionParams.argument_spec,
        **argument_spec
    }, supports_check_mode=True)
    CaConnectionParams(module).check()
    module_params = cast(Dict, module.params)

    cli = CLIWrapper(module, module_params["step_cli_executable"])

    # Regular args
    revoke_cliargs = ["cert", "key", "reason", "reason_code",
                      "token"]
    # Most parameters can be converted to a mapping by just appending -- and replacing the underscores
    revoke_cliarg_map = {arg: f"--{arg.replace('_', '-')}" for arg in revoke_cliargs}
    # This step-cli argument uses camelCase for some reason
    revoke_cliarg_map["reason_code"] = "--reasonCode"

    # Positional Parameters
    cli_params = [
        "ca", "revoke"
    ] + cli.build_params({
        **revoke_cliarg_map,
        **CaConnectionParams.cliarg_map
    })
    if module_params["serial_number"]:
        cli_params.append([module_params["serial_number"]])  # type: ignore

    result["stdout"], result["stderr"] = cli.run_command(cli_params)[1:3]
    result["changed"] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
