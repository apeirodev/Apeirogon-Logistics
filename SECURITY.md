# SECURITY POLICY

Apeirogon Logistics is an operational logistics-analysis platform.

## Reporting Vulnerabilities

Report security issues privately. Do not open a public issue. Contact the maintainer via the GitHub Security Advisories tab or the contact details on apeirogon.gg.

## Secure Coding Rules

This project integrates security rules from [TikiTribe/claude-secure-coding-rules](https://github.com/TikiTribe/claude-secure-coding-rules) (MIT).

Rules are applied via Claude Code through `CLAUDE.md` (project root) and `.claude/rules/`:

- `.claude/rules/owasp-2025.md`: OWASP Top 10:2025 core rules
- `.claude/rules/ai-security.md`: AI/ML system security (NIST AI RMF, MITRE ATLAS, Google SAIF)
- `.claude/rules/agent-security.md`: Agentic AI security (OWASP LLM Top 10, NIST AI RMF)

Project-specific mandatory rules (see `CLAUDE.md`):

| Rule | Summary |
|------|---------|
| FILE-01 | Validate all file paths: prevent path traversal |
| FILE-02 | Never use pickle: JSON deserialization only |
| FILE-03 | No subprocess with shell interpolation |
| AI-01 | AI provider outputs are always advisory_only=true |
| AI-02 | Sanitize provider outputs before downstream use |
| INT-01 | Verify integrity of all release artefacts |
| INT-02 | Pin dependencies with hashes |
| ERR-01 | Fail closed: deny access on validation error |
| ERR-02 | Never expose internal paths or stack traces to output |
| LOG-01 | Never log API keys, tokens, or user credentials |
| SRC-01 | Never silently merge source classes |

## Scope

The following are explicitly prohibited:

- gameplay automation
- botting
- memory reading
- packet inspection
- gameplay injection
- input simulation
- anti-cheat bypassing
- unauthorized client modification
- exploit tooling

The project is intended for:

- screenshot analysis
- route analysis
- telemetry organization
- operational planning
- OCR normalization
- hauling workflow assistance

No anti-cheat interaction is permitted.
