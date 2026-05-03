"""Extract built-in Codex pet spritesheets from app.asar."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from .pet_constants import BUILTIN_INTERNAL


def default_asar_candidates() -> list[Path]:
    candidates: list[Path] = []
    env = os.environ.get("CODEX_APP_ASAR")
    if env:
        candidates.append(Path(env).expanduser())
    if sys.platform == "darwin":
        candidates.append(Path("/Applications/Codex.app/Contents/Resources/app.asar"))
    elif sys.platform.startswith("linux"):
        candidates.extend(
            [
                Path("/usr/lib/codex/resources/app.asar"),
                Path("/opt/Codex/resources/app.asar"),
                Path.home() / ".local" / "share" / "codex" / "resources" / "app.asar",
            ]
        )
    elif sys.platform.startswith("win"):
        local = os.environ.get("LOCALAPPDATA", "")
        program = os.environ.get("PROGRAMFILES", "")
        candidates.extend(
            [
                Path(local) / "Programs" / "Codex" / "resources" / "app.asar",
                Path(program) / "Codex" / "resources" / "app.asar",
            ]
        )
    return candidates


def resolve_asar(explicit: Path | None) -> Path | None:
    if explicit:
        return explicit.expanduser()
    for candidate in default_asar_candidates():
        if candidate.exists():
            return candidate
    return None


def read_asar_header(blob: bytes) -> tuple[dict, int]:
    header_size = int.from_bytes(blob[4:8], "little")
    json_len = int.from_bytes(blob[12:16], "little")
    header = json.loads(blob[16 : 16 + json_len].rstrip(b"\0").decode("utf-8"))
    return header, 8 + header_size


def asar_lookup(header: dict, internal_path: str) -> dict:
    node = header
    for part in internal_path.split("/"):
        node = node["files"][part]
    return node


def extract_builtins(codex_home: Path, asar_arg: Path | None) -> list[dict]:
    asar = resolve_asar(asar_arg)
    if not asar or not asar.exists():
        return []
    data = asar.read_bytes()
    header, data_base = read_asar_header(data)
    out_dir = codex_home / "cache" / "pet-browser-preview" / "builtin"
    out_dir.mkdir(parents=True, exist_ok=True)

    pets: list[dict] = []
    for pet_id, name, internal in BUILTIN_INTERNAL:
        try:
            entry = asar_lookup(header, internal)
        except KeyError:
            continue
        start = data_base + int(entry["offset"])
        end = start + int(entry["size"])
        content = data[start:end]
        if content[:4] != b"RIFF" or content[8:12] != b"WEBP":
            continue
        out = out_dir / Path(internal).name
        if not out.exists() or out.read_bytes() != content:
            out.write_bytes(content)
        pets.append(
            {
                "id": f"builtin:{pet_id}",
                "name": name,
                "source": "builtin",
                "description": "Built-in Codex pet",
                "path": str(out),
            }
        )
    return pets
