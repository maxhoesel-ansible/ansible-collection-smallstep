# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type


def check_step_cli_install(module, cli_executable, result):
    rc, step_stdout, step_stderr = module.run_command(cli_executable)
    if rc != 0:
        result["msg"] = (
            "Could not find step-cli binary at '{cmd}' on remote host.".format(cmd=cli_executable)
        )
        result["stdout"] = step_stdout
        result["stderr"] = step_stderr
        module.fail_json(**result)
