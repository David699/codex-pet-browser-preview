#!/usr/bin/env python3
"""Serve a local browser preview for Codex Desktop pet spritesheets."""

from __future__ import annotations

import argparse
import webbrowser
from pathlib import Path

from pet_catalog import build_catalog
from preview_server import find_free_port, make_server


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--asar", type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--open", action="store_true", help="open the preview URL in the default browser")
    parser.add_argument("--scan", action="store_true", help="print discovered pets and exit")
    args = parser.parse_args()

    codex_home = args.codex_home.expanduser()
    if args.scan:
        pets, _ = build_catalog(codex_home, args.asar)
        for pet in pets:
            print(f"{pet['source']:7} {pet['id']:28} {pet['name']} -> {pet['path']}")
        print(f"total: {len(pets)}")
        return

    port = args.port or find_free_port(args.host)
    server = make_server(args.host, port, codex_home, args.asar)
    url = f"http://{args.host}:{port}/"
    print(url)
    print(f"pets: {len(server.pets)}")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
