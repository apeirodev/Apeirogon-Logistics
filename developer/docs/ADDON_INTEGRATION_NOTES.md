# Addon Integration Notes

**Status:** Planning and research documentation. The addon is a functionality stub
pending CIG's release of a plugin framework for Star Citizen.
**Last reviewed:** 2026-05-26
**Addon code location:** `addon/` (scoring logic complete; all game API calls are stubs)

---

## Overview

The long-term goal is an in-game addon that analyzes contracts in real time as the
player browses the missions terminal, with no screenshots or copy-paste. This
document records what has been researched, what the architecture would look like,
and what external tools are doing the same thing today -- both as reference and
as the baseline for the intermediate companion tool (see Phase 2 below).

---

## Phase 1: CIG Plugin Framework (primary long-term path)

**Dependency:** CIG (Cloud Imperium Games) must release an addon or plugin
framework for Star Citizen. No such framework exists as of Alpha 4.8.0.

When CIG releases the framework, the addon would:
- Read contract data directly from the game's official plugin API
- Render Accept / Defer / Reject scores as an in-game overlay on the contracts panel
- Pull live pricing from UEX or an equivalent source for cross-referencing
- Use the existing deterministic scorer (`developer/tools/deterministic_scorer.py`)
  as the scoring engine, called locally
- Require no screenshots, no copy-paste, no alt-tabbing

**What exists today (`addon/`):**
- Scoring logic is complete and wired to the same weights as the Python tools
- All game API calls are placeholder stubs (e.g. `get_available_contracts()`,
  `get_current_location()`, `render_overlay_panel()`)
- The stub functions document the expected CIG API shape so that when the
  framework is released, integration is a matter of replacing stubs with real calls

**Design constraint:** The addon must use only official CIG plugin framework APIs.
No game memory reading, no DLL injection, no network traffic interception. Anything
that modifies the game client or reads memory outside an official framework violates
RSI's Terms of Service.

---

## Phase 2: OCR Companion Tool (intermediate path, before CIG framework)

Until CIG releases a plugin framework, the realistic intermediate path is a
companion desktop tool that uses OCR to read the contracts terminal from the screen.
This is what the current AI-assistant workflow does manually -- the companion tool
would automate the screen capture step.

### Architecture (Windows companion app)

