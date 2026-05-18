# sample_fragmented_cargo_route

Hull-B Covalex mission with 4 delivery stops — the maximum fragmentation scenario. The fragmentation penalty (-52.8) and stop density penalty (-12.0) drive the score to 0, producing a `reject` recommendation despite the high headline reward (85,000 aUEC). This example illustrates why the scorer rejects high-stop missions even when they pay well.

**Command:**
```bash
python tools/ingest_mission_batch.py -i your_batch.json
```

**Key factors in `sample_output.json`:** `score: 0`, `recommendation: reject`, `score_breakdown` shows both `fragmentation` and `stop_density` penalties; `warnings` flags fragmentation threshold breach.
