# pylint: disable=redefined-outer-name

def test_plugins_sanity(collection_test_env, test_versions):
    params = [
        "ansible-test",
        "sanity", "--docker", "--color", "-v",
        "--python", test_versions.node_python_version,
    ]

    if int(test_versions.ansible_version.split(".")[1]) <= 16:
        # these flags are only valid with ansible-test 2.16 and older, as they refer to python 2.7.
        # Do not include them with newer versions of ansible-test
        params.extend([
            "--skip-test", "metaclass-boilerplate",
            "--skip-test", "future-import-boilerplate"
        ])

    collection_test_env.run(params)
