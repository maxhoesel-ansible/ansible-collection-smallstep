# Copyright: (c) 2023, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Dict, Any

from ansible.module_utils.basic import AnsibleModule

from ..cli_wrapper import CliCommandArgs
from .params_helper import ParamsHelper


class CaConnectionParams(ParamsHelper):

    argument_spec: Dict[str, Dict[str, Any]] = dict(
        ca_url=dict(type="str"),
        root=dict(type="path"),
        ca_config=dict(type="path"),
        offline=dict(type="bool"),
    )

    @classmethod
    def cli_args(cls) -> CliCommandArgs:
        return CliCommandArgs([], {key: f"--{key.replace('_', '-')}" for key in cls.argument_spec})

    # pylint: disable=useless-parent-delegation
    def __init__(self, module: AnsibleModule) -> None:
        super().__init__(module)

    def check(self):
        if (
            (self.module.params["offline"]) and  # type: ignore
            (self.module.params["ca_url"] or self.module.params["root"])  # type: ignore
        ):
            self.module.fail_json(msg="ca_config/offline and root/ca_url are mutually exclusive")

    def is_local(self):
        return True if self.module.params["offline"] or self.module.params["ca_config"] else False  # type: ignore

    def is_remote(self):
        return not self.is_local()
