# Structure Steering — Spec Ghost

```
kiroween/
  README.md                  # what it does, how Kiro is used, honest limits
  run.py                     # serve the UI, or `scan` a folder to JSON
  app/
    specghost.py             # scanner core: discover, reference, stale, banish plan
    server.py                # stdlib web server, two allowed scan targets only
    index.html               # haunted-house UI (dark, candlelight amber)
  tests/
    test_specghost.py        # unittest tests for the scanner
  sample/                    # bundled demo haunted house (safe to scan)
    .kiro/specs/
      room-lighting/         # covered spec (code references it)
      ghost-door/            # orphan spec (no code references it)
    app/
      lights.py              # references room-lighting
      unmarked.py            # references no spec
  .kiro/
    steering/
      product.md             # this file's siblings: product, tech, structure
      tech.md
      structure.md
    specs/
      spec-ghost/            # the spec for Spec Ghost itself
        requirements.md
        design.md
        tasks.md
  .gitignore                 # excludes __pycache__ and runs/ — NEVER .kiro/
```

## Conventions
- One module, one job: `specghost.py` scans, `server.py` serves,
  `index.html` displays. The scanner never imports the server.
- A spec is a directory under `.kiro/specs/<name>/`, or a single
  `.md` file directly under `.kiro/specs/`. Both shapes are supported.
- Sample data lives under `sample/` and is part of the repo, so the
  demo works offline with no setup and no real repo to point at.
- `.gitignore` must never list `.kiro/` — Kiroween requires the
  `/.kiro` directory in the public repo, un-ignored. This is checked
  by a test.
