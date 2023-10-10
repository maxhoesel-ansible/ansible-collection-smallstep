# pylint: disable=redefined-outer-name
from dataclasses import dataclass
from pathlib import Path
import random
import string
from typing import cast, Generator, Optional

import docker
from docker.models.containers import Container
from docker.models.images import Image
from docker.models.networks import Network
from docker.errors import NotFound
import pytest

from tests.conftest import TestEnv, GALAXY_YML

REMOTE_CA_NETWORK = "ansible-collection-smallstep-test-remote-ca"
REMOTE_CA_CONTAINER_NAME = "ansible-collection-smallstep-test-remote-ca"
REMOTE_CA_HOSTNAME = "ca"
REMOTE_CA_PROVISIONER_NAME = "ansible"
REMOTE_CA_PROVISIONER_PASSWORD = "secret-secret-secret"

LOCAL_CA_DOCKERFILE_DIR = Path("tests/integration/docker/local-ca").resolve()
LOCAL_CA_TAG = "ansible-collection-smallstep-local-ca"


class AnsibleTestEnv(TestEnv):
    # pylint: disable=redefined-outer-name
    def __init__(self, virtualenv, collection_path, test_versions) -> None:
        self.cwd = collection_path / "ansible_collections" / GALAXY_YML["namespace"] / GALAXY_YML["name"]
        super().__init__(virtualenv)

        self.run(["pip", "install", test_versions.ansible_version_pip])

    def run(self, *args, **kwargs):
        kwargs["cwd"] = self.cwd
        return super().run(*args, **kwargs)


ANSIBLE_TEST_ENV: Optional[AnsibleTestEnv] = None


@pytest.fixture()
# This fixture should be session-scoped, but cannot be since it requires the function-scoped virtualenv fixture
# Use memoization for now.
# pylint: disable=redefined-outer-name
def ansible_test_env(virtualenv, collection_path, test_versions) -> AnsibleTestEnv:
    global ANSIBLE_TEST_ENV  # pylint: disable=global-statement
    if ANSIBLE_TEST_ENV is not None:
        return ANSIBLE_TEST_ENV

    ANSIBLE_TEST_ENV = AnsibleTestEnv(virtualenv, collection_path, test_versions)
    return ANSIBLE_TEST_ENV


@pytest.fixture(scope="session")
def remote_ca_network() -> Generator[Network, None, None]:
    client = docker.from_env()
    try:
        net = client.networks.get(REMOTE_CA_NETWORK)
    except NotFound:
        net = client.networks.create(REMOTE_CA_NETWORK)
    net = cast(Network, net)
    yield net

    net.remove()


@dataclass
class RemoteCaContainerConfig:
    ct: Container
    ct_hostname: str
    ct_network: str
    ca_url: str
    ca_fingerprint: str
    ca_provisioner_name: str
    ca_provisioner_password: str


@pytest.fixture(scope="session")
def remote_ca_container(remote_ca_network, test_versions) -> Generator[RemoteCaContainerConfig, None, None]:
    client = docker.from_env()
    try:
        # cleanup old container to ensure REMOTE_CA_HOSTNAME points to the right container
        ct = cast(Container, client.containers.get(REMOTE_CA_CONTAINER_NAME))
        ct.remove(force=True)
    except NotFound:
        pass

    ct = cast(Container, client.containers.run(
        f"docker.io/smallstep/step-ca:{test_versions.step_ca_version}", detach=True, remove=True,
        name=REMOTE_CA_CONTAINER_NAME, hostname=REMOTE_CA_HOSTNAME,
        network=remote_ca_network.name,
        environment={
            "DOCKER_STEPCA_INIT_NAME": "smallstep-test-remote",
            "DOCKER_STEPCA_INIT_DNS_NAMES": f"localhost,{REMOTE_CA_HOSTNAME}",
            "DOCKER_STEPCA_INIT_PROVISIONER_NAME": REMOTE_CA_PROVISIONER_NAME,
            "DOCKER_STEPCA_INIT_PASSWORD": REMOTE_CA_PROVISIONER_PASSWORD
        },
    ))
    # Wait for the CA to come online
    rc = ct.exec_run("bash -c 'for i in {1..10}; do step ca health && exit 0 || sleep 1; done && exit 1'")[0]
    assert rc == 0
    # Read the CA fingerprint, tty required due to this: https://github.com/docker/docker-py/issues/2044
    rc, _fp = ct.exec_run("step certificate fingerprint certs/root_ca.crt", stdout=True, stderr=False, tty=True)
    assert rc == 0
    fingerprint = bytes(_fp).decode().strip()  # type: ignore

    yield RemoteCaContainerConfig(
        ct, ct_hostname=REMOTE_CA_HOSTNAME, ct_network=REMOTE_CA_NETWORK,
        ca_url=f"https://{REMOTE_CA_HOSTNAME}:9000", ca_fingerprint=fingerprint,
        ca_provisioner_name=REMOTE_CA_PROVISIONER_NAME, ca_provisioner_password=REMOTE_CA_PROVISIONER_PASSWORD
    )

    ct.remove(force=True)


@pytest.fixture(scope="session")
def local_ca_image(test_versions) -> Generator[Image, None, None]:
    image_suffix = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
    client = docker.from_env()

    img = client.images.build(
        path=LOCAL_CA_DOCKERFILE_DIR.as_posix(),
        tag=f"{LOCAL_CA_TAG}-{image_suffix}:latest",
        buildargs={
            "STEP_CA_VERSION": test_versions.step_ca_version,
            "ANSIBLE_VERSION": test_versions.ansible_version
        })[0]  # type: ignore
    img = cast(Image, img)

    yield img

    img.remove(force=True)
