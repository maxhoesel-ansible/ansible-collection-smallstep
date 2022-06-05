#!/usr/bin/python

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: step_ca_renew
author: Max Hösel (@maxhoesel)
short_description: Renew a valid certificate
version_added: '0.3.0'
description: Renew a valid certificate
notes:
  - Check mode is supported.
options:
  crt_file:
    description: The certificate in PEM format that we want to renew.
    required: yes
    type: path
  expires_in:
    description: >
      The amount of time remaining before certificate expiration, at which point a renewal should be attempted.
      The certificate renewal will not be performed if the time to expiration is greater than the I(expires_in) value.
      A random jitter (duration/20) will be added to avoid multiple services hitting the renew endpoint at the same time.
      The duration is a sequence of decimal numbers, each with optional fraction and a unit suffix, such as "300ms", "-1.5h" or "2h45m".
      Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
  force:
    description: Force the overwrite of files without asking.
    type: bool
  exec:
    description: The command to run after the certificate has been renewed.
    type: str
  key_file:
    description: They key file of the certificate.
    required: yes
    type: path
  output_file:
    description: The new certificate file path. Defaults to overwriting the crt-file positional argument.
    type: path
  password_file:
    description: The path to the file containing the password to encrypt or decrypt the private key.
    type: path
  pid:
    description: >
      The process id to signal after the certificate has been renewed. By default the the SIGHUP (1) signal will be used,
      but this can be configured with the I(signal) parameter.
    type: int
  pid_file:
    description: >
      The path from which to read the process id that will be signaled after the certificate has been renewed.
      By default the the SIGHUP (1) signal will be used, but this can be configured with the I(signal) parameter.
    type: path
  signal:
    description: >
      The signal number to send to the selected PID, so it can reload the configuration and load the new certificate.
      Default value is SIGHUP (1).
    type: int

extends_documentation_fragment:
  - maxhoesel.smallstep.step_cli
  - maxhoesel.smallstep.connection
"""

EXAMPLES = r"""
# See https://smallstep.com/docs/step-cli/reference/ca/renew for more examples

- name: Renew a certificate
  maxhoesel.smallstep.step_ca_renew:
    crt_file: internal.crt
    key_file: internal.key
    ca_url: https://ca.smallstep.com:9000
    force: yes
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.step_cli_wrapper import CLIWrapper
from ..module_utils import connection


def run_module():
    module_args = dict(
        crt_file=dict(type="path", required=True),
        expires_in=dict(type="str"),
        force=dict(type="bool"),
        exec=dict(type="str"),
        key_file=dict(type="path", required=True),
        output_file=dict(type="path"),
        password_file=dict(type="path", no_log=False),
        pid=dict(type="int"),
        pid_file=dict(type="path"),
        signal=dict(type="int"),
        step_cli_executable=dict(type="path", default="step-cli"),
    )
    result = dict(changed=False, stdout="", stderr="", msg="")
    module = AnsibleModule(argument_spec={**connection.args, **module_args}, supports_check_mode=True)

    connection.check_argspec(module, result)

    cli = CLIWrapper(module, result, module.params["step_cli_executable"])

    # Positional Parameters
    params = ["ca", "renew", module.params["crt_file"],
              module.params["key_file"]]
    # Regular args
    args = ["expires_in", "force", "exec", "output_file", "password_file", "pid", "pid_file",
            "signal"]
    # All parameters can be converted to a mapping by just appending -- and replacing the underscores
    param_spec = {arg: f"--{arg.replace('_', '-')}" for arg in args}

    result["stdout"], result["stderr"] = cli.run_command(params, {**param_spec, **connection.param_spec})[1:3]
    if "Your certificate has been saved in" in result["stderr"]:
        result["changed"] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
