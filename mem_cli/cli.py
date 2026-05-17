from __future__ import annotations

import argparse
import json

from .core import (
    SCHEMA_VERSION,
    collect_captures,
    collect_duplicates,
    count_files,
    ensure_layout,
    ingest_file,
    parse_frontmatter,
    slugify,
    validate_frontmatter,
    write_json,
)
from pathlib import Path

OUTPUT_FORMAT = "json"


def with_schema(command: str, payload: dict) -> dict:
    merged = {"schema_version": SCHEMA_VERSION, "command": command}
    merged.update(payload)
    return merged


def render_tty(obj: dict) -> str:
    command = obj.get("command", "mem-cli")
    if command == "init":
        return f"bóveda inicializada: {obj.get('vault')}"
    if command == "add":
        return f"agregados {obj.get('count', 0)} elemento(s) en {obj.get('vault')}" + (
            f"; faltantes {len(obj.get('missing', []))}" if obj.get("missing") else ""
        )
    if command == "index":
        return f"indexadas {obj.get('captures_indexed', 0)} captura(s) en {obj.get('vault')}"
    if command == "connect":
        return f"encontradas {obj.get('connections_count', 0)} conexión(es) en {obj.get('vault')}"
    if command == "brief":
        return f"brief guardado para el tema: {obj.get('topic')}"
    if command == "status":
        return f"bóveda={obj.get('vault')} existe={obj.get('exists')}"
    return json.dumps(obj, ensure_ascii=True, indent=2)


def emit(obj: dict, exit_code: int = 0) -> int:
    if OUTPUT_FORMAT == "tty":
        print(render_tty(obj))
    else:
        print(json.dumps(obj, ensure_ascii=True, indent=2))
    return exit_code


def cmd_init(args: argparse.Namespace) -> int:
    vault = Path(args.vault).expanduser().resolve()
    ensure_layout(vault)
    return emit(with_schema("init", {"vault": str(vault), "created": True}))


def cmd_add(args: argparse.Namespace) -> int:
    vault = Path(args.vault).expanduser().resolve()
    if not vault.exists():
        return emit(with_schema("add", {"error": "bóveda no encontrada", "vault": str(vault)}), 1)
    ensure_layout(vault)
    requested = [Path(p).expanduser().resolve() for p in args.paths]
    missing = [str(p) for p in requested if not p.exists()]
    added: list[str] = []
    warnings: list[dict] = []
    for source in requested:
        if not source.exists():
            continue
        if source.is_dir():
            for file_path in sorted(source.rglob("*")):
                if file_path.is_file():
                    if file_path.suffix.lower() in {".md", ".markdown"}:
                        frontmatter = parse_frontmatter(file_path.read_text(encoding="utf-8"))
                        extras = validate_frontmatter(frontmatter)
                        if extras:
                            warnings.append({"path": str(file_path), "unknown_keys": extras})
                    relative_path = file_path.relative_to(source)
                    added_path, collided = ingest_file(vault, file_path, relative_path)
                    added.append(added_path)
                    if collided:
                        warnings.append({"path": str(file_path), "collision_resolved_to": added_path})
        else:
            if source.suffix.lower() in {".md", ".markdown"}:
                frontmatter = parse_frontmatter(source.read_text(encoding="utf-8"))
                extras = validate_frontmatter(frontmatter)
                if extras:
                    warnings.append({"path": str(source), "unknown_keys": extras})
            added_path, collided = ingest_file(vault, source)
            added.append(added_path)
            if collided:
                warnings.append({"path": str(source), "collision_resolved_to": added_path})
    return emit(
        with_schema(
            "add",
            {
                "vault": str(vault),
                "requested": [str(p) for p in requested],
                "added": added,
                "missing": missing,
                "count": len(added),
                "warnings": warnings,
                "warnings_count": len(warnings),
            },
        ),
        1 if missing else 0,
    )


def cmd_index(args: argparse.Namespace) -> int:
    root = Path(args.vault).expanduser().resolve()
    if not root.exists():
        return emit(with_schema("index", {"error": "bóveda no encontrada", "vault": str(root)}), 1)
    ensure_layout(root)
    captures = collect_captures(root)
    duplicates = collect_duplicates(captures)
    payload = with_schema(
        "index",
        {
            "vault": str(root),
            "files_indexed": count_files(root),
            "captures_indexed": len(captures),
            "captures": captures,
            "duplicates": duplicates,
            "duplicates_count": len(duplicates),
        },
    )
    write_json(root / ".tmp" / "index.json", payload)
    return emit(payload)


