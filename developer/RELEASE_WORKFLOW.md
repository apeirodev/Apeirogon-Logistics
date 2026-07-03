# Release Workflow

Step-by-step process for creating and publishing a release.

---

## Pre-Release Checklist

Before generating release artifacts:

1. All tests pass: `python -m pytest tests/`
2. `runtime/scoring_config.json` is calibrated for the target patch
3. `runtime/OCR_normalization_rules.json` includes aliases for any new stations
4. All schema files are in sync with their corresponding tool implementations
5. `CHANGELOG.md` (if present) updated with the release summary
6. Branch is clean: `git status` shows no uncommitted changes

---

## Generating the Release

```bash
# Build the release archive
python tools/build_reproducible_release.py \
  --output releases/apeirogon-logistics-3.24.0.zip

# Generate checksums
python tools/generate_release_checksums.py \
  --release releases/apeirogon-logistics-3.24.0.zip \
  --output RELEASE_CHECKSUMS.sha256

# Verify before publishing
python tools/verify_release_integrity.py \
  --manifest RELEASE_MANIFEST.json
```

The build tool excludes `.git`, `__pycache__`, `*.pyc`, and other non-distributable files. The output is a reproducible archive: the same source tree produces the same zip.

---

## Tagging

After verification:

```bash
git tag -a 3.24.0 -m "Release 3.24.0 -- calibrated for Alpha 3.24"
git push origin 3.24.0
```

Tag names match the Star Citizen patch the scoring config was calibrated for (see `RELEASE_POLICY.md`).

---

## Publishing

Attach the zip and checksum file to the GitHub release. The release description should include:

- Which SC patch the scoring config targets
- Summary of weight or alias changes since the previous release
- Any breaking changes to input/output schemas

---

## Post-Release

After publishing:

1. Update `patch_version` references in example files to the new patch era
2. Archive the previous `scoring_config.json` snapshot to `hauling-state/patches/` if you track calibration history
3. Open a discussion issue for community calibration feedback on the new patch
