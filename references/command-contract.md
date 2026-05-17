# Command Contract

Canonical command surface for the baseline implementation:

```text
mem-cli init --vault <path>
mem-cli add <path...>
mem-cli index --vault <path>
mem-cli connect --vault <path> --days <n>
mem-cli brief --vault <path> --topic <text>
mem-cli status --vault <path>
```

## Required Behaviors

- Commands must be deterministic for the same inputs.
- Commands must prefer structured JSON output.
- Commands must not mutate outside the vault or explicit input paths.
- Commands must keep `.tmp/` ephemeral.

