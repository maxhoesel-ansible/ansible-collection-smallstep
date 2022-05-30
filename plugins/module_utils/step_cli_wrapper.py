from .constants import COLLECTION_VERSION


class CLIWrapper():
    def __init__(self, module, result, executable):
        self.module = module
        self.exec = executable
        self.result = result

        rc, stdout, stderr = module.run_command([self.exec, "version"])
        if rc != 0:
            result["msg"] = f"Could not launch step-cli executable. Error: {stderr}"
            module.fail_json(**result)
        version = stdout.split(" ")[1].split("/")[1]
        self.check_cli_version(version)

    def run_command(self, command, param_spec=None, check_mode_safe=False, exit_on_error=True):
        """
        Run a step-cli command on the remote host. Supports check_mode.

        Command must be a list of subcommands, e.g. ["ca", "bootstrap"]

        Command parameters are automatically gathered from module args, using param_spec.
        param_spec must be a dict, mapping module arguments to their command-line parameters.

        Example:
        param_spec = {"module_args": "--cli-flag"}

        Parameters are handled according to their type in the argspec:
            - str/path/int/float/raw/bytes are passed as a value to their mapped parameter (e.g. --parameter=value)
            - bool only passes the mapped parameter (e.g. --force)
            - list causes the mapped parameter to be repeated for each value (e.g. --in=1 --in=2)

        If check_mode_safe is true, the command will always be run, even if the module is in --check mode.

        If exit_on_error is false, the module will not fail upon command failure.

        Returns a tuple of rc, stdout and stderr.
        """
        args = [self.exec]
        args.extend(command)
        if not param_spec:
            param_spec = []

        for param in param_spec:
            if self.module.params[param]:
                if self.module.argument_spec[param].get("type", "str") in [
                    "str", "int", "float", "path", "raw", "bytes"
                ]:
                    args.append(f"{param_spec[param]}={str(self.module.params[param])}")
                elif self.module.argument_spec[param].get("type", "str") == "bool":
                    args.append(param_spec[param])
                elif self.module.argument_spec[param].get("type", "str") == "list":
                    for item in self.module.params[param]:
                        args.append(f"{param_spec[param]}={str(item)}")

        if not self.module.check_mode or check_mode_safe:
            rc, stdout, stderr = self.module.run_command(args)
            if rc != 0 and exit_on_error:
                if ("error allocating terminal" in stderr or
                        "open /dev/tty: no such device or address" in stderr):
                    self.result["msg"] = (
                        "step-cli tried and failed to open a terminal for interactive input. "
                        "This usually means that you are missing a parameter that step-cli is now asking for, "
                        "such as a password file, provisioner, or confirmation to overwrite existing files. "
                        f"Failed command: \'{' '.join(args)}\'"
                    )
                else:
                    self.result["stdout"] = stdout
                    self.result["stderr"] = stderr
                    self.result["msg"] = f"Error running command \'{' '.join(args)}\'. See stderr for details."
                self.module.fail_json(**self.result)
            return rc, stdout, stderr
        return 0, "", ""

    def check_cli_version(self, cli_version):
        """
        Check whether the CLI version is supported by this collection version.
        Performs a basic version check, as packaging may not be available on target systems
        """
        warn_msg = (f"This version of step-cli ({cli_version}) is not "
                    f"supported by this collection version ({COLLECTION_VERSION})."
                    "See the collection documentation for which collection versions supports which step-cli version.")
        coll_segments = COLLECTION_VERSION.split(".")
        cli_segments = cli_version.split(".")

        if coll_segments[0] != cli_segments[0]:
            self.module.warn(warn_msg)
        elif coll_segments[0] == "0" and coll_segments[1] != cli_segments[1]:
            # Major version == 0 -> minor version changes count as breaking, no compat guaranteed (eg 0.20.0 != 0.21.0)
            self.module.warn(warn_msg)
