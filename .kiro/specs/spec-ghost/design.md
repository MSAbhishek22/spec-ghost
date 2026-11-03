# Design — Spec Ghost

## Overview
Spec Ghost is a file-reading tool, not a service. The design has
three layers: a scanner (pure file logic), a thin web server
(stdlib HTTP, two allowed targets), and a one-page UI. No database,
no model, no network call exists anywhere in the design.

## Architecture

```
Browser
  -> Web UI (app/index.html, vanilla JS)
  -> Web server (app/server.py, ThreadingHTTPServer)
       -> Scanner (app/specghost.py)
            -> .kiro/specs/  (spec discovery + prose)
            -> code files    (reference matching)
       -> Banish plan (app/specghost.py, plan only, no writes)
CLI
  -> run.py scan [sample|.]  -> scanner -> JSON report on stdout
```

## Components

### Scanner (`app/specghost.py`)
- `discover_specs(root)`: walks `<root>/.kiro/specs/`. A
  subdirectory with `.md` files is one spec (name = directory
  name); a lone `.md` file is one spec (name = file stem).
  Returns spec dir, file list, and concatenated prose text.
- `discover_code_files(root)`: walks the root, skipping `.git`,
  `__pycache__`, `node_modules`, `.venv`, `venv`, `runs`, and the
  `.kiro` directory itself. Returns relative paths for known code
  extensions, sorted.
- `mentioned_files(text)`: regex for plausible file paths with a
  known extension, de-duplicated, in order of appearance.
- `spec_referenced_by(name, code_text)`: normalises hyphens and
  underscores to hyphens, lowercases, and checks for the spec name
  in the code text, or an explicit `spec: <name>` /
  `.kiro/specs/<name>` marker.
- `scan(root)`: combines the above into one report — spec count,
  code file count, covered specs, ghost specs, unmarked code
  files, stale specs (mentioned path with a slash that does not
  exist under root), and the spec → code mapping.
- `banish_plan(name, report)`: returns a plan for a ghost spec.
  It never writes to disk. For a non-ghost name it says so.

### Web server (`app/server.py`)
- `GET /`: serves the UI.
- `GET /health`: `{status: ok, service: spec-ghost, llm: none}`.
- `GET /api/scan?target=sample|.`: returns the scan report.
  Any other target returns 400. This allowlist is the safety
  design: the server is a local tool, not a file-reading service.
- `POST /api/banish-plan`: `{target, ghost}` → banish plan JSON.
  Same allowlist, same 400 on anything else.

### UI (`app/index.html`)
- Dark haunted-house theme: near-black brown background, warm
  candlelight amber headings and borders, a subtle candle flicker
  on the title only. Rooms are cards, ghosts are listed with a
  ghost mark and a "Banish plan" button, unmarked code and stale
  specs are plain lists with monospace paths.
- The UI fetches `/api/scan` on load (demo house by default) and
  re-fetches on button click. The banish plan is labelled
  "Plan only — Spec Ghost never deletes, moves, or edits files."
- Distinct from other projects by design: not a purple dashboard,
  not ChatBoss's dark game gradient, not CageCheck's paper/stamp
  look. The visual metaphor here is a house at night, lit by
  candles — because the product is about a house full of ghosts.

## Correctness
- Determinism: sorted listings, sorted walks, no randomness, no
  timestamps in the scan report itself.
- A stale check only counts mentioned paths containing a slash,
  so generic prose words (e.g. a bare filename with no directory)
  are not falsely flagged as stale.
- A spec mentioned file that exists is never stale, even if no
  code references the spec — staleness and ghost-ness are separate
  questions, and the report keeps them separate.

## Error handling
- Missing `.kiro/specs/`: zero specs, not a crash.
- Unreadable file: read with `errors="ignore"`, so one bad file
  cannot break the whole scan.
- Unknown scan target: HTTP 400 with a plain error, not a stack
  trace.
- Unknown ghost name in a banish plan: a plain "not a ghost"
  response, not an invented plan.

## Testing strategy
- Unit tests on temporary directories built in the test itself
  (no fixture repo to keep in sync): spec discovery (directory
  and lone-file shapes), code discovery and skipping, covered vs
  ghost, unmarked code, stale detection, banish plan safety
  (no files changed), and the `.gitignore` never ignoring `.kiro/`.
- The bundled demo house (`sample/`) is itself a test of the
  whole pipeline: it must contain one covered spec, one ghost,
  one unmarked code file, and one stale mention, so the UI demo
  shows all four categories without setup.