def cmd_connect(args: argparse.Namespace) -> int:
    root = Path(args.vault).expanduser().resolve()
    if not root.exists():
        return emit(with_schema("connect", {"error": "bóveda no encontrada", "vault": str(root)}), 1)
    ensure_layout(root)
    days = max(args.days, 0)
    captures = collect_captures(root)
    connections = []
    for i, left in enumerate(captures):
        left_tags = set(left.get("tags") or [])
        for right in captures[i + 1 :]:
            right_tags = set(right.get("tags") or [])
            shared = sorted(left_tags.intersection(right_tags))
            if shared:
                connections.append({"left": left["path"], "right": right["path"], "shared_tags": shared, "reason": "shared_tags"})
    payload = with_schema(
        "connect",
        {
            "vault": str(root),
            "days": days,
            "connections": connections,
            "connections_count": len(connections),
            "status": "draft",
        },
    )
    write_json(root / ".tmp" / "connections.json", payload)
    return emit(payload)


def cmd_brief(args: argparse.Namespace) -> int:
    root = Path(args.vault).expanduser().resolve()
    if not root.exists():
        return emit(with_schema("brief", {"error": "bóveda no encontrada", "vault": str(root)}), 1)
    ensure_layout(root)
    topic = args.topic.strip()
    proof = [item for item in args.proof] if args.proof else []
    payload = with_schema(
        "brief",
        {
            "vault": str(root),
            "topic": topic,
            "one_thing": args.one_thing or f"Brief para {topic}",
            "proof": proof,
            "reader_transformation": args.reader_transformation or "Sintetizar patrones accionables",
            "three_hooks": args.three_hooks or [],
            "three_closers": args.three_closers or [],
            "status": "draft",
        },
    )
    brief_name = f"{slugify(topic)}.json"
    write_json(root / "03-BRIEFS" / brief_name, payload)
    write_json(root / ".tmp" / "brief.json", payload)
    return emit(payload)


def cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.vault).expanduser().resolve()
    exists = root.exists()
    counts = {entry: 0 for entry in ["00-INBOX", "01-CAPTURES", "02-CONNECTIONS", "03-BRIEFS", "docs", ".tmp"]}
    artifacts = {}
    if exists:
        for entry in counts:
            counts[entry] = count_files(root / entry)
        for name in ["index.json", "connections.json", "brief.json"]:
            artifact = root / ".tmp" / name
            artifacts[name] = artifact.exists()
        artifacts["briefs"] = count_files(root / "03-BRIEFS")
    return emit(with_schema("status", {"vault": str(root), "exists": exists, "layout": counts, "artifacts": artifacts}))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mem-cli", description="CLI local de memoria de proyecto.")
    parser.add_argument("--format", choices=["json", "tty"], default="json")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Inicializar la bóveda.")
    p_init.add_argument("--vault", required=True)
    p_init.set_defaults(func=cmd_init)

    p_add = sub.add_parser("add", help="Agregar archivos o carpetas a la bóveda.")
    p_add.add_argument("paths", nargs="+")
    p_add.add_argument("--vault", required=True)
    p_add.set_defaults(func=cmd_add)

    p_index = sub.add_parser("index", help="Indexar capturas normalizadas.")
    p_index.add_argument("--vault", required=True)
    p_index.set_defaults(func=cmd_index)

    p_connect = sub.add_parser("connect", help="Derivar conexiones heurísticas.")
    p_connect.add_argument("--vault", required=True)
    p_connect.add_argument("--days", type=int, default=7)
    p_connect.set_defaults(func=cmd_connect)

    p_brief = sub.add_parser("brief", help="Generar un brief temático.")
    p_brief.add_argument("--vault", required=True)
    p_brief.add_argument("--topic", required=True)
    p_brief.add_argument("--one-thing")
    p_brief.add_argument("--proof", action="append")
    p_brief.add_argument("--reader-transformation")
    p_brief.add_argument("--three-hooks", action="append")
    p_brief.add_argument("--three-closers", action="append")
    p_brief.set_defaults(func=cmd_brief)

    p_status = sub.add_parser("status", help="Reportar el estado de la bóveda.")
    p_status.add_argument("--vault", required=True)
    p_status.set_defaults(func=cmd_status)
    return parser


def main(argv: list[str] | None = None) -> int:
    global OUTPUT_FORMAT
    parser = build_parser()
    args = parser.parse_args(argv)
    OUTPUT_FORMAT = args.format
    return args.func(args)
