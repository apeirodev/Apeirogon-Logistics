# Telemetry Submission Workflow

How to package and submit telemetry data. Submission is always opt-in.

---

## Before You Submit

Telemetry should only be submitted after you have:

1. Recorded patch version, ship, and issuer for every session
2. Verified that OCR-sourced values are marked with `ocr_verified: true` only when you actually checked them against your screen
3. Removed any personal information you do not want to share (account names, private chat content, identifiers)
4. Reviewed the bundle contents yourself

See `docs/TELEMETRY_COLLECTION_WORKFLOW.md` for how to record telemetry during a session.

---

## Validate Your Telemetry Files

Run the validation tool on each file before bundling:

```bash
python tools/telemetry_ingestion_pipeline.py -i telemetry/my_session.json
```

Check the output for:
- `"accepted": true`: the record passed validation
- `errors: []`: no blocking errors
- `warnings`: non-blocking issues; decide whether to fix them

Common validation issues and fixes:
- `missing required field: ship`: add `"ship": "hull-b"` (or your actual ship) to the record
- `patch_version unresolved`: add `"patch_version": "Alpha 4.8.0"` (or current patch)
- `cargo_scu exceeds plausible threshold`: check that you did not accidentally enter a value in the wrong units

---

## Bundle Your Telemetry

Bundle all validated telemetry files from the telemetry directory:

```bash
python tools/bundle_telemetry.py --input-dir telemetry/ --output exports/telemetry_bundle.zip
```

The bundle tool:
- Scans the `telemetry/` directory for `.json` files
- Sanitizes each file (removes fields containing `api_key`, `token`, `secret`, `password`)
- Creates a bundle manifest inside the zip
- Writes the zip to your specified output path

You can inspect the zip contents before submitting:

```bash
python -c "import zipfile; z=zipfile.ZipFile('exports/telemetry_bundle.zip'); print(z.namelist())"
```

---

## Review Before Submitting

Open the zip and check:

- `_BUNDLE_MANIFEST.json`: lists every file included and their key fields
- Each telemetry file — confirm it contains only what you intended to share

Check specifically:
- No location information that identifies you personally
- No screen captures of private chat
- No account names or personal identifiers you did not intend to include
- No fields you did not want to share

---

## Submit

Submit via the current contribution channel listed in the project's GitHub repository. The exact submission method may change over time — check the repository for current instructions.

When submitting, include:
- The bundle zip file
- The Star Citizen patch version covered by the bundle
- Which ship and issuer the sessions used (also in the bundle manifest, but helpful to note)
- Any known issues with the data (unverified OCR fields, aborted runs, server instability)

---

## Privacy Defaults

| Default | Setting |
|---------|---------|
| Telemetry contribution | Opt-in only — nothing sent automatically |
| Screenshots | Local only by default |
| Contributor identity | Optional |
| API keys | Never collected |

You are never required to submit. The project works without any telemetry. Submission helps calibrate future scoring but is entirely voluntary.
