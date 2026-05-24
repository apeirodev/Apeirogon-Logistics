> **LEGACY -- this guide describes the old two-step JSON extraction workflow (AI extracts JSON, Python scores it). The current workflow is AI-as-advisor: paste the instruction block from your platform's SETUP file in `player/project_instructions/` and use screenshots directly. This file is kept for historical reference only.**

# LM Studio Usage Guide

## Recommended Mode
Use LM Studio as a local OpenAI-compatible endpoint.

## Steps
1. Start LM Studio local server.
2. Select a model with sufficient context.
3. Configure the tool or prompt workflow to use the local endpoint.
4. Preserve user state in JSON files.
5. Validate structured outputs.

## Limitation
Vision and structured-output quality depend on the selected model.
