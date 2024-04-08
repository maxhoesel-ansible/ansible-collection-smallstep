from abc import ABC, abstractmethod
from typing import Dict, Any

from ansible.module_utils.basic import AnsibleModule

from ..cli_wrapper import CliCommandArgs


class ParamsHelper(ABC):
    """A helper class that provides a set of module parameters and a method to validate them.
    """

    @abstractmethod
    def __init__(self, module: AnsibleModule) -> None:
        self.module = module

    @abstractmethod
    def check(self):
        """Validate the helpers arguments.
        If validation fails, the module exists with fail_json()

        Args:
            module (AnsibleModule): module to validate
        """

    @property
    @abstractmethod
    def argument_spec(self) -> Dict[str, Dict[str, Any]]:
        """Returns the helpers argument spec, as expected by AnsibleModule()
        """

    @classmethod
    @abstractmethod
    def cli_args(cls) -> CliCommandArgs:
        """Returns a CliCommandArgs object containing all the arguments needed for this parameter group
        """
