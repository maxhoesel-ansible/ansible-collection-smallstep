# Copyright: (c) 2023, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Dict, Any

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common import validation

from .params_helper import ParamsHelper


class AdminParams(ParamsHelper):

    argument_spec: Dict[str, Dict[str, Any]] = dict(
        admin_cert=dict(type="path"),
        admin_key=dict(type="path"),
        admin_provisioner=dict(type="str", aliases=["admin_issuer"]),
        admin_subject=dict(type="str", aliases=["admin_name"]),
        admin_password_file=dict(type="path", no_log=False)
    )
    cliarg_map: Dict[str, str] = {key: f"--{key.replace('_', '-')}" for key in argument_spec}

    # pylint: disable=useless-parent-delegation
    def __init__(self, module: AnsibleModule) -> None:
        super().__init__(module)

    def check(self):
        try:
            validation.check_required_together(["admin_cert", "admin_key"], self.module.params)
        except ValueError:
            self.module.fail_json(msg="admin_cert and admin_key must be specified together")

    def is_defined(self):
        return bool(self.module.params["admin_cert"])  # type: ignore
