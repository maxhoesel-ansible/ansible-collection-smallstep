from pathlib import Path

import pytest

from tests.conftest import TestOptions

# List of molecule scenario directories
MOLECULE_SCENARIOS = [
    subdir
    for role in Path("./roles").iterdir()
    for subdir in Path(role, 'molecule').glob('*')
    if subdir.is_dir() and (subdir / "molecule.yml").exists()
]


def scenario_id(path: Path) -> str:
    return f"{path.parent.parent.name}-{path.name}"


@pytest.mark.parametrize("scenario", MOLECULE_SCENARIOS, ids=scenario_id)
def test_scenario(scenario: Path, collection_test_env, test_options: TestOptions) -> None:
    role_dir = collection_test_env.cwd / scenario.parent.parent
    molecule_args = ["molecule", "test", "-s", scenario.name]
    if test_options.molecule_skip_destroy:
        molecule_args.extend(["--destroy", "never"])

    # Apparently molecule needs this to pick up on project-level config files in .config/molecule 🤷
    # https://github.com/ansible/molecule/blob/e6d63adea6be74a8548dab30ba00bf8474d6c088/src/molecule/util.py#L339
    collection_test_env.run(["git", "init"])
    collection_test_env.run(molecule_args, cwd=role_dir)
