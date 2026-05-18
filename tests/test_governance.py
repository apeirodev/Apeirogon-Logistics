"""Tests for governance metadata validation (lib/common.py)"""
import pytest
from lib.common import (
    validate_governance_metadata,
    governance_metadata,
    collect_unresolved,
    stable_hash,
    normalize_patch,
    parse_positive_number,
    normalize_text,
)


class TestGovernanceMetadata:
    def _valid_meta(self, **overrides):
        meta = governance_metadata(source_class="deterministic_output")
        meta.update(overrides)
        return meta

    def test_valid_metadata_passes(self):
        ok, problems = validate_governance_metadata(self._valid_meta())
        assert ok, problems

    def test_missing_source_class_fails(self):
        meta = self._valid_meta()
        del meta["source_class"]
        ok, problems = validate_governance_metadata(meta)
        assert not ok
        assert any("missing" in p for p in problems)

    def test_advisory_only_false_fails(self):
        meta = self._valid_meta(advisory_only=False)
        ok, problems = validate_governance_metadata(meta)
        assert not ok

    def test_invalid_trust_tier_fails(self):
        meta = self._valid_meta(contributor_trust_tier="T99")
        ok, problems = validate_governance_metadata(meta)
        assert not ok

    def test_valid_trust_tiers(self):
        for tier in ("T0", "T1", "T2", "T3", "T4"):
            meta = self._valid_meta(contributor_trust_tier=tier)
            ok, _ = validate_governance_metadata(meta)
            assert ok, f"tier {tier} should be valid"

    def test_provenance_chain_must_be_list(self):
        meta = self._valid_meta(provenance_chain="not a list")
        ok, problems = validate_governance_metadata(meta)
        assert not ok

    def test_unresolved_field_list_must_be_list(self):
        meta = self._valid_meta(unresolved_field_list="not a list")
        ok, problems = validate_governance_metadata(meta)
        assert not ok

    def test_ai_output_source_class(self):
        meta = governance_metadata(source_class="ai_output", derivation_type="ai_generated")
        ok, _ = validate_governance_metadata(meta)
        assert ok


class TestCollectUnresolved:
    def test_none_value_flagged(self):
        fields = collect_unresolved({"price": None})
        assert "price" in fields

    def test_empty_string_flagged(self):
        fields = collect_unresolved({"issuer": ""})
        assert "issuer" in fields

    def test_unresolved_string_flagged(self):
        fields = collect_unresolved({"location": "UNRESOLVED"})
        assert "location" in fields

    def test_nested_unresolved(self):
        fields = collect_unresolved({"outer": {"inner": None}})
        assert "inner" in fields

    def test_list_with_unresolved_items(self):
        fields = collect_unresolved({"unresolved_field_list": ["fee_usc", "distance"]})
        assert "fee_usc" in fields

    def test_present_values_not_flagged(self):
        fields = collect_unresolved({"price": 100, "issuer": "Covalex"})
        assert "price" not in fields
        assert "issuer" not in fields


class TestStableHash:
    def test_same_data_same_hash(self):
        d = {"a": 1, "b": [1, 2]}
        assert stable_hash(d) == stable_hash(d)

    def test_key_order_independent(self):
        d1 = {"a": 1, "b": 2}
        d2 = {"b": 2, "a": 1}
        assert stable_hash(d1) == stable_hash(d2)

    def test_different_data_different_hash(self):
        assert stable_hash({"a": 1}) != stable_hash({"a": 2})

    def test_hash_length(self):
        assert len(stable_hash({})) == 64


class TestParsePositiveNumber:
    def test_integer_string(self):
        assert parse_positive_number("42") == 42.0

    def test_float_string(self):
        assert parse_positive_number("3.14") == 3.14

    def test_negative_returns_none(self):
        assert parse_positive_number("-5") is None

    def test_none_input_returns_none(self):
        assert parse_positive_number(None) is None

    def test_non_numeric_returns_none(self):
        assert parse_positive_number("abc") is None

    def test_number_embedded_in_text(self):
        assert parse_positive_number("24 SCU") == 24.0


class TestNormalizePatch:
    def test_patch_version_field(self):
        assert normalize_patch({"patch_version": "3.23"}) == "3.23"

    def test_patch_era_fallback(self):
        assert normalize_patch({"patch_era": "3.22"}) == "3.22"

    def test_override_wins(self):
        assert normalize_patch({"patch_version": "3.22"}, override="3.23") == "3.23"

    def test_missing_returns_unresolved(self):
        assert normalize_patch({}) == "UNRESOLVED"
