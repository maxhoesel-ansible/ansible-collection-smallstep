# pylint: disable=redefined-outer-name

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

LOCAL_CA_TAG = "local-ca"

INTEGRATION_CONFIG_DIR = Path("tests/integration/")
INTEGRATION_CONFIG_TEMPLATE_REMOTE = "integration_config_remote.yml.j2"
INTEGRATION_CONFIG_TEMPLATE_LOCAL = "integration_config_local.yml.j2"
INTEGRATION_CONFIG_FILE = "integration_config.yml"


def render_integration_config(template, dest: Path, **kwargs):
    env = Environment(loader=FileSystemLoader(INTEGRATION_CONFIG_DIR))
    template = env.get_template(template)
    content = template.render(**kwargs)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(f"{content}\n")


def test_plugins_integration_remote(collection_test_env, test_versions, remote_ca_container, ):
    render_integration_config(
        INTEGRATION_CONFIG_TEMPLATE_REMOTE,
        collection_test_env.cwd / "tests" / "integration" / INTEGRATION_CONFIG_FILE,
        step_ca_version=test_versions.step_ca_version,
        step_cli_version=test_versions.step_cli_version,
        step_remote_ca_url=remote_ca_container.ca_url,
        step_remote_ca_fingerprint=remote_ca_container.ca_fingerprint,
        step_remote_ca_provisioner_name=remote_ca_container.ca_provisioner_name,
        step_remote_ca_provisioner_password=remote_ca_container.ca_provisioner_password
    )

    collection_test_env.run([
        "ansible-test", "integration", "--color", "-v",
        "--controller", "docker:default",
        "--target", f"docker:default,python={test_versions.node_python_version}",
        "--docker-network", remote_ca_container.ct_network,
        "--skip-tags", LOCAL_CA_TAG
    ])


def test_plugins_integration_local(collection_test_env, test_versions, local_ca_image):
    render_integration_config(
        INTEGRATION_CONFIG_TEMPLATE_LOCAL,
        collection_test_env.cwd / "tests" / "integration" / INTEGRATION_CONFIG_FILE,
        step_ca_version=test_versions.step_ca_version,
        step_cli_version=test_versions.step_cli_version,
    )

    collection_test_env.run([
        "ansible-test", "integration", "--color", "-v",
        "--controller", "docker:default",
        "--target", f"docker:{local_ca_image.tags[0]},python={test_versions.node_python_version}",
        "--tags", LOCAL_CA_TAG
    ])


def test_plugins_sanity(collection_test_env, test_versions):
    collection_test_env.run([
        "ansible-test",
        "sanity", "--docker", "--color", "-v",
        "--python", test_versions.node_python_version,
        "--skip-test", "metaclass-boilerplate",
        "--skip-test", "future-import-boilerplate",
    ])
