"""Tests for Session 5 tools: session_state_manager, user_profile_loader,
bundle_telemetry, weight_sensitivity_analyzer, calculate_traversal,
build_reproducible_release."""
from __future__ import annotations
import io
import json
import os
import sys
import tempfile
import time
import zipfile
from pathlib import Path

import pytest

_TOOLS = Path(__file__).parent.parent / "tools"
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))


# ---------------------------------------------------------------------------
# session_state_manager
# ---------------------------------------------------------------------------

from session_state_manager import validate_session


class TestSessionStateManager:
    def _minimal(self):
        return {"session_id": "sess-001"}

    def test_minimal_valid(self):
        r = validate_session(self._minimal())
        assert r["valid"] is True
        assert r["errors"] == []
        assert r["session_hash"]

    def test_missing_session_id(self):
        r = validate_session({})
        assert r["valid"] is False
        assert any("session_id" in e for e in r["errors"])

    def test_recommended_fields_absent_produces_warnings(self):
        r = validate_session(self._minimal())
        assert len(r["warnings"]) > 0
        assert "ship" in r["missing_recommended"]
        assert "issuer" in r["missing_recommended"]

    def test_known_ship_no_warning(self):
        r = validate_session({"session_id": "s1", "ship": "hull-b", "issuer": "covalex"})
        assert r["valid"] is True
        ship_warns = [w for w in r["warnings"] if "unrecognised ship" in w]
        assert ship_warns == []

    def test_unknown_ship_warning(self):
        r = validate_session({"session_id": "s1", "ship": "star-runner-xl"})
        assert any("unrecognised ship" in w for w in r["warnings"])

    def test_unknown_issuer_warning(self):
        r = validate_session({"session_id": "s1", "issuer": "space-express"})
        assert any("unrecognised issuer" in w for w in r["warnings"])

    def test_invalid_completed_missions_type(self):
        r = validate_session({"session_id": "s1", "completed_missions": "not-a-list"})
        assert r["valid"] is False
        assert any("completed_missions" in e for e in r["errors"])

    def test_valid_completed_missions(self):
        r = validate_session({"session_id": "s1", "completed_missions": [{"pickup": "Port Olisar"}]})
        assert r["valid"] is True

    def test_future_epoch_warning(self):
        future = int(time.time()) + 200_000
        r = validate_session({"session_id": "s1", "session_start_epoch": future})
        assert any("future" in w for w in r["warnings"])

    def test_unresolved_patch_warning(self):
        r = validate_session(self._minimal())
        assert any("patch_version" in w for w in r["warnings"])

    def test_patch_version_override(self):
        state = dict(self._minimal())
        state["patch_version"] = "Alpha 3.23"
        r = validate_session(state)
        patch_warns = [w for w in r["warnings"] if "patch_version" in w]
        assert patch_warns == []

    def test_governance_metadata_present(self):
        r = validate_session(self._minimal())
        assert "governance_metadata" in r
        assert r["governance_metadata"]["source_class"] == "session_state_validation"

    def test_unresolved_fields_collected(self):
        state = {"session_id": "s1", "ship": "UNRESOLVED"}
        r = validate_session(state)
        assert "ship" in r["unresolved_fields"]


# ---------------------------------------------------------------------------
# user_profile_loader
# ---------------------------------------------------------------------------

from user_profile_loader import load_profile


class TestUserProfileLoader:
    def _minimal(self):
        return {"user_profile_id": "player-001"}

    def test_minimal_valid(self):
        r = load_profile(self._minimal())
        assert r["valid"] is True
        assert r["profile_hash"]

    def test_missing_id(self):
        r = load_profile({})
        assert r["valid"] is False
        assert any("user_profile_id" in e for e in r["errors"])

    def test_recommended_fields_absent(self):
        r = load_profile(self._minimal())
        assert "preferred_ship" in r["missing_recommended"]

    def test_known_ship_no_warning(self):
        r = load_profile({"user_profile_id": "p1", "preferred_ship": "hull-b"})
        assert not any("unrecognised" in w for w in r["warnings"])

    def test_unknown_ship_warning(self):
        r = load_profile({"user_profile_id": "p1", "preferred_ship": "mega-hauler"})
        assert any("preferred_ship" in w for w in r["warnings"])

    def test_reputation_dict_valid(self):
        r = load_profile({
            "user_profile_id": "p1",
            "reputation": {"covalex": 450, "ling": 120},
        })
        assert r["valid"] is True

    def test_reputation_non_dict_error(self):
        r = load_profile({"user_profile_id": "p1", "reputation": "high"})
        assert r["valid"] is False
        assert any("reputation" in e for e in r["errors"])

    def test_governance_metadata(self):
        r = load_profile(self._minimal())
        assert r["governance_metadata"]["source_class"] == "user_profile_validation"

    def test_profile_included_in_output(self):
        p = {"user_profile_id": "p1", "preferred_ship": "hull-b"}
        r = load_profile(p)
        assert r["profile"]["preferred_ship"] == "hull-b"


# ---------------------------------------------------------------------------
# weight_sensitivity_analyzer
# ---------------------------------------------------------------------------

