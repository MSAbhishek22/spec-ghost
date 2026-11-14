<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1f6feb,100:8957e5&height=190&section=header&text=Spec%20Ghost&fontSize=44&fontColor=ffffff&animation=fadeIn&desc=Finds%20specs%20with%20no%20code%20%E2%80%94%20and%20code%20with%20no%20spec&descSize=16"/>

> **📖 The Story** Every spec-driven project quietly rots: specs that were never implemented, code nobody specified, and specs still pointing at files deleted months ago. Built for Kiroween 2026, Spec Ghost walks the repo like a haunted house and names every ghost it finds.
>
> **🎯 The Problem** Nobody can see where specs and code have drifted apart until a stale spec sends someone building the wrong thing.
>
> **👥 Who It's For** Developers and teams practising spec-driven development, especially with Kiro.
>
> **🔑 The USP** A fully deterministic scan — no LLM, same repo, same verdict every run — across all three ghost types, with tests at 14/14.
>
> **🚀 What's Next** More spec formats and drift patterns, so fewer ghosts stay invisible.
>
> **🔗 Live: [spec-ghost-green.vercel.app](https://spec-ghost-green.vercel.app)**

---

# Spec Ghost — Haunted Kiro specs, found before they haunt you

> **One line:** Spec Ghost reads a repo's Kiro specs (`.kiro/specs/`)
> and its code, and tells you which specs are covered, which are
> ghosts (orphan specs nobody implemented), which code has no spec,
> and which specs point at files that no longer exist.

## Live demo

**Try it now: https://spec-ghost-green.vercel.app** — deployed on
Vercel (free tier) on 14 Nov 2026 from commit `670b8fac`, verified
live the same day: the page loads signed-out, `/health` answers
`{status: ok, service: spec-ghost}`, and the sample scan runs
end-to-end.

> ⚠️ **URL warning:** https://spec-ghost.vercel.app is a
> **different project's app** — it is *not* this deployment and
> must never be referenced as ours. The `-green` URL above is the
> only production URL for this project.

## Why this idea, and why it fits Kiroween

Kiroween is about building *with* Kiro — spec-driven development with
steering, requirements, design, and tasks. Every Kiro user eventually
faces the same haunted house: specs pile up, code moves on, and nobody
remembers which specs are real, which were abandoned, and which point
at deleted files. Existing tools check code quality, test coverage,
or linting. None of them, as a small local tool, answers the
spec ↔ code linkage question directly — and that question is the
one Kiro users actually ask after a few weeks of spec-driven work.

Spec Ghost is therefore *about* Kiro specs, not just built with a
Kiro-shaped label. It uses real Kiro spec files for itself
(`.kiro/steering/` + `.kiro/specs/spec-ghost/`), and its whole job
is to keep other people's Kiro specs honest. It is not an agriculture
chatbot, an education chatbot, an inventory CRUD app, or a payment
wrapper. It is a developer tool for the exact workflow this
hackathon celebrates.

**Kiroween status, honestly:** the code is published in a public
GitHub repo — https://github.com/MSAbhishek22/spec-ghost (MIT) —
and the app is **deployed and live** at
https://spec-ghost-green.vercel.app (Vercel, deployed 14 Nov 2026
from commit `670b8fac`; see the Live demo section above and
`deployment/RELEASE_MANIFEST.json`). It is **not yet submitted**
to Kiroween, and this local folder is the working copy, not a git
checkout of that repo. It is **not** a before-December cash track — Kiroween
winners are announced around February 2027, per the Devpost-linked
summaries verified 3 Nov 2026 — so do not claim December winnings
for this project. The cash-goal tracks remain Vultr, Otari, NEAR,
ClinicLink/Bharat, and PayPal; Kiroween is the long-runway track.

## What it does

- **Rooms (covered specs):** specs referenced by at least one code
  file (by spec name, case-insensitive, hyphens/underscores
  equivalent, or an explicit `spec: <name>` marker).
- **Ghosts (orphan specs):** specs referenced by no code file.
  The "banish ghost" action is a **plan only** — it never deletes,
  moves, or edits files. A human decides, by hand.
- **Unmarked corridors (code with no spec):** code files that
  reference no spec.
- **Stale portraits (stale specs):** specs mentioning a file path
  (with a slash) that no longer exists under the scanned root.
- **Deterministic, no AI:** the same files always give the same
  report. There is no LLM call, no model, no network call, and no
  GitHub API call anywhere in this tool. Saying otherwise would be
  dishonest, so this README does not.

## How Kiro specs are used

- **Steering** (`.kiro/steering/`): `product.md` (what Spec Ghost
  is and is not), `tech.md` (stdlib-only, determinism, safety),
  `structure.md` (layout and conventions, including the rule that
  `.gitignore` must never ignore `.kiro/`).
