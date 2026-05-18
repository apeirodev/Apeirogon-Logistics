# Telemetry Privacy Guide

What the project collects, what it does not collect, and how to control your data.

---

## Defaults

| Item | Default |
|------|---------|
| Telemetry contribution | Opt-in — nothing is sent automatically |
| Screenshots | Local only — never uploaded unless you choose to |
| Contributor identity | Optional — you decide what to include |
| API keys | Never requested or stored by the project |
| Personal account information | Never collected |

Nothing leaves your machine unless you explicitly run the bundle and submission steps. The scoring tools are local Python scripts with no network activity.

---

## What Is in a Telemetry Record

A telemetry record typically contains:

- Patch version
- Ship and issuer
- Pickup and delivery location names
- Mission rewards and cargo sizes (as you recorded them)
- Session timing and completion status
- Notes you wrote manually
- Whether OCR values were verified

What is **not** in a telemetry record unless you put it there:
- Your RSI account name
- Your in-game character name
- Any API keys
- Screenshots (the bundle tool includes only JSON files)
- Private chat messages or overlays
- Any information about your real identity

The telemetry schema is purpose-limited: it captures route outcomes, not personal information.

---

## API Keys

The project never asks for API keys, stores API keys, or includes them in any template or schema.

If you use an AI provider for screenshot OCR, your API key is supplied to that provider directly (not through this project). The scoring tools do not handle API keys at all.

If you have accidentally put an API key into a telemetry or session file, the bundle tool will redact any field whose name contains `api_key`, `token`, `secret`, `password`, or `credential`. But check your files before bundling as an additional precaution.

---

## Screenshots

Screenshots of the mission terminal stay local on your machine by default. The bundle tool (`tools/bundle_telemetry.py`) only bundles `.json` files from the `telemetry/` directory — not images.

If you want to share a screenshot as supporting evidence for a telemetry submission (for example, to show a specific UI element or mission offer), you may include it separately. Before sharing any screenshot:

- Crop to only the mission terminal area if possible
- Check that no private chat, account information, or unrelated overlays are visible
- Confirm you are comfortable with the cropped image being public

---

## Sanitization Before Submission

Before submitting a bundle, check each telemetry file for:

1. **Location information** — delivery and pickup location names are not personal. Your home location field in the user profile is personal if it identifies something about you outside the game.
2. **Notes fields** — you write these yourself. Check that nothing in the `notes` field contains information you did not intend to share.
3. **Identifiers** — if you set a `session_id` or `user_profile_id` that includes your real name or RSI handle, consider using a generic identifier instead.

The bundle tool applies automatic redaction for sensitive key names, but the sanitization step is your responsibility for content that is sensitive but has an innocuous key name.

---

## Reviewing a Bundle Before Submission

```bash
python -c "
import zipfile, json
with zipfile.ZipFile('exports/telemetry_bundle.zip') as z:
    for name in z.namelist():
        print('---', name)
        print(z.read(name).decode()[:500])
"
```

This prints the first 500 characters of each file in the bundle. Review each one before submitting.

---

## What Happens After Submission

Submitted telemetry is reviewed by project maintainers and used to validate and calibrate the deterministic scoring heuristics. It is not used to identify individuals, build profiles, or sell data.

Submitted telemetry may be published as anonymized datasets to support the broader Star Citizen hauling community. If you do not want your telemetry published even in anonymized form, note this when submitting.

---

## Opting Out Completely

You never need to submit telemetry. The scoring tools work identically with and without telemetry. If you prefer to use the tool privately with no data sharing, nothing in the workflow requires you to take any action — just do not run the bundle or submission steps.
