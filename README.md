# Apeirogon Logistics

A hauling advisor for Star Citizen. Show it your contracts terminal. It tells you which contracts to take, how to stack them, and where to place cargo on your ship so every stop is a clean unload.

Works with Claude, ChatGPT, Gemini, Copilot, Perplexity, LM Studio, Ollama, and most other AI assistants. No installation required.

---

## How to use it

**→ Go to the [`player/`](player/) folder and follow the setup file for your AI.**

| Your AI | Setup file |
|---|---|
| Claude (claude.ai) | [`player/project_instructions/SETUP_CLAUDE.md`](player/project_instructions/SETUP_CLAUDE.md) |
| ChatGPT | [`player/project_instructions/SETUP_CHATGPT.md`](player/project_instructions/SETUP_CHATGPT.md) |
| Gemini | [`player/project_instructions/SETUP_GEMINI.md`](player/project_instructions/SETUP_GEMINI.md) |
| Microsoft Copilot | [`player/project_instructions/SETUP_COPILOT.md`](player/project_instructions/SETUP_COPILOT.md) |
| Perplexity | [`player/project_instructions/SETUP_PERPLEXITY.md`](player/project_instructions/SETUP_PERPLEXITY.md) |
| LM Studio / Ollama (local AI) | [`player/project_instructions/SETUP_LMSTUDIO.md`](player/project_instructions/SETUP_LMSTUDIO.md) |
| Something else | [`player/project_instructions/SETUP_OTHER.md`](player/project_instructions/SETUP_OTHER.md) |

Setup takes about 5 minutes and you only do it once.

---

## Each session

1. Open your AI project
2. Start a new conversation
3. Paste [`player/session_start_prompt.md`](player/session_start_prompt.md) and fill in your ship and location
4. Screenshot your contracts terminal and paste the images in
5. Get your recommendations

---

## What it does

Apeirogon Logistics helps you plan your haul before you commit to it: which contracts to take, how to stack them, and where to physically place cargo on your ship so each stop is a clean unload rather than a hunt through mixed boxes.

For example: if you take ten Member-rank Covalex contracts with shared pickups and three drop-offs each, it will tell you which panel on your Hull-B to load each destination's cargo onto as it comes up the freight elevator. When you arrive at CRU-L1, you focus one panel, unload everything on it, and leave. No sorting mid-route, no cross-referencing contracts, no guessing which boxes go where.

It scores each contract from 0 to 100 and recommends Accept, Defer, or Reject. It also looks at route order, same-pickup stacking, dead legs, and whether your ship suits the cargo. It won't invent numbers. If it can't read something from your screenshot it will ask you rather than guess.

---

## Ships supported

23 ships with 90+ SCU capacity, including Hull-B through Hull-E, C2/M2/A2 Hercules, Caterpillar, Ironclad, Railen, Hermes, RAFT, Starlancer MAX, and more. See [`player/uploads/SHIP_SPECIALIZATION_GUIDE.md`](player/uploads/SHIP_SPECIALIZATION_GUIDE.md) for the full list and per-ship advice.

## Mission issuers supported

Covalex (all 7 reputation ranks) · Ling / Ling Family · Red Wind · Hurston Dynamics · microTech · ArcCorp · others (with base scoring)

---

## Licensing

**CC BY-NC 4.0**: all project contents. Attribution required. Non-commercial use only.
Files in `.claude/rules/` retain their original MIT license from [TikiTribe/claude-secure-coding-rules](https://github.com/TikiTribe/claude-secure-coding-rules).
See [`LICENSES.md`](LICENSES.md) for full details.

---

## What's coming: in-game addon

The long-term goal is an **in-game addon** that analyzes contracts in real time as you browse the missions terminal, with no screenshots or copy-paste. You'd see contract scores and recommendations overlaid directly in the game UI.

**This requires CIG (Cloud Imperium Games) to release an addon or plugin framework for Star Citizen.** No such framework exists as of Alpha 4.8.0. The addon code lives in [`addon/`](addon/) and is currently a functionality stub: the scoring logic is complete, but all game API calls are placeholders pending CIG's spec. When CIG releases the framework, Apeirogon Logistics will:

- Let you connect your own API key for OpenAI, Claude, or another provider
- Show Accept / Defer / Reject indicators on contracts as you scroll the terminal
- Display a configurable info panel with scores, best combinations, and run order
- Work entirely within the game, with no alt-tabbing or screenshots needed

The current AI assistant workflow continues to work alongside it. Nothing about the existing setup changes.

---

## For developers and contributors

The scoring tools, test suite, schemas, and documentation are in [`developer/`](developer/).

The deterministic Python scorer runs without any AI, useful if you want full auditability, batch processing, or to tune the scoring weights. See [`developer/docs/`](developer/docs/) to get started.

Contributions welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

**Maintainer:** ApeiroDev · v0.61.2
