# sample_dead_leg_recovery

Red Wind batch showing dead-leg rejection. The first mission requires flying from the current position to MIC-L1 before pickup — a dead leg — and scores `reject` (34/100). The second mission at Baijini Point scores `defer`. This example shows how the dead-leg penalty drives the scorer to discard the Red Wind mission and focus on the closer pickup.

**Command:**
```bash
python tools/ingest_mission_batch.py -i your_batch.json
```

**Key factors in `sample_output.json`:** First mission in `ranked_missions` has `recommendation: reject` with `score_breakdown.dead_leg: -16.5`; second mission defers; `batch_summary` shows 1 rejected, 1 deferred.
