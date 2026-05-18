# sample_multi_stop_route

Hull-B Covalex four-stop route with same-pickup and orbital loop bonuses. The route scores 73/100 (`accept`) by combining a same-pickup bonus (+16) and an orbital loop bonus (+12.6 with Hull-B modifier), partially offset by a stop density penalty (-6). Shows how the orbital loop bonus rewards routes that return through high-traffic orbital stations.

**Command:**
```bash
python tools/deterministic_scorer.py -i your_route.json
```

**Key factors in `sample_output.json`:** `score: 73`, `recommendation: accept`, `score_breakdown` shows `same_pickup`, `orbital_loop`, and `stop_density` factors; `operational_risk: medium`.
