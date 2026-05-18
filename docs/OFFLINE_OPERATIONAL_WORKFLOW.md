# Offline Operational Workflow

This document is a short redirect. The complete guide for operating without any network connection or AI provider is in `docs/LOCAL_ONLY_OPERATION_GUIDE.md`.

---

## Summary

Apeirogon Logistics is designed to work fully offline. The deterministic scoring pipeline requires only Python and your local JSON files. No internet connection, no AI provider, and no account are needed to score routes.

The standard offline workflow:

1. Read mission details from the in-game terminal
2. Type the values into a JSON file following `schema/mission_schema.json`
3. Run `python tools/ingest_mission_batch.py -i your_missions.json`
4. Review the scored output and make your hauling decision

For the complete offline workflow with setup instructions, troubleshooting, and tips for manual data entry, see `docs/LOCAL_ONLY_OPERATION_GUIDE.md`.
