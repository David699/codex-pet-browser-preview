---
name: codex-pet-browser-preview
description: Start or use the codex-pet-preview CLI to preview Codex Desktop pet spritesheets in a local browser, including built-in app pets from app.asar and custom pets from ~/.codex/pets. Use when the user asks to inspect, compare, debug, play, pause, step through, zoom, or browser-preview Codex pet actions, frames, custom pets, built-in pets, spritesheet.png, spritesheet.webp, or pet.json rendering behavior.
---

# Codex Pet Browser Preview

This is a thin wrapper around the standalone `codex-pet-preview` CLI.

## Workflow

1. Prefer the installed CLI:

```bash
codex-pet-preview --port 8765 --daemon --open
```

2. If the CLI is unavailable but the repository checkout is available, run from the checkout root:

```bash
./bin/codex-pet-preview --port 8765 --daemon --open
```

3. Use `--scan` when you only need to verify discovered pets:

```bash
codex-pet-preview --scan
```

4. If Codex is installed outside the default macOS path, pass `--asar /path/to/app.asar`.
5. If the user asks to inspect a specific custom Codex home, pass `--codex-home /path/to/.codex`.
6. After starting, give the user `http://127.0.0.1:8765/` and mention that the server log is under `${CODEX_HOME:-~/.codex}/cache/pet-browser-preview/server.log`.

## Notes

- The CLI mirrors Codex's fixed atlas layout: `1536x1872`, `8` columns by `9` rows, `192x208` per frame.
- It previews files only and does not modify pet files.
- Built-in WebP files are cached under `${CODEX_HOME:-~/.codex}/cache/pet-browser-preview/builtin`.
- Background server pid/log files are written under `${CODEX_HOME:-~/.codex}/cache/pet-browser-preview`.
- If a custom pet was just overwritten, refresh the browser page or use the page's reload button.
