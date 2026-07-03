# What's New in Apeirogon Logistics

This file covers changes that affect how you use the system: updated scoring rules,
new setup options, and anything you need to re-paste or re-configure.

Changes that are purely internal (tooling, CI, developer workflow) are not listed here.

---

## v0.65.1 -- Star Citizen Alpha 4.8.3 compatibility (no action needed)

**The toolkit is now validated against Star Citizen Alpha 4.8.3.** The declared patch compatibility has been updated from Alpha 4.8.0 to Alpha 4.8.3 across the project.

**No re-paste is required.** The instruction block and upload files did not change. Ship availability rules (Hull-D, Hull-E, Merchantman, and Galaxy are still not flyable) and the container size sequence are unchanged in 4.8.3.

**Calibration scope is unchanged.** Scoring weights remain validated against the Hull-B only. All other ships still use heuristic modifiers that have not been in-game verified.

---

## v0.64.6 -- Scoring instruction bug fixes (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.** This entry was added retroactively: the release shipped without a player changelog entry.

**Container breakdown is now calculated correctly.** Minimum qualifying loads were previously calculated assuming that every container is 16 SCU. The freight elevator actually presents a mixed-size container set (32, 16, 8, 4, 2, 1 SCU, player-reported). Rank mode minimum load calculation, output format, route tables, and the DEFERRED list now show actual container breakdowns.

**Your AI will no longer explain how delivery crediting works.** An AI assistant was caught confidently inventing the game mechanic for how containers are credited to contracts from a shared elevator pool. A hard prohibition was added; your AI now presents the three safe handling options without asserting how the game works.

**Same-pickup same-commodity conflicts are now detected.** When two contracts share a pickup location and commodity, the elevator presents an undifferentiated container pool. Your AI now checks for this at contract acceptance and at run plan construction.

**What to do:** Re-paste the instruction block from your platform's SETUP file.

---

## v0.60.1 to v0.64.5 -- Internal releases (no action needed)

These releases covered internal tooling, CI, security hardening, and documentation work: codebase audit fixes, security rule files, version consistency testing, dependency pinning, and pre-release validation. Nothing in them changes how you set up or use your AI. No re-paste or re-upload is required.

---

## v0.59.1 -- Rep grinding ship selection rules (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

**Ship selection is now checked when you activate Covalex rank mode.** If you have not stated your ship, your AI will ask. It will then check your ship against a list of hard disqualifiers before proceeding with run setup.

**Hard disqualifiers applied automatically.** Ramp-loading ships (C2/M2/A2 Hercules, Caterpillar, Starlancer series, Hermes, and others) are flagged as not recommended for rep grinding because ramp loading at freight elevators adds time per stop that compounds across every run. Hull-C is blocked because it cannot land at standard orbital stations when loaded. Non-flyable ships are blocked.

**Hull-B is the confirmed optimal ship** and is approved immediately with no additional checks.

**Railen and Ironclad are flagged as unconfirmed alternatives.** If you want to use either, your AI will ask you to confirm that you have verified freight elevator compatibility, 16 SCU container handling, and pad availability at all four Covalex Senior destinations (Port Tressler, Baijini Point, Seraphim Station, Everus Harbor) in the current patch.

**Ship recommendation decision tree.** If you ask your AI which ship to use for rep grinding, it will walk you through the confirmed-optimal-first decision: Hull-B first, Railen second (if verified), Ironclad third (if verified).

**Scoring modifier suppression in rank mode.** Fragmentation penalty, stop density penalty, and cargo panel clarity bonus are no longer applied in rep grinding mode. These factors are irrelevant for single-leg partial submit and were producing misleading output.

**`COVALEX_RANK_STRATEGY.md` updated** with a new ship selection section covering all disqualifiers, verdicts, and verification requirements. Replace your copy in your AI project uploads.

**What to do:** Re-paste the instruction block from your platform's SETUP file. Replace `COVALEX_RANK_STRATEGY.md` in your AI project uploads.

---

## v0.58.1 -- Audit fixes and player content update (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