from weight_sensitivity_analyzer import analyze


class TestWeightSensitivityAnalyzer:
    def _route(self):
        return {"issuer": "covalex", "ship": "hull-b", "same_pickup": 2, "dead_leg": 1}

    def test_returns_baseline(self):
        r = analyze(self._route())
        assert "baseline_score" in r
        assert isinstance(r["baseline_score"], int)

    def test_sensitivity_table_present(self):
        r = analyze(self._route())
        assert "sensitivity_table" in r
        assert len(r["sensitivity_table"]) > 0

    def test_active_factors_detected(self):
        r = analyze(self._route())
        assert "same_pickup" in r["active_factors"]
        assert "dead_leg" in r["active_factors"]

    def test_most_sensitive_factor_present(self):
        r = analyze(self._route())
        assert r["most_sensitive_factor"] in r["active_factors"]

    def test_scales_in_row(self):
        r = analyze(self._route())
        row = r["sensitivity_table"][0]
        assert "×1.0 (baseline)" in row["scales"]
        assert "×2.0" in row["scales"]

    def test_baseline_scale_matches_baseline_score(self):
        r = analyze(self._route())
        for row in r["sensitivity_table"]:
            assert row["scales"]["×1.0 (baseline)"]["score"] == r["baseline_score"]

    def test_no_active_factors_handled(self):
        r = analyze({"issuer": "covalex"})
        assert r["most_sensitive_factor"] is None

    def test_governance_metadata(self):
        r = analyze(self._route())
        assert r["governance_metadata"]["derivation_type"] == "sensitivity_analysis"


# ---------------------------------------------------------------------------
# calculate_traversal
# ---------------------------------------------------------------------------

from calculate_traversal import analyze_traversal


class TestCalculateTraversal:
    def _orbital_route(self):
        return {"stops": ["Port Olisar", "Covalex Hub Shopp-L4", "Baijini Point"]}

    def _atm_route(self):
        return {"stops": ["Port Olisar", "Hurston", "Covalex Hub Shopp-L4"]}

    def _long_route(self):
        return {"stops": [f"Stop {i}" for i in range(8)]}

    def test_basic_counts(self):
        r = analyze_traversal(self._orbital_route())
        assert r["stop_count"] == 3
        assert r["orbital_stops"] >= 2

    def test_atmosphere_detected(self):
        r = analyze_traversal(self._atm_route())
        assert r["atmosphere_stops"] >= 1
        assert r["atmosphere_burden"] is True
        assert any("atmosphere" in risk for risk in r["risks"])

    def test_chain_collapse_flagged(self):
        r = analyze_traversal(self._long_route())
        assert r["chain_collapse_risk"] is True
        assert any("chain_collapse" in risk for risk in r["risks"])

    def test_no_risks_clean_route(self):
        r = analyze_traversal(self._orbital_route())
        assert r["chain_collapse_risk"] is False
        assert r["atmosphere_burden"] is False

    def test_empty_stops_returns_error(self):
        r = analyze_traversal({})
        assert "error" in r

    def test_suggested_ordering_present(self):
        r = analyze_traversal(self._atm_route())
        assert "suggested_ordering" in r
        assert len(r["suggested_ordering"]) == 3

    def test_atmosphere_moves_to_end(self):
        r = analyze_traversal(self._atm_route())
        # Hurston (atmosphere) should come after orbital stops
        suggestion = r["suggested_ordering"]
        atm_idx = next(i for i, s in enumerate(suggestion) if "hurston" in s.lower())
        orb_idx = next(i for i, s in enumerate(suggestion) if "shopp" in s.lower())
        assert atm_idx > orb_idx

    def test_dead_leg_detection(self):
        route = {"stops": ["Port Olisar", "Shopp-L4", "Baijini", "Port Olisar", "Shopp-L4"]}
        r = analyze_traversal(route)
        assert len(r["dead_leg_candidates"]) > 0

    def test_governance_metadata(self):
        r = analyze_traversal(self._orbital_route())
        assert r["governance_metadata"]["derivation_type"] == "traversal_analysis"

    def test_route_sequence_alias(self):
        r = analyze_traversal({"route_sequence": ["Port Olisar", "Baijini Point"]})
        assert r["stop_count"] == 2


# ---------------------------------------------------------------------------
# bundle_telemetry
# ---------------------------------------------------------------------------

from bundle_telemetry import bundle


