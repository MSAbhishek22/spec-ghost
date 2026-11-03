# Tech Steering — Spec Ghost

## Stack
- Python 3.12, standard library only. No third-party packages, no
  build step, no Docker, no database.
- Web server: `http.server.ThreadingHTTPServer` (stdlib).
- UI: one HTML file, inline CSS and vanilla JavaScript. No framework,
  no CDN dependency, so the UI cannot break because a CDN is down.
- Tests: `unittest` (stdlib), run with `python3 -m unittest discover -s tests -v`.

## Why stdlib only
This is a file-reading tool. It does not need a framework, a database,
or a model. Every dependency is a failure mode and a supply-chain
question; for a tool whose whole point is trust, fewer dependencies
is the honest choice. It also runs on a student laptop with no
install step beyond Python itself.

## Determinism
- Spec discovery: sorted directory listing, sorted file lists.
- Code discovery: sorted walk, skipping `.git`, `__pycache__`,
  `node_modules`, `.venv`, `venv`, `runs`.
- Spec reference: case-insensitive match on the normalised spec name
  (hyphens and underscores equivalent), or an explicit `spec: <name>`
  / `.kiro/specs/<name>` marker.
- File mentions in specs: regex for plausible file paths with a
  known extension, de-duplicated, in order of appearance.
- No timestamps, randomness, or network calls in the scan itself.
  (Receipt-style ids are not used here; the report is the scan.)

## Safety
- The web server accepts only two scan targets: `sample` (the
  bundled demo house) and `.` (this repo itself). Any other target
  returns 400. This is deliberate: a local tool must not become a
  file-reading service for arbitrary paths.
- The banish action never writes. It returns a plan as JSON.
- No secrets are read, stored, or displayed. Spec and code text are
  read from disk only for matching; the API returns file lists and
  linkage, not full file contents.
