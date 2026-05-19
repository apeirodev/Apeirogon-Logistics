"""Tests for schema_validator and manifest_validator."""
import json
import subprocess
import sys
from pathlib import Path
import pytest

_REPO = Path(__file__).parent.parent
_TOOLS = _REPO / "tools"


def _run_tool(script: str, args: list[str] = None) -> dict:
    cmd = [sys.executable, str(_TOOLS / script)] + (args or [])
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(_REPO))
    assert result.returncode == 0, f"{script} exited {result.returncode}: {result.stderr}"
    return json.loads(result.stdout)


class TestSchemaValidator:
    def test_all_schemas_valid(self):
        result = _run_tool("schema_validator.py", ["--root", "schema"])
        assert result["valid"] is True, result

    def test_schema_count_nonzero(self):
        result = _run_tool("schema_validator.py", ["--root", "schema"])
        assert result["file_count"] > 0


class TestManifestValidator:
    def test_manifests_dir_valid(self):
        result = _run_tool("manifest_validator.py", ["--root", "manifests", "--base", "."])
        assert result["valid"] is True, result

    def test_root_manifests_valid(self):
        result = _run_tool("manifest_validator.py", ["--root", ".", "--base", ".", "--exclude", "tests/*"])
        assert result["valid"] is True, result

    def test_no_missing_references_in_manifests(self):
        result = _run_tool("manifest_validator.py", ["--root", "manifests", "--base", "."])
        for finding in result["findings"]:
            assert finding.get("missing_references", []) == [], \
                f"Manifest {finding['manifest']} has missing refs: {finding['missing_references']}"


class TestReleaseIntegrity:
    def test_round_trip(self):
        """Generate a checksum manifest and immediately verify it."""
        gen = subprocess.run(
            [sys.executable, str(_TOOLS / "generate_release_checksums.py"), "--root", "tests"],
            capture_output=True, text=True, cwd=str(_REPO)
        )
        assert gen.returncode == 0
        manifest_json = gen.stdout

        verify = subprocess.run(
            [sys.executable, str(_TOOLS / "verify_release_integrity.py"), "--root", "tests"],
            input=manifest_json, capture_output=True, text=True, cwd=str(_REPO)
        )
        assert verify.returncode == 0
        result = json.loads(verify.stdout)
        assert result["valid"] is True
        assert result["mismatch_count"] == 0
        assert result["missing_count"] == 0


class TestSetupSync:
    def test_all_setup_files_match_template(self):
        result = subprocess.run(
            [sys.executable, str(_TOOLS / "sync_setup_scoring.py"), "--check"],
            capture_output=True, text=True, cwd=str(_REPO)
        )
        assert result.returncode == 0, f"SETUP sync check failed:\n{result.stderr}"


class TestScoringNumbers:
    def test_template_matches_config(self):
        result = _run_tool("validate_scoring_numbers.py")
        assert result["valid"] is True, result
        assert result["mismatch_count"] == 0
        assert result["not_found_count"] == 0
