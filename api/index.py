"""Spec Ghost on Vercel — WSGI entrypoint (serverless adaptation).

The scanner logic is unchanged (app/specghost.py: same deterministic
scan, same banish plan); this file is only a transport adapter.
Vercel's Python runtime calls ``app(environ, start_response)``.

Route-for-route parity with app/server.py (same paths, same JSON
shapes — including its plain ``json.dumps`` encoding — same status
codes, same error strings):

- ``GET /``                     -> app/index.html, ``text/html``
- ``GET /health``               -> service status JSON
- ``GET /api/scan?target=...``  -> scan report (targets restricted to
  ``sample`` and ``.`` by app.server.resolve_target, exactly as
  locally; anything else is a 400)
- ``POST /api/banish-plan``     -> banish plan for one ghost
- anything else                 -> 404 ``{"error": "not found"}``

Unlike the local server there is no process and no mutable state to
keep: Spec Ghost computes every scan fresh from files on disk, so a
serverless instance answers identically to the local one, cold or
warm. The only behavioural difference is transport: no listening
socket — each request is handled by this WSGI app. (app/server.py's
BaseHTTPRequestHandler answers unimplemented methods such as HEAD
with 501; this adapter answers them 404 like any unknown route.)

No credentials, no environment variables, no external assets, no
secrets.
"""

import json
import os
import sys
from urllib.parse import parse_qs

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.server import resolve_target  # noqa: E402
from app.specghost import banish_plan, scan  # noqa: E402

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(BASE_DIR, "app", "index.html")

_JSON = "application/json"


def _json(payload, status: int = 200):
    # Same encoding as app/server.py's _send: plain json.dumps.
    return status, _JSON, json.dumps(payload).encode()


def handle_get(path: str, query: str):
    if path == "/":
        with open(INDEX_HTML, "rb") as fh:
            return 200, "text/html", fh.read()
    if path == "/health":
        return _json({"status": "ok", "service": "spec-ghost",
                      "llm": "none — deterministic scan only"})
    if path == "/api/scan":
        target = resolve_target(parse_qs(query).get("target", ["sample"])[0])
        if target is None:
            return _json({"error": "Only 'sample' and '.' targets are allowed"},
                         400)
        return _json(scan(target))
    return _json({"error": "not found"}, 404)


def _read_body(environ):
    """Mirror of app/server.py's do_POST body handling: parsed JSON
    body, or ``{}`` when the body is empty or unparseable."""
    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        length = 0
    raw = environ["wsgi.input"].read(length) if length > 0 else b"{}"
    try:
        return json.loads(raw.decode() or "{}")
    except Exception:
        return {}


def handle_post(path: str, environ):
    if path == "/api/banish-plan":
        body = _read_body(environ)
        if not isinstance(body, dict):
            body = {}
        target = resolve_target(body.get("target", "sample"))
        if target is None:
            return _json({"error": "Only 'sample' and '.' targets are allowed"},
                         400)
        report = scan(target)
        return _json(banish_plan(body.get("ghost", ""), report))
    return _json({"error": "not found"}, 404)


_STATUSES = {
    200: "200 OK", 400: "400 Bad Request", 404: "404 Not Found",
    500: "500 Internal Server Error",
}


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET").upper()
    raw_path = environ.get("PATH_INFO", "/") or "/"
    # Vercel rewrites /(.*) to /api/index: treat the function root as app root.
    path = "/" if raw_path in ("/api/index", "/api") else raw_path
    query = environ.get("QUERY_STRING", "")
    try:
        if method == "GET":
            code, ctype, body = handle_get(path, query)
        elif method == "POST":
            code, ctype, body = handle_post(path, environ)
        else:
            code, ctype, body = _json({"error": "not found"}, 404)
    except Exception as exc:  # never leak a stack trace to the client
        code, ctype, body = _json({"error": f"Server error: {exc}"}, 500)
    start_response(_STATUSES.get(code, "200 OK"),
                   [("Content-Type", ctype),
                    ("Content-Length", str(len(body)))])
    return [body]
