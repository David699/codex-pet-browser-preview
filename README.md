# Codex Pet Browser Preview

Preview Codex Desktop pet spritesheets in a local browser.

It shows Codex built-in pets and custom pets from `~/.codex/pets`, with playback, frame stepping, zoom, grid overlay, checkerboard background, and source file path.

## Quick Start

macOS / Linux:

```bash
git clone <your-repo-url>
cd codex-pet-browser-preview
PYTHONPATH=src python3 -m codex_pet_browser_preview --daemon --open
```

Then open:

```text
http://127.0.0.1:8765/
```

Windows PowerShell:

```powershell
git clone <your-repo-url>
cd codex-pet-browser-preview
$env:PYTHONPATH="src"
python -m codex_pet_browser_preview --daemon --open
```

## What It Finds

- Built-in Codex pets from `app.asar`
- Custom pets from `~/.codex/pets/<pet-id>/pet.json`

If the built-in pets are not found automatically, pass the Codex app archive:

```bash
PYTHONPATH=src python3 -m codex_pet_browser_preview --asar /path/to/app.asar --daemon --open
```

## Useful Commands

List discovered pets:

```bash
PYTHONPATH=src python3 -m codex_pet_browser_preview --scan
```

Use another port:

```bash
PYTHONPATH=src python3 -m codex_pet_browser_preview --port 8766 --daemon --open
```

Use another Codex home:

```bash
PYTHONPATH=src python3 -m codex_pet_browser_preview --codex-home /path/to/.codex --daemon --open
```

## Optional Install

For a permanent `codex-pet-preview` command:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
codex-pet-preview --daemon --open
```

## Optional Codex Skill

This repo also includes a thin Codex skill wrapper:

```bash
mkdir -p ~/.codex/skills
cp -R codex-pet-browser-preview ~/.codex/skills/codex-pet-browser-preview
```

After that, ask Codex:

```text
启动 codex-pet-browser-preview
```

## Development

```bash
python3 scripts/self_check.py
```
