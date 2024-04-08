#!/usr/bin/python

# Copyright: (c) 2023, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: step_certificate_info
author: Max Hösel (@maxhoesel)
short_description: Retrieve certificate details and validation status
version_added: '1.0.0'
description: >
    This module runs C(step certificate inspect) on the specified file and returns its JSON/PEM-formatted output.
    If the certificate file contains multiple certificates (i.e., it is a certificate "bundle") the first certificate
    in the bundle will be output. Pass the bundle option to return all certificates in the order in which
    they appear in the bundle.
    Additionally, this module also returns the validation status of the certificate (see return values),
    as determined by C(step certificate verify)
notes:
  - Check mode is supported.
options:
  path:
    description: Path to a certificate or certificate signing request (CSR) to inspect
    type: path
    aliases:
      - crt_file
    required: true
  format:
    description: What format to return. Determines which of the return values will be populated.
    type: str
    choices:
      - json
      - text
      - text-short
      - pem
    default: json
  roots:
    description: >
        Root certificate(s) that will be used to verify the authenticity of the remote server.
        Case-sensitive string, may be one of:
        Relative or full path to a file - All certificates in the file will be used for path validation.
        Comma-separated list of relative or full file paths - Every PEM encoded certificate from each file will be used for path validation.
        Relative or full path to a directory - Every PEM encoded certificate from each file in the directory will be used for path validation.
    type: str
  server_name:
    description: TLS Server Name Indication that should be sent to request a specific certificate from the server.
    type: str
    aliases:
        - servername
  bundle:
    description: >
        Print all certificates in the order in which they appear in the bundle.
        If the output format is 'json' then output a list of certificates,
        even if the bundle only contains one certificate.
        This flag will result in an error if the input bundle includes any PEM that does not have type CERTIFICATE.
    type: bool
    default: false
  insecure:
    description: >
        Use an insecure client to retrieve a remote peer certificate.
        Useful for debugging invalid certificates remotely.
    type: bool
    default: false

extends_documentation_fragment:
  - maxhoesel.smallstep.cli_executable
"""

EXAMPLES = r"""
# See https://smallstep.com/docs/step-cli/reference/certificate/inspect for more examples

- name: Inspect a local certificate bundle
  maxhoesel.smallstep.step_certificate_info:
    path: /path/to/certificate.crt
    bundle: true
"""

RETURN = r"""
json:
  description: The certificate data returned by step-cli, as a JSON data structure.
  type: raw
  returned: When I(format=json)
pem:
  description: The certificate data returned by step-cli, in PEM format
  type: str
  returned: When I(format=pem)
text:
  description: The certificate data returned by step-cli, in text format
  type: str
  returned: When I(format=text) or I(format=text-short)
valid:
  description: Whether the certificate passed verification by C(step certificate verify)
  type: bool
  returned: always
validity_fail_reason:
  description: Reason for failed certificate validity check, as output by step-cli.
  type: str
  returned: When I(valid=false)
"""
from typing import cast, Dict, Any

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.cli_wrapper import CliCommandArgs, StepCliExecutable, CliCommand
from ..module_utils import helpers
from ..module_utils.constants import DEFAULT_STEP_CLI_EXECUTABLE

FORMAT_CLIARGS = {
    "pem": ["--format", "pem"],
    "text": ["--format", "text"],
    "text-short": ["--format", "text", "--short"],
}
RESULT_FORMAT_KEYNAME = {
    "json": "json",
    "pem": "pem",
    "text": "text",
    "text-short": "text",
}


def inspect_non_json(executable: StepCliExecutable, module: AnsibleModule) -> str:
    """Run step-cli certificate inspect and return data for a non-json format

    Args:
        executable (StepCliExecutable): Executable to run with
        module (AnsibleModule): ansible module

    Returns:
        str: stdout data from step-cli certificate inspect
    """
    module_params = cast(Dict, module.params)
    certificate_info_cliarg_map = {
        "bundle": "--bundle",
        "insecure": "--insecure",
        "server_name": "--server-name",
        "roots": "--roots",
    }
    args = CliCommandArgs(["certificate", "inspect", module_params["path"]] +
                          FORMAT_CLIARGS[module_params["format"]], certificate_info_cliarg_map)
    cmd = CliCommand(executable, args)

    # The docs say inspect outputs to stderr, but my shell says otherwise:
    # https://github.com/smallstep/cli/issues/1032
    res = cmd.run(module)
    return res.stdout


def main():
    argument_spec = dict(
        path=dict(type="path", aliases=["crt_file"], required=True),
        format=dict(type="str", choices=["json", "text", "text-short", "pem"], default="json"),
        server_name=dict(type="str", aliases=["servername"]),
        roots=dict(type="str"),
        bundle=dict(type="bool", default=False),
        insecure=dict(type="bool", default=False),
        step_cli_executable=dict(type="path", default=DEFAULT_STEP_CLI_EXECUTABLE)
    )
    result: Dict[str, Any] = dict(changed=False)
    module = AnsibleModule(argument_spec={
        **argument_spec
    }, supports_check_mode=True)
    module_params = cast(Dict, module.params)

    executable = StepCliExecutable(module, module_params["step_cli_executable"])

    cert_info = helpers.get_certificate_info(executable, module, module_params["path"],
                                             bundle=module_params["bundle"],
                                             insecure=module_params["insecure"],
                                             server_name=module_params["server_name"],
                                             roots=module_params["roots"])
    data = cert_info.data if module_params["format"] == "json" else inspect_non_json(executable, module)
    result.update({
        "valid": cert_info.valid,
        "validity_fail_reason": cert_info.invalid_reason,
        RESULT_FORMAT_KEYNAME[module_params["format"]]: data
    })

    module.exit_json(**result)


if __name__ == "__main__":
    main()
