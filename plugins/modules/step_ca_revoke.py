#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

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
  - maxhoesel.smallstep.step_cli
  - maxhoesel.smallstep.ca_connection_hybrid
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

from ..module_utils.ca_connection_hybrid import connection_run_args, connection_argspec
from ..module_utils.run import run_step_cli_command
from ..module_utils.validation import check_step_cli_install
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        cert=dict(type="path"),
        key=dict(type="path"),
        reason=dict(type="str"),
        reason_code=dict(type="int"),
        serial_number=dict(type="int"),
        token=dict(type="str", no_log=True),
        step_cli_executable=dict(type="path", default="step-cli"),
    )
    result = dict(changed=False, stdout="", stderr="", msg="")
    module = AnsibleModule(argument_spec={**module_args, **connection_argspec}, supports_check_mode=True)

    check_step_cli_install(
        module, module.params["step_cli_executable"], result)

    # Positional Parameters
    params = ["ca", "revoke"]
    if module.params["serial_number"]:
        params.append([module.params["serial_number"]])
    # Regular args
    args = ["cert", "key", "reason", "reason_code",
            "token"]
    # All parameters can be converted to a mapping by just appending -- and replacing the underscores
    args = {arg: "--{a}".format(a=arg.replace("_", "-")) for arg in args}
    # This step-cli argument uses camelCase for some reason
    args["reason_code"] = "--reasonCode"

    result = run_step_cli_command(
        module.params["step_cli_executable"], params,
        module, result, {**args, **connection_run_args}
    )
    result["changed"] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
