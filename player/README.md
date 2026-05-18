# Apeirogon Logistics — Player Files

This folder contains everything you need to use Apeirogon Logistics with your AI.

---

## Two things, used differently

**`project_instructions/`** — Set up once. These are the instructions you load into your AI so it knows how to score hauling contracts. You do this one time when you create your AI project.

**`session_start_prompt.md`** — Use every session. Paste this at the start of every hauling session to tell the AI which ship you're flying and where you are.

---

## Pick your AI and follow the setup file

| Your AI | File to open |
|---|---|
| Claude (claude.ai) | `project_instructions/SETUP_CLAUDE.md` |
| ChatGPT | `project_instructions/SETUP_CHATGPT.md` |
| Gemini | `project_instructions/SETUP_GEMINI.md` |
| Something else | `project_instructions/SETUP_OTHER.md` |

---

## After setup, every session works like this

1. Open your AI project
2. Start a new conversation
3. Paste `session_start_prompt.md` and fill in your ship and location
4. Take screenshots of the contracts terminal and paste them in
5. The AI will tell you what to take, what to skip, and in what order to run them

---

## Files to upload when setting up your AI project

Along with the instructions in your setup file, upload these two files from the `developer/runtime/` folder:

- `developer/runtime/scoring_config.json` — the scoring weights
- `developer/runtime/OCR_normalization_rules.json` — the location name table

The AI uses these to score routes correctly. Without them it will still work but scoring will be approximate.
