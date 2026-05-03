"""Discover built-in and custom Codex pets for the preview server."""

from __future__ import annotations

import base64
import json
from pathlib import Path

from .asar_extract import extract_builtins
from .pet_constants import COLS, FRAME_H, FRAME_W, HEIGHT, ROWS, STATES, WIDTH


def discover_custom(codex_home: Path) -> list[dict]:
    pets_dir = codex_home / "pets"
    pets: list[dict] = []
    if not pets_dir.exists():
        return pets
    for pet_dir in sorted(path for path in pets_dir.iterdir() if path.is_dir()):
        manifest_path = pet_dir / "pet.json"
        if not manifest_path.exists():
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        sheet_path = pet_dir / manifest.get("spritesheetPath", "spritesheet.png")
        if not sheet_path.exists():
            continue
        pets.append(
            {
                "id": f"custom:{pet_dir.name}",
                "name": manifest.get("displayName") or pet_dir.name,
                "source": "custom",
                "description": manifest.get("description") or "",
                "path": str(sheet_path),
            }
        )
    return pets


def asset_id(path: str) -> str:
    return base64.urlsafe_b64encode(path.encode("utf-8")).decode("ascii").rstrip("=")


def build_catalog(codex_home: Path, asar_arg: Path | None) -> tuple[list[dict], dict[str, Path]]:
    raw = extract_builtins(codex_home, asar_arg) + discover_custom(codex_home)
    assets: dict[str, Path] = {}
    pets: list[dict] = []
    sheet = {"width": WIDTH, "height": HEIGHT, "cols": COLS, "rows": ROWS, "frame": [FRAME_W, FRAME_H]}

    for item in raw:
        path = Path(item["path"]).expanduser().resolve()
        aid = asset_id(str(path))
        assets[aid] = path
        enriched = dict(item)
        enriched["path"] = str(path)
        enriched["image_url"] = f"/asset/{aid}"
        enriched["states"] = STATES
        enriched["sheet"] = sheet
        pets.append(enriched)
    return pets, assets
