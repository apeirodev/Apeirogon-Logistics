# Local Tooling Architecture

## Principle
The platform must work locally without centralized inference, hosted SaaS, telemetry contribution, or future addon support.

## Local Components
- screenshot input
- optional local OCR
- manual mission entry
- schema validation
- deterministic route scoring
- optional provider adapter
- local telemetry store
- local export generator

## Durable Core
The durable core is the schema and operational rule set. AI providers and future addons are adapters.
