# Copyright: (c) 2023, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Dict, Any

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common import validation

from ..cli_wrapper import CliCommandArgs
from .params_helper import ParamsHelper


class AdminParams(ParamsHelper):

    argument_spec: Dict[str, Dict[str, Any]] = dict(
        admin_cert=dict(type="path"),
        admin_key=dict(type="path"),
        admin_provisioner=dict(type="str", aliases=["admin_issuer"]),
        admin_subject=dict(type="str", aliases=["admin_name"]),
        admin_password=dict(type="str", no_log=True),
        admin_password_file=dict(type="path", no_log=False)
    )

    @classmethod
    def cli_args(cls) -> CliCommandArgs:
        return CliCommandArgs([], {
            "admin_cert": "--admin-cert",
            "admin_key": "--admin-key",
            "admin_provisioner": "--admin-provisioner",
            "admin_subject": "--admin-subject",
            "admin_password_file": "--admin-password-file",
        }, {
            "admin_password": "--admin-password-file"
        })

    # pylint: disable=useless-parent-delegation
    def __init__(self, module: AnsibleModule) -> None:
        super().__init__(module)

    def check(self):
        validation.check_required_together(["admin_cert", "admin_key"], self.module.params)
        validation.check_mutually_exclusive(["admin_password", "admin_password_file"], self.module.params)

    def is_defined(self):
        return bool(self.module.params["admin_cert"])  # type: ignore
