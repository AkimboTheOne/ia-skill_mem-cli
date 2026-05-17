from __future__ import annotations

import json
from pathlib import Path
import unittest

from tests.helpers import REPO_ROOT, load_json, new_vault, run_cli, write_capture
from mem_cli.api import SCHEMA_VERSION, VAULT_LAYOUT, ensure_layout


class MemCliTests(unittest.TestCase):
    def test_init_creates_vault_layout(self) -> None:
        tmp, vault = new_vault()
        with tmp:
            proc = run_cli("init", "--vault", str(vault))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = load_json(proc.stdout)
            self.assertEqual(payload["command"], "init")
            self.assertEqual(payload["schema_version"], 1)
            for entry in ["00-INBOX", "01-CAPTURES", "02-CONNECTIONS", "03-BRIEFS", "docs", ".tmp"]:
                self.assertTrue((vault / entry).exists())

    def test_status_reports_layout(self) -> None:
        tmp, vault = new_vault()
        with tmp:
            run_cli("init", "--vault", str(vault))
            proc = run_cli("status", "--vault", str(vault))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = load_json(proc.stdout)
            self.assertEqual(payload["schema_version"], 1)
            self.assertTrue(payload["exists"])
            self.assertEqual(payload["layout"]["docs"], 0)

    def test_add_reports_missing_paths(self) -> None:
        tmp, root_vault = new_vault()
        with tmp:
            root = Path(tmp.name)
            vault = root_vault
            run_cli("init", "--vault", str(vault))
            sample_dir = root / "sample"
            sample_dir.mkdir()
            sample = sample_dir / "sample.md"
            sample.write_text("hello\n", encoding="utf-8")
            proc = run_cli("add", "--vault", str(vault), str(sample), str(root / "missing.md"))
            self.assertEqual(proc.returncode, 1)
            payload = load_json(proc.stdout)
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["count"], 1)
            self.assertEqual(len(payload["missing"]), 1)
            self.assertTrue((vault / "01-CAPTURES" / "sample.md").exists())

    def test_index_and_connect_use_frontmatter(self) -> None:
        tmp, vault = new_vault()
        with tmp:
            run_cli("init", "--vault", str(vault))
            capture_dir = vault / "01-CAPTURES"
            capture_dir.mkdir(parents=True, exist_ok=True)
            write_capture(capture_dir / "a.md", created="2026-05-17T12:00:00Z", tags=["alpha", "shared"], source_file="src/a.md", title="A")
            write_capture(capture_dir / "b.md", created="2026-05-17T12:00:00Z", tags=["beta", "shared"], source_file="src/b.md", title="B")
            index_proc = run_cli("index", "--vault", str(vault))
            self.assertEqual(index_proc.returncode, 0, index_proc.stderr)
            index_payload = load_json(index_proc.stdout)
            self.assertEqual(index_payload["schema_version"], 1)
            self.assertEqual(index_payload["captures_indexed"], 2)
            self.assertTrue((vault / ".tmp" / "index.json").exists())
            connect_proc = run_cli("connect", "--vault", str(vault), "--days", "7")
            self.assertEqual(connect_proc.returncode, 0, connect_proc.stderr)
            connect_payload = load_json(connect_proc.stdout)
            self.assertEqual(connect_payload["schema_version"], 1)
            self.assertEqual(connect_payload["connections_count"], 1)
            self.assertEqual(connect_payload["connections"][0]["shared_tags"], ["shared"])
            self.assertTrue((vault / ".tmp" / "connections.json").exists())
            status_proc = run_cli("status", "--vault", str(vault))
            self.assertEqual(status_proc.returncode, 0, status_proc.stderr)
            status_payload = json.loads(status_proc.stdout)
            self.assertTrue(status_payload["artifacts"]["index.json"])
            self.assertTrue(status_payload["artifacts"]["connections.json"])

    def test_index_detects_duplicate_captures(self) -> None:
        tmp, vault = new_vault()
        with tmp:
            run_cli("init", "--vault", str(vault))
            capture_dir = vault / "01-CAPTURES"
            capture_dir.mkdir(parents=True, exist_ok=True)
            write_capture(capture_dir / "a.md", created="2026-05-17T12:00:00Z", tags=["dup"], source_file="src/shared.md", title="Shared A")
            write_capture(capture_dir / "b.md", created="2026-05-17T12:00:00Z", tags=["dup"], source_file="src/shared.md", title="Shared B")
            proc = run_cli("index", "--vault", str(vault))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = load_json(proc.stdout)
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["duplicates_count"], 1)
            self.assertEqual(len(payload["duplicates"][0]["paths"]), 2)
            self.assertTrue((vault / ".tmp" / "index.json").exists())

    def test_add_promotes_markdown_without_frontmatter(self) -> None:
        tmp, vault = new_vault()
        with tmp:
            root = Path(tmp.name)
            vault = root / "vault"
            run_cli("init", "--vault", str(vault))
            source = root / "note.md"
            source.write_text("# Note\n", encoding="utf-8")
            proc = run_cli("add", "--vault", str(vault), str(source))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = load_json(proc.stdout)
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["count"], 1)
            copied = vault / "01-CAPTURES" / "note.md"
            self.assertTrue(copied.exists())
            text = copied.read_text(encoding="utf-8")
            self.assertIn("source_file:", text)

    def test_add_normalizes_existing_frontmatter(self) -> None:
        tmp, vault = new_vault()
        with tmp:
            root = Path(tmp.name)
            vault = root / "vault"
            run_cli("init", "--vault", str(vault))
            source = root / "mixed.md"
            source.write_text(
                """---
tags: alpha, shared
type: weird
---

# Mixed
""",
                encoding="utf-8",
            )
            proc = run_cli("add", "--vault", str(vault), str(source))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            copied = vault / "01-CAPTURES" / "mixed.md"
            text = copied.read_text(encoding="utf-8")
            self.assertIn("type: weird", text)
            self.assertIn("tags: [alpha, shared]", text)
            self.assertIn("source_file: ", text)

    def test_add_reports_unknown_frontmatter_keys(self) -> None:
        tmp, vault = new_vault()
        with tmp:
            root = Path(tmp.name)
            vault = root / "vault"
            run_cli("init", "--vault", str(vault))
            source = root / "extra.md"
            source.write_text(
                """---
created: 2026-05-17T12:00:00Z
type: capture
status: new
source: local
tags: [alpha]
source_file: src/extra.md
custom: value
---

# Extra
""",
                encoding="utf-8",
            )
            proc = run_cli("add", "--vault", str(vault), str(source))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = load_json(proc.stdout)
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["warnings_count"], 1)
            self.assertEqual(payload["warnings"][0]["unknown_keys"], ["custom"])

    def test_add_deduplicates_identical_ingest(self) -> None:
        tmp, vault = new_vault()
        with tmp:
            root = Path(tmp.name)
            vault = root / "vault"
            run_cli("init", "--vault", str(vault))
            source = root / "note.md"
            source.write_text("# Note\n", encoding="utf-8")
            first = run_cli("add", "--vault", str(vault), str(source))
            second = run_cli("add", "--vault", str(vault), str(source))
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            payload = load_json(second.stdout)
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["count"], 1)
            copied = vault / "01-CAPTURES" / "note.md"
            self.assertTrue(copied.exists())

    def test_brief_returns_draft_json(self) -> None:
        tmp, vault = new_vault()
        with tmp:
            run_cli("init", "--vault", str(vault))
            proc = run_cli(
                "brief",
                "--vault",
                str(vault),
                "--topic",
                "refactor patterns",
                "--proof",
                "module_a.py: lines 12-30",
                "--proof",
                "module_b.py: lines 5-25",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = load_json(proc.stdout)
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["topic"], "refactor patterns")
            self.assertEqual(len(payload["proof"]), 2)
            brief_file = vault / "03-BRIEFS" / "refactor-patterns.json"
            self.assertTrue(brief_file.exists())
            status_proc = run_cli("status", "--vault", str(vault))
            status_payload = json.loads(status_proc.stdout)
            self.assertTrue(status_payload["artifacts"]["brief.json"])
            self.assertEqual(status_payload["artifacts"]["briefs"], 1)

    def test_tty_format_renders_human_text(self) -> None:
        tmp, vault = new_vault()
        with tmp:
            proc = run_cli("--format", "tty", "init", "--vault", str(vault))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("initialized vault:", proc.stdout)
            self.assertNotIn("{", proc.stdout)

    def test_contract_file_exists(self) -> None:
        for rel in ["references/output-schemas.md", "references/behavior-contract.md"]:
            self.assertTrue((REPO_ROOT / rel).exists())

    def test_public_api_exports(self) -> None:
        self.assertEqual(SCHEMA_VERSION, 1)
        self.assertIn("01-CAPTURES", VAULT_LAYOUT)
        tmp, vault = new_vault()
        with tmp:
            ensure_layout(vault)
            self.assertTrue((vault / "03-BRIEFS").exists())


if __name__ == "__main__":
    unittest.main()
