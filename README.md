# Codex Pet Browser Preview

Local browser preview tool for Codex Desktop pet spritesheets.

It scans Codex's built-in pet spritesheets from `app.asar`, scans custom pets from `~/.codex/pets`, and opens a browser UI for inspecting every fixed Codex pet action row frame by frame.

The repository also includes a thin optional Codex skill wrapper that tells Codex how to start the CLI.

## Features

- Preview built-in Codex pets and custom pets in one browser page.
- Switch between `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, and `review`.
- Play, pause, step previous/next frame, adjust speed, and zoom.
- Show checkerboard transparency, frame outline, contact strip, full sheet grid, and source file path.
- Run as a normal Python CLI without installing a Codex skill.
- No third-party Python dependencies.

## Install CLI

With `pipx`:

```bash
pipx install .
```

From GitHub after publishing:

```bash
pipx install git+https://github.com/<your-name>/codex-pet-browser-preview.git
```

For local development without `pipx`, use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

## Use CLI

Scan available pets:

```bash
codex-pet-preview --scan
```

Start the browser preview as a background server:

```bash
codex-pet-preview --port 8765 --daemon --open
```

Then open:

```text
http://127.0.0.1:8765/
```

You can also run without installing, from a checkout:

```bash
./bin/codex-pet-preview --port 8765 --daemon --open
```

The equivalent module command is:

```bash
PYTHONPATH=src python3 -m codex_pet_browser_preview --port 8765 --daemon --open
```

If Codex is installed outside the default path, pass the app archive explicitly:

```bash
codex-pet-preview --asar /path/to/app.asar --open
```

If you want to inspect a different Codex home:

```bash
codex-pet-preview --codex-home /path/to/.codex --open
```

The background server writes runtime files under:

```text
~/.codex/cache/pet-browser-preview/server.pid
~/.codex/cache/pet-browser-preview/server.log
```

## Optional Codex Skill Wrapper

The `codex-pet-browser-preview/` folder is a thin Codex skill wrapper. It does not contain the preview implementation. Install the CLI first, then copy the skill wrapper if you want Codex to launch it for you:

```bash
mkdir -p ~/.codex/skills
cp -R codex-pet-browser-preview ~/.codex/skills/codex-pet-browser-preview
```

After that, ask Codex to start the pet browser preview. The skill will run:

```bash
codex-pet-preview --port 8765 --daemon --open
```

If the CLI is not installed but this repository checkout is available, Codex can run:

```bash
./bin/codex-pet-preview --port 8765 --daemon --open
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

Validate the skill wrapper with Codex's skill creator helper if available:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py codex-pet-browser-preview
```

## Repository Layout

```text
src/codex_pet_browser_preview/
  __main__.py
  cli.py
  asar_extract.py
  pet_catalog.py
  pet_constants.py
  preview_server.py
  assets/index.html
codex-pet-browser-preview/
  SKILL.md
  agents/openai.yaml
bin/codex-pet-preview
scripts/self_check.py
```
