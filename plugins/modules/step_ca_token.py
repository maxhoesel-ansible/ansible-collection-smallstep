#!/usr/bin/python

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: step_ca_token
author: Max Hösel (@maxhoesel)
short_description: Generate an OTT granting access to the CA
version_added: '0.3.0'
description: >
  Generate an OTT granting access to the CA. This module returns the token by default,
  but you can also save it on the remote host if you prefer.
notes:
  - Check mode is supported.
options:
  cert_not_after:
    description: >
      The time/duration when the certificate validity period ends. If a time is used it is expected to be in RFC 3339 format.
      If a duration is used, it is a sequence of decimal numbers, each with optional fraction and a unit suffix,
      such as "300ms", "-1.5h" or "2h45m". Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
  cert_not_before:
    description: >
      The time/duration when the certificate validity period starts. If a time is used it is expected to be in RFC 3339 format.
      If a duration is used, it is a sequence of decimal numbers, each with optional fraction and a unit suffix,
      such as "300ms", "-1.5h" or "2h45m". Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
  force:
    description: Force the overwrite of files without asking.
    type: bool
  host:
    description: Create a host certificate instead of a user certificate.
    type: bool
  k8ssa_token_path:
    description: Configure the file from which to read the kubernetes service account token.
    type: path
  key:
    description: The private key path used to sign the JWT. This is usually downloaded from the certificate authority.
    type: path
  kid:
    description: The provisioner kid to use.
    type: str
  name:
    aliases:
      - subject
    description: >
      The Common Name, DNS Name, or IP address that will be set by the certificate authority.
      When there are no additional Subject Alternative Names configured (via the I(san) parameter,
      the subject will be added as the only element of the 'sans' claim on the token.
    type: str
    required: yes
  not_after:
    description: >
      The time/duration when the certificate validity period ends. If a time is used it is expected to be in RFC 3339 format.
      If a duration is used, it is a sequence of decimal numbers, each with optional fraction and a unit suffix,
      such as "300ms", "-1.5h" or "2h45m". Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
  not_before:
    description: >
      The time/duration when the certificate validity period starts. If a time is used it is expected to be in RFC 3339 format.
      If a duration is used, it is a sequence of decimal numbers, each with optional fraction and a unit suffix,
      such as "300ms", "-1.5h" or "2h45m". Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
  output_file:
    description: The destination file of the generated one-time token. Conflicts with I(return_token)
    type: path
  principal:
    description: >
      Add the principals (user or host names) that the token is authorized to request.
      The signing request using this token won't be able to add extra names. Must be a list
    type: list
    elements: str
  provisioner:
    aliases:
      - issuer
    description: The provisioner name to use.
    type: str
  provisioner_password_file:
    description: The path to the file containing the password to decrypt the one-time token generating key.
    type: path
  return_token:
    description: >
      Return the OTT through the module return values.
      Depending on your security needs, you might want to use I(output_path) instead.
    type: bool
  revoke:
    description: Create a token for authorizing 'Revoke' requests. The audience will be invalid for any other API request.
    type: bool
  renew:
    description: Create a token for authorizing 'renew' requests. The audience will be invalid for any other API request.
    type: bool
  rekey:
    description: Create a token for authorizing 'rekey' requests. The audience will be invalid for any other API request.
    type: bool
  san:
    description: >
      Add dns/ip/email/uri Subject Alternative Name(s) (SANs) that should be authorized.
      A certificate signing request using this token must match the complete set of SANs in the token 1:1.
      Must be a list
    type: list
    elements: str
  ssh:
    description: Create a token for authorizing an SSH certificate signing request.
    type: bool
  sshpop_cert:
    description: Certificate (chain) in PEM format to store in the 'sshpop' header of a JWT.
    type: str
  sshpop_key:
    description: Private key path, used to sign a JWT, corresponding to the certificate that will be stored in the 'sshpop' header.
    type: path
  x5c_cert:
    description: Certificate (chain) in PEM format to store in the 'x5c' header of a JWT.
    type: str
  x5c_key:
    description: Private key path, used to sign a JWT, corresponding to the certificate that will be stored in the 'x5c' header.
    type: path

extends_documentation_fragment:
  - maxhoesel.smallstep.cli_executable
  - maxhoesel.smallstep.ca_connection
"""

EXAMPLES = r"""
- name: Generate a token on the CA, using the values from $STEPPATH
  maxhoesel.smallstep.step_ca_token:
    name: foo.bar
"""

RETURNS = r"""
token:
  description: The generated token.
  returned: When I(return_token) is set
  type: str
  no_log: yes
"""
from typing import cast, Dict

from ansible.module_utils.common.validation import check_required_one_of
from ansible.module_utils.common.validation import check_mutually_exclusive
from ansible.module_utils.basic import AnsibleModule

from ..module_utils.cli_wrapper import CLIWrapper
from ..module_utils.params.ca_connection import CaConnectionParams
from ..module_utils.constants import DEFAULT_STEP_CLI_EXECUTABLE


def run_module():
    argument_spec = dict(
        cert_not_after=dict(type="str"),
        cert_not_before=dict(type="str"),
        force=dict(type="bool"),
        host=dict(type="bool"),
        k8ssa_token_path=dict(type="path"),
        key=dict(type="path"),
        kid=dict(type="str"),
        name=dict(aliases=["subject"], type="str", required=True),
        not_after=dict(type="str"),
        not_before=dict(type="str"),
        output_file=dict(type="path"),
        principal=dict(type="list", elements="str"),
        provisioner=dict(type="str", aliases=["issuer"]),
        provisioner_password_file=dict(type="path", no_log=False),
        return_token=dict(type="bool"),
        revoke=dict(type="bool"),
        renew=dict(type="bool"),
        rekey=dict(type="bool"),
        san=dict(type="list", elements="str"),
        ssh=dict(type="bool"),
        sshpop_cert=dict(type="str"),
        sshpop_key=dict(type="path"),
        x5c_cert=dict(type="str"),
        x5c_key=dict(type="path"),
        step_cli_executable=dict(type="path", default=DEFAULT_STEP_CLI_EXECUTABLE)
    )

    result = dict(changed=False, stdout="", stderr="", msg="")
    module = AnsibleModule(argument_spec={
        **CaConnectionParams.argument_spec,
        **argument_spec
    }, supports_check_mode=True)
    CaConnectionParams(module).check()
    module_params = cast(Dict, module.params)

    try:
        check_mutually_exclusive(["return_token", "output_file"], module.params)
    except TypeError:
        result["msg"] = "return_token and output_file cannot be specified at the same time"
        module.fail_json(**result)
    try:
        check_required_one_of(["return_token", "output_file"], module.params)
    except TypeError:
        result["msg"] = "At least one of return_token and output_file must be specified"
        module.fail_json(**result)

    cli = CLIWrapper(module, module_params["step_cli_executable"])

    # Regular args
    token_cliargs = ["cert_not_after", "cert_not_before", "force", "host", "k8ssa_token_path", "key", "kid",
                     "not_after", "not_before", "output_file", "principal", "provisioner", "provisioner_password_file",
                     "revoke", "renew", "rekey", "san", "ssh", "sshpop_cert", "sshpop_key", "x5c_cert",
                     "x5c_key"]
    # All parameters can be converted to a mapping by just appending -- and replacing the underscores
    token_cliarg_map = {arg: f"--{arg.replace('_', '-')}" for arg in token_cliargs}

    # Positional Parameters
    cli_params = [
        "ca", "token", module_params["name"]
    ] + cli.build_params({
        **token_cliarg_map,
        **CaConnectionParams.cliarg_map
    })

    result["stdout"], result["stderr"] = cli.run_command(cli_params)[1:3]
    result["changed"] = True
    if module_params["return_token"]:
        result["token"] = result["stdout"]
    result["stdout"] = ""
    result["stdout_lines"] = ""
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
