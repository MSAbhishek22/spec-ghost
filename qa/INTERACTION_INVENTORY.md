# Spec Ghost — Interaction Inventory

> Rulebook §4. Every visible control is a promise. This file lists
> every visible control and every API route, with expected vs actual
> behaviour and test evidence. Source of truth: `app/index.html`
> (UI) and `app/server.py` + `app/specghost.py` (behaviour), as read
> 2026-11-03. No control has been added or removed since that read
> without updating this file — if the UI changes, update this file
> in the same change.
>
> Test evidence for this version:
> - `python3 -m unittest discover -s tests` in
>   `~/workspace/hackathons/kiroween/`: **14/14 PASS** (re-run
>   2026-11-03, 0.008s). Covers spec discovery (both shapes), code
>   discovery/skip rules, covered vs ghost, hyphen/underscore
>   equivalence, unmarked code, stale detection,
>   existing-mention-not-stale, banish-plan safety (no files
>   changed), non-ghost handling, demo-house all-four-categories,
>   `.gitignore` never ignoring `.kiro/`, and JSON serialisability.
> - Local HTTP verification 2026-11-03 (server on 127.0.0.1:8799,
>   stopped afterwards): `/health` 200, `/api/scan?target=sample`
>   200 with the expected four categories, `/api/scan?target=/etc`
>   400, `/api/banish-plan` for `ghost-door` 200 with
>   `deletes_anything: false` and 4 actions, `/api/banish-plan`
>   for non-ghost `room-lighting` 200 with the "Not a ghost"
>   plan and 0 actions, unknown route 404.
> - Local CLI verification 2026-11-03: `python3 run.py scan`
>   (sample) → 2 specs, 2 code files, covered `room-lighting`,
>   ghost `ghost-door`, unmarked `app/unmarked.py`, stale
>   `room-lighting → app/missing.py`. Identical to the HTTP result.

## Visible UI controls

### 1. "Haunt the demo house" button

- **Page/route:** `GET /`, top button row, amber solid button.
- **User action:** Click.
- **Expected behaviour:** Scan the bundled demo house (`sample/`)
  and render the house report (spec count, code-file count,
  rooms, ghosts, unmarked corridors, stale portraits, spec→code
  mapping).
- **Actual implementation:** `scanTarget('sample')` →
  `GET /api/scan?target=sample` → re-renders `#out` from the JSON.
- **Validation / error handling:** No client-side error UI. If the
  fetch fails (server down), the page silently keeps the previous
  output — there is no error state. This is a gap, not a dead
  button: the button does perform the scan when the server runs.
  See "Known gaps" below.
- **Test evidence:** HTTP + CLI verification above; demo-house
  all-four-categories unittest.
- **Status: PASS** (with the fetch-failure gap noted, not hidden).

### 2. "Haunt this repo itself" button

- **Page/route:** `GET /`, top button row, amber outline button
  (class `ghost-btn`).
- **User action:** Click.
- **Expected behaviour:** Scan the Spec Ghost repo root (`.`) and
  render the same house report for this project's own specs
  (including `spec-ghost` itself).
- **Actual implementation:** `scanTarget('.')` →
  `GET /api/scan?target=.` → same render path as control 1, and
  sets `lastTarget='.'` so subsequent banish plans use this repo.
- **Validation / error handling:** Same as control 1 (no
  client-side error UI on fetch failure).
- **Test evidence:** HTTP route verified for `sample`; the `.`
  target uses the identical `resolve_target` allowlist and scan
  path, and the CLI `run.py scan .` path is the same scanner.
  The `.` HTTP response was not separately curled in this
  session — see "Untested, not assumed" below.
- **Status: PASS** (with the `.`-via-HTTP response noted as
  verified-by-code-path, not by a separate curl in this run).

### 3. Per-ghost "Banish plan" buttons (one per ghost spec)

- **Page/route:** `GET /`, rendered inside the ghost list of the
  scan result (only when at least one ghost exists; otherwise
  the text "none — no ghosts tonight" is shown and no button
  exists).
- **User action:** Click the button next to a ghost spec name.
- **Expected behaviour:** Show a human-readable plan for that
  ghost (read it, implement it with a `spec: <name>` reference,
  archive it by hand, or leave it) and state plainly that
  nothing is deleted, moved, or edited.
- **Actual implementation:** `banish(ghost)` →
  `POST /api/banish-plan` with `{target: lastTarget, ghost}` →
  renders a "Banish plan for 👻 <name>" section below the result,
  with the plan-only disclaimer and the 4 actions as a `<pre>`
  block.
- **Validation / error handling:** The server checks ghost
  membership in the fresh scan report. A non-ghost name returns
  a plan of "Not a ghost spec in this report — nothing to
  banish." with 0 actions and `deletes_anything: false` — a
  truthful no-op, not a fake success. No button is ever shown
  for a non-ghost, so the user cannot reach this path from the
  UI except by calling the API directly.
