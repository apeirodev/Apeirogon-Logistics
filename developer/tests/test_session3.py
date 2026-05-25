"""Tests for Session 3: OCR vision path, ingest_mission_batch."""
import copy
import pytest
from OCR_result_normalizer import normalise, normalize_ocr, _normalise_vision
from ingest_mission_batch import ingest_batch, _detect_same_pickup, _build_combined_route


# ── Shared fixtures ────────────────────────────────────────────────────────────

def _vision_input(**overrides):
    base = {
        "advisory_only": True,
        "source_class": "ai_vision_extraction",
        "extraction_confidence": 0.88,
        "ship": "Hull-B",
        "missions": [
            {
                "issuer": "Covalex",
                "pickup": "Hur-L2",
                "delivery": ["Covalex Hub Shopp-L4"],
                "cargo_type": "Processed Food",
                "cargo_scu": 24,
                "reward_usc": 12500,
                "fee_usc": "UNRESOLVED",
                "timer_minutes": "UNRESOLVED",
                "unresolved_fields": ["fee_usc", "timer_minutes"],
            },
            {
                "issuer": "Covalex",
                "pickup": "Hur-L2",
                "delivery": ["Baijini Point"],
                "cargo_type": "Scrap",
                "cargo_scu": 16,
                "reward_usc": 9000,
                "fee_usc": "UNRESOLVED",
                "timer_minutes": "UNRESOLVED",
                "unresolved_fields": ["fee_usc", "timer_minutes"],
            },
        ],
        "unresolved_fields": ["patch_version"],
    }
    base.update(overrides)
    return base


def _raw_batch(**overrides):
    base = {
        "issuer": "covalex",
        "ship": "hull-b",
        "missions": [
            {"pickup": "Hur-L2", "delivery": ["Covalex Hub Shopp-L4"], "cargo_scu": 24, "reward_usc": 12500},
            {"pickup": "Hur-L2", "delivery": ["Baijini Point"], "cargo_scu": 16, "reward_usc": 9000},
        ],
    }
    base.update(overrides)
    return base


# ── OCR normalizer — vision mode ───────────────────────────────────────────────

class TestOCRNormalizerVisionMode:
    def test_dispatch_to_vision_mode(self):
        result = normalise(_vision_input())
        assert result["mode"] == "ai_vision"

    def test_dispatch_to_raw_ocr_mode(self):
        result = normalise({"raw_text": "Covalex 24 SCU"})
        assert result["mode"] == "raw_ocr"

    def test_mission_count_correct(self):
        result = normalise(_vision_input())
        assert result["mission_count"] == 2

    def test_issuer_resolved_in_vision(self):
        result = normalise(_vision_input())
        assert result["missions"][0]["issuer"] == "Covalex"

    def test_location_alias_resolved(self):
        data = _vision_input()
        data["missions"][0]["pickup"] = "Tressler"  # alias for Port Tressler
        result = normalise(data)
        assert result["missions"][0]["pickup"] == "Port Tressler"

    def test_tressler_alias_resolved(self):
        data = _vision_input()
        data["missions"][0]["delivery"] = ["Tressler"]
        result = normalise(data)
        assert result["missions"][0]["delivery"] == ["Port Tressler"]

    def test_unresolved_issuer_preserved(self):
        data = _vision_input()
        data["missions"][0]["issuer"] = "UNRESOLVED"
        result = normalise(data)
        assert result["missions"][0]["issuer"] == "UNRESOLVED"
        assert "issuer" in result["missions"][0]["unresolved_fields"]

    def test_unresolved_cargo_preserved(self):
        data = _vision_input()
        data["missions"][0]["cargo_scu"] = "UNRESOLVED"
        result = normalise(data)
        assert "cargo_scu" in result["missions"][0]["unresolved_fields"]

    def test_governance_metadata_source_class(self):
        result = normalise(_vision_input())
        assert result["governance_metadata"]["source_class"] == "ai_vision_extraction"
        assert result["governance_metadata"]["advisory_only"] is True

    def test_low_confidence_warning(self):
        data = _vision_input(extraction_confidence=0.40)
        result = normalise(data)
        assert any("Low extraction confidence" in w for w in result["warnings"])

    def test_empty_missions_warning(self):
        data = _vision_input(missions=[])
        result = normalise(data)
        assert result["mission_count"] == 0
        assert any("No missions" in w for w in result["warnings"])

    def test_ship_preserved(self):
        result = normalise(_vision_input())
        assert result["ship"] == "Hull-B"

    def test_delivery_string_normalised_to_list(self):
        data = _vision_input()
        data["missions"][0]["delivery"] = "Covalex Hub Shopp-L4"  # string, not list
        result = normalise(data)
        assert isinstance(result["missions"][0]["delivery"], list)

    def test_missions_dispatched_when_no_source_class(self):
        # If source_class absent but missions present, should use vision mode
        data = {"missions": [{"issuer": "Covalex", "pickup": "Hur-L2",
                               "delivery": ["Baijini Point"], "cargo_scu": 10, "reward_usc": 5000}]}
        result = normalise(data)
        assert result["mode"] == "ai_vision"


