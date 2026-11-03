"""Spec Ghost web server — stdlib only, fresh code for Kiroween 2026.

Safe by design: the web UI may only scan two folders — this project's
own root (".") and the bundled demo haunted house ("sample"). Any
other path is rejected with 400. This is a local tool, not a public
service: it never reads arbitrary paths a visitor asks for.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from app.specghost import scan, banish_plan

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = {".": BASE, "sample": os.path.join(BASE, "sample")}


def resolve_target(name):
    if name in ALLOWED:
        return ALLOWED[name]
    return None


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj, ctype="application/json"):
        body = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            with open(os.path.join(BASE, "app", "index.html"), "rb") as f:
                self._send(200, f.read(), "text/html")
        elif parsed.path == "/health":
            self._send(200, {"status": "ok", "service": "spec-ghost", "llm": "none — deterministic scan only"})
        elif parsed.path == "/api/scan":
            target = resolve_target(parse_qs(parsed.query).get("target", ["sample"])[0])
            if target is None:
                self._send(400, {"error": "Only 'sample' and '.' targets are allowed"})
                return
            self._send(200, scan(target))
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode() or "{}")
        except Exception:
            body = {}
        if parsed.path == "/api/banish-plan":
            target = resolve_target(body.get("target", "sample"))
            if target is None:
                self._send(400, {"error": "Only 'sample' and '.' targets are allowed"})
                return
            report = scan(target)
            self._send(200, banish_plan(body.get("ghost", ""), report))
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, *args):
        pass


def main():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8768"))
    print(f"Spec Ghost on http://{host}:{port}/")
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
