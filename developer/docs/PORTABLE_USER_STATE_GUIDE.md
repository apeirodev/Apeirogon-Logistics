# Portable User State Guide

Your user profile and session state are local JSON files that you control. This guide covers what they contain, how to manage them across sessions, and how to use them with the tools.

---

## What User State Is

Two files carry your persistent data between sessions:

**`portable_user_profile.json`** — your preferences and context: preferred ship, preferred issuer, home location, reputation levels. This changes infrequently.

**`hauling_session_state.json`** — the current session: active missions, completed missions, current position, notes. This changes every run.

Neither file is required. The scoring tools work without them. They become useful when you want session continuity — knowing where you ended last time, which missions you completed, and what reputation you have with which issuer.

---

## User Profile Format

Minimal profile:

```json
{
  "user_profile_id": "my-profile-001",
  "preferred_ship": "hull-b",
  "preferred_issuer": "covalex",
  "home_location": "Port Olisar"
}
```

Optional fields:

```json
{
  "user_profile_id": "my-profile-001",
  "preferred_ship": "hull-b",
  "preferred_issuer": "covalex",
  "home_location": "Port Olisar",
  "patch_version": "Alpha 4.8.0",
  "reputation": {
    "covalex": 450,
    "ling family": 120
  },
  "notes": "Focused on Stanton orbital loops"
}
```

Validate your profile:

```bash
python tools/user_profile_loader.py -i my_profile.json
```

The loader will flag missing recommended fields and warn about unknown ships or issuers.

---

## Session State Format

Minimal session state:

```json
{
  "session_id": "session-2024-001",
  "ship": "hull-b",
  "issuer": "covalex",
  "patch_version": "Alpha 4.8.0"
}
```

Extended example:

```json
{
  "session_id": "session-2024-001",
  "ship": "hull-b",
  "issuer": "covalex",
  "patch_version": "Alpha 4.8.0",
  "session_start_epoch": 1700000000,
  "current_pickup": "Port Olisar",
  "completed_missions": [
    {"pickup": "Port Olisar", "delivery": "Covalex Hub Shopp-L4", "reward_usc": 12500}
  ],
  "pending_missions": [],
  "notes": "Good server tonight, elevator wait under 1 minute"
}
```

Validate your session state:

```bash
python tools/session_state_manager.py -i session_state.json
```

---

## Managing Files Across Sessions

Suggested folder structure:

```
hauling-state/
  user_profile.json
  patches/
    Alpha 4.8.0/
      sessions/
        2024-01-15.json
        2024-01-16.json
      telemetry/
      OCR_corrections/
  exports/
```

At session start:
1. Load your profile: `python tools/user_profile_loader.py -i hauling-state/user_profile.json`
2. Load your most recent session state if continuing: `python tools/session_state_manager.py -i hauling-state/patches/Alpha\ 3.23/sessions/2024-01-15.json`

At session end:
1. Update your session state JSON with completed missions.
2. Save it with today's date.

---

## What the Tools Do With Profile Data

The profile and session state are inputs you can reference manually — the tools do not automatically load them. When you run the scorer, you pass ship and issuer directly in your mission JSON. The profile is a convenient record, not an automatic config loader.

If you want ship and issuer defaults applied without typing them every time, include them in your mission input templates or write a small shell alias that prepopulates the fields from your profile.

---

## Portability

Both files are plain JSON. You can:
- Copy them to another machine and continue from where you left off.
- Open them in any text editor.
- Back them up alongside your game screenshots.
- Share session state files when reporting a route outcome for community telemetry.

There is no account system, no cloud sync, and no lock-in. The files are yours.
