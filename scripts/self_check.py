#!/usr/bin/env python3
"""Repository self-check for codex-pet-browser-preview."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "codex-pet-browser-preview"
PACKAGE_ROOT = REPO_ROOT / "src" / "codex_pet_browser_preview"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    required = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "LICENSE",
        REPO_ROOT / "pyproject.toml",
        REPO_ROOT / "requirements.txt",
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "agents" / "openai.yaml",
        PACKAGE_ROOT / "__init__.py",
        PACKAGE_ROOT / "__main__.py",
        PACKAGE_ROOT / "assets" / "index.html",
        PACKAGE_ROOT / "asar_extract.py",
        PACKAGE_ROOT / "cli.py",
        PACKAGE_ROOT / "pet_catalog.py",
        PACKAGE_ROOT / "pet_constants.py",
        PACKAGE_ROOT / "preview_server.py",
    ]
    for path in required:
        if not path.exists():
            fail(f"missing required file: {path.relative_to(REPO_ROOT)}")

    for path in PACKAGE_ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")

    generated = [
        path
        for path in REPO_ROOT.rglob("*")
        if path.name == "__pycache__" or path.suffix == ".pyc" or path.name.endswith(".egg-info")
    ]
    if generated:
        fail("generated Python cache files found: " + ", ".join(str(p.relative_to(REPO_ROOT)) for p in generated))

    text_paths = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "pyproject.toml",
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "agents" / "openai.yaml",
        PACKAGE_ROOT / "assets" / "index.html",
        *PACKAGE_ROOT.glob("*.py"),
    ]
    forbidden = ["/" + "Users/", "xuwan" + "biao", "测试" + "codex任务"]
    for path in text_paths:
        text = path.read_text(encoding="utf-8")
        for marker in forbidden:
            if marker in text:
                fail(f"forbidden local marker {marker!r} in {path.relative_to(REPO_ROOT)}")

    print("self-check passed")


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT / "src"))
    main()
