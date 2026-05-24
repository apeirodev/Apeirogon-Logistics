> **LEGACY -- this guide describes the old two-step JSON extraction workflow (AI extracts JSON, Python scores it). The current workflow is AI-as-advisor: paste the instruction block from your platform's SETUP file in `player/project_instructions/` and use screenshots directly. This file is kept for historical reference only.**

# Ollama Usage Guide

## Recommended Mode
Run a local model and use the manual or API-compatible adapter workflow.

## Steps
1. Start Ollama locally.
2. Load a capable model.
3. Provide lightweight context and user state.
4. Use deterministic fallback when model outputs are weak.
5. Keep telemetry and state in local JSON files.

## Limitation
Vision support depends on the chosen model.
