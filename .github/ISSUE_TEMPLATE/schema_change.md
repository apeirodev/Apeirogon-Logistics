---
name: Schema Change
about: Propose an addition or correction to a JSON schema file
labels: schema
---

## Schema File

<!-- Which schema file does this affect? -->

File: `schema/`

## Change Type

- [ ] Add a missing field that tools already use
- [ ] Correct a field type or constraint
- [ ] Add a new field to support a new tool feature
- [ ] Remove a field that no longer exists in tool output
- [ ] Add or correct enum values

## Current Schema (relevant section)

```json

```

## Proposed Change

```json

```

## Why This Change Is Needed

<!-- Describe the mismatch between the schema and the actual tool output, or the gap the new field fills. Include which tool produces or consumes the field. -->

## Backward Compatibility

<!-- Does this change break existing valid JSON files? If so, what migration is needed? -->

- [ ] Backward compatible (existing valid files remain valid)
- [ ] Breaking change (existing files would fail validation after this change)

## Supporting Evidence

<!-- If this is a correction: paste a sample tool output showing the actual field shape. If this is an addition: paste the relevant tool code that reads or writes the new field. -->
