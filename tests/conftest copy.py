from dataclasses import dataclass
import importlib
import importlib.metadata
import os
from pathlib import Path
import subprocess
import sys

from packaging import version
import pytest
import yaml

NODE_PYTHON_DEFAULT_VERSION = "3.8"
STEP_CLI_DEFAULT_VERSION = "latest"
STEP_CA_DEFAULT_VERSION = "latest"

with open("galaxy.yml", encoding="utf-8") as f:
    GALAXY_YML = yaml.safe_load(f)


@dataclass
class TestVersions:
    step_cli_version: str
    step_ca_version: str
    node_python_version: str
    ansible_version: str


class CollectionTestEnv():
    # pylint: disable=redefined-outer-name
    def __init__(self, request, test_versions: TestVersions, tmp_path_factory: pytest.TempPathFactory) -> None:
        # Sanity check against modifying user/system packages.
        # We need to manually pip-install a version of ansible-core to test with, lets make sure
        # we don't hose the users personal install.
        in_venv = sys.prefix != sys.base_prefix
        if not in_venv and not request.config.getoption("--ci"):
            raise ValueError("Aborting ansible-core install for tests because we are not inside a virtualenv. "
                             "Please use ./scripts/setup.sh to setup a virtualenv, then activate it.")
        # install the specified version of ansible-core into our venv
        subprocess.run(["pip", "install", f"ansible-core~={test_versions.ansible_version}.0"], check=True)

        # Build collection into isolated install path
        build_path: Path = tmp_path_factory.mktemp("build")
        collection_tar = build_path / f"{GALAXY_YML['namespace']}-{GALAXY_YML['name']}-{GALAXY_YML['version']}.tar.gz"
        subprocess.run(
            ["ansible-galaxy", "collection", "build", "--output-path", build_path],
            check=True
        )

        # Now install the collection into our temporary structure
        self._collections_path = tmp_path_factory.mktemp("collections")
        self._env = {
            "ANSIBLE_COLLECTIONS_PATH": self._collections_path,
            "STEP_CLI_VERSION": test_versions.step_cli_version,
            "STEP_CA_VERSION": test_versions.step_ca_version,
        }
        subprocess.run(
            ["ansible-galaxy", "collection", "install", "-p", self._collections_path, collection_tar],
            check=True, env={**os.environ.copy(), **self._env}
        )

        # in case subprocesses need to override the directory, such as for molecule tests
        self.cwd: Path = (self._collections_path / "ansible_collections" /
                          GALAXY_YML["namespace"] / GALAXY_YML["name"]).resolve()

    def run(self, *args, **kwargs):
        # merge env
        if "env" in kwargs:
            kwargs["env"] = {**kwargs["env"], **self._env}
        else:
            kwargs["env"] = {**os.environ.copy(), **self._env}

        if "cwd" not in kwargs:
            kwargs["cwd"] = self.cwd  # let subclasses overwrite the path, they can get it from self.cwd
        if "check" not in kwargs:
            kwargs["check"] = True  # check by default
        # pylint: disable=subprocess-run-check
        subprocess.run(*args, **kwargs)


@pytest.fixture()
# pylint: disable=redefined-outer-name
def collection_test_env(request, test_versions, tmp_path_factory) -> CollectionTestEnv:
    return CollectionTestEnv(request, test_versions, tmp_path_factory)


@pytest.fixture(scope="session")
def test_versions(request) -> TestVersions:
    return TestVersions(
        request.config.getoption("--step-cli-version"),
        request.config.getoption("--step-ca-version"),
        request.config.getoption("--node-python-version"),
        request.config.getoption("--ansible-version")
    )


def get_ansible_version():
    base_version = version.parse(importlib.metadata.version("ansible-core"))
    return f"{base_version.major}.{base_version.minor}"


def pytest_addoption(parser):
    parser.addoption("--ci", action="store_true", default=False,
                     help="Allow unsafe actions such as installing ansible-core directly in CI environments")
    parser.addoption("--ansible-version", action="store", default=get_ansible_version(),
                     help="Version of ansible to use for tests, in format 'x.yy', such as '2.15'."
                     "Default: no constraint (latest/installed)")
    parser.addoption("--step-cli-version", action="store", default=STEP_CLI_DEFAULT_VERSION,
                     help="Version of step-cli to use for tests, "
                     f"either '{STEP_CLI_DEFAULT_VERSION}' (default) or a version ('0.24.0')")
    parser.addoption("--step-ca-version", action="store", default=STEP_CA_DEFAULT_VERSION,
                     help="Version of step-ca to use for tests, "
                     f"either '{STEP_CA_DEFAULT_VERSION}' (default) or a version ('0.24.0')")
    parser.addoption("--node-python-version", action="store", default=NODE_PYTHON_DEFAULT_VERSION,
                     help="Python version to test Ansible modules with, "
                     f"in the format '3.x'. Default: '{NODE_PYTHON_DEFAULT_VERSION}'")
