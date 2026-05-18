---
name: Provider Compatibility
about: Report that an AI provider produced output incompatible with the pipeline, or request support for a new provider
labels: provider-compatibility
---

## Provider

<!-- Which AI provider is this about? -->

Provider: 
Model (if known): 

## Issue Type

- [ ] Provider produced output that failed schema validation
- [ ] Provider ignored or violated `STRICT_AI_SESSION_PROMPT.md` constraints
- [ ] Provider hallucinated numeric values not present in the source screenshot
- [ ] Request to add a new provider to the supported list
- [ ] Other

## What Happened

<!-- Describe the specific failure. For validation failures, paste the validation error. For hallucinated values, describe which fields were fabricated and what the correct values were. -->

## Input Used

<!-- What prompt or session opening did you use? Did you paste `prompts/STRICT_AI_SESSION_PROMPT.md`? -->

- [ ] Used `prompts/STRICT_AI_SESSION_PROMPT.md` as session opener
- [ ] Provider acknowledged the constraints before extraction
- [ ] Used `prompts/MISSION_EXTRACTION_PROMPT.md` for the extraction call

## Provider Output

<!-- Paste the relevant portion of the provider's output (JSON or text). Remove any API keys or account details. -->

```json

```

## Validation Error (if applicable)

<!-- If `provider_output_validator.py` produced an error, paste it here. -->

```

```

## Patch Version and Screenshot Context

<!-- Which Star Citizen patch and terminal were you extracting from? -->

Patch: 
Terminal type: 
