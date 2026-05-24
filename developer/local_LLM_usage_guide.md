> **LEGACY -- this guide describes the old two-step JSON extraction workflow (AI extracts JSON, Python scores it). The current workflow is AI-as-advisor: paste the instruction block from your platform's SETUP file in `player/project_instructions/` and use screenshots directly. This file is kept for historical reference only.**

# Local LLM Usage Guide

## Recommended Use
Use local models when privacy, cost control, or offline operation matters.

## Requirements
- local model runtime
- enough context for the lightweight subset
- manual validation of outputs
- local JSON state files

## Rule
Model quality varies. Deterministic fallback must remain available.
