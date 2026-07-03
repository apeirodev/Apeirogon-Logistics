# sample_provider_neutral_workflow

Demonstrates that the scoring pipeline is provider-neutral: the same JSON input produces the same deterministic output regardless of which AI provider (or none) the user has access to. Input is a manually constructed route with same-pickup stacking; output is identical to any AI-assisted workflow that produces the same normalized JSON.

**Command:**
```bash
python tools/deterministic_scorer.py -i your_route.json
```

**Key factors in `sample_output.json`:** `score: 82`, `recommendation: accept`; `governance_metadata.source_class` is `deterministic_output`; the provenance does not mention any AI provider because none was involved; `deterministic_hash` is reproducible from the same input.
