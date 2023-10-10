import os
from pathlib import Path
from typing import Optional

import pytest

from tests.conftest import TestEnv

MOLECULE_REQUIREMENTS_PIP = Path("tests/roles/requirements.txt").resolve()
MOLECULE_REQUIREMENTS_ANSIBLE = Path("tests/roles/requirements.yml").resolve()


class MoleculeTestEnv(TestEnv):
    # pylint: disable=redefined-outer-name
    def __init__(self, virtualenv, test_versions, collection_path) -> None:
        self.env = {**os.environ.copy(), **{
            "ANSIBLE_COLLECTIONS_PATH": collection_path,
            "STEP_CLI_VERSION": test_versions.step_cli_version,
            "STEP_CA_VERSION": test_versions.step_ca_version,
        }}
        super().__init__(virtualenv)

        self.run(["pip", "install", test_versions.ansible_version_pip])
        self.run(["pip", "install", "-r", MOLECULE_REQUIREMENTS_PIP])
        self.run(["ansible-galaxy", "collection", "install", "-r", MOLECULE_REQUIREMENTS_ANSIBLE])

    def run(self, *args, **kwargs):
        kwargs["env"] = self.env
        return super().run(*args, **kwargs)


MOLECULE_ENV: Optional[MoleculeTestEnv] = None


@pytest.fixture()
# This fixture should be session-scoped, but cannot be since it requires the function-scoped virtualenv fixture.
# Use memoization for now.
# pylint: disable=redefined-outer-name
def molecule_env(virtualenv, test_versions, collection_path) -> MoleculeTestEnv:
    global MOLECULE_ENV  # pylint: disable=global-statement
    if MOLECULE_ENV is not None:
        return MOLECULE_ENV

    MOLECULE_ENV = MoleculeTestEnv(virtualenv, test_versions, collection_path)
    return MOLECULE_ENV
