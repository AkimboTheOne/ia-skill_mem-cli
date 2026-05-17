#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target_dir="${CODEX_HOME:-$HOME/.codex}/skills/mem-cli"

mkdir -p "$target_dir"

copy_if_changed() {
  local src="$1"
  local dst="$2"
  if [[ ! -e "$dst" ]] || ! cmp -s "$src" "$dst"; then
    cp "$src" "$dst"
  fi
}

copy_if_changed "$repo_root/SKILL.md" "$target_dir/SKILL.md"
copy_if_changed "$repo_root/README.md" "$target_dir/README.md"
copy_if_changed "$repo_root/AGENTS.md" "$target_dir/AGENTS.md"
mkdir -p "$target_dir/bin"
copy_if_changed "$repo_root/bin/mem-cli" "$target_dir/bin/mem-cli"
mkdir -p "$target_dir/mem_cli"
copy_if_changed "$repo_root/mem_cli/__init__.py" "$target_dir/mem_cli/__init__.py"
copy_if_changed "$repo_root/mem_cli/api.py" "$target_dir/mem_cli/api.py"
copy_if_changed "$repo_root/mem_cli/core.py" "$target_dir/mem_cli/core.py"
copy_if_changed "$repo_root/mem_cli/cli.py" "$target_dir/mem_cli/cli.py"
chmod +x "$target_dir/bin/mem-cli"

printf '{"installed":true,"target_dir":"%s"}\n' "$target_dir"
