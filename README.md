# Codex Pet Browser Preview

Browser preview skill for Codex Desktop pets.

It scans Codex's built-in pet spritesheets from `app.asar`, scans custom pets from `~/.codex/pets`, and opens a local browser UI for inspecting every fixed Codex pet action row frame by frame.

## Features

- Preview built-in Codex pets and custom pets in one browser page.
- Switch between `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, and `review`.
- Play, pause, step previous/next frame, adjust speed, and zoom.
- Show checkerboard transparency, frame outline, contact strip, full sheet grid, and source file path.
- No third-party Python dependencies.

## Install

Copy the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R codex-pet-browser-preview ~/.codex/skills/codex-pet-browser-preview
```

## Usage

Scan available pets:

```bash
python3 ~/.codex/skills/codex-pet-browser-preview/scripts/serve_pet_preview.py --scan
```

Start the browser preview:

```bash
python3 ~/.codex/skills/codex-pet-browser-preview/scripts/serve_pet_preview.py --port 8765 --daemon --open
```

Then open:

```text
http://127.0.0.1:8765/
```

If Codex is installed outside the default path, pass the app archive explicitly:

```bash
python3 ~/.codex/skills/codex-pet-browser-preview/scripts/serve_pet_preview.py --asar /path/to/app.asar --open
```

If you want to inspect a different Codex home:

```bash
python3 ~/.codex/skills/codex-pet-browser-preview/scripts/serve_pet_preview.py --codex-home /path/to/.codex --open
```

The background server writes runtime files under:

```text
~/.codex/cache/pet-browser-preview/server.pid
~/.codex/cache/pet-browser-preview/server.log
```

## Pet Sources

Built-in pets are extracted from:

```text
/Applications/Codex.app/Contents/Resources/app.asar
```

or from the `CODEX_APP_ASAR` environment variable.

Extracted built-in WebP files are cached under:

```text
~/.codex/cache/pet-browser-preview/builtin
```

Custom pets are discovered from:

```text
~/.codex/pets/<pet-id>/pet.json
```

## Development

Run local checks:

```bash
python3 scripts/self_check.py
```

Validate the skill with Codex's skill creator helper if available:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py codex-pet-browser-preview
```

## Repository Layout

```text
codex-pet-browser-preview/
  SKILL.md
  agents/openai.yaml
  assets/index.html
  scripts/
    asar_extract.py
    pet_catalog.py
    pet_constants.py
    preview_server.py
    serve_pet_preview.py
```
