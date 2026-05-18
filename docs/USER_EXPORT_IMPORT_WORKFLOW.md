# User Export and Import Workflow

How to save your session state at the end of a run and resume from it next time.

---

## Why Export/Import Matters

The scoring tools do not maintain any persistent state themselves. They process inputs and produce outputs each time you run them. If you want continuity across sessions — knowing where you ended, which missions you completed, what reputation level you have — you manage that state yourself using portable JSON files.

This is intentional. Your data is a file you control, not a database you depend on.

---

## The Two State Files

**User profile** (`user_profile.json`): your ship, preferred issuer, home location, reputation levels. Changes infrequently. One per player.

**Session state** (`session_state.json`): active session — current position, completed missions, pending missions, notes. Changes every run.

See `docs/PORTABLE_USER_STATE_GUIDE.md` for the full field reference for each file.

---

## Exporting at Session End

After a run, update your session state file manually:

1. Open your current `session_state.json`.
2. Move the missions you completed from `pending_missions` to `completed_missions`.
3. Update `current_pickup` to your current location.
4. Add any notes from the session.
5. Save the file.

Then validate it:

```bash
python tools/session_state_manager.py -i session_state.json
```

Check for errors in the output. If the session is valid, save it with a dated filename for archiving:

```bash
cp session_state.json hauling-state/patches/Alpha\ 3.23/sessions/2024-01-15.json
```

---

## Importing at Session Start

When starting a new session:

1. Load your user profile to confirm your preferences are current:

```bash
python tools/user_profile_loader.py -i hauling-state/user_profile.json
```

2. If continuing from a previous session, load the most recent session state:

```bash
python tools/session_state_manager.py -i hauling-state/patches/Alpha\ 3.23/sessions/2024-01-15.json
```

3. Update the session state with the current date and a new session ID if starting a fresh session, or continue editing the file if the run is a direct continuation.

---

## Cross-Machine Portability

The state files are plain JSON. To continue a session on a different machine:

1. Copy `user_profile.json` and your latest session state file to the new machine.
2. The scoring tools will work identically — there is no account sync, no cloud state, and no machine-specific data.

---

## Folder Structure

Recommended layout:

```
hauling-state/
  user_profile.json
  patches/
    Alpha 3.23/
      sessions/
        2024-01-15.json
        2024-01-16.json
      telemetry/
        2024-01-15_session_telemetry.json
      OCR_corrections/
  exports/
    telemetry_bundle_1700000000.zip
```

Keep one user profile. Keep one session file per day or per significant run. Archive older session files by patch version so you can look back at what you were doing on a specific patch if needed.

---

## If You Are Using AI for Sessions

If you used AI-assisted extraction during a session, do not save the AI's extraction output as your session state. The session state should contain verified values you confirmed against your screen, not raw AI extraction output.

The AI extraction → normalizer → scorer pipeline produces output files (`missions_norm.json`, scored result). These are pipeline artifacts, not your session state. Your session state is the record of what you accepted, what you completed, and where you ended up.
