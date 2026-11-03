# Spec Ghost — Deployment Runbook

> Rulebook §5. This runbook is **ON PAPER ONLY**. Spec Ghost is NOT
> deployed as of 2026-11-03. No production URL exists, no Render
> service exists, and nothing in this file claims otherwise. The
> config it describes (`render.yaml`, commit `e370a6b`) is present
> in the repo, but a config file is not a deployment.

## 1. Intended deployment

- **Provider (planned):** Render, free tier.
- **Service name (planned):** `spec-ghost-demo` (as in `render.yaml`).
- **Repo:** https://github.com/MSAbhishek22/spec-ghost
- **Branch for deployment:** `main` (production branch; deploy
  only from a release commit, and record that commit's SHA in
  `deployment/RELEASE_MANIFEST.json` at deploy time — do not
  backfill it).
- **Stack:** Python 3.12, stdlib only. No dependencies to install,
  no database, no background worker, no file storage.
- **Start command:** `python3 run.py` (serves the UI; `run.py`
  with no arguments calls the server's `main()`).
- **Build command (from `render.yaml`):**
  `pip install -r requirements.txt || echo 'stdlib only — nothing to install'`
  — note: there is no `requirements.txt` in the repo, so the
  fallback `echo` is what actually runs. That is intentional and
  harmless for a stdlib-only app, but a green build is not proof
  that pip ran. If a dependency is ever added, add a real
  `requirements.txt` and remove the fallback.
- **Health check path:** `/health` — must return
  `{status: ok, service: spec-ghost, llm: none — deterministic scan only}`.

## 2. Environment variables (NAMES only — never values)

| Name | Value / source | Required? |
|---|---|---|
| `HOST` | `0.0.0.0` (set in `render.yaml`) | Yes — the server defaults to `127.0.0.1`, which Render cannot reach. Without this, the service will start and immediately fail health checks. |
| `PORT` | Supplied by Render at runtime; the server reads `PORT` (default `8768` locally) | Yes (Render-provided) |
| `PYTHON_VERSION` | `3.12.0` (set in `render.yaml`) | Yes |

No secrets exist for this project: no API key, no token, no
password, no LLM credential. Do not invent any env var. If a
future version adds one, list its name here with a safe
placeholder only, never its value.

## 3. Deploy steps (user taps — none of this has happened)

1. **Render signup (user, own browser).** Stop at once if Render
   asks for a card or any payment method. Free tier must stay
   free; this runbook does not authorise any payment.
2. **Create the service from the repo via `render.yaml`.**
   Confirm the service shows plan **Free** before proceeding.
3. **Deploy.** Wait for the build to finish, then open the live
   URL in a fresh browser session (not the deploy dashboard).
4. **Smoke test on the live URL, in order:**
   - `GET /health` → 200 with the exact JSON above.
   - `GET /` → haunted-house UI renders, demo-house report
     visible (the page auto-scans `sample` on load).
   - Click "Haunt the demo house" → report shows covered
     `room-lighting`, ghost `ghost-door`, unmarked
     `app/unmarked.py`, stale `room-lighting → app/missing.py`.
   - Click "Banish plan" for `ghost-door` → plan renders with
     "Plan only — Spec Ghost never deletes, moves, or edits
     files" and `deletes_anything: false` in the underlying JSON.
   - Click "Haunt this repo itself" → report for the repo root
     renders (specs include `spec-ghost`).
   - Check the browser console for errors and the network tab
     for failed requests.
5. **Record the deployment** in `deployment/RELEASE_MANIFEST.json`:
   exact deployed commit SHA, production URL, provider, build/
   deployment identifier if available, and UTC + IST timestamps.
   Then — and only then — record the demo video from that URL
   (see `submission/DEMO_VIDEO_MANIFEST.md`).

## 4. Free-tier behaviour (must be stated, not hidden)

- **Sleep:** Render free web services sleep after ~15 minutes
  idle. The first request after sleep takes ~60 seconds (cold
  start). `healthCheckPath` is not a keep-alive: warm the service
  before filming, judging, or demoing, and say so on camera if
  it is asleep.
- **Ephemeral disk:** No database and no persistent state exist
  in this app, so there is nothing to lose on restart — but
  equally, there is no state to persist. Every scan is computed
  fresh from files on disk.
- **Scan safety on the live service:** The deployed service can
  only scan `sample` (bundled demo house) and `.` (the repo
  itself). It cannot read arbitrary visitor paths — any other
  target returns 400. The live demo must therefore use the demo
  house (and optionally "this repo itself"), never an arbitrary
  path. Do not present the live service as a general-purpose
  scanner for other people's repos.

## 5. Rollback

- **If the live service fails health checks or the smoke test:**
  stop, record the failure (URL, commit SHA, error, timestamp),
  and do not record a demo video from a broken deployment.
- **Rollback path:** Redeploy the previous release commit from
  the repo (Render dashboard → manual deploy → select commit),
  re-run the smoke test, and update the release manifest to the
  commit actually serving. Never edit files directly on the
  server: the repo is the source of truth.
- **If Render itself is unusable (card demanded, quota, outage):**
  mark the deployment BLOCKED with the exact reason, do not
  substitute a screenshot, a localhost URL, or another project's
  URL, and propose the smallest compliant alternative (e.g. a
  different free provider, verified at that time — not assumed
  here).

## 6. Current blocker (exact reason, not a vague "pending")

- **BLOCKED — Render signup + deploy pending the user.**
  No Render account has been created for this project, no
  service has been created, and no live URL exists. The
  `render.yaml` in the repo is a plan, not a deployment.
- **Stop conditions that remain in force:** stop at once if
  Render asks for a card or payment; do not create an account
  in the user's name without their explicit go-ahead for that
  signup; do not claim a deployment from the config file alone.

## 7. Ownership

- **Owner:** M S Abhishek (repo owner, MSAbhishek22).
- **Code owner for deploy decisions:** the user — deployment
  (Render signup, service creation, live URL verification) is a
  user tap, not an agent action, because it requires the user's
  own Render account.
- **This runbook's status:** written 2026-11-03 from the actual
  `render.yaml` and `app/server.py`; it will be updated at
  deploy time with the real URL, commit SHA, and timestamps.
  Until then, every deployment field in the release manifest
  stays `null`.