**Reference implementation:** ArkanisOverlay (https://github.com/ArkanisCorporation/ArkanisOverlay)
- WPF-hosted Blazor application (.NET 8, C#)
- Always-on-top overlay window, activated via keyboard shortcut (e.g. Left Alt + Shift + S)
- No DLL injection, no game memory reading, no game file modification
- Displays community data (UEX prices, location info) while the game is running
- Explicitly excludes automation, cheats, or game-breaking features

This architecture is TOS-compliant because it is a separate desktop application
that observes the screen and displays information in its own window, the same
as any companion app or second monitor.

**OCR screen capture approach:**

The player would:
1. Open the contracts terminal in-game
2. Press the companion tool hotkey
3. The companion captures a screen region (calibrated once at setup)
4. OCR extracts contract fields (issuer, pickup, delivery, cargo, reward, fee, timer)
5. Extracted values are fed to the deterministic scorer
6. Scores and Accept/Defer/Reject recommendations appear in the overlay panel

**Reference for OCR approach:** The existing `developer/tools/local_OCR_preprocessor.py`
and `developer/tools/OCR_result_normalizer.py` already implement the preprocessing
and normalization pipeline. The companion tool would call the same logic, replacing
the current manual screenshot + AI-paste workflow with automated screen capture.

**Key implementation notes for the OCR companion:**
- Screen region calibration must be saved between sessions (the contracts panel
  position may vary by resolution and UI scale)
- Location name fuzzy matching is essential -- OCR frequently misreads station names.
  The existing `developer/data/` location hierarchy is the reference corpus.
- The `unresolved_fields` mechanism already handles OCR failures gracefully -- fields
  that cannot be read are marked UNRESOLVED and surfaced to the player for manual
  entry rather than guessing
- Injection risk check (`check_injection_risk()` in `lib/common.py`) should be applied
  to all OCR-extracted string fields before they reach the scorer

**Planned stack for the companion tool:**
- Python (consistent with the rest of the project) or C# .NET 8 (better Windows
  integration for overlay rendering)
- Screen capture: `mss` (Python) or `BitBlt` (C#)
- OCR: `tesseract-ocr` via `pytesseract` (Python) or a .NET OCR binding
- Overlay rendering: `tkinter` (simple) or a WPF/Blazor window (ArkanisOverlay pattern)
- Pricing: UEX API (`fetch_trade_prices.py`, documented in EXTERNAL_DATA_SOURCES.md)
- Scoring: `deterministic_scorer.py` called as a subprocess or imported as a library

---

## Phase 3: When CIG releases the plugin framework

When CIG releases a framework, the transition from Phase 2 to Phase 1 would be:
1. Replace the OCR screen capture with the official contract data API
2. Replace the companion overlay window with in-game UI rendering (if the framework
   supports it) or keep the companion window if the framework only exposes data
3. The scoring engine and pricing integration remain unchanged
4. The OCR pipeline is retired (but kept in the repo -- useful for players on
   platforms where the addon is not yet available)

---

## External tools in this space

The following community tools have been evaluated as reference implementations.
None are integrated into this project.

### ArkanisOverlay

**URL:** https://github.com/ArkanisCorporation/ArkanisOverlay / https://arkanis.cc/overlay
**Language:** C# .NET 8, WPF-hosted Blazor
**What it does:** In-game companion overlay displaying UEX trade data. MVP stage;
real-time OCR and location-aware features are planned but not yet shipped.
**Relevance:** Primary architectural reference for the Phase 2 companion tool.
The keyboard-shortcut overlay pattern, WPF/Blazor stack, and UEX integration
are all directly applicable.
**TOS posture:** Explicit policy against cheats, automation, or game-breaking features.
No game memory access.

### SC Trade Tools

**URL:** https://sc-trade.tools
**What it does:** Web-based trade route optimizer using UEX pricing data.
**Relevance:** Route optimization algorithm design reference. Not for direct
integration (see EXTERNAL_DATA_SOURCES.md).

### ContractTracker (unverified -- requires confirmation)

**Reported location:** nexusmods.com/starcitizen (verify before citing)
**What it reportedly does:** OCR-based real-time capture of delivery contract
information from the in-game Contract Manager UI. Groups missions by
pickup/dropoff, totals earnings, includes fuzzy location matching.
**Relevance if real:** Direct reference for the Phase 2 OCR implementation.
The calibration workflow, fuzzy matching approach, and F4 retry pattern
(re-scan on OCR failure) are all worth studying.
**Status:** Treat as an unverified lead. Confirm existence and examine
implementation before incorporating into design decisions.

### Game.log parsing

Multiple community tools parse Star Citizen's `Game.log` file to extract
runtime event data. The log is written by the game client during play and
contains telemetry, server events, and some contract state changes.

**Relevance:** Limited. The log does not contain full contract detail (issuer,
cargo type, reward amount). Useful for detecting that the player has arrived
at a location or submitted a contract, not for reading available contracts
at a terminal.

---

## What external APIs cannot provide

No API exists for live contract/mission data. The missions available at a
contracts terminal at a given moment are not exposed by any official or
community API. The only mechanisms that can extract this data are:

1. OCR of the rendered game UI (Phase 2 approach)
2. Official CIG plugin framework (Phase 1, not yet available)
3. Game memory reading -- explicitly excluded as a TOS violation

This is the fundamental constraint that makes the screenshot/AI workflow the
correct current approach, and OCR the correct intermediate approach, until
CIG provides an official integration path.

---

## Environment variables required by the companion tool (future)

| Variable | Purpose |
|---|---|
| `UEX_API_KEY` | Live commodity pricing from UEX (see EXTERNAL_DATA_SOURCES.md) |
| `APEIROGON_OVERLAY_HOTKEY` | Keyboard shortcut to activate overlay (default: not yet decided) |
| `APEIROGON_SCREEN_REGION` | Saved calibration for contracts panel capture region |

---

## Design constraints and non-negotiables

These constraints apply to both Phase 1 and Phase 2 and must not be relaxed:

1. **No game memory reading.** The companion tool observes the screen only.
2. **No DLL injection or game file modification.** Separate process only.
3. **No automation of player actions.** The tool recommends; the player decides
   and clicks. Accept/Defer/Reject are suggestions, not executed actions.
4. **All AI output is advisory_only: true.** Even when contract data is
   extracted automatically, scoring output carries the advisory flag and
   the player confirms before committing.
5. **No external prices overwrite sourced facts.** UEX prices appear as
   cross-references, not as authoritative values. The player's observed
   in-game price is always the primary source.
6. **Hallucination guardrails apply.** Any numeric field not directly read
   from the game UI or user-confirmed must be flagged per AI-03/AI-04 rules.

---

## Version history

- **0.64.2** -- Initial document. Phase 1 (CIG framework), Phase 2 (OCR companion),
  and Phase 3 (transition) documented. External tools evaluated. Design constraints
  and non-negotiables recorded.
