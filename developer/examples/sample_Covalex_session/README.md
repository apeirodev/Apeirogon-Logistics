# sample_Covalex_session

Hull-B Covalex batch with same-pickup stacking. Two missions depart from Port Olisar (same-pickup group), and a third originates from Seraphim Station. The batch tool identifies the Port Olisar stack and surfaces it in `same_pickup_stacking`. All three missions score as `defer` individually but the combined route gains a same-pickup bonus.

**Command:**
```bash
python tools/ingest_mission_batch.py -i your_batch.json
```

**Key factors in `sample_output.json`:** `same_pickup_stacking` shows the Port Olisar group; `suggested_combined_route.same_pickup_bonus` reflects the stacking value; `batch_summary` shows all three missions deferred pending combined-route acceptance decision.
