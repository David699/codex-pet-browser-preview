#!/usr/bin/env python3
"""Repository self-check for codex-pet-browser-preview."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "codex-pet-browser-preview"
SCRIPT_DIR = SKILL_ROOT / "scripts"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    required = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "LICENSE",
        REPO_ROOT / "requirements.txt",
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "agents" / "openai.yaml",
        SKILL_ROOT / "assets" / "index.html",
        SCRIPT_DIR / "asar_extract.py",
        SCRIPT_DIR / "pet_catalog.py",
        SCRIPT_DIR / "pet_constants.py",
        SCRIPT_DIR / "preview_server.py",
        SCRIPT_DIR / "serve_pet_preview.py",
    ]
    for path in required:
        if not path.exists():
            fail(f"missing required file: {path.relative_to(REPO_ROOT)}")

    for path in SCRIPT_DIR.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")

    generated = [path for path in REPO_ROOT.rglob("*") if path.name == "__pycache__" or path.suffix == ".pyc"]
    if generated:
        fail("generated Python cache files found: " + ", ".join(str(p.relative_to(REPO_ROOT)) for p in generated))

    text_paths = [
        REPO_ROOT / "README.md",
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "agents" / "openai.yaml",
        SKILL_ROOT / "assets" / "index.html",
        *SCRIPT_DIR.glob("*.py"),
    ]
    forbidden = ["/" + "Users/", "xuwan" + "biao", "测试" + "codex任务"]
    for path in text_paths:
        text = path.read_text(encoding="utf-8")
        for marker in forbidden:
            if marker in text:
                fail(f"forbidden local marker {marker!r} in {path.relative_to(REPO_ROOT)}")

    print("self-check passed")


if __name__ == "__main__":
    sys.path.insert(0, str(SCRIPT_DIR))
    main()
