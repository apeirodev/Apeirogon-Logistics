# sample_deterministic_only_workflow

Fully deterministic scoring with no AI provider. The user types mission data directly as JSON and pipes it to the scorer — no screenshot, no OCR, no AI. This is the baseline workflow that always remains available regardless of AI provider access.

**Command:**
```bash
echo '{"issuer":"covalex","ship":"hull-b","same_pickup":2,...}' | python tools/deterministic_scorer.py
```

**Key factors in `sample_output.json`:** `score: 82`, `recommendation: accept`, `same_pickup` bonus of 32 points; `governance_metadata.source_class` is `deterministic_output`; no `unresolved_fields`.
