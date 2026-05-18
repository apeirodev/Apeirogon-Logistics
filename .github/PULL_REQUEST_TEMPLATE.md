## Summary

<!-- What does this PR do and why? One to three sentences. -->

## Patch Version

<!-- If this PR includes telemetry, config changes, or scoring weight adjustments, which Star Citizen patch is the data from? -->

Patch: 

## Source Classification

<!-- How was the data in this PR obtained? Check all that apply. -->

- [ ] Observed in-game values (sourced fact)
- [ ] Deterministic tool output (reproducible)
- [ ] AI-extracted values (advisory only, validated against screen)
- [ ] Documentation or code change (no data)
- [ ] Bug fix (no new data)

## UNRESOLVED Values Preserved

<!-- Confirm that no fields with uncertain values have been filled with estimates or invented numbers. -->

- [ ] All unconfirmed values are set to `"UNRESOLVED"`, not estimated
- [ ] No numeric values have been sourced from memory, forums, or AI output without screen verification

## Provenance Metadata Included

<!-- For PRs that include JSON data files or tool output: -->

- [ ] All output JSON files include a valid `governance_metadata` block
- [ ] `advisory_only: true` is present on all AI-assisted outputs
- [ ] `patch_era` is set (or `"UNRESOLVED"` if genuinely unknown)
- [ ] `contributor_trust_tier` is appropriate for the source

## Testing

<!-- What did you do to verify this change? -->

- [ ] Ran `python -m pytest tests/` and all tests pass
- [ ] Ran the affected tool manually with a known input and verified output shape
- [ ] Checked `deterministic_hash` reproduces on replay (for scoring changes)

## Notes

<!-- Anything else reviewers should know. -->
