# AGENTS.md

## Purpose
This repo is the baseline for the `mem-cli` skill. Future Codex runs should preserve the contract in `20260517_mem-cli_SKILL.md` and keep the implementation deterministic, local, and shell-friendly.

## Working Rules
- Inspect the repo before editing.
- Do not overwrite user changes unless explicitly requested.
- Use `apply_patch` for manual file edits.
- Prefer small, explicit shell scripts over hidden framework behavior.
- Keep CLI output JSON-first and deterministic.
- Keep user-facing documentation in `docs/`.
- Keep stable contracts, schemas, and canonical examples in `references/`.
- Keep transient data out of version control, especially `.tmp/` and vault contents.

## Baseline Expectations
- The skill defines the command surface: `init`, `add`, `index`, `connect`, `brief`, and `status`.
- Vault layout is canonical:
  - `00-INBOX/`
  - `01-CAPTURES/`
  - `02-CONNECTIONS/`
  - `03-BRIEFS/`
  - `docs/`
  - `.tmp/`
- File frontmatter must remain Markdown YAML and follow the fields described in the skill.
- Deterministic operations come first; the LLM only summarizes or judges after local processing.

## Change Policy
- If a change affects the public contract, update the skill spec, the README, and the reference examples together.
- If a command shape changes, update the canonical examples in `references/`.
- If a new folder or file type is introduced, document why it exists and whether it is generated or source-controlled.

## Verification
- Prefer quick, reproducible checks:
  - shell syntax checks for scripts
  - smoke tests for generated directories and help output
  - JSON shape validation for sample outputs when examples are added
- If verification is not possible in the current environment, state that clearly in the final handoff.

