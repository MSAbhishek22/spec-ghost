# Tasks — Spec Ghost

## Implementation plan

- [x] 1. Scanner core (`app/specghost.py`)
  - [x] 1.1 Discover specs (directory shape and lone-file shape)
  - [x] 1.2 Discover code files with skip rules
  - [x] 1.3 Mentioned-file extraction from spec prose
  - [x] 1.4 Spec-reference matching (name + explicit marker)
  - [x] 1.5 Covered / ghost / unmarked / stale report
  - [x] 1.6 Banish plan (plan only, never writes)
- [x] 2. Web server (`app/server.py`)
  - [x] 2.1 Serve UI, health, scan, and banish-plan endpoints
  - [x] 2.2 Allowlist scan targets to `sample` and `.` only (400 otherwise)
- [x] 3. Web UI (`app/index.html`)
  - [x] 3.1 Haunted-house theme (dark, candlelight amber), rooms as cards
  - [x] 3.2 Ghost list with banish-plan button, labelled plan-only
  - [x] 3.3 Unmarked code and stale spec lists
- [x] 4. Demo haunted house (`sample/`)
  - [x] 4.1 Covered spec: room-lighting, referenced by app/lights.py
  - [x] 4.2 Ghost spec: ghost-door, referenced by nothing
  - [x] 4.3 Unmarked code: app/unmarked.py
  - [x] 4.4 Stale mention: room-lighting mentions app/missing.py (does not exist)
- [x] 5. Tests (`tests/test_specghost.py`)
  - [x] 5.1 At least 10 unittest tests, run and reported honestly
  - [x] 5.2 Test that `.gitignore` never ignores `.kiro/`
- [x] 6. README with honest limits (local scan only, no GitHub API,
  no live Kiro call, Kiro credits are a user tap)
- [ ] 7. After user approval (NOT done in this local build)
  - [ ] 7.1 Create a NEW public GitHub repo, push this folder, verify
    `/.kiro` is present at root and not gitignored
  - [ ] 7.2 Request 4,000 free Kiro credits on the Devpost Resources
    tab by 1 Dec 2026 12:00 PT (user tap, own account)
  - [ ] 7.3 Run a real Kiro build session (IDE/CLI/Web/Crew) and
    write the Devpost "how Kiro was used" write-up from that session
  - [ ] 7.4 Record a demo video under 3 minutes of the real UI,
    upload it public on YouTube
  - [ ] 7.5 Submit on Devpost by 5 Dec 2026 03:30 IST
