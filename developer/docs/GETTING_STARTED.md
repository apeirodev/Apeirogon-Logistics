# Getting Started

This guide walks you from zero to your first route score. No coding required.
Estimated time: 15 to 30 minutes.

---

## What You Need

- **Python 3.10 or newer**: download from https://www.python.org/downloads/
  - Windows: tick "Add Python to PATH" during installation
  - Mac/Linux: usually pre-installed; check with `python3 --version` in a terminal
- **This repository**: either downloaded as a ZIP or cloned with git
- **A terminal**: Command Prompt or PowerShell on Windows; Terminal on Mac/Linux
- **Optionally: a ChatGPT, Claude, or Gemini account**: only needed for screenshot OCR

That's it. No database, no server, no internet required for scoring.

---

## Step 1: Install Python

If you already have Python 3.10+, skip this step.

1. Go to https://www.python.org/downloads/
2. Download the latest Python 3.x installer
3. Run the installer. **On Windows, tick "Add Python to PATH"**
4. Open a terminal and run: `python --version` (or `python3 --version` on Mac/Linux)
5. You should see something like `Python 3.12.x`

---

## Step 2: Get the Repository

**Option A: Download ZIP:**
1. Go to the repository page on GitHub
2. Click Code → Download ZIP
3. Extract the ZIP to a folder you'll remember (e.g. `Documents/Apeirogon-Logistics`)

**Option B: Git clone:**
```
git clone https://github.com/apeirodev/Apeirogon-Logistics.git
```

---

## Step 3: Open a Terminal in the Repository Folder

**Windows:**
1. Open the folder in File Explorer
2. Click the address bar, type `cmd`, press Enter

**Mac:**
1. Open Terminal (Spotlight → Terminal)
2. Type `cd ` (with a space), then drag the folder into the Terminal window
3. Press Enter

**Linux:**
Right-click inside the folder → Open Terminal (or use `cd`)

---

## Step 4: Run Your First Score

Paste this into the terminal and press Enter:

**Windows:**
```
echo {"same_pickup":1} | python tools\deterministic_scorer.py
```

**Mac/Linux:**
```
echo '{"same_pickup":1}' | python tools/deterministic_scorer.py
```

You should see a JSON result with a score, recommendation, and risk level.
If you see an error, check that Python is installed and you're in the right folder.

---

## Step 5: Score a Real Hull-B Route

Replace the example values with your actual mission details:

**Mac/Linux:**
```bash
echo '{
  "issuer": "covalex",
  "ship": "hull-b",
  "same_pickup": 2,
  "stops": ["Port Olisar", "Covalex Hub Shopp-L4", "Baijini Point"]
}' | python tools/deterministic_scorer.py
```

**Windows (PowerShell):**
```powershell
'{"issuer":"covalex","ship":"hull-b","same_pickup":2,"stops":["Port Olisar","Covalex Hub Shopp-L4","Baijini Point"]}' | python tools\deterministic_scorer.py
```

Look for:
- `"score"`: 0 to 100
- `"recommendation"`: accept, defer, or reject
- `"operational_risk"`: low, medium, or high

---

## Step 6: Understand the Output

| Field | What it means |
|-------|---------------|
| `score` | 0 to 100. 70+ = accept, 45 to 69 = defer, below 45 = reject |
| `recommendation` | The system's suggestion. You decide. |
| `operational_risk` | low/medium/high |
| `warnings` | Things that lowered the score (dead legs, fragmentation, etc.) |
| `unresolved_fields` | Data you didn't provide; score is less confident |
| `score_breakdown` | Which factors added or subtracted points |

---

## Step 7: Work With Multiple Missions

When you have several missions to compare, use the batch tool instead:

**Mac/Linux:**
```bash
echo '{
  "issuer": "covalex",
  "ship": "hull-b",
  "missions": [
    {"pickup": "Port Olisar", "delivery": ["Covalex Hub Shopp-L4"], "cargo_scu": 24, "reward_usc": 12500},
    {"pickup": "Port Olisar", "delivery": ["Baijini Point"], "cargo_scu": 16, "reward_usc": 9000},
    {"pickup": "Microtech", "delivery": ["ARC-L1"], "cargo_scu": 32, "reward_usc": 8000}
  ]
}' | python tools/ingest_mission_batch.py
```

The batch tool:
- Scores each mission individually
- Detects same-pickup stacking opportunities
- Suggests an optimal combined route for accepted/deferred missions

---

## Step 8: Use AI to Read Screenshots (Optional)

If you want the AI to extract mission data from your in-game screenshots:

1. Open your AI account (ChatGPT, Claude, Gemini)
2. Paste the strict guardrail prompt: `prompts/STRICT_AI_SESSION_PROMPT.md`
3. Wait for the AI to say "STRICT MODE ACTIVE"
4. Paste the vision extraction prompt: `prompts/AI_VISION_EXTRACTION_PROMPT.md`
5. Attach your screenshot
6. Copy the JSON the AI returns → save as `missions.json`
7. Run: `python tools/OCR_result_normalizer.py -i missions.json -o missions_norm.json`
8. Run: `python tools/ingest_mission_batch.py -i missions_norm.json`

**Important:** Always verify the AI's numbers against your screen before scoring.
The AI will invent values if you don't use the strict prompt. See `docs/HALLUCINATION_GUARDRAILS.md`.

---

## What's Next

- `docs/QUICK_START.md`: Condensed reference once you know the basics
- `docs/FIRST_ROUTE_ANALYSIS.md`: Step-by-step walkthrough of a real Hull-B session
- `hull_b_covalex_route_playbook.md`: Hull-B specific strategy and stacking guide
- `docs/ROUTE_ANALYSIS_HANDBOOK.md`: Understanding the score and factors in depth
- `ChatGPT_usage_guide.md` / `Claude_usage_guide.md`: Provider-specific AI setup
- `docs/FAQ.md`: Common questions

---

## Troubleshooting

**"Python is not recognized" (Windows):**
Reinstall Python and tick "Add Python to PATH".

**"No such file or directory" / "can't find tools/":**
You're not in the repository folder. `cd` to the folder first.

**"JSONDecodeError" or "Expecting value":**
Check your JSON syntax; every key and string needs double quotes. Use the examples above.

**The score seems wrong:**
The score is a heuristic. It uses only what you provide. If important fields are
UNRESOLVED, the score will be less accurate. Supply more mission details for a
more accurate result.
