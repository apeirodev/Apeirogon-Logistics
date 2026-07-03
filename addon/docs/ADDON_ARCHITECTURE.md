# Addon Architecture

Design decisions for the Apeirogon Logistics in-game addon.

**All game API surface areas are speculative.** CIG has not published an addon framework as of Alpha 4.8.3. When they do, the stub files will need their `CIG_API.*` placeholder calls replaced with the actual API.

---

## Core Principle: Deterministic-First

The scoring engine runs entirely in Lua with no external dependencies. No internet access, no AI provider call, no Python process required. A player with no API key gets the same deterministic scores as a player with one. The API key only unlocks the optional AI commentary layer.

This means:
- **The addon works offline** (except for AI commentary)
- **The scoring is auditable**: the same weights that power the Python scorer power the Lua scorer
- **The config is shared**: `scoring_config.lua` is a direct translation of `developer/runtime/scoring_config.json`

---

## Two-Layer Architecture

```
Layer 1 -- Deterministic (Lua, local, complete)
  scoring_config.lua   weights, modifiers, thresholds
  scoring_engine.lua   math: base score + factors → verdict
  contract_parser.lua  game data → internal contract format (stub)

Layer 2 -- AI Commentary (HTTP, optional, requires API key)
  api_client.lua       sends contract context to provider, returns plain text
  settings.lua         stores and retrieves the API key securely
```

The layers are independent. Layer 1 runs first. Layer 2 runs after, if an API key is configured, and appends commentary to the overlay panel.

---

## Event-Driven Model

The addon registers handlers for game events. When CIG publishes their addon API, event names will replace the `CIG_API.EVENT.*` placeholders.

Expected events (names speculative):

| Placeholder | Fires when |
|---|---|
| `CIG_API.EVENT.CONTRACTS_TERMINAL_OPENED` | Player opens the mission terminal |
| `CIG_API.EVENT.CONTRACT_SELECTED` | Player highlights a contract |
| `CIG_API.EVENT.CONTRACTS_LIST_UPDATED` | Terminal refreshes (new missions loaded) |
| `CIG_API.EVENT.TERMINAL_CLOSED` | Player exits the terminal |

---

## Contract Data Model

The addon parses game contract data into the same internal format as the Python pipeline. Fields that cannot be read from the game UI are flagged as UNRESOLVED (same rule as the AI screenshot workflow).

```lua
-- Internal contract format (mirrors mission_schema.json)
{
    issuer          = "Covalex",        -- string
    pickup          = "Everus Harbor",  -- string
    delivery        = {"Baijini Point", "Covalex Hub Shopp-L4"},  -- array
    cargo_scu       = 96,               -- number or nil (UNRESOLVED)
    reward_usc      = 42000,            -- number or nil (UNRESOLVED)
    atmosphere_stops = 0,              -- number
    dead_leg        = false,            -- bool
    unresolved_fields = {},             -- list of field names that couldn't be read
}
```

---

## UI Overlay Design

The overlay attaches to the contracts list. For each contract it shows:

```
[ACCEPT 84]  Covalex -- Everus Harbor → Baijini Point
[DEFER  61]  Covalex -- Everus Harbor → Shopp-L4 → Riker Memorial
[REJECT 38]  Red Wind -- MIC-L1 → New Babbage
```

When a player hovers over a contract line:
- Breakdown of top positive and negative factors
- If AI commentary is available, one sentence of analysis
- Stack indicator: "3 contracts share this pickup, accept together for +32"

The overlay panel is configurable:
- Show/hide the numeric score
- Show/hide factor breakdown
- Show/hide AI commentary
- Compact mode (verdict only)

---

## Settings Storage

Settings are stored using CIG's addon settings mechanism (API TBD). Settings include:

| Key | Type | Default | Notes |
|---|---|---|---|
| `ship` | string | "" | Current ship key (e.g., "hull-b") |
| `location` | string | "" | Current location for dead-leg detection |
| `ai_provider` | string | "" | "openai", "anthropic", or "" for none |
| `api_key` | string | "" | Stored securely, never logged |
| `show_score` | bool | true | Show numeric score in overlay |
| `show_factors` | bool | true | Show factor breakdown on hover |
| `show_ai_commentary` | bool | true | Show AI text when available |
| `compact_mode` | bool | false | Show verdict only |

---

## API Key Security

The API key is the only security-sensitive piece of data this addon handles.

Rules (mirror the project's CLAUDE.md security rules, adapted for addon context):
1. The key is never written to a log file or chat output
2. The key is never included in error messages
3. The key is loaded from settings immediately before the API call and not stored in a global variable
4. If the key is missing or invalid, the addon falls back to deterministic-only mode silently, with no error popup that could expose the key in a screenshot

---

## AI Provider Calls

When an API key is configured, the addon sends a compact contract summary to the provider and requests a one-sentence recommendation. The request uses the same STRICT_MODE rules as the screenshot workflow; the AI is instructed not to invent numbers and to defer to the deterministic score.

The AI call is:
- **Non-blocking**: the contract is scored and displayed with deterministic results while the AI call is in flight
- **Cached**: if the same contract appears again in the same session, the cached response is used
- **Optional**: disabling AI commentary does not reduce scoring accuracy

---

## Synchronization with Python Scorer

The Lua and Python scorers must produce identical scores for the same input. To verify:

1. Run a contract batch through the Python scorer (`deterministic_scorer.py`)
2. Run the same input through the Lua scorer (test harness TBD)
3. Compare outputs. Any difference is a bug in one of the two implementations.

When `scoring_config.json` is updated, `scoring_config.lua` must be updated to match. The CI pipeline should eventually include a test that checks both produce the same result on the reference fixture set.
