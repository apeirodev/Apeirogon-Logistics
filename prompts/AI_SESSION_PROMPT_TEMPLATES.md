# AI Session Prompt Templates

## Start New Hauling Session
Load my Star Citizen hauling profile and begin a new hauling session. Preserve all unresolved values. Do not rely on memory. Ask me for ship, issuer, patch version, and screenshots or mission text if not provided.

## Analyze Mission Screenshots
Analyze these hauling mission screenshots. Extract mission details, preserve unresolved OCR values, and produce accepted, rejected, and deferred mission recommendations.

## Correct OCR Output
Review this OCR output against the screenshot or user correction. Preserve raw OCR separately from corrected values.

## Recommend Route
Recommend an ordered route using same-pickup stacking, destination overlap, cargo fragmentation rules, dead-leg avoidance, and ship/issuer context.

## Log Telemetry
Log the observed route outcome, completion timing, unloading delays, dead-leg events, and user corrections as observational telemetry.

## Export Session State
Export updated portable user profile and hauling session state as JSON. Do not omit unresolved values.

## Import Previous State
Use this portable user profile and hauling session state as the source of continuity. Do not rely on chat memory.

## Validate Patch-Era Compatibility
Compare this session against the stated patch era. Flag stale telemetry or heuristics if current patch behaviour appears different.

## Prepare Public Telemetry Submission
Prepare anonymized telemetry suitable for public contribution. Exclude private or identifying information.
