"""HTTP server for the Codex pet browser preview."""

from __future__ import annotations

import json
import mimetypes
import socket
import sys
import threading
from importlib import resources
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .pet_catalog import build_catalog


def read_index_html() -> bytes:
    return resources.files("codex_pet_browser_preview").joinpath("assets/index.html").read_bytes()


def find_free_port(host: str) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


class PreviewServer(ThreadingHTTPServer):
    def __init__(self, server_address, handler_class, codex_home: Path, asar_arg: Path | None):
        super().__init__(server_address, handler_class)
        self.codex_home = codex_home
        self.asar_arg = asar_arg
        self.lock = threading.Lock()
        self.pets: list[dict] = []
        self.assets: dict[str, Path] = {}
        self.reload()

    def reload(self) -> None:
        pets, assets = build_catalog(self.codex_home, self.asar_arg)
        with self.lock:
            self.pets = pets
            self.assets = assets


class Handler(BaseHTTPRequestHandler):
    server: PreviewServer

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def send_headers_only(self, status: int, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def send_bytes(self, status: int, content: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, payload: dict) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_bytes(200, content, "application/json; charset=utf-8")

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_bytes(200, read_index_html(), "text/html; charset=utf-8")
            return
        if parsed.path == "/api/pets":
            with self.server.lock:
                pets = list(self.server.pets)
            self.send_json({"pets": pets})
            return
        if parsed.path == "/api/reload":
            self.server.reload()
            with self.server.lock:
                pets = list(self.server.pets)
            self.send_json({"pets": pets})
            return
        if parsed.path.startswith("/asset/"):
            aid = parsed.path.removeprefix("/asset/")
            with self.server.lock:
                path = self.server.assets.get(aid)
            if not path or not path.exists():
                self.send_error(404)
                return
            ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            self.send_bytes(200, path.read_bytes(), ctype)
            return
        self.send_error(404)

    def do_HEAD(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_headers_only(200, "text/html; charset=utf-8")
            return
        if parsed.path in {"/api/pets", "/api/reload"}:
            self.send_headers_only(200, "application/json; charset=utf-8")
            return
        if parsed.path.startswith("/asset/"):
            aid = parsed.path.removeprefix("/asset/")
            with self.server.lock:
                path = self.server.assets.get(aid)
            if not path or not path.exists():
                self.send_error(404)
                return
            self.send_headers_only(200, mimetypes.guess_type(path.name)[0] or "application/octet-stream")
            return
        self.send_error(404)


def make_server(host: str, port: int, codex_home: Path, asar_arg: Path | None) -> PreviewServer:
    return PreviewServer((host, port), Handler, codex_home, asar_arg)
