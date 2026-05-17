from __future__ import annotations

from .cli import main
from .core import (
    ALLOWED_FRONTMATTER_KEYS,
    SCHEMA_VERSION,
    VAULT_LAYOUT,
    collect_captures,
    collect_duplicates,
    count_files,
    ensure_layout,
    ingest_file,
    normalize_frontmatter,
    parse_frontmatter,
    serialize_frontmatter,
    slugify,
    validate_frontmatter,
    write_json,
)

__all__ = [
    "ALLOWED_FRONTMATTER_KEYS",
    "SCHEMA_VERSION",
    "VAULT_LAYOUT",
    "collect_captures",
    "collect_duplicates",
    "count_files",
    "ensure_layout",
    "ingest_file",
    "main",
    "normalize_frontmatter",
    "parse_frontmatter",
    "serialize_frontmatter",
    "slugify",
    "validate_frontmatter",
    "write_json",
]

