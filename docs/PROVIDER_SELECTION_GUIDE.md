# Provider Selection Guide

How to choose the right AI provider for Apeirogon Logistics, or how to skip AI entirely.

---

## No AI Required

The deterministic scorer and batch pipeline run entirely on your machine with no AI provider. If you have your mission data and can type it into a JSON file, you do not need an AI account, an API key, or an internet connection.

The manual copy-paste workflow (see `docs/MANUAL_COPY_PASTE_WORKFLOW.md`) is fully supported and is the highest-reliability path because it eliminates hallucination risk entirely.

Only reach for an AI provider if you want to speed up data entry by having the AI extract values from a screenshot.

---

## If You Have Screenshots and Want Fast Extraction

**ChatGPT (GPT-4o)** and **Claude (claude.ai)** both support image attachments in their web interface. No API key required — the free or paid web interface works.

- Paste `prompts/STRICT_AI_SESSION_PROMPT.md`, get acknowledgement
- Attach your mission terminal screenshot
- Paste the extraction prompt from `prompts/AI_VISION_EXTRACTION_PROMPT.md`

See `ChatGPT_usage_guide.md` or `Claude_usage_guide.md` for the step-by-step for each provider.

Both providers produce comparable extraction quality when the strict prompt is used. Without the strict prompt, both hallucinate at roughly the same rate. **The provider is not what controls quality — the strict prompt is.**

---

## If Privacy Is the Priority

**Ollama** and **LM Studio** run AI models locally on your machine. No data is sent to any external server.

Trade-offs:
- Requires a machine with adequate RAM and GPU memory to run the model
- Vision support (reading screenshots) depends on which model you choose — not all local models support image input
- Performance varies by hardware and model size
- Model availability and names change — check current documentation

If vision support is not available in your local model, use it with manually typed mission text rather than screenshots.

All the same rules apply: paste the strict prompt, get acknowledgement, verify output.

---

## If You Have No API Key and No Local Model

Use the manual copy-paste workflow. See `docs/MANUAL_COPY_PASTE_WORKFLOW.md`.

This requires no accounts, no software beyond what is in this repository, and no internet connection.

---

## Cost

The scoring tools, normalizer, and batch pipeline are local Python scripts. They are free. AI provider costs are determined by your choice of provider:

- ChatGPT and Claude have free tiers that cover typical extraction sessions
- Ollama and LM Studio are free to run
- Manual entry has no AI cost at all

---

## The Strict Prompt Is Required for Every Provider

The hallucination rate without the strict prompt is above 50% regardless of which provider you use. ChatGPT, Claude, Ollama, and LM Studio all hallucinate mission-critical numeric fields at similar rates when not constrained.

`prompts/STRICT_AI_SESSION_PROMPT.md` must be pasted at the start of every AI session, with every provider. See `docs/HOW_TO_AVOID_BAD_AI_RECOMMENDATIONS.md` for what to do if the AI does not acknowledge the constraints.

---

## Provider Comparison

| Feature | ChatGPT (GPT-4o) | Claude (claude.ai) | Ollama / LM Studio | Manual Entry |
|---------|-----------------|-------------------|-------------------|-------------|
| Vision support | Yes | Yes | Model-dependent | N/A |
| Cost | Free tier available | Free tier available | Free (local) | Free |
| Privacy | Sent to OpenAI | Sent to Anthropic | Stays local | Stays local |
| Setup effort | Low | Low | Medium | None |
| Internet required | Yes | Yes | No | No |
| Hallucination risk without strict prompt | High (>50%) | High (>50%) | High (>50%) | None |
| Hallucination risk with strict prompt | Reduced | Reduced | Reduced | None |

Manual entry is the only path with zero hallucination risk. All AI providers reduce — but do not eliminate — that risk when the strict prompt is used.
