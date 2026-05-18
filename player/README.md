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

Upload all eight files from the `uploads/` folder in this directory. Your setup guide lists them with descriptions.

The AI uses these files to score routes correctly. Without them it will still work but scoring will be approximate.

---

## What's coming — in-game addon

The long-term goal for Apeirogon Logistics is an **in-game addon** that analyzes contracts in real time as you browse the missions terminal — no screenshots, no copy-paste. You'd see contract scores and recommendations overlaid directly in the game UI.

**This requires CIG (Cloud Imperium Games) to open up the game to addons or plugins.** That capability does not exist yet. When CIG enables it, Apeirogon Logistics will let you:

- Connect your own OpenAI, Claude, Anthropic, or other AI provider API key
- See Accept / Defer / Reject indicators on contracts as you scroll through the terminal
- Get a smart summary panel showing the best combinations and run order
- Configure what information shows and how the overlay looks

Nothing about this requires changes to how you use the current version. When the addon becomes available it will be an optional installation — the AI assistant workflow you're using today will continue to work.
