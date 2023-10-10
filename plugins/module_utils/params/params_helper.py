from abc import ABC, abstractmethod
from typing import Dict, Any

from ansible.module_utils.basic import AnsibleModule


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

    @property
    @abstractmethod
    def cliarg_map(self) -> Dict[str, str]:
        """Returns a map of params with their corresponding cli parameter, for use in CliWrapper
        """
