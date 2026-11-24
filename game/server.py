"""Servidor HTTP com a biblioteca standard do Python (sem Flask nem dependências)."""

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .api import SessionStore, handle

STATIC_DIR = (Path(__file__).resolve().parent.parent / "static").resolve()
MAX_BODY = 4096
MIME = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8", ".json": "application/json",
        ".svg": "image/svg+xml", ".png": "image/png", ".ico": "image/x-icon"}


class Handler(BaseHTTPRequestHandler):
    server_version = "BrainTrainingHub/2.0"
    store = SessionStore()

    # ---- utilitários ----
    def _send(self, status, body=b"", ctype="text/plain; charset=utf-8", head_only=False):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def _json(self, status, data):
        self._send(status, json.dumps(data, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8")

    # ---- GET / HEAD: ficheiros estáticos ----
    def _static(self, head_only=False):
        path = unquote(urlsplit(self.path).path)
        if path == "/healthz":
            return self._send(200, b"ok", head_only=head_only)
        if path == "/favicon.ico":
            return self._send(204, head_only=head_only)
        rel = "index.html" if path in ("", "/") else path.lstrip("/")
        target = (STATIC_DIR / rel).resolve()
        if not target.is_relative_to(STATIC_DIR) or not target.is_file():
            return self._send(404, "Não encontrado".encode("utf-8"), head_only=head_only)
        ctype = MIME.get(target.suffix.lower()) or mimetypes.guess_type(target.name)[0] \
            or "application/octet-stream"
        self._send(200, target.read_bytes(), ctype, head_only)

    def do_GET(self):
        self._static()

    def do_HEAD(self):
        self._static(head_only=True)

    # ---- POST: API do jogo ----
    def do_POST(self):
        path = urlsplit(self.path).path
        if not path.startswith("/api/"):
            return self._json(404, {"error": "rota desconhecida"})
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = -1
        if not 0 <= length <= MAX_BODY:
            return self._json(413, {"error": "pedido demasiado grande"})
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, UnicodeDecodeError):
            return self._json(400, {"error": "JSON inválido"})
        try:
            status, data = handle(path[len("/api/"):], payload, self.store)
        except Exception as exc:  # nunca deixar um erro derrubar o servidor
            self.log_error("erro interno: %r", exc)
            status, data = 500, {"error": "erro interno"}
        self._json(status, data)


def create_server(host="0.0.0.0", port=8000):
    server = ThreadingHTTPServer((host, port), Handler)
    server.daemon_threads = True
    return server
