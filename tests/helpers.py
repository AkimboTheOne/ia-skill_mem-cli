from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BIN = REPO_ROOT / "bin" / "mem-cli"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(BIN), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def new_vault() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    tmp = tempfile.TemporaryDirectory()
    vault = Path(tmp.name) / "vault"
    return tmp, vault


def write_capture(path: Path, *, created: str, tags: list[str], source_file: str, title: str) -> None:
    path.write_text(
        "\n".join(
            [
                "---",
                f"created: {created}",
                "type: capture",
                "status: new",
                "source: local",
                f"tags: [{', '.join(tags)}]",
                f"source_file: {source_file}",
                "---",
                "",
                f"# {title}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def load_json(stdout: str) -> dict:
    return json.loads(stdout)