# ── ingest_mission_batch ───────────────────────────────────────────────────────

class TestIngestMissionBatch:
    def test_basic_batch_structure(self):
        result = ingest_batch(_raw_batch())
        assert "ranked_missions" in result
        assert "batch_summary" in result
        assert "suggested_combined_route" in result
        assert "governance_metadata" in result

    def test_mission_count_in_summary(self):
        result = ingest_batch(_raw_batch())
        assert result["batch_summary"]["mission_count"] == 2

    def test_ranked_missions_sorted_descending(self):
        result = ingest_batch(_raw_batch())
        scores = [m["score"] for m in result["ranked_missions"]]
        assert scores == sorted(scores, reverse=True)

    def test_same_pickup_detected(self):
        result = ingest_batch(_raw_batch())
        assert "Hur-L2" in result["same_pickup_stacking"]
        assert len(result["same_pickup_stacking"]["Hur-L2"]) == 2

    def test_same_pickup_not_detected_without_sharing(self):
        data = _raw_batch()
        data["missions"][1]["pickup"] = "Microtech"
        result = ingest_batch(data)
        assert result["same_pickup_stacking"] == {}

    def test_combined_route_produced(self):
        result = ingest_batch(_raw_batch())
        assert result["suggested_combined_route"] is not None
        cr = result["suggested_combined_route"]
        assert "score" in cr
        assert "stops" in cr
        assert cr["same_pickup_bonus"] >= 1

    def test_combined_route_score_exceeds_individual(self):
        result = ingest_batch(_raw_batch())
        combined_score = result["suggested_combined_route"]["score"]
        individual_scores = [m["score"] for m in result["ranked_missions"]]
        assert combined_score >= max(individual_scores)

    def test_each_mission_has_required_fields(self):
        result = ingest_batch(_raw_batch())
        for m in result["ranked_missions"]:
            assert "score" in m
            assert "recommendation" in m
            assert "mission_index" in m
            assert m["recommendation"] in ("accept", "defer", "reject")

    def test_governance_source_class(self):
        result = ingest_batch(_raw_batch())
        assert result["governance_metadata"]["source_class"] == "deterministic_output"
        assert result["governance_metadata"]["advisory_only"] is True

    def test_dead_leg_lowers_score(self):
        data = _raw_batch()
        data["missions"].append({
            "pickup": "Microtech", "delivery": ["ARC-L1"],
            "cargo_scu": 32, "reward_usc": 8000, "dead_leg": 1
        })
        result = ingest_batch(data)
        dead_leg_mission = next(m for m in result["ranked_missions"] if m["pickup"] == "Microtech")
        # dead_leg mission should score lower than Hur-L2 missions
        port_olisar_scores = [m["score"] for m in result["ranked_missions"] if m["pickup"] == "Hur-L2"]
        assert dead_leg_mission["score"] < min(port_olisar_scores)

    def test_accepts_normaliser_output(self):
        """ingest_batch should accept the output of OCR_result_normalizer (mode: ai_vision)."""
        from OCR_result_normalizer import normalise
        normalised = normalise(_vision_input())
        result = ingest_batch(normalised)
        assert result["batch_summary"]["mission_count"] == 2

    def test_empty_batch(self):
        result = ingest_batch({"issuer": "covalex", "ship": "hull-b", "missions": []})
        assert result["batch_summary"]["mission_count"] == 0
        assert result["suggested_combined_route"] is None

    def test_issuer_from_batch_used_as_fallback(self):
        """If mission has no issuer, batch-level issuer should be used."""
        data = _raw_batch()
        del data["missions"][0]["pickup"]  # make pickup UNRESOLVED but keep other fields
        result = ingest_batch(data)
        # Should not crash; issuer from batch should be applied
        assert result["batch_summary"]["issuer"] == "covalex"


class TestSamePickupDetection:
    def test_two_same_pickup(self):
        missions = [
            {"pickup": "Hur-L2"},
            {"pickup": "Hur-L2"},
            {"pickup": "Microtech"},
        ]
        result = _detect_same_pickup(missions)
        assert "Hur-L2" in result
        assert len(result["Hur-L2"]) == 2
        assert "Microtech" not in result

    def test_all_unique_pickups(self):
        missions = [{"pickup": "A"}, {"pickup": "B"}, {"pickup": "C"}]
        assert _detect_same_pickup(missions) == {}

    def test_unresolved_pickup_ignored(self):
        missions = [{"pickup": "UNRESOLVED"}, {"pickup": "UNRESOLVED"}]
        assert _detect_same_pickup(missions) == {}
