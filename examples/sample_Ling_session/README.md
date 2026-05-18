# sample_Ling_session

Taurus Ling Family batch with same-pickup stacking at HUR-L1. Both missions share the same pickup, giving a stacking opportunity. The Taurus is suited for smaller Ling cargo sizes and lighter atmosphere routes. This example demonstrates using a non-Hull-B ship with the batch scorer.

**Command:**
```bash
python tools/ingest_mission_batch.py -i your_batch.json
```

**Key factors in `sample_output.json`:** `same_pickup_stacking` shows HUR-L1 as a stack group; `batch_summary.ship` is `taurus`; `suggested_combined_route` reflects the two-mission stack bonus.
