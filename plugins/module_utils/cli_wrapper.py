from typing import List, Tuple, Dict, cast

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.compat.version import LooseVersion

from .constants import COLLECTION_VERSION, COLLECTION_MIN_STEP_CLI_VERSION, COLLECTION_REPO


class CLIError(Exception):
    pass


class CLIWrapper():
    def __init__(self, module: AnsibleModule, executable: str) -> None:
        self.exec = executable
        self.module = module

        ret = self.run_command(["version"], check=False, check_mode_safe=True)
        if ret[0] != 0:
            self.module.fail_json(msg=f"Could not launch step-cli executable. Error: {ret[2]}")
        self.check_cli_version()

    def build_params(self, module_params_cliarg_map: Dict[str, str]) -> List[str]:
        """Construct step-cli command parameters from module params.
        Reads the modules parameters and transforms them to step-cli arguments
        based on the values in module_params_cliarg_map.

        module_params_cliarg_map is a dict with module params as keys and corresponding command-line flags as values.
        Module params are transformed according to their type:
          - str/path/int/float/raw/bytes are formatted and passed as-is
          - bools only pass the corresponding value (e.g. --force)
          - list causes the mapped parameter to be repeated for each value (e.g. --in=1 --in=2)


        Example:
            module_args = {
                normal_arg = "hello"
                some_flag = True
                a_list = [1,2]
            }
            module_params_cliarg_map = {
                "normal_arg": "--normal-param"
                "some_flag": "--some-flag"
                "a_list": "--listy"
            }
            Results in
            ["--normal-param", "hello", "--some-flag", "--listy", "1", "--listy", "2"]


        Returns:
            List[str]: Parameters to pass to run_command

        Raises:
            CLIError if a key in param_spec is not in the module argspec
        """
        args = []
        module_params = cast(Dict, self.module.params)
        for param_name in module_params_cliarg_map:
            param_type = self.module.argument_spec[param_name].get("type", "str")
            if param_name not in module_params:
                raise CLIError(f"Could not build command parameters: "
                               f"param '{param_name}' not in module argspec, this is most likely a bug")
            if param_type == "bool":
                if bool(module_params[param_name]) is False:
                    # some flags (such as --ssh in ca provisioner add/update are enabled by default),
                    # this allows the user to disable them if needed
                    args.append(f"{module_params_cliarg_map[param_name]}=false")
                else:
                    args.append(module_params_cliarg_map[param_name])
            elif not module_params[param_name]:
                # parameter is unset
                pass
            elif param_type == "list":
                for item in cast(List, module_params[param_name]):
                    args.extend([module_params_cliarg_map[param_name], str(item)])
            else:
                # all other types
                args.extend([module_params_cliarg_map[param_name], str(module_params[param_name])])
        return args

    def run_command(self, params: List[str], check_mode_safe=False, check=True) -> Tuple[int, str, str]:
        """Run a step-cli command.

        Args:
            args (List[str]): Arguments to pass to the step-cli invocation
            check_mode_safe (bool, optional): Set this to true if your command should be run even in check mode.
                Only set this to true if your command does not alter the system in a meaningful way. Defaults to False.
            check (bool, optional): If true, exit the module with fail_json and a msg if the command fails

        Returns:
            Tuple[int, str, str]: rc, stdout and stderr
        """
        args = [self.exec]
        args.extend(params)

        if self.module.check_mode and not check_mode_safe:
            return 0, "", ""

        rc, stdout, stderr = self.module.run_command(args)
        if rc != 0 and check:
            if ("error allocating terminal" in stderr or "open /dev/tty: no such device or address" in stderr):
                self.module.fail_json(
                    "Failed to run command: step-cli tried to open a terminal for interactive input. "
                    "This happens when step-cli prompts for additional parameters or asks for confirmation. "
                    "You may be missing a required parameter (such as 'force'). Check the module documentation. "
                    "If you are sure that you provided all required parameters, you may have encountered a bug. "
                    f"Please file an issue at {COLLECTION_REPO} if you think this is the case. "
                    f"Failed command: \'{' '.join(args)}\'"
                )
            else:
                self.module.fail_json(f"Error running command \'{' '.join(args)}\'. Error: {stderr}")
        return rc, stdout, stderr

    def check_cli_version(self):
        """Check whether the CLI version is supported by this collection version.
        Performs a basic version check, as packaging may not be available on target systems.
        """
        stdout = self.run_command(["version"], check_mode_safe=True)[1]
        cli_version = LooseVersion(stdout.split(" ")[1].split("/")[1])
        collection_min_version = LooseVersion(COLLECTION_MIN_STEP_CLI_VERSION)
        if cli_version < collection_min_version:
            self.module.warn(
                f"step-cli version {cli_version} is not supported by this collection version ({COLLECTION_VERSION}). "
                f"The minimum supported step-cli version is: {COLLECTION_MIN_STEP_CLI_VERSION}."
            )
