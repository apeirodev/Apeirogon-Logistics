# sample_manual_copy_paste_workflow

Scoring a mission where the user could only read the pickup location from the terminal; delivery, cargo_scu, and reward_usc are all `UNRESOLVED`. The scorer processes the mission with reduced confidence and penalizes each unresolved field. The output shows a `reject` at 44/100 with a human review warning.

**Command:**
```bash
python tools/ingest_mission_batch.py -i your_batch.json
```

**Key factors in `sample_output.json`:** `governance_metadata.confidence_level` is `low`; `unresolved_field_list` lists three fields; mission `warnings` flag human review requirement; `recommendation: reject` reflects insufficient data to commit.
