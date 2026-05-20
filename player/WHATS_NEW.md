# What's New in Apeirogon Logistics

This file covers changes that affect how you use the system: updated scoring rules,
new setup options, and anything you need to re-paste or re-configure.

Changes that are purely internal (tooling, CI, developer workflow) are not listed here.

---

## v0.52.1 — Cargo tracking overhaul and new edge case guards (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

A full live test session was run and the AI's failures were logged and fixed. These rules are now in the instruction block and the AI will follow them without you having to ask:

**Separate LOADED and PENDING PICKUP tables.** Your AI now maintains two distinct tables. LOADED is cargo confirmed on the ship. PENDING PICKUP is panels assigned to contracts where the pickup has not happened yet. They are never merged. A panel only moves from PENDING PICKUP to LOADED when you say so -- screenshots do not count as confirmation.

**SCU totals derived from source contracts, never accumulated.** If the AI showed 137 SCU last response and you add a 9 SCU contract, it does not just write 146 -- it re-derives the total from every contract's original data. Drift between responses is now flagged immediately.

**One destination per panel, enforced without asking.** The AI will never propose mixing two delivery destinations on the same panel.

**Drop-before-pickup enforced in all route output.** When a panel delivers and then loads new cargo at a later stop, the AI will always sequence the delivery first and pickup second. It flags this dependency in the state table every time that panel appears.

**Response format standardized.** When you paste an accepted contract for loading, the AI shows: (1) contract fields from the screenshot, (2) which of your existing panels already cover these destinations, (3) panel assignment for this contract only. The full state table is shown only when you ask, or when a conflict makes it necessary.

**Session phase tracking.** The AI tracks whether you are PRE-DEPARTURE, IN-TRANSIT, AT-DESTINATION, or RETURNING. It will not describe events from a phase you have not confirmed.

**Number format normalization.** "4,608 SCU" is read as 4608. "1.5M aUEC" is read as 1500000. "50 SCU x 4 containers" is read as 200 SCU total. The AI will confirm the normalized value with you.

**Session start clears panel state.** Starting a new session now clears all panel assignments, not just contract data. If you start a session with cargo already on your ship, tell your AI each loaded panel before continuing.

**Ship switch handling.** If you switch ships mid-session, your AI clears all panel assignments and asks you to re-declare panel names for the new ship.

**Dropped contract with loaded cargo.** If you drop a contract after its cargo is already loaded, the AI will flag those panels as ORPHANED and ask what happened to that cargo -- it will not silently delete the entries.

**No unprompted state dumps.** If you ask a simple question, you get a direct answer. The AI will not re-run the full state table every time you ask which panel holds a specific commodity.

Also in this update: non-flyable ship guard (Hull-D, Hull-E, Merchantman, Galaxy), placeholder issuer guard (Hurston Dynamics, microTech, ArcCorp), ship modifier table expanded to 19 flyable ships, and atmosphere weight override removed from documentation.

**What to do:** Open your SETUP file for your platform, copy the instruction block, and re-paste it into your AI project or system prompt.

---

## v0.50.1 — Hallucination guardrails expanded (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

Five new rule sections were added to the instructions. Without re-pasting, your AI has no
constraints against the following failure modes:

**Atmosphere and congestion status from training data.** The AI will claim a route is fully
orbital, or that a station is congested, based on its outdated training knowledge. Both are
now explicitly player-reported only. If the screenshot does not show it, the AI must ask
rather than infer.

**Ship cargo capacity from training data.** If you ask whether your cargo fits, the AI will
give a confident SCU number from its training. Capacity changes between patches. The AI is
now instructed to tell you to check your in-game loadout screen instead.

**Contract field confusion.** The AI can misread which field is reward vs fee vs collateral
on the contracts terminal. The new CONTRACT READING section requires the AI to identify and
show all fields before scoring, and to flag when a field is unclear.

**Session state drift.** In long sessions the AI mixes up contracts from different messages.
The new SESSION STATE section requires the AI to expire all prior contract data when a new
session starts, and to track Available / Accepted / Delivered states explicitly.

**Travel time and profit-per-hour estimates.** The AI now knows not to give these. They are
not scoring inputs and the numbers are always invented.

Also in this version: Hull-B cargo panel quadrant rules were added (v0.49.1) and the session
start prompt was embedded inline in all SETUP files (v0.48.1). If you set up before v0.49.1,
re-pasting covers all of these at once.

**What to do:** Open your SETUP file for your platform, copy the instruction block, and
re-paste it into your AI project or system prompt.

---

## v0.42.1 — Scoring completeness fix (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

Two scoring factors were missing from the instructions in every platform guide. They existed
in the scoring engine but were not included in the text you paste to your AI:

- **Cargo panels assign cleanly to each delivery destination: +8 (x1.15 for Hull-B)**
  This bonus applies when cargo can be loaded by destination at the elevator, so each stop
  is a clean unload from one panel. Hull-B players get a slightly higher bonus.

- **Complex unloading sequence at destination: -7**
  Applies when the unloading order at a stop is complicated or likely to cause confusion.

The UNRESOLVED penalty cap was also missing from the text. The correct rule is:
**-2 per unreadable field, maximum -12 total** (not unlimited -2 per field).

The Hull-B SHIP ADJUSTMENTS line was updated to explicitly mention the cargo panel clarity
bonus (x1.15) alongside the other Hull-B modifiers.

**What to do:** Open your SETUP file for your platform, copy the instruction block, and
re-paste it into your AI project or system prompt. For Claude Projects and ChatGPT Projects,
update the project instructions. For Perplexity and LM Studio, paste the updated block at
the start of your next session.

---

## v0.41.1 to v0.41.6 — New platform guides and wording fixes

Added dedicated setup guides for three new platforms:
- **Microsoft Copilot** (see `project_instructions/SETUP_COPILOT.md`)
- **Perplexity** (see `project_instructions/SETUP_PERPLEXITY.md`)
- **LM Studio and Ollama** (see `project_instructions/SETUP_LMSTUDIO.md`)

Minor wording fixes across all guides:
- "Covalex issuer alignment: +9" wording clarified (was "Covalex issuer: +9 extra for alignment")
- Hull-B freight multiplier notation simplified in the bad factors line
- Em dashes and en dashes removed throughout (plain punctuation only)

No scoring logic changed in these versions. If your setup was working, it still works.

---

## v0.38.1 — 23 ships and Covalex reputation ranks

Ship coverage expanded from 5 to 23 ships (all 90+ SCU haulers in Alpha 4.8.0).

Covalex reputation ranks added (7 tiers: Trainee through Master) with recommended ships
and strategies for each tier. Three new issuer placeholders added: Hurston Dynamics,
microTech, ArcCorp.

If you use ship_profiles.json as an upload, replace your copy with the updated file from
`uploads/ship_profiles.json`. If you use SHIP_SPECIALIZATION_GUIDE.md, replace that too.

---

## v0.36.1 to v0.36.2 — Player folder and Alpha 4.8.0

The `player/` folder was introduced in this version. If you were using an earlier version
you were working directly with developer files. Everything is now in `player/`.

Star Citizen patch version updated to Alpha 4.8.0 across all files.
