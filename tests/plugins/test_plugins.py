# pylint: disable=redefined-outer-name

from tests.conftest import TestOptions


def test_plugins_sanity(collection_test_env, test_options: TestOptions):
    params = [
        "ansible-test",
        "sanity", "--docker", "--color", "-v",
        "--python", test_options.node_python_version,
    ]

    collection_test_env.run(params)
