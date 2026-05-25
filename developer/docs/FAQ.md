# Frequently Asked Questions

## What does this tool actually do?

It helps you decide which hauling missions to accept and in what order to run them.
You give it your mission list (by typing it in or using AI to read a screenshot),
and it scores each mission based on route efficiency factors: same-pickup stacking,
dead-leg risk, cargo fragmentation, issuer modifiers, and ship suitability.

It tells you: accept, defer, or reject. You make the final call.

---

## Do I need to know how to code?

No. You type commands in a terminal and copy-paste JSON. If you can open a command
prompt and copy text, you can use this tool.

The setup guide is at `docs/GETTING_STARTED.md`.

---

## What is Python and do I need it?

Python is a programming language. You need version 3.10 or newer installed to run
the tools. You don't need to write any Python; you just need it installed.

Download from https://www.python.org/downloads/ (get the latest 3.x release).
On Windows, tick "Add Python to PATH" during installation.

---

## What does the score number mean?

| Score | Recommendation | What it means |
|-------|---------------|---------------|
| 70 to 100 | **accept** | Good route, worth taking |
| 45 to 69 | **defer** | Marginal, consider combining with other missions |
| 0 to 44 | **reject** | Poor route, avoid unless no alternatives |

The score starts at 50 and goes up or down based on factors like same-pickup
stacking (+16 per match), dead-leg risk (-15), cargo fragmentation (-12), and
ship/issuer modifiers.

These are heuristics based on Star Citizen hauling patterns, not guaranteed outcomes.
Server conditions, player traffic, and cargo availability change what actually happens.

---

## What is "same-pickup stacking"?

When two or more missions share the same pickup location, you can load cargo for
all of them in one stop. This is the most valuable efficiency gain in Hull-B hauling.

The scoring system adds +16 points for each additional mission sharing a pickup.
Two missions from Hur-L2 score 16 points higher than two separate pickups.

---

## What is a "dead leg"?

A route segment with no cargo. You fly from delivery point A to pickup point B
empty, burning fuel and time without earning anything. The scoring system
penalizes dead legs by -15 points.

---

## What is "cargo fragmentation"?

When deliveries are spread across many different destinations, each requiring
a separate stop. High fragmentation means more unloading complexity and more
stops per run. The scoring system penalizes fragmentation by -12 points.

---

## Why does the score change based on my ship?

Different ships have different operational profiles. The Hull-B has modifiers
that boost `cargo_panel_clarity` (+15%), `fragmentation` (+10%), and
`freight` (+5%) because its external spindle layout makes managing large
fragmented cargo loads more complex than internal-cargo ships.

You can customise all ship modifiers in `runtime/scoring_config.json`.

---

## Why do I need an AI account (ChatGPT, Claude, Gemini)?

You don't need AI; the scoring tool works without it. If you type your mission
details by hand, you get a full score without touching any AI.

The AI is only needed for OCR: reading your mission screenshots and turning
them into structured data. If you prefer to type your missions manually,
skip the AI steps entirely.

---

## The AI made up numbers that weren't on my screen. What do I do?

This is the most important known problem. AI assistants hallucinate
Star Citizen data more than 50% of the time without strict constraints.

**Always paste the strict session prompt before asking the AI anything.**
The prompt is at `prompts/STRICT_AI_SESSION_PROMPT.md`.

If the AI still invents numbers, paste this re-anchor:
> "You invented that number. I did not provide it. Remove it and replace it
> with UNRESOLVED."

See `docs/HALLUCINATION_GUARDRAILS.md` for the full explanation.

---

## What is "UNRESOLVED"?

A field that was not supplied or could not be read. The scoring system
handles UNRESOLVED fields gracefully; they are excluded from calculations
and flagged in the output. An UNRESOLVED field is safer than an invented number.

---

## Does the score account for current prices?

No. The scoring system does not know current commodity prices. It scores
route efficiency (stacking, dead legs, fragmentation) based on what you provide.
If you supply `reward_usc` from your screen, that value is used. If not, it is UNRESOLVED.

Never let the AI fill in prices from its training data. They will be wrong.

---

## Does this work offline?

Yes. The scoring tool runs entirely on your computer. No internet connection is
required for scoring. The AI OCR step requires internet (to reach the AI provider),
but you can skip it and type missions manually.

---

## What is the Hull-B's cargo capacity?

This tool does not store patch-specific Hull-B capacity because it changes.
Check your in-game ship loadout screen for the current value and supply it
when using AI OCR extraction.

Data from training memory is unreliable. Your loadout screen is authoritative.

---

## Can I use this with other ships?

Yes. The tool has built-in modifiers for Hull-B, Hull-C, Constellation Taurus,
Freelancer MAX, and Caterpillar. Pass `"ship": "hull-c"` (or whatever ship you use)
in your route input and the appropriate modifiers are applied.

To add your own ship modifiers, edit `runtime/scoring_config.json`.

---

## Can I change the scoring weights?

Yes. All weights and thresholds are in `runtime/scoring_config.json`. Edit that
file to tune the scoring to match your playstyle. No code changes needed.

---

## What is "advisory only"?

Every output from the AI is tagged `"advisory_only": true`. This means the
AI's recommendation is a suggestion, not a command. Your in-game judgment,
real-time server conditions, and current market prices override the score.

The scoring tool's own output is also advisory; it tells you what patterns
historically work well, not what will definitely work right now.

---

## Something is wrong with the output / the tool crashed. Where do I get help?

Check `docs/KNOWN_ISSUES.md` for known problems and workarounds.

Report issues at the project's GitHub repository.
