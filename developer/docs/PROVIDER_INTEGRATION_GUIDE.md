# Provider Integration Guide

How AI providers fit into the pipeline and how to work with each category.

---

## Supported Provider Classes

The pipeline is designed to accept extraction output from any provider that can produce JSON conforming to the AI vision extraction schema (`schema/ai_vision_extraction.schema.json`). Provider categories:

| Class | Examples | Vision Support | Notes |
|-------|---------|----------------|-------|
| OpenAI-compatible | ChatGPT (GPT-4o), Azure OpenAI | Yes | Web interface or API; see `ChatGPT_usage_guide.md` |
| Anthropic-compatible | Claude (claude.ai) | Yes | Web interface or API; see `Claude_usage_guide.md` |
| Ollama | Any Ollama-served model | Model-dependent | Local only; check model for vision support |
| LM Studio | Any LM Studio model | Model-dependent | Local only; check model for vision support |
| Manual copy-paste | Any provider with chat | N/A | No vision needed; see `docs/MANUAL_COPY_PASTE_WORKFLOW.md` |

---

## Core Integration Rules

**Users provide their own API keys.** This project does not provide, store, or manage API keys. Keys are supplied by users via environment variable at runtime. The project code never handles API keys directly.

**Provider output is untrusted until validated.** The output of any AI provider, regardless of provider reputation, must pass through `provider_output_validator.py` before entering the scoring pipeline. This validation checks that `advisory_only: true` and `source_class: ai_output` are present, and flags unsourced numeric fields.

**Manual mode must remain supported.** No feature or workflow may become unavailable to users without an AI provider. The deterministic scoring pipeline must always be runnable with manually-entered JSON. Provider-specific enhancements are optional improvements, not requirements.

**Provider-specific enhancements must not become required.** If a workflow is built that uses a provider-specific API feature, it must have a non-provider path as a fallback.

---

## The Extraction Contract

Any provider used for screenshot OCR is expected to:

1. Accept `prompts/STRICT_AI_SESSION_PROMPT.md` as a session-opening constraint
2. Acknowledge those constraints explicitly before extraction begins
3. Return extraction output conforming to `schema/ai_vision_extraction.schema.json`
4. Set `"advisory_only": true` and `"source_class": "ai_vision_extraction"` in governance metadata
5. Use `"UNRESOLVED"` for any field that cannot be read from the source material

Providers that cannot or will not meet these requirements should not be used for extraction. Fall back to manual entry.

---

## Adding a New Provider

To add support for a new AI provider:

1. Verify the provider can produce JSON output in the required schema format.
2. Write a usage guide following the pattern of `ChatGPT_usage_guide.md` or `Claude_usage_guide.md`. Include: strict prompt usage, screenshot attachment, extraction prompt usage, output verification, pipeline commands.
3. Test the provider against `examples/ai_vision_extraction/sample_vision_input.json` to confirm schema compatibility.
4. Add the provider to the comparison table in `docs/PROVIDER_SELECTION_GUIDE.md`.

No code changes are required to the core pipeline for a new provider; the pipeline is provider-neutral. Only documentation is needed.

---

## API Key Handling

Supply keys via environment variable only:

```bash
export OPENAI_API_KEY=your-key-here
export ANTHROPIC_API_KEY=your-key-here
```

Never put keys in:
- JSON input files
- Config files
- Command-line arguments (visible in process list)
- Log files

The project's security rules (LOG-01 in `CLAUDE.md`) require that API keys never appear in logs or output files. If you extend any tool to use a provider API, ensure that the key is read from the environment and never written to any output structure.
