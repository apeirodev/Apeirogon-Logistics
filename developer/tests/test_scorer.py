"""Tests for deterministic_scorer.py"""
import pytest
from deterministic_scorer import clamp, factor, score_route, DEFAULT_WEIGHTS, ISSUER_MODIFIERS, SHIP_MODIFIERS


class TestClamp:
    def test_within_range(self):
        assert clamp(55.4) == 55

    def test_below_zero_clamped(self):
        assert clamp(-10) == 0

    def test_above_100_clamped(self):
        assert clamp(110) == 100

    def test_exactly_zero(self):
        assert clamp(0) == 0

    def test_exactly_100(self):
        assert clamp(100) == 100

    def test_rounds_correctly(self):
        # Python uses banker's rounding: round(66.5) == 66, round(67.5) == 68
        assert clamp(66.5) == 66
        assert clamp(67.5) == 68


class TestFactor:
    def test_explicit_value(self):
        assert factor({"same_pickup": 3}, "same_pickup") == 3.0

    def test_missing_key_returns_zero(self):
        assert factor({}, "dead_leg") == 0.0

    def test_invalid_type_returns_zero(self):
        assert factor({"same_pickup": "bad"}, "same_pickup") == 0.0

    def test_stop_density_threshold(self):
        assert factor({"route_sequence": ["A", "B", "C", "D"]}, "stop_density") == 1
        assert factor({"route_sequence": ["A", "B", "C"]}, "stop_density") == 0

    def test_chain_collapse_trigger(self):
        assert factor({"route_sequence": ["A", "B", "C", "D", "E", "F", "G"]}, "chain_collapse") == 1
        assert factor({"route_sequence": ["A", "B", "C"]}, "chain_collapse") == 0

    def test_route_continuity_with_repeat(self):
        assert factor({"route_sequence": ["A", "B", "A"]}, "route_continuity") == 1

    def test_route_continuity_no_repeat(self):
        assert factor({"route_sequence": ["A", "B", "C"]}, "route_continuity") == 0

    def test_same_pickup_from_missions(self):
        missions = [
            {"pickup": "Port Olisar"},
            {"pickup": "Port Olisar"},
            {"pickup": "Microtech"},
        ]
        assert factor({"missions": missions}, "same_pickup") == 1

    def test_destination_overlap_from_missions(self):
        missions = [
            {"destination": "Baijini Point"},
            {"destination": "Baijini Point"},
        ]
        assert factor({"missions": missions}, "destination_overlap") == 1


class TestScoreRoute:
    def test_baseline_score_no_factors(self):
        result = score_route({})
        assert 0 <= result["score"] <= 100
        assert result["recommendation"] in ("accept", "defer", "reject")

    def test_same_pickup_raises_score(self):
        base = score_route({})
        boosted = score_route({"same_pickup": 2})
        assert boosted["score"] > base["score"]

    def test_dead_leg_lowers_score(self):
        base = score_route({})
        penalised = score_route({"dead_leg": 1})
        assert penalised["score"] < base["score"]

    def test_hull_b_covalex_modifiers_applied(self):
        result = score_route({
            "issuer": "covalex",
            "ship": "hull-b",
            "same_pickup": 2,
        })
        assert result["score"] >= 70, "Hull-B + Covalex + same_pickup should score accept"

    def test_governance_metadata_present(self):
        result = score_route({"same_pickup": 1})
        assert "governance_metadata" in result
        gm = result["governance_metadata"]
        assert gm["source_class"] == "deterministic_output"
        assert gm["advisory_only"] is True

    def test_deterministic_hash_present(self):
        result = score_route({"same_pickup": 1})
        assert "deterministic_hash" in result
        assert len(result["deterministic_hash"]) == 64

    def test_same_input_same_hash(self):
        route = {"issuer": "covalex", "ship": "hull-b", "same_pickup": 2}
        r1 = score_route(route)
        r2 = score_route(route)
        assert r1["deterministic_hash"] == r2["deterministic_hash"]

    def test_unresolved_fields_downgrade_score(self):
        without = score_route({"same_pickup": 3})
        with_unresolved = score_route({"same_pickup": 3, "patch_version": None})
        # unresolved fields reduce score
        assert with_unresolved["score"] <= without["score"]

    def test_recommendation_accept_high_score(self):
        result = score_route({"same_pickup": 4, "destination_overlap": 3, "issuer": "covalex", "ship": "hull-b"})
        assert result["recommendation"] == "accept"

    def test_recommendation_reject_bad_route(self):
        result = score_route({"dead_leg": 3, "fragmentation": 3, "atmosphere": 2, "chain_collapse": 1})
        assert result["recommendation"] in ("reject", "defer")

    def test_custom_weights_override(self):
        custom = {"same_pickup": 50}  # massively boost same_pickup
        result = score_route({"same_pickup": 2}, weights=custom)
        assert result["score"] > 90

    def test_issuer_case_insensitive(self):
        lower = score_route({"issuer": "covalex", "same_pickup": 1})
        upper = score_route({"issuer": "COVALEX", "same_pickup": 1})
        assert lower["score"] == upper["score"]

    def test_score_breakdown_keys(self):
        result = score_route({"same_pickup": 2, "dead_leg": 1})
        assert "same_pickup" in result["score_breakdown"]
        assert "dead_leg" in result["score_breakdown"]

    def test_config_file_weights_loaded(self):
        # DEFAULT_WEIGHTS should have been loaded from runtime/scoring_config.json
        # Verify it has the expected keys
        assert "same_pickup" in DEFAULT_WEIGHTS
        assert "dead_leg" in DEFAULT_WEIGHTS
        assert DEFAULT_WEIGHTS["same_pickup"] > 0
        assert DEFAULT_WEIGHTS["dead_leg"] < 0

    def test_hull_b_in_ship_modifiers(self):
        assert "hull-b" in SHIP_MODIFIERS
        assert "fragmentation" in SHIP_MODIFIERS["hull-b"]