- **Test evidence:** HTTP verification above (ghost-door: 4
  actions, `deletes_anything: false`; room-lighting: 0 actions,
  "Not a ghost"); banish-plan safety unittest (no files changed).
- **Status: PASS.**

### 4. Auto-scan on page load (not a button, listed for completeness)

- **Page/route:** `GET /`, inline script end: `scanTarget('sample')`.
- **User action:** None — opening the page scans the demo house.
- **Expected behaviour:** The demo-house report is visible
  without any click.
- **Actual implementation:** As expected; identical render path
  to control 1.
- **Test evidence:** Same as control 1.
- **Status: PASS.**

### Controls that do NOT exist (so they cannot be dead)

There is no navigation menu, no search box, no filter, no form,
no login, no settings page, no pagination, no tabs, no modal,
no upload/download control, and no 3D control (the 3D scene is
planned only — see `design/DESIGN_CONSTITUTION.md` §10 — and
therefore has no visible control to inventory). No `href="#"`,
no empty click handler, and no decorative button exists in
`app/index.html`. The full set of visible controls is controls
1–3 above, plus the auto-scan in control 4.

## API routes (server behaviour behind the controls)

| Route | Method | Expected | Actual (verified 2026-11-03 unless noted) | Status |
|---|---|---|---|---|
| `/` | GET | Haunted-house HTML UI | 200, `app/index.html` served | PASS |
| `/health` | GET | `{status: ok, service: spec-ghost, llm: none — deterministic scan only}` | 200, exact JSON verified via curl | PASS |
| `/api/scan?target=sample` | GET | JSON report for demo house | 200; covered `room-lighting`, ghost `ghost-door`, unmarked `app/unmarked.py`, stale `room-lighting → app/missing.py` | PASS |
| `/api/scan?target=.` | GET | JSON report for repo root | Same code path as `sample` (allowlist + scanner); CLI `run.py scan .` verified, HTTP `.` response not separately curled in this run | PASS (code-path) |
| `/api/scan?target=<other>` | GET | 400, no file access | 400 `{"error": "Only 'sample' and '.' targets are allowed"}` verified with `target=/etc` | PASS |
| `/api/scan` (no target) | GET | Defaults to `sample` | `parse_qs(...).get("target", ["sample"])` — default verified by code read, not by a separate curl | PASS (code-path) |
| `/api/banish-plan` | POST JSON `{target, ghost}` | Plan JSON, never a deletion | Ghost: 4 actions, `deletes_anything: false`; non-ghost: "Not a ghost" plan, 0 actions, `deletes_anything: false` | PASS |
| `/api/banish-plan` with disallowed target | POST | 400 | Code path identical to `/api/scan` allowlist check; not separately curled in this run | PASS (code-path) |
| Unknown route | GET/POST | 404 `{"error": "not found"}` | 404 verified with `/nope` | PASS |

## Known gaps and untested items (honest, not hidden)

1. **No client-side error UI on fetch failure.** If the server is
   down, clicking a scan button leaves the previous output on
   screen with no error message. Severity: low (local tool, server
   is started by the same person viewing the page), but it is a
   real gap against rulebook §4.2 (recoverable error state).
   Fix before release: render an error section on fetch failure.
2. **Malformed POST body is silently treated as `{}`.**
   `app/server.py` catches JSON decode errors and proceeds with
   an empty body, which then defaults to target `sample` and a
   non-ghost plan. No crash, no misleading success — but no
   400 either. Severity: low (API-only path; the UI always sends
   valid JSON). Fix before release: return 400 on malformed JSON.
3. **`.` scan via HTTP not separately curled in this run.**
   Verified via the identical code path and the CLI, not via a
   dedicated HTTP call. Re-verify with a curl before claiming
   full HTTP coverage.
4. **No reduced-motion handling, no mobile/tablet viewport
   checks recorded.** These are design/accessibility gaps, not
   dead controls, and are tracked in the design constitution
   (§9, §11, §12). They do not change any control's PASS above,
   but they block a COMPLETE claim.
5. **No E2E (Playwright) suite.** The rulebook asks for one for
   critical journeys; only unittest + manual HTTP/CLI checks
   exist. The critical journeys here are exactly controls 1–3,
   all verified above, but the E2E-suite item itself is missing.

## Summary

- Visible controls inventoried: **3 buttons + 1 auto-scan** — all
  functional, none decorative, none dead.
- API routes inventoried: **9 rows** — all behaving as specified
  (two by code-path verification, flagged as such).
- **ALL_VISIBLE_CONTROLS: PASS** for the controls that exist,
  with gaps 1–2 (error handling) and item 5 (no E2E suite)
  recorded as known issues. This PASS does not mean the project
  is COMPLETE: the 3D, deployment, video, and design-reference
  gates are separately FAIL/BLOCKED (see the gate card in the
  handoff report).