**Run size is now calculated automatically in Covalex rank mode.** Previously the system asked "how many contracts do you want in this run?" You now confirm your ship capacity instead, and the system calculates the run cap after analyzing available contracts. It tells you how many minimum qualifying loads fit in your capacity and asks you to confirm or reduce.

**Port Olisar has been removed from all examples.** Port Olisar is no longer in the game. All location examples now use active Stanton stations (Hur-L2, Baijini Point, Everus Harbor).

**Hull-B route playbook updated.** Added COMBINED STOP handling instructions (deliver first, submit contract, then load pickup cargo), route table format reference, and a Covalex rank mode discovery note.

**Ship modifier table corrected.** M2 Hercules Starlifter and C2 Hercules Starlifter were missing fragmentation x1.08 in the GENERALIZED_HAULING_HANDBOOK. Asgard was missing freight x1.03. All corrected.

**What to do:** Open your SETUP file for your platform, copy the instruction block, and re-paste it into your AI project or system prompt. If you use the Hull-B playbook or generalized handbook as uploads, replace those files too.

---

## v0.57.1 -- Rank mode run management (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

Eight live-session fixes to Covalex rank mode:

**Running capacity tracking.** After each accepted contract, your AI shows running total SCU, ship capacity, and remaining capacity. It warns you when capacity is nearly full (under 96 SCU remaining) and hard-blocks further acceptance when capacity is reached.

**Run size confirmed at run start.** The system now asks how many contracts you want before evaluating any contracts. This is the run cap -- your AI will not recommend accepting beyond this number.

**Opportunistic same-location contracts handled.** When a contract's pickup is your current location or a stop already in the run, your AI recalculates total SCU before recommending acceptance and blocks it if adding the contract would exceed capacity.

**COMBINED STOP detection.** When a delivery destination and pickup location are the same, your AI now treats that as a single COMBINED STOP in the route plan (deliver first, submit, then load). These are never split into two separate rows.

**DEFERRED list introduced.** VIABLE contracts that don't fit in the current run are tracked in a DEFERRED list. It is shown at the start of every new run planning cycle so you can include them.

**Declared run target for drop-off consolidation.** You now declare the run target destination at run start. Any contract whose qualifying leg delivers elsewhere is flagged immediately as an outlier rather than discovered after analysis.

**Route table column order fixed.** All route output now uses: Location | Action | Contract | Commodity | Containers. This order is mandatory.

**Current location pickup check.** After confirming run target and size, your AI now asks whether any contracts are available at your current location. Qualifying contracts are flagged as ZERO DEAD LEG PICKUP and factored into capacity before evaluating other contracts.

**What to do:** Re-paste the instruction block from your platform's SETUP file.

---

## v0.56.1 -- Rank mode run plan infrastructure (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

Seven live-session fixes to Covalex rank mode:

**NOT VIABLE contracts fully excluded from downstream.** After the NOT VIABLE output, the contract is never referenced again in capacity totals, run plan, stacking summary, or drop-off checks.

**Multi-commodity contracts handled correctly.** Each commodity-to-destination pair is evaluated independently. If one commodity qualifies alone, only that one is recommended and others are explicitly suppressed with "Do not load [commodity] -- [reason]." Combined qualifiers are listed per-commodity with separate container counts.

**Container counts always shown with minimum loads.** The minimum qualifying SCU is never output alone -- it is always paired with container count and actual loaded SCU (e.g. "3 containers x 16 SCU = 48 SCU").

**Drop-off consolidation check added.** Before run plan construction, your AI checks that all accepted contracts deliver to the run target. Outliers are flagged before the run plan is built.

**Panel separation for outlier contracts.** If you choose to keep a contract that delivers to a non-target destination, your AI asks which panel to assign it to before printing the route.

**Route table format enforced.** Location | Action | Contract | Commodity | Containers column order introduced.

**COMBINED STOP detection introduced.** Locations appearing as both delivery destination and pickup across accepted contracts are identified and handled as combined stops.

**What to do:** Re-paste the instruction block from your platform's SETUP file.

---

## v0.55.1 -- Rank mode viability and multi-commodity fixes (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

**All four blocking fields enforced with exact output format.** In normal scoring mode, the four blocking fields (pickup location, delivery destination, cargo SCU, reward) now each produce a specific request message when UNRESOLVED, rather than a generic flag. In rank mode, reward is non-blocking -- the AI marks it UNRESOLVED and proceeds.

