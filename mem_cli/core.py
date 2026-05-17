from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Iterable

VAULT_LAYOUT = [
    "00-INBOX",
    "01-CAPTURES",
    "02-CONNECTIONS",
    "03-BRIEFS",
    "docs",
    ".tmp",
]

SCHEMA_VERSION = 1
ALLOWED_FRONTMATTER_KEYS = {"created", "type", "status", "source", "tags", "source_file"}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    cleaned = []
    for char in value.lower():
        cleaned.append(char if char.isalnum() else "-")
    slug = "".join(cleaned).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "brief"


def ensure_layout(vault: Path) -> None:
    for entry in VAULT_LAYOUT:
        (vault / entry).mkdir(parents=True, exist_ok=True)


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return 1
    return sum(1 for item in path.rglob("*") if item.is_file())


def iter_markdown_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        if path.suffix.lower() in {".md", ".markdown"}:
            yield path
        return
    if not path.exists():
        return
    for item in sorted(path.rglob("*")):
        if item.is_file() and item.suffix.lower() in {".md", ".markdown"}:
            yield item


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    raw = parts[1].strip().splitlines()
    data: dict[str, object] = {}
    for line in raw:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
            data[key] = items
        else:
            data[key] = value.strip("'\"")
    return data


def normalize_tags(value: object) -> list[str]:
    if value is None:
        return ["mem-cli"]
    if isinstance(value, list):
        tags = [str(item).strip() for item in value if str(item).strip()]
    else:
        tags = [item.strip() for item in str(value).split(",") if item.strip()]
    return tags or ["mem-cli"]


def normalize_frontmatter(raw: dict, source_file: Path, kind: str) -> dict:
    return {
        "created": str(raw.get("created") or "2026-05-17T12:00:00Z"),
        "type": str(raw.get("type") or kind),
        "status": str(raw.get("status") or "new"),
        "source": str(raw.get("source") or "local"),
        "tags": normalize_tags(raw.get("tags")),
        "source_file": str(raw.get("source_file") or source_file.as_posix()),
    }


def validate_frontmatter(raw: dict) -> list[str]:
    return sorted(key for key in raw.keys() if key not in ALLOWED_FRONTMATTER_KEYS)


def serialize_frontmatter(data: dict) -> str:
    tags = ", ".join(data.get("tags", []))
    return "\n".join(
        [
            "---",
            f"created: {data['created']}",
            f"type: {data['type']}",
            f"status: {data['status']}",
            f"source: {data['source']}",
            f"tags: [{tags}]",
            f"source_file: {data['source_file']}",
            "---",
            "",
        ]
    )


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") and text.count("---\n", 2) >= 1


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def build_frontmatter(source_file: Path, kind: str = "capture") -> str:
    return serialize_frontmatter(normalize_frontmatter({}, source_file, kind))


def ingest_file(vault: Path, source: Path) -> str:
    target_root = vault / ("01-CAPTURES" if source.suffix.lower() in {".md", ".markdown"} else "00-INBOX")
    destination = target_root / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and file_digest(destination) == file_digest(source):
        return str(destination)
    if source.suffix.lower() in {".md", ".markdown"}:
        text = source.read_text(encoding="utf-8")
        body = text
        frontmatter = {}
        if has_frontmatter(text):
            frontmatter = parse_frontmatter(text)
            parts = text.split("---\n", 2)
            body = parts[2] if len(parts) > 2 else ""
        normalized = normalize_frontmatter(frontmatter, source, "capture")
        destination.write_text(serialize_frontmatter(normalized) + body.lstrip("\n"), encoding="utf-8")
    else:
        shutil.copy2(source, destination)
    return str(destination)


def collect_captures(vault: Path) -> list[dict]:
    captures_root = vault / "01-CAPTURES"
    items: list[dict] = []
    for md in iter_markdown_files(captures_root):
        text = md.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        normalized = normalize_frontmatter(frontmatter, md, "capture")
        items.append(
            {
                "path": str(md),
                "created": normalized["created"],
                "type": normalized["type"],
                "status": normalized["status"],
                "source": normalized["source"],
                "tags": normalized["tags"],
                "source_file": normalized["source_file"],
            }
        )
    return items


def capture_fingerprint(capture: dict) -> str:
    source_file = str(capture.get("source_file") or "")
    created = str(capture.get("created") or "")
    tags = ",".join(capture.get("tags") or [])
    raw = "|".join([source_file, created, tags])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def collect_duplicates(captures: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for capture in captures:
        key = capture_fingerprint(capture)
        groups.setdefault(key, []).append(capture)
    duplicates = []
    for group in groups.values():
        if len(group) < 2:
            continue
        duplicates.append(
            {
                "reason": "same_fingerprint",
                "paths": [item["path"] for item in group],
                "source_files": [item["source_file"] for item in group],
            }
        )
    return duplicates

