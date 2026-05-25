import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[2]


def test_all_version_files_agree():
    version_json = json.loads((ROOT / "VERSION.json").read_text())["version"]

    pyproject_match = re.search(
        r'^version\s*=\s*"([^"]+)"',
        (ROOT / "pyproject.toml").read_text(),
        re.MULTILINE,
    )
    assert pyproject_match, "Could not find version in pyproject.toml"
    pyproject = pyproject_match.group(1)

    readme_match = re.search(r"v(\d+\.\d+\.\d+)", (ROOT / "README.md").read_text())
    assert readme_match, "Could not find version in README.md"
    readme = readme_match.group(1)

    status_match = re.search(
        r"\*\*Version:\*\*\s*(\S+)",
        (ROOT / "developer" / "PROJECT_STATUS.md").read_text(),
    )
    assert status_match, "Could not find version in PROJECT_STATUS.md"
    project_status = status_match.group(1)

    assert version_json == pyproject == readme == project_status, (
        f"Version files disagree:\n"
        f"  VERSION.json      = {version_json}\n"
        f"  pyproject.toml    = {pyproject}\n"
        f"  README.md         = {readme}\n"
        f"  PROJECT_STATUS.md = {project_status}"
    )


def test_version_json_history_includes_current():
    data = json.loads((ROOT / "VERSION.json").read_text())
    current = data["version"]
    history_versions = [entry["version"] for entry in data.get("version_history", [])]
    assert current in history_versions, (
        f"Current version {current!r} is not in VERSION.json version_history. "
        f"Add it before committing."
    )


def test_version_json_previous_differs_from_current():
    data = json.loads((ROOT / "VERSION.json").read_text())
    current = data["version"]
    previous = data.get("previous_version")
    assert previous != current, (
        f"previous_version equals current version ({current!r}). "
        f"Update previous_version to the prior release."
    )
