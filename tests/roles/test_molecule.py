from pathlib import Path

import pytest

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
def test_scenario(scenario: Path, molecule_env) -> None:
    molecule_env.run(
        ["molecule", "test", "-s", scenario.name],
        cwd=scenario.parent.parent.resolve()
    )
