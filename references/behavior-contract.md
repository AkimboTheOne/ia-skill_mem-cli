# Behavior Contract

This repository uses `schema_version: 1` for all machine-readable outputs.

## Global Rules

- Output is JSON by default.
- `--format tty` produces stable, human-readable text.
- Commands are deterministic for the same inputs.
- Vault writes are confined to the requested vault and its managed subdirectories.
- Markdown ingestion normalizes frontmatter but preserves explicit semantic fields when present.

## Ingestion Rules

- Markdown files go to `01-CAPTURES/`.
- Non-Markdown files go to `00-INBOX/`.
- Missing paths are reported and do not stop valid inputs from being processed.
- Identical ingests are deduplicated by content hash at the destination.
- Existing frontmatter keys outside the allowed set are reported as warnings.

## Index Rules

- `index` reads normalized captures from `01-CAPTURES/`.
- Duplicate captures are reported when they share the same semantic fingerprint.
- Index results are persisted to `.tmp/index.json`.

## Brief Rules

- `brief` writes its artifact to `03-BRIEFS/` and `.tmp/brief.json`.
- The filename is derived from the topic slug.
- The payload must include the topic and the canonical brief fields.

