# Apeirogon Logistics: In-Game Addon

**Status: Functionality Stub / Pre-Implementation**

This folder is a placeholder for the future in-game addon for Apeirogon Logistics. CIG (Cloud Imperium Games) has not released any addon or plugin framework for Star Citizen. When they do, this is where the addon will live and will be developed.

The code here is a **functionality stub**: the architecture is designed, the scoring logic is complete and correct, but all game API calls are placeholder stubs that will be replaced when CIG publishes their addon framework specification.

---

## What it will do

When CIG releases an addon framework and this addon is installed, it will:

- Detect when you open the contracts terminal in-game
- Read contract data directly from the game UI (no screenshots needed)
- Score each contract using the same deterministic engine as the current AI assistant version
- Display Accept / Defer / Reject indicators next to each contract in the terminal
- Show a configurable info panel with scores, stacking opportunities, and suggested run order
- Optionally call your AI provider (Claude, OpenAI, or others) for one-sentence commentary per contract

---

## Current state of the code

| File | Status | Notes |
|---|---|---|
| `lua/scoring_engine.lua` | Complete | Deterministic scorer, no game API dependency |
| `lua/scoring_config.lua` | Complete | Scoring weights as Lua tables, synced with `developer/runtime/scoring_config.json` |
| `lua/utils.lua` | Complete | Shared helpers, no game API dependency |
| `lua/settings.lua` | Stub | Settings storage uses `CIG_API.*` placeholders |
| `lua/contract_parser.lua` | Stub | Game contract data reading uses `CIG_API.*` placeholders |
| `lua/ui_overlay.lua` | Stub | UI widgets use `SC_UI.*` placeholders |
| `lua/api_client.lua` | Stub | AI provider HTTP calls use `CIG_API.*` placeholders |
| `lua/main.lua` | Stub | Event registration uses `CIG_API.*` placeholders |
| `ApeirogonLogistics.toc` | Stub | Manifest format follows WoW convention as placeholder |

---

## Architecture overview

```
addon/
  ApeirogonLogistics.toc      -- manifest (format TBD -- WoW-style placeholder)
  docs/
    ADDON_ARCHITECTURE.md     -- design decisions and data flow
    LUA_API_NOTES.md          -- what we expect CIG's Lua API to provide
  lua/
    main.lua                  -- entry point, event registration
    scoring_engine.lua        -- deterministic scorer (COMPLETE)
    scoring_config.lua        -- scoring weights as Lua tables (COMPLETE)
    contract_parser.lua       -- reads game contract data → internal format (STUB)
    ui_overlay.lua            -- in-game overlay and info panel (STUB)
    settings.lua              -- user settings and API key storage (STUB)
    api_client.lua            -- AI provider HTTP calls (STUB)
    utils.lua                 -- shared helpers (COMPLETE)
```

---

## Lua baseline

Written in Lua 5.1, the most common game addon/plugin Lua version (World of Warcraft, FFXIV, ESO, and others). CIG uses Lua extensively in their own game code. If CIG uses LuaJIT, all Lua 5.1 code remains compatible.

**All game API calls use placeholder names** prefixed with `CIG_API.` or `SC_UI.`. These will be replaced with actual CIG addon API calls when the spec is published.

---

## API key security

The addon will store your AI provider API key using CIG's secure addon settings storage. The key will:
- Never be written to a log, chat frame, or error message
- Be loaded only immediately before an API call and not held in global state
- Not be required for deterministic scoring; contracts score locally without any AI call

Deterministic-only mode (no API key) gives you full scores and verdicts. The AI key only adds optional one-sentence commentary per contract.

---

## For developers

When contributing to the addon:

1. Keep `lua/scoring_config.lua` in sync with `developer/runtime/scoring_config.json`: same weights, two languages.
2. Do not add game API calls using guessed CIG function names. All game API interaction belongs in the clearly-marked stub files using the `CIG_API.*` prefix.
3. See `docs/ADDON_ARCHITECTURE.md` for design decisions and `docs/LUA_API_NOTES.md` for a summary of what CIG's addon framework will need to provide.
4. When CIG publishes their addon spec, update `docs/LUA_API_NOTES.md` first with the confirmed API details before touching the stub files.
