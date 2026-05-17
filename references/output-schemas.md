# Output Schemas

`schema_version: 1` is required on every JSON payload emitted by `mem-cli`.

## Common Fields

- `schema_version`: integer schema version.
- `command`: command name.
- `vault`: resolved vault path when the command operates on a vault.

## Command-Specific Fields

- `init`: `created`
- `add`: `requested`, `added`, `missing`, `count`
- `index`: `files_indexed`, `captures_indexed`, `captures`
- `connect`: `days`, `connections`, `connections_count`, `status`
- `brief`: `topic`, `one_thing`, `proof`, `reader_transformation`, `three_hooks`, `three_closers`, `status`
- `status`: `exists`, `layout`, `artifacts`

