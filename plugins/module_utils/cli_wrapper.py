from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import tempfile
from typing import List, Dict, cast

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.compat.version import LooseVersion

from .constants import COLLECTION_VERSION, COLLECTION_MIN_STEP_CLI_VERSION, COLLECTION_REPO


class CliError(Exception):
    pass


class StepCliExecutable:
    """Represents the presence of a step-cli executable with a given version on the system
    """

    def __init__(self, module: AnsibleModule, executable: str = "step-cli") -> None:
        self._exec = executable

        rc, stdout, stderr = module.run_command([executable, "version"])
        if rc != 0:
            module.fail_json(msg=f"Could not launch step-cli executable. Error: {stderr}")

        # Check whether the CLI version is supported by this collection version.
        # Performs a basic version check, as packaging may not be available on target systems.
        cli_version = LooseVersion(stdout.split(" ")[1].split("/")[1])
        collection_min_version = LooseVersion(COLLECTION_MIN_STEP_CLI_VERSION)
        if cli_version < collection_min_version:
            module.warn(
                f"step-cli version {cli_version} is not supported by this collection version ({COLLECTION_VERSION}). "
                f"The minimum supported step-cli version is: {COLLECTION_MIN_STEP_CLI_VERSION}."
            )

    @property
    def path(self) -> str:
        return self._exec


@dataclass
class CliCommandResult:
    """The result of a CliCommand run() command
    """
    rc: int
    stdout: str
    stderr: str


@dataclass
class CliCommandArgs:
    """Arguments to be passed to the command.

    args is a plain list of arguments to be passed in
    module_param_args is a str-str dict that maps module params to command-line args.
        For example, {"provisioner": "--provisioner"} will cause the module param "provisioner" to be passed in
        as the value to the "--provisioner" argument. Values are transformed according to their type:
            - bools only pass the corresponding flag (e.g. --force)
            - list causes the mapped arg to be repeated for each value (e.g. --in=1 --in=2)
            - all other types are formatted and passed as-is
    module_tmpfile_args is the same as module_param_args, except that the value is written to a temporary file
        at runtime and the path to that file is passed instead. This is primarily intended for password files.
    """
    args: List[str]
    module_param_args: Dict[str, str] = field(default_factory=dict)
    module_tmpfile_args: Dict[str, str] = field(default_factory=dict)

    def join(self, other: CliCommandArgs) -> CliCommandArgs:
        """Joins this Args object with another one and produces a new object containing values from both.
        `args` are appended while the module_x_args values are merged. The other object takes precedence.

        Args:
            other (Self): The other object to merge with

        Returns:
            Self: New Args object
        """
        return CliCommandArgs(self.args + other.args,
                              {**self.module_param_args, **other.module_param_args},
                              {**self.module_tmpfile_args, **other.module_tmpfile_args}
                              )

    def build(self, module: AnsibleModule, tmpdir: Path) -> List[str]:
        args = self.args
        module_params = cast(Dict, module.params)

        # Create temporary files for any parameters that need to point to files, such as password-file
        # Since these files may contain sensitive data, we first create the fd with locked-down permissions,
        # then write the actual content
        for module_arg in [arg for arg in self.module_tmpfile_args if module_params[arg]]:
            path = tmpdir / module_arg
            path.touch(0o700, exist_ok=False)
            with open(path, "w", encoding="utf-8") as f:
                f.write(module_params[module_arg])
            args.extend([self.module_tmpfile_args[module_arg], path.as_posix()])

        # transform the values in module_params into valid step-coi arguments using module_args_params mapping
        for param_name in [arg for arg in self.module_param_args if module_params[arg]]:
            if param_name not in module_params:
                raise CliError(f"Could not build command parameters: "
                               f"param '{param_name}' not in module argspec, this is most likely a bug")

            param_type = module.argument_spec[param_name].get("type", "str")
            if param_type == "bool" and bool(module_params[param_name]):
                args.append(self.module_param_args[param_name])
            elif param_type == "list":
                for item in cast(List, module_params[param_name]):
                    args.extend([self.module_param_args[param_name], str(item)])
            else:
                # all other types
                args.extend([self.module_param_args[param_name], str(module_params[param_name])])
        return args


@dataclass
class CliCommand:
    """CliCommand represents a single command to be run by step-cli

    Args:
        executable(StepCliExecutable): The executable to run the command with
        argspec (CliCommandArgs): Arguments to be passed to the executable
        run_in_check_mode (bool): Whether to run this command even if Ansibles check_mode is enabled.
                                  If false and check_mode is enabled, the invocation will exit with rc=0 and no output.
                                  Only set this on invocations that don't change the system state! Default is false
        fail_on_error(bool): Whether to run module_fail if this invocation fails. Default is true
    """
    executable: StepCliExecutable
    args: CliCommandArgs
    run_in_check_mode: bool = False
    fail_on_error: bool = True

    def run(self, module: AnsibleModule) -> CliCommandResult:
        """Execute the command with the given step-cli executable and Ansible module

        Args:
            module (AnsibleModule): The Ansible module

        Returns:
            CliCommandResult: Result of the command.

        Raises:
            CliError if the module args don't match with the provided params
        """
        # use a context manager to ensure that our sensitive temporary files are *always* deleted
        with tempfile.TemporaryDirectory("-ansible-smallstep") as tmpdir:
            cmd = [self.executable.path] + self.args.build(module, Path(tmpdir))

            if module.check_mode and not self.run_in_check_mode:
                return CliCommandResult(0, "", "")

            rc, stdout, stderr = module.run_command(cmd)
            if rc != 0 and self.fail_on_error:
                if ("error allocating terminal" in stderr or "open /dev/tty: no such device or address" in stderr):
                    module.fail_json(
                        "Failed to run command: step-cli tried to open a terminal for interactive input. "
                        "This happens when step-cli prompts for additional parameters or asks for confirmation. "
                        "You may be missing a required parameter (such as 'force'). Check the module documentation. "
                        "If you are sure that you provided all required parameters, you may have encountered a bug. "
                        f"Please file an issue at {COLLECTION_REPO} if you think this is the case. "
                        f"Failed command: \'{' '.join(cmd)}\'"
                    )
                else:
                    module.fail_json(f"Error running command \'{' '.join(cmd)}\'. Error: {stderr}")
            return CliCommandResult(rc, stdout, stderr)