**Multi-commodity leg handling corrected.** When a contract contains multiple commodities, each commodity-to-destination pair is evaluated separately for viability. Previously, commodities were not evaluated independently.

**NOT VIABLE flag on zero-qualifying contracts.** Contracts with no single leg at or above 26% of total SCU now receive a NOT VIABLE output with the highest leg percentage, rather than a partial analysis.

**What to do:** Re-paste the instruction block from your platform's SETUP file.

---

## v0.54.3 -- Covalex rank mode at all ranks (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

**Rank mode now applies at all Covalex ranks, not just Senior to Master.** The 26% threshold and output format are identical regardless of rank. Earlier releases implied the mode was only for Senior-to-Master grinding.

**What to do:** Re-paste the instruction block from your platform's SETUP file.

---

## v0.54.1 to v0.54.2 -- Covalex rank strategy mode introduced (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

**New mode: Covalex rank strategy mode.** Type "covalex rank mode" to activate it. In rank mode your AI uses the partial submission mechanic: delivering at least 26% of a contract's total SCU to a single destination earns Covalex reputation. The AI calculates minimum qualifying loads (with container counts), identifies viable and non-viable contracts, and builds a run plan optimized for reputation grinding rather than credit maximization.

**New upload: `COVALEX_RANK_STRATEGY.md`.** A full player guide to the rank grinding mechanic, contract patterns by rank, and how to stack multiple contracts within your ship capacity. Upload it to your AI project alongside the other files in `player/uploads/`.

**What to do:** Re-paste the instruction block from your platform's SETUP file. Upload `COVALEX_RANK_STRATEGY.md` to your AI project.

---

## v0.53.1 -- Session capability gaps (re-paste your instructions)

**You need to re-paste the instruction block into your AI if you set it up before this version.**

Five session workflow improvements identified from live use:

**Duplicate contract detection.** If you abandon a contract and the same contract (same pickup, commodity, SCU, and leg structure) appears again, your AI immediately flags it: "This is the same contract you just abandoned. Abandon again." No re-analysis.

**Non-flyable ship guard improved.** If you mention a ship not yet in the game (Hull-D, Hull-E, Merchantman, Galaxy), your AI now explicitly tells you it cannot score for that ship in Alpha 4.8.

**Issuer guard improved.** For issuers without calibrated modifiers (Hurston Dynamics, microTech, ArcCorp), your AI tells you explicitly which issuer it is scoring on base weights.

**Timer + stop count warning.** When a contract's timer is 90 minutes or less and you have 3 or more delivery stops total, your AI flags the combination for you to assess. It does not estimate whether you can make it -- that judgment is yours.

**Session start clears all contract and panel state.** Starting a new session fully resets all prior contract data, panel assignments, and phase tracking.

**What to do:** Re-paste the instruction block from your platform's SETUP file.

---

## v0.52.1 -- Cargo tracking overhaul and new edge case guards (re-paste your instructions)

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

## v0.50.1 -- Hallucination guardrails expanded (re-paste your instructions)

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

## v0.42.1 -- Scoring completeness fix (re-paste your instructions)

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

## v0.41.1 to v0.41.6 -- New platform guides and wording fixes

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

## v0.38.1 -- 23 ships and Covalex reputation ranks

Ship coverage expanded from 5 to 23 ships (all 90+ SCU haulers in Alpha 4.8.0).

Covalex reputation ranks added (7 tiers: Trainee through Master) with recommended ships
and strategies for each tier. Three new issuer placeholders added: Hurston Dynamics,
microTech, ArcCorp.

If you use ship_profiles.json as an upload, replace your copy with the updated file from
`uploads/ship_profiles.json`. If you use SHIP_SPECIALIZATION_GUIDE.md, replace that too.

---

## v0.36.1 to v0.36.2 -- Player folder and Alpha 4.8.0

The `player/` folder was introduced in this version. If you were using an earlier version
you were working directly with developer files. Everything is now in `player/`.

Star Citizen patch version updated to Alpha 4.8.0 across all files.
