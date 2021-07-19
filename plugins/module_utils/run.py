# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type


def run_step_cli_command(cli_executable, cli_command, module, result, params=None):
    """Run a step-cli command on the remote host. Supports check_mode
    Parameters:
        - cli_executable: Name or path to the step-cli executable
        - cli_command: The command to run (e.g. ["ca", "bootstrap"])
        - module: Current module object
        - result: dict containing result values to be passed to exit_json()
        - params: Dictionary of module parameters mapped to their command-line arg equivalent. Each parameter
          is processed according to its type in the argspec:
            - str/path/int/float/raw/bytes are passed as a value to their mapped parameter (e.g. --parameter=value)
            - bool only passes the mapped parameter (e.g. --force)
            - list causes the mapped parameter to be repeated for each value (e.g. --in=1 --in=2)
          The values for each parameter are read from module.params

    Example for params: {
        "module_arg_1": "--cli-arg",
        "module_arg_2": "--different-arg"
    }
    """
    args = [cli_executable]
    args.extend(cli_command)
    if not params:
        params = []

    for param in params:
        if module.params[param]:
            if module.argument_spec[param].get("type", "str") in ["str", "int", "float", "path", "raw", "bytes"]:
                args.append("{param}={val}".format(param=params[param], val=str(module.params[param])))
            elif module.argument_spec[param].get("type", "str") == "bool":
                args.append(params[param])
            elif module.argument_spec[param].get("type", "str") == "list":
                for item in module.params[param]:
                    args.append("{param}={val}".format(param=params[param], val=str(item)))

    if not module.check_mode:
        rc, result["stdout"], result["stderr"] = module.run_command(args)
        if rc != 0:
            if ("error allocating terminal" in result["stderr"] or "open /dev/tty: no such device or address" in result["stderr"]):
                result["msg"] = (
                    "step-cli tried and failed to open a terminal for interactive input. "
                    "This usually means that you're missing a parameter that step-cli is now asking for, "
                    "such as a password file, provisioner, or confirmation to overwrite existing files. "
                    "Failed command: '{cmd}'".format(cmd=" ".join(args))
                )
            else:
                result["msg"] = "Error running command '{cmd}'".format(cmd=" ".join(args))
            module.fail_json(**result)
    return result
