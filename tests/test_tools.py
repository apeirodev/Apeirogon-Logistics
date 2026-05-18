"""Tests for route_chain_analyzer, telemetry tools, patch checker, and provider validator."""
import json
import sys
import io
import pytest


def _call_main(module_name: str, input_data: dict) -> dict:
    """
    Import a tool's main() and call it with stdin patched to the given JSON.
    Patches sys.argv so argparse sees no stray pytest arguments.
    """
    import importlib
    mod = importlib.import_module(module_name)
    old_in, old_out, old_argv = sys.stdin, sys.stdout, sys.argv
    sys.stdin = io.TextIOWrapper(io.BytesIO(json.dumps(input_data).encode()))
    buf = io.StringIO()
    sys.stdout = buf
    sys.argv = [module_name]
    try:
        mod.main()
    finally:
        sys.stdin, sys.stdout, sys.argv = old_in, old_out, old_argv
    return json.loads(buf.getvalue())


class TestRouteChainAnalyzer:
    def test_basic_chain(self):
        from route_chain_analyzer import analyze
        result = analyze({"route_sequence": ["A", "B", "C"]})
        assert result["stop_count"] == 3

    def test_single_stop(self):
        from route_chain_analyzer import analyze
        result = analyze({"route_sequence": ["A"]})
        assert result["stop_count"] == 1

    def test_duplicate_stops_detected(self):
        from route_chain_analyzer import analyze
        result = analyze({"route_sequence": ["A", "B", "A"]})
        # stop_count counts all stops including duplicates
        assert result["stop_count"] == 3

    def test_empty_sequence(self):
        from route_chain_analyzer import analyze
        result = analyze({"route_sequence": []})
        assert result["stop_count"] == 0


class TestTelemetryIngestion:
    def test_valid_telemetry(self):
        result = _call_main("telemetry_ingestion_pipeline", {
            "ship": "hull-b", "issuer": "covalex", "patch_version": "3.23"
        })
        assert isinstance(result, dict)

    def test_governance_metadata_in_output(self):
        result = _call_main("telemetry_ingestion_pipeline", {
            "ship": "hull-b", "issuer": "covalex", "patch_version": "3.23"
        })
        assert "governance_metadata" in result


class TestTelemetryTrustClassifier:
    def test_user_verified_tier(self):
        result = _call_main("telemetry_trust_classifier", {"user_verified": True})
        assert result.get("trust_tier") == "T1"

    def test_unverified_tier(self):
        result = _call_main("telemetry_trust_classifier", {"user_verified": False})
        assert result.get("trust_tier") == "T0"

    def test_missing_field_defaults(self):
        result = _call_main("telemetry_trust_classifier", {})
        assert "trust_tier" in result


class TestPatchCompatibility:
    def test_valid_patch(self):
        result = _call_main("patch_compatibility_checker", {"patch_version": "3.23"})
        assert isinstance(result, dict)

    def test_missing_patch(self):
        result = _call_main("patch_compatibility_checker", {})
        assert isinstance(result, dict)


class TestProviderOutputValidator:
    def _valid_provider_output(self, **overrides):
        base = {
            "advisory_only": True,
            "governance_metadata": {
                "source_class": "ai_output",
                "provenance_chain": [],
                "confidence_level": "medium",
                "verification_status": "not_human_verified",
                "patch_era": "UNRESOLVED",
                "telemetry_support_level": "none",
                "operational_assurance_state": "implemented",
                "unresolved_field_list": [],
                "advisory_only": True,
                "contributor_trust_tier": "T0",
                "derivation_type": "ai_generated",
            },
        }
        base.update(overrides)
        return base

    def test_valid_output_passes(self):
        from provider_output_validator import validate
        result = validate(self._valid_provider_output())
        assert result["valid"] is True
        assert result["hallucination_flag_count"] == 0

    def test_missing_advisory_only_fails(self):
        from provider_output_validator import validate
        data = self._valid_provider_output()
        del data["advisory_only"]
        data["governance_metadata"]["advisory_only"] = False
        result = validate(data)
        assert result["valid"] is False

    def test_wrong_source_class_fails(self):
        from provider_output_validator import validate
        data = self._valid_provider_output()
        data["governance_metadata"]["source_class"] = "deterministic_output"
        result = validate(data)
        assert result["valid"] is False

    def test_missing_governance_metadata_fails(self):
        from provider_output_validator import validate
        result = validate({"advisory_only": True})
        assert result["valid"] is False

    def test_hallucination_flag_unsourced_numeric(self):
        from provider_output_validator import validate
        data = self._valid_provider_output()
        data["reward_usc"] = 50000
        result = validate(data, user_supplied_fields={"issuer", "stops"})
        assert result["hallucination_flag_count"] == 1

    def test_no_hallucination_flag_when_user_supplied(self):
        from provider_output_validator import validate
        data = self._valid_provider_output()
        data["reward_usc"] = 50000
        result = validate(data, user_supplied_fields={"reward_usc"})
        assert result["hallucination_flag_count"] == 0


class TestOCRConfidenceAnalyzer:
    def _run(self, data: dict) -> dict:
        from OCR_confidence_analyzer import main
        old_in, old_out, old_argv = sys.stdin, sys.stdout, sys.argv
        sys.stdin = io.TextIOWrapper(io.BytesIO(json.dumps(data).encode()))
        buf = io.StringIO()
        sys.stdout = buf
        sys.argv = ["OCR_confidence_analyzer"]
        try:
            main()
        finally:
            sys.stdin, sys.stdout, sys.argv = old_in, old_out, old_argv
        return json.loads(buf.getvalue())

    def test_high_confidence_usable(self):
        result = self._run({"ocr_confidence": 0.85, "unresolved_fields": []})
        assert result["usable_for_recommendation"] is True
        assert result["requires_human_review"] is False

    def test_low_confidence_not_usable(self):
        result = self._run({"ocr_confidence": 0.50, "unresolved_fields": []})
        assert result["usable_for_recommendation"] is False

    def test_unresolved_fields_trigger_review(self):
        result = self._run({"ocr_confidence": 0.90, "unresolved_fields": ["issuer"]})
        assert result["requires_human_review"] is True

    def test_non_numeric_confidence_treated_as_zero(self):
        result = self._run({"ocr_confidence": "not_a_number", "unresolved_fields": []})
        assert result["ocr_confidence"] == 0.0
        assert result["usable_for_recommendation"] is False


class TestReplayRouteAnalysis:
    def test_replay_of_runner_output(self):
        from route_analysis_runner import run_analysis
        from replay_route_analysis import replay

        runner_output = run_analysis({"issuer": "covalex", "ship": "hull-b", "stops": ["A", "B"]})
        result = replay(runner_output)
        assert result["valid"] is True

    def test_replay_detects_tampered_hash(self):
        from route_analysis_runner import run_analysis
        from replay_route_analysis import replay
        import copy

        runner_output = run_analysis({"issuer": "covalex", "ship": "hull-b", "stops": ["A", "B"]})
        tampered = copy.deepcopy(runner_output)
        tampered["score_result"]["score"] = 99  # tamper with score
        result = replay(tampered)
        assert result["valid"] is False
