# Apeirogon Logistics

A hauling advisor for Star Citizen. Show it your contracts terminal. It tells you what to take, what to skip, and in what order to run them.

Works with Claude, ChatGPT, Gemini, and most other AI assistants. No installation required.

---

## How to use it

**→ Go to the [`player/`](player/) folder and follow the setup file for your AI.**

| Your AI | Setup file |
|---|---|
| Claude (claude.ai) | [`player/project_instructions/SETUP_CLAUDE.md`](player/project_instructions/SETUP_CLAUDE.md) |
| ChatGPT | [`player/project_instructions/SETUP_CHATGPT.md`](player/project_instructions/SETUP_CHATGPT.md) |
| Gemini | [`player/project_instructions/SETUP_GEMINI.md`](player/project_instructions/SETUP_GEMINI.md) |
| Something else | [`player/project_instructions/SETUP_OTHER.md`](player/project_instructions/SETUP_OTHER.md) |

Setup takes about 5 minutes and you only do it once.

---

## Each session

1. Open your AI project
2. Start a new conversation
3. Paste [`player/session_start_prompt.md`](player/session_start_prompt.md) — fill in your ship and location
4. Screenshot your contracts terminal and paste the images in
5. Get your recommendations

---

## What it does

The advisor scores each contract from 0 to 100 and recommends Accept, Defer, or Reject.

It looks at things like:

- **Same-pickup stacking** — two contracts leaving from the same location is worth a lot
- **Orbital vs. atmosphere** — routes that stay in space are more efficient
- **Dead legs** — flying empty to reach a pickup hurts your run
- **Too many drop-off stops** — fragmented deliveries eat your time
- **Ship fit** — some routes suit certain ships better

It won't invent numbers. If it can't read something from your screenshot it will ask you to type that one value. This is intentional — AI assistants regularly make up Star Citizen prices and distances, and that will waste your contracts.

---

## Ships supported

Hull-B · Hull-C · Taurus · Caterpillar · Freelancer MAX · any ship (with reduced scoring precision)

## Mission issuers supported

Covalex · Ling / Ling Family · Red Wind · others (with base scoring)

---

## Licensing

**CC BY-NC 4.0** — all project contents. Attribution required. Non-commercial use only.
Files in `.claude/rules/` retain their original MIT license from [TikiTribe/claude-secure-coding-rules](https://github.com/TikiTribe/claude-secure-coding-rules).
See [`LICENSES.md`](LICENSES.md) for full details.

---

## For developers and contributors

The scoring tools, test suite, schemas, and documentation are in [`developer/`](developer/).

The deterministic Python scorer runs without any AI — useful if you want full auditability, batch processing, or to tune the scoring weights. See [`developer/docs/`](developer/docs/) to get started.

Contributions welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

**Maintainer:** ApeiroDev · apeirogon.gg · v0.37.1
