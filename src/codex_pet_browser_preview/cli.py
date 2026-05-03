#!/usr/bin/env python3
"""Serve a local browser preview for Codex Desktop pet spritesheets."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import webbrowser
from pathlib import Path

from .pet_catalog import build_catalog
from .preview_server import find_free_port, make_server


def is_port_listening(host: str, port: int) -> bool:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex((host, port)) == 0


def daemon_paths(codex_home: Path) -> tuple[Path, Path]:
    run_dir = codex_home / "cache" / "pet-browser-preview"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir / "server.pid", run_dir / "server.log"


def start_daemon(args: argparse.Namespace, codex_home: Path) -> None:
    pid_file, log_file = daemon_paths(codex_home)
    if is_port_listening(args.host, args.port):
        print(f"http://{args.host}:{args.port}/")
        print(f"already running on port {args.port}")
        if args.open:
            webbrowser.open(f"http://{args.host}:{args.port}/")
        return

    cmd = [
        sys.executable,
        "-m",
        "codex_pet_browser_preview",
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--codex-home",
        str(codex_home),
    ]
    if args.asar:
        cmd.extend(["--asar", str(args.asar)])

    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    log = log_file.open("ab")
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
        env=env,
    )
    pid_file.write_text(str(process.pid) + "\n", encoding="utf-8")

    url = f"http://{args.host}:{args.port}/"
    print(url)
    print(f"pid: {process.pid}")
    print(f"log: {log_file}")
    if args.open:
        webbrowser.open(url)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--asar", type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--open", action="store_true", help="open the preview URL in the default browser")
    parser.add_argument("--scan", action="store_true", help="print discovered pets and exit")
    parser.add_argument("--daemon", action="store_true", help="start the preview server in the background")
    args = parser.parse_args()

    codex_home = args.codex_home.expanduser()
    if args.scan:
        pets, _ = build_catalog(codex_home, args.asar)
        for pet in pets:
            print(f"{pet['source']:7} {pet['id']:28} {pet['name']} -> {pet['path']}")
        print(f"total: {len(pets)}")
        return

    if args.daemon:
        start_daemon(args, codex_home)
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
