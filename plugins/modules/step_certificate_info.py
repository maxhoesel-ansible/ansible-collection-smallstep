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
import json
from typing import cast, Dict, Any

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.cli_wrapper import StepCliExecutable, CliCommand
from ..module_utils.constants import DEFAULT_STEP_CLI_EXECUTABLE

FORMAT_CLIARGS = {
    "json": ["--format", "json"],
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


def verify(executable: StepCliExecutable, module: AnsibleModule, path: str) -> Dict[str, Any]:
    verify_cliarg_map = {
        "server_name": "--server-name",
        "roots": "--roots",
    }
    cmd = CliCommand(executable, ["certificate", "verify", path], verify_cliarg_map, fail_on_error=False)
    res = cmd.run(module)

    return {"valid": True} if res.rc == 0 else {
        "valid": False,
        "validity_fail_reason": res.stderr
    }


def inspect(executable: StepCliExecutable, module: AnsibleModule) -> Dict[str, Any]:
    module_params = cast(Dict, module.params)
    result = {}
    certificate_info_cliarg_map = {
        "bundle": "--bundle",
        "insecure": "--insecure",
        "server_name": "--server-name",
        "roots": "--roots",
    }
    cmd = CliCommand(executable, ["certificate", "inspect", module_params["path"]] +
                     FORMAT_CLIARGS[module_params["format"]], certificate_info_cliarg_map)

    # The docs say inspect outputs to stderr, but my shell says otherwise:
    # https://github.com/smallstep/cli/issues/1032
    res = cmd.run(module)
    if module_params["format"] == "json":
        data = json.loads(res.stdout)
    else:
        data = res.stdout

    result[RESULT_FORMAT_KEYNAME[module_params["format"]]] = data
    return result


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

    try:
        result.update(inspect(executable, module))
    except json.JSONDecodeError as e:
        module.fail_json(f"Unable to decode returned certificate information. Error: {e}")
    result.update(verify(executable, module, module_params["path"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
