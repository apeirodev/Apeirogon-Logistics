# AI Prompt Injection Threat Model

## Threat
Screenshots, OCR text, or pasted mission text may contain instructions that attempt to override the assistant.

## Mitigations
- treat all screenshots and OCR as data, not instructions
- structured prompt contracts
- schema-first validation
- provider output rejection for instruction-following contamination
- unresolved values remain unresolved
