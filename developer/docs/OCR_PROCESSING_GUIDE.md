# OCR Processing Guide

How the OCR normalization pipeline works, when to use it, and how to fix common problems.

---

## What OCR Processing Does

The OCR normalizer (`tools/OCR_result_normalizer.py`) takes raw extraction output, either from an AI provider reading a screenshot or from a manual copy-paste, and:

1. Resolves location aliases (e.g. "Shopp-L4" → "Covalex Hub Shopp-L4")
2. Resolves issuer aliases (e.g. "cov alex" → "Covalex")
3. Normalizes delivery fields to lists
4. Marks fields that could not be resolved as UNRESOLVED
5. Adds governance metadata tracking provenance

The output of the normalizer is what you pass to `ingest_mission_batch.py`.

---

## Two Input Modes

### AI Vision Mode

When the input contains a `"missions"` array or has `"source_class": "ai_vision_extraction"`, the normalizer processes it as structured AI output:

```bash
python tools/OCR_result_normalizer.py -i raw_extraction.json -o missions_norm.json
```

The input should be the JSON the AI returned after reading your screenshot.

### Raw OCR Mode

When the input is unstructured text extracted from OCR (no `"missions"` key), the normalizer applies regex-based field extraction and alias resolution.

---

## Alias Resolution

Aliases are defined in `runtime/OCR_normalization_rules.json`. The file contains:

- `issuer_aliases`: common misspellings and variants → canonical issuer name
- `location_aliases`: partial names and OCR variants → full canonical location name

Examples already defined:
- `"Shopp-L4"` → `"Covalex Hub Shopp-L4"`
- `"Baijini"` → `"Baijini Point"`
- `"Tressler"` → `"Port Tressler"`
- `"cov alex"` → `"Covalex"`
- `"ling family"` → `"Ling Family"`

### Adding a Missing Alias

If a location or issuer is not resolving correctly:

1. Open `runtime/OCR_normalization_rules.json`.
2. Find the `location_aliases` or `issuer_aliases` block.
3. Add an entry: `"ocr variant": "Canonical Name"`.
4. Save the file; changes take effect immediately.

Example:
```json
"location_aliases": {
  "Shopp-L4": "Covalex Hub Shopp-L4",
  "your-new-variant": "Full Canonical Location Name"
}
```

---

## Handling UNRESOLVED Fields

When a field cannot be resolved from the extraction, the normalizer sets it to `"UNRESOLVED"`. This propagates to the scorer, which applies a -2 penalty per unresolved field (capped at -12).

Common reasons for UNRESOLVED:
- Reward or fee was not visible in the screenshot
- Location name did not match any alias
- OCR read the field but it was ambiguous

To fix: add the correct value manually to the normalized JSON before scoring, or re-extract from a clearer screenshot.

---

## Verifying the Normalizer Output

Before running the batch scorer, open `missions_norm.json` and check:

- Every `pickup` field matches your in-game pickup location
- Every `delivery` field is a list of the correct locations
- `reward_usc` is a number, not UNRESOLVED; if UNRESOLVED, check the original screenshot
- No locations appear that were not in your terminal

If anything looks wrong, fix it in the JSON before running the scorer. The normalizer output is a plain JSON file you can edit directly.

---

## Confidence Threshold

The normalizer applies a minimum confidence threshold (default: 0.65, configurable in `OCR_normalization_rules.json` under `ocr_ambiguity_handling.minimum_confidence_threshold`). Extractions below this threshold are flagged in warnings.

If you are getting many low-confidence warnings:
- Use a higher-resolution screenshot
- Increase in-game UI scale before screenshotting
- Crop the screenshot to show only the mission terminal

---

## Full Pipeline

```bash
# Step 1: AI extracts from screenshot (see ChatGPT_usage_guide.md or Claude_usage_guide.md)
# Save AI output as raw_extraction.json

# Step 2: Normalize
python tools/OCR_result_normalizer.py -i raw_extraction.json -o missions_norm.json

# Step 3: Score
python tools/ingest_mission_batch.py -i missions_norm.json
```

If you entered mission data manually (no screenshot), skip steps 1 to 2 and run the batch scorer directly on your manually-written JSON.