- **Spec for the tool itself** (`.kiro/specs/spec-ghost/`):
  `requirements.md` (8 requirements with acceptance criteria),
  `design.md` (scanner / server / UI, correctness, error handling),
  `tasks.md` (implementation checklist; the repo step is done —
  see below — while the remaining post-approval steps, credits,
  real Kiro session, video, and Devpost submit, are still
  unchecked because none of those has happened yet).
- **Scanned specs:** any repo's `.kiro/specs/` directory, in the
  standard Kiro shape (a directory per spec, or a lone `.md` file).

## How to run

```bash
cd ~/workspace/hackathons/kiroween
python3 run.py
# open http://127.0.0.1:8768/  (PORT/HOST overridable)
# The UI defaults to the bundled demo house (sample/).
# Click "Haunt this repo itself" to scan this repo's own specs.

python3 run.py scan          # scan sample/ to JSON on stdout
python3 run.py scan .        # scan this repo itself to JSON

python3 -m unittest discover -s tests -v
```

## The demo house (`sample/`)

The bundled demo exists so the UI shows all four categories with
no setup and no real repo to point at:

- `room-lighting` — **covered** (sample/app/lights.py references
  it) **and stale** (it also mentions sample/app/missing.py,
  which does not exist). A spec can be both; the report keeps
  those questions separate.
- `ghost-door` — **ghost** (nothing references it).
- `app/unmarked.py` — **unmarked code** (references no spec).

## API

- `GET /` — the haunted-house UI
- `GET /health` — `{status: ok, service: spec-ghost, llm: none}`
- `GET /api/scan?target=sample|.` — scan report (JSON)
- `POST /api/banish-plan` — `{"target": "sample", "ghost": "ghost-door"}`
  → plan JSON, never a deletion

**Safety:** the web UI may only scan `sample` and `.` (this repo).
Any other target returns 400. This is deliberate — a local tool
must not become a file-reading service for arbitrary paths.

## Honest limits — read before judging or submitting

- **Local scan only.** No GitHub API, no pull requests, no issues,
  no remote repos. Pointing it at a folder is the whole input.
- **No live Kiro call.** No Kiro IDE/CLI/Web/Crew session has been
  run for this build, and no Kiro credits have been requested.
  The Kiro spec files in this repo are real spec files written
  for this tool, not proof of a Kiro build session.
- **Reference matching is textual, not semantic.** A code file
  that implements a spec without ever naming it will be listed
  as unmarked, and a code file that merely mentions a spec name
  in a comment will count as covering it. That is a stated
  limitation of a deterministic scanner, not a bug to hide.
- **Stale detection is path-based.** It flags mentioned paths
  with a slash that do not exist; generic prose without a path
  is not flagged.
- **Deployed, but not submitted; the only video is a local draft.**
  Live: https://spec-ghost-green.vercel.app (Vercel, deployed
  14 Nov 2026 from commit `670b8fac`, production-verified — see
  `deployment/RELEASE_MANIFEST.json`). Public GitHub repo:
  https://github.com/MSAbhishek22/spec-ghost. No Kiroween
  submission has been filed yet, and the only video is a local
  internal draft (see `submission/DEMO_VIDEO_MANIFEST.md`) —
  never a submission video. The remaining steps are user taps,
  listed below.

## What still needs the user (items 2–5 have not happened)

1. **Public GitHub repo — DONE ✅:** the repo exists at
   https://github.com/MSAbhishek22/spec-ghost (public, `main`,
   head `6d09f7ba`, MIT), with `/.kiro` present at root and **not**
   gitignored (verified via the public GitHub API on 3 Nov 2026;
   a test also enforces the gitignore rule). Caveat: this local
   folder is NOT a git checkout, and local-vs-remote byte equality
   is unverified — reconcile before any release claim.
2. **Kiro credits (user, Devpost Resources tab):** request the
   4,000 free Kiro credits by **1 Dec 2026 12:00 PT**. Do not pay
   for credits; stop if a card is asked.
3. **Real Kiro build session (user):** run a Kiro IDE/CLI/Web/Crew
   session on this project, and write the Devpost "how Kiro was
   used" write-up from that session — not from this README.
4. **Demo video (user):** record under 3 minutes of the real UI,
   upload it public on YouTube.
5. **Devpost submit (user, own browser):** submit by
   **5 Dec 2026 03:30 IST** at https://kiroween.devpost.com/,
   with the repo (including `/.kiro`), the live URL
   (https://spec-ghost-green.vercel.app), the video, and the
   Kiro write-up. Winners are announced around Feb 2027.

## Files

- `app/specghost.py` — scanner core
- `app/server.py` — stdlib web server (two allowed targets only)
- `app/index.html` — haunted-house UI (dark, candlelight amber)
- `run.py` — serve or scan
- `api/index.py` + `vercel.json` — Vercel WSGI adapter (production)
- `tests/test_specghost.py` — unittest tests
- `.kiro/steering/` + `.kiro/specs/spec-ghost/` — real Kiro specs
- `sample/` — bundled demo haunted house
