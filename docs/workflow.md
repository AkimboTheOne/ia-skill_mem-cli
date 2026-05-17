# Workflow

Recommended baseline flow:

1. Initialize a vault.
2. Add files or folders to the inbox/capture pipeline.
3. Index the vault to normalize and catalogue content.
4. Generate heuristic connections from indexed content.
5. Produce a brief for a topic when synthesis is needed.
6. Check status to confirm the vault is healthy.

## Example

```bash
$mem-cli init --vault ./mem-cli-vault
$mem-cli add ./src ./docs
$mem-cli index --vault ./mem-cli-vault
$mem-cli connect --vault ./mem-cli-vault --days 7
$mem-cli brief --vault ./mem-cli-vault --topic "refactor patterns"
$mem-cli status --vault ./mem-cli-vault
```

