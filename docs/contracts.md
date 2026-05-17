# Contracts

This file captures the baseline command contract for the skill.

## Commands

- `init`: create the vault directory layout.
- `add`: capture files or folders into the vault workflow.
- `index`: index files or a vault tree.
- `connect`: derive heuristic links from captured content.
- `brief`: generate a topic brief from prepared content.
- `status`: report vault health and inventory.

## Output Policy

- Primary machine output should be JSON.
- Human TTY output may be readable text, but it must reflect the same underlying data.
- Failures should be explicit and structured where possible.

## Frontmatter

Captured markdown files should preserve a YAML frontmatter block with fields like:

```yaml
---
created: 2026-05-17T12:00:00Z
type: source
status: new
source: local
tags: [tag1, tag2]
source_file: path/to/file
---
```

