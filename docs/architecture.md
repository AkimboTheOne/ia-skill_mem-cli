# Architecture

`mem-cli` is a local memory CLI with a strict boundary:

- The CLI handles filesystem operations, capture, indexing, and deterministic bookkeeping.
- The LLM handles synthesis, summarization, and judgment after the local data has been prepared.

## Core Principles

- Local first: the vault is the source of truth.
- Deterministic first: commands should produce stable output for the same inputs.
- JSON first: structured output should be easy to consume by agents.
- Markdown friendly: captured files remain readable and portable.

## Vault Responsibilities

- `00-INBOX/`: raw incoming material waiting to be processed.
- `01-CAPTURES/`: normalized captures with frontmatter.
- `02-CONNECTIONS/`: relation notes and heuristics.
- `03-BRIEFS/`: topic briefs and synthesized summaries.
- `docs/`: repository-local documentation associated with the vault.
- `.tmp/`: transient working state, not source of truth.

