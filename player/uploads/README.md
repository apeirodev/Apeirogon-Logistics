# Files to Upload to Your AI Project

Upload **all files in this folder** to your AI project when you set it up.
You only do this once. These files give your AI the exact scoring weights,
location lookups, and route strategy it needs to advise you accurately.

| File | What it does |
|---|---|
| `scoring_config.json` | Exact scoring weights: the math behind every Accept / Defer / Reject |
| `OCR_normalization_rules.json` | Location and issuer name lookups; helps AI read your screenshots correctly |
| `mission_schema.json` | Mission field definitions; helps AI structure what it extracts from screenshots |
| `mission_issuer_profiles.json` | Issuer tendencies: Covalex (with all 7 reputation ranks), Ling, Red Wind, and more |
| `ship_profiles.json` | Operational data for all 23 supported ships (90+ SCU) |
| `SHIP_SPECIALIZATION_GUIDE.md` | Per-ship advice: which ships suit which missions and how modifiers work |
| `hull_b_covalex_route_playbook.md` | Hull-B Covalex operational guide: patterns, stacking, route sequencing |
| `GENERALIZED_HAULING_HANDBOOK.md` | Advice for other ships and issuers beyond Hull-B Covalex |

## How to upload

- **Claude Projects**: drag all files into the project knowledge area
- **ChatGPT Projects**: attach all files when configuring your GPT
- **Gemini Gems**: upload all files in the gem's knowledge section
- **Other AI**: paste file contents if your AI does not support file uploads

See your platform's setup guide in `player/project_instructions/` for step-by-step instructions.
