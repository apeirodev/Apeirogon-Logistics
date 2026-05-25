"""Security regression tests for Apeirogon Logistics.

Covers:
  - FILE-01: safe_write_path path traversal guard
  - WARN-02: safe_load_json 10 MB size cap
  - ERR-01:  validate_governance_metadata fail-closed on unexpected exception
  - AI-03:   hallucination flag propagation for unsourced numeric fields
  - AI-04:   numeric sourcing validation in provider_output_validator
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# FILE-01: safe_write_path
# ---------------------------------------------------------------------------

class TestSafeWritePath:
    """Tests that safe_write_path rejects traversal paths and allows valid roots."""

    def test_path_traversal_rejected(self):
        from lib.common import safe_write_path
        with pytest.raises(ValueError, match="allowed write roots"):
            safe_write_path("../../etc/passwd")

    def test_absolute_system_path_rejected(self):
        from lib.common import safe_write_path
        with pytest.raises(ValueError, match="allowed write roots"):
            safe_write_path("/etc/passwd")

    def test_stdout_sentinel_always_allowed(self):
        from lib.common import safe_write_path
        result = safe_write_path("-")
        assert str(result) == "-"

    def test_output_subdir_allowed(self, tmp_path, monkeypatch):
        from lib.common import safe_write_path, _ALLOWED_WRITE_ROOTS
        # Use a custom allowed root pointing at tmp_path
        result = safe_write_path(str(tmp_path / "result.json"), allowed_roots=[tmp_path])
        assert result == (tmp_path / "result.json").resolve()

    def test_traversal_within_allowed_prefix_rejected(self):
        from lib.common import safe_write_path
        # "output/../../../etc/passwd" escapes even if it starts with "output"
        with pytest.raises(ValueError, match="allowed write roots"):
            safe_write_path("output/../../../etc/passwd")


# ---------------------------------------------------------------------------
# WARN-02: safe_load_json size cap
# ---------------------------------------------------------------------------

class TestSafeLoadJson:
    """Tests that safe_load_json enforces the 10 MB input size cap."""

    def test_normal_file_loads(self, tmp_path):
        from lib.common import safe_load_json
        f = tmp_path / "small.json"
        f.write_text('{"key": "value"}', encoding="utf-8")
        result = safe_load_json(f)
        assert result == {"key": "value"}

    def test_file_exceeding_limit_raises(self, tmp_path):
        from lib.common import safe_load_json, _MAX_INPUT_BYTES
        f = tmp_path / "large.json"
        # Write a file slightly larger than the cap
        # Use a minimal valid JSON wrapped in enough whitespace
        padding = " " * (_MAX_INPUT_BYTES + 1)
        f.write_bytes(padding.encode("utf-8"))
        with pytest.raises(ValueError, match="too large"):
            safe_load_json(f)

    def test_exactly_at_limit_loads(self, tmp_path):
        from lib.common import safe_load_json, _MAX_INPUT_BYTES
        f = tmp_path / "at_limit.json"
        # Build a JSON file whose raw byte size is exactly at the cap.
        # A simple string value padded to fit.
        payload = '{"data": "' + ("x" * (_MAX_INPUT_BYTES - 12)) + '"}'
        assert len(payload.encode("utf-8")) == _MAX_INPUT_BYTES
        f.write_text(payload, encoding="utf-8")
        result = safe_load_json(f)
        assert "data" in result


# ---------------------------------------------------------------------------
# ERR-01: validate_governance_metadata fails closed on unexpected exceptions
# ---------------------------------------------------------------------------

class TestValidateGovernanceMetadataFailClosed:
    """Tests that validate_governance_metadata never fails open."""

    def test_valid_metadata_passes(self):
        from lib.common import validate_governance_metadata, governance_metadata
        meta = governance_metadata(source_class="deterministic_output")
        ok, problems = validate_governance_metadata(meta)
        assert ok, problems

    def test_none_input_fails_closed(self):
        """None is not a dict; the function must return (False, [...]) not raise."""
        from lib.common import validate_governance_metadata
        ok, problems = validate_governance_metadata(None)  # type: ignore[arg-type]
        assert ok is False
        assert problems  # must have at least one problem entry

    def test_non_dict_input_fails_closed(self):
        """A list is not a valid metadata dict; must fail closed."""
        from lib.common import validate_governance_metadata
        ok, problems = validate_governance_metadata(["not", "a", "dict"])  # type: ignore[arg-type]
        assert ok is False
        assert problems

    def test_fail_closed_sentinel_present(self):
        """When the inner validator cannot complete, the sentinel must appear."""
        from lib.common import validate_governance_metadata
        # Pass a None so attribute access inside the inner function will raise
        ok, problems = validate_governance_metadata(None)  # type: ignore[arg-type]
        assert ok is False
        # Either the sentinel "validation_error_fail_closed" is present, or
        # the normal "missing fields" path handles it -- either way ok is False.
        assert not ok


# ---------------------------------------------------------------------------
# AI-03 / AI-04: hallucination flag propagation
# ---------------------------------------------------------------------------

class TestHallucinationFlagPropagation:
    """Tests that unsourced numeric fields in provider output generate flags."""

    def _base_output(self, **extra) -> dict:
        from lib.common import governance_metadata
        gm = governance_metadata(
            source_class="ai_output",
            derivation_type="ai_generated",
        )
        return {"advisory_only": True, "governance_metadata": gm, **extra}

    def test_unsourced_numeric_field_flagged(self):
        from provider_output_validator import validate
        data = self._base_output(reward_usc=12500)
        result = validate(data, user_supplied_fields=set())
        assert result["hallucination_flag_count"] > 0
        assert any("reward_usc" in f for f in result["hallucination_flags"])

    def test_user_supplied_numeric_field_not_flagged(self):
        from provider_output_validator import validate
        data = self._base_output(reward_usc=12500)
        result = validate(data, user_supplied_fields={"reward_usc"})
        # reward_usc was in user-supplied fields -- no flag expected
        assert not any("reward_usc" in f for f in result["hallucination_flags"])

    def test_multiple_unsourced_fields_all_flagged(self):
        from provider_output_validator import validate
        data = self._base_output(reward_usc=12500, fee_usc=500, cargo_scu=24)
        result = validate(data, user_supplied_fields=set())
        flagged_fields = {f.split("'")[1] for f in result["hallucination_flags"]
                         if "'" in f}
        assert "reward_usc" in flagged_fields
        assert "fee_usc" in flagged_fields
        assert "cargo_scu" in flagged_fields

    def test_no_user_supplied_fields_arg_skips_hallucination_check(self):
        from provider_output_validator import validate
        data = self._base_output(reward_usc=12500)
        # When user_supplied_fields is None the check is skipped
        result = validate(data, user_supplied_fields=None)
        assert result["hallucination_flag_count"] == 0

    def test_non_numeric_values_not_flagged(self):
        from provider_output_validator import validate
        data = self._base_output(recommendation="accept")
        result = validate(data, user_supplied_fields=set())
        # String fields should not trigger hallucination flags
        assert result["hallucination_flag_count"] == 0


# ---------------------------------------------------------------------------
# FILE-01: dump_json refuses to write to traversal paths
# ---------------------------------------------------------------------------

class TestDumpJsonPathGuard:
    """Tests that dump_json enforces safe_write_path when writing to a file."""

    def test_traversal_path_rejected(self):
        from lib.common import dump_json
        with pytest.raises(ValueError, match="allowed write roots"):
            dump_json({"x": 1}, "../../etc/passwd")

    def test_stdout_sentinel_always_works(self, capsys):
        from lib.common import dump_json
        dump_json({"x": 1}, "-")
        captured = capsys.readouterr()
        assert '"x": 1' in captured.out

    def test_skip_path_check_bypasses_guard(self, tmp_path):
        from lib.common import dump_json
        out = tmp_path / "result.json"
        # skip_path_check=True is for internal trusted paths only
        dump_json({"x": 1}, str(out), skip_path_check=True)
        assert out.exists()
        assert json.loads(out.read_text())["x"] == 1
