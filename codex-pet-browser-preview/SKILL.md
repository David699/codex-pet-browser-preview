---
name: codex-pet-browser-preview
description: Preview Codex Desktop pet spritesheets in a local browser, including built-in app pets from app.asar and custom pets from ~/.codex/pets. Use when the user asks to inspect, compare, debug, play, pause, step through, zoom, or browser-preview Codex pet actions, frames, custom pets, built-in pets, spritesheet.png, spritesheet.webp, or pet.json rendering behavior.
---

# Codex Pet Browser Preview

Use this skill to inspect Codex Desktop pet spritesheets in a browser UI.

## Workflow

1. Run `scripts/serve_pet_preview.py` from this skill.
2. Use `--scan` first when you only need to verify discovered pets.
3. Start the server for interactive preview:

```bash
python3 scripts/serve_pet_preview.py --port 8765 --open
```

4. If Codex is installed outside the default macOS path, pass `--asar /path/to/app.asar`.
5. If the user asks to inspect a specific custom Codex home, pass `--codex-home /path/to/.codex`.

## What The Preview Shows

- Built-in Codex pets extracted from `/Applications/Codex.app/Contents/Resources/app.asar` or `CODEX_APP_ASAR`.
- Custom pets discovered under `~/.codex/pets/*/pet.json`.
- All fixed Codex action rows:
  - `idle` 6 frames
  - `running-right` 8 frames
  - `running-left` 8 frames
  - `waving` 4 frames
  - `jumping` 5 frames
  - `failed` 8 frames
  - `waiting` 6 frames
  - `running` 6 frames
  - `review` 6 frames
- Per-action playback, pause, previous/next frame, speed, zoom, checkerboard background, frame outline, frame contact strip, and full sheet view with grid.

## Notes

- The preview mirrors Codex's fixed atlas layout: `1536x1872`, `8` columns by `9` rows, `192x208` per frame.
- It does not modify pet files.
- Built-in WebP files are cached under `${CODEX_HOME:-~/.codex}/cache/pet-browser-preview/builtin`.
- If a custom pet was just overwritten, refresh the browser page or use the page's reload button.

