#!/usr/bin/env bash
set -euo pipefail

vault_dir="${1:-mem-cli-vault}"

mkdir -p \
  "$vault_dir/00-INBOX" \
  "$vault_dir/01-CAPTURES" \
  "$vault_dir/02-CONNECTIONS" \
  "$vault_dir/03-BRIEFS" \
  "$vault_dir/docs" \
  "$vault_dir/.tmp"

printf '{"vault":"%s","created":true}\n' "$vault_dir"