class TestBundleTelemetry:
    def _write_telemetry(self, tmpdir: Path, records: list[dict]) -> Path:
        tel_dir = tmpdir / "telemetry"
        tel_dir.mkdir()
        for i, rec in enumerate(records):
            (tel_dir / f"record_{i}.json").write_text(json.dumps(rec), encoding="utf-8")
        return tel_dir

    def test_bundle_creates_zip(self, tmp_path):
        tel = self._write_telemetry(tmp_path, [
            {"ship": "hull-b", "issuer": "covalex", "patch_version": "3.23"},
        ])
        out = str(tmp_path / "out.zip")
        r = bundle(str(tel), out)
        assert r["bundled"] == 1
        assert Path(out).exists()

    def test_zip_contains_manifest(self, tmp_path):
        tel = self._write_telemetry(tmp_path, [{"ship": "hull-b"}])
        out = str(tmp_path / "out.zip")
        bundle(str(tel), out)
        with zipfile.ZipFile(out) as zf:
            names = zf.namelist()
        assert "_BUNDLE_MANIFEST.json" in names

    def test_bundle_multiple_files(self, tmp_path):
        records = [{"ship": "hull-b", "issuer": "covalex"} for _ in range(5)]
        tel = self._write_telemetry(tmp_path, records)
        out = str(tmp_path / "out.zip")
        r = bundle(str(tel), out)
        assert r["bundled"] == 5

    def test_missing_dir_returns_error(self, tmp_path):
        r = bundle(str(tmp_path / "nonexistent"), str(tmp_path / "out.zip"))
        assert "error" in r

    def test_empty_dir_returns_error(self, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        r = bundle(str(empty), str(tmp_path / "out.zip"))
        assert "error" in r

    def test_api_key_redacted(self, tmp_path):
        tel = self._write_telemetry(tmp_path, [{"ship": "hull-b", "api_key": "sk-secret"}])
        out = str(tmp_path / "out.zip")
        bundle(str(tel), out)
        with zipfile.ZipFile(out) as zf:
            content = json.loads(zf.read("record_0.json"))
        assert content.get("api_key") == "[REDACTED]"

    def test_non_sensitive_fields_preserved(self, tmp_path):
        tel = self._write_telemetry(tmp_path, [{"ship": "hull-b", "issuer": "covalex"}])
        out = str(tmp_path / "out.zip")
        bundle(str(tel), out)
        with zipfile.ZipFile(out) as zf:
            content = json.loads(zf.read("record_0.json"))
        assert content["ship"] == "hull-b"


# ---------------------------------------------------------------------------
# build_reproducible_release
# ---------------------------------------------------------------------------

from build_reproducible_release import build_release


class TestBuildReproducibleRelease:
    def _setup_repo(self, tmp_path: Path) -> Path:
        (tmp_path / "tools").mkdir()
        (tmp_path / "tools" / "scorer.py").write_text("# scorer", encoding="utf-8")
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "README.md").write_text("# Docs", encoding="utf-8")
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / "__pycache__" / "scorer.cpython-310.pyc").write_bytes(b"\x00\x01")
        (tmp_path / ".git").mkdir()
        (tmp_path / ".git" / "config").write_text("[core]", encoding="utf-8")
        return tmp_path

    def test_creates_zip(self, tmp_path):
        repo = self._setup_repo(tmp_path)
        out = str(tmp_path / "release.zip")
        r = build_release(str(repo), out)
        assert Path(out).exists()
        assert r["included_count"] > 0

    def test_excludes_git(self, tmp_path):
        repo = self._setup_repo(tmp_path)
        out = str(tmp_path / "release.zip")
        r = build_release(str(repo), out)
        assert all(".git" not in f for f in r["included_files"])

    def test_excludes_pycache(self, tmp_path):
        repo = self._setup_repo(tmp_path)
        out = str(tmp_path / "release.zip")
        r = build_release(str(repo), out)
        assert all("__pycache__" not in f for f in r["included_files"])

    def test_excludes_pyc(self, tmp_path):
        repo = self._setup_repo(tmp_path)
        out = str(tmp_path / "release.zip")
        r = build_release(str(repo), out)
        assert all(not f.endswith(".pyc") for f in r["included_files"])

    def test_includes_py_and_md(self, tmp_path):
        repo = self._setup_repo(tmp_path)
        out = str(tmp_path / "release.zip")
        r = build_release(str(repo), out)
        assert any(f.endswith(".py") for f in r["included_files"])
        assert any(f.endswith(".md") for f in r["included_files"])

    def test_gitignore_patterns_applied(self, tmp_path):
        repo = self._setup_repo(tmp_path)
        (repo / ".gitignore").write_text("*.log\nexports/\n", encoding="utf-8")
        (repo / "debug.log").write_text("log", encoding="utf-8")
        (repo / "exports").mkdir()
        (repo / "exports" / "out.zip").write_bytes(b"data")
        out = str(tmp_path / "release.zip")
        r = build_release(str(repo), out)
        assert all(not f.endswith(".log") for f in r["included_files"])
        assert all("exports" not in f for f in r["included_files"])

    def test_extra_excludes(self, tmp_path):
        repo = self._setup_repo(tmp_path)
        (repo / "secret.key").write_text("key", encoding="utf-8")
        out = str(tmp_path / "release.zip")
        r = build_release(str(repo), out, extra_excludes=["*.key"])
        assert all(not f.endswith(".key") for f in r["included_files"])

    def test_deterministic_order(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        self._setup_repo(repo)
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        out1 = str(out_dir / "r1.zip")
        out2 = str(out_dir / "r2.zip")
        r1 = build_release(str(repo), out1)
        r2 = build_release(str(repo), out2)
        assert r1["included_files"] == r2["included_files"]
