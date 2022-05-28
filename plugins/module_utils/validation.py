# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


def check_step_cli_install(module, cli_executable, result):
    rc, step_stdout, step_stderr = module.run_command(cli_executable)
    if rc != 0:
        result["msg"] = (
            f"Could not find step-cli binary at '{cli_executable}' on remote host."
        )
        result["stdout"] = step_stdout
        result["stderr"] = step_stderr
        module.fail_json(**result)
