# Spec Ghost — Demo Video Manifest

> Rulebook §7. The mandatory order is: Deploy → Verify Production
> → Freeze Release Commit → Record Demo from Production URL →
> Review Video → Publish/Deliver Video → Attach Verified Video URL.
> Spec Ghost is at step zero of that order: not deployed, not
> verified, no release commit frozen. Nothing in this file claims
> otherwise.

## 1. The local video — INTERNAL DRAFT ONLY, NOT for submission

- **File:** `~/workspace/your_files/spec-ghost-demo.mp4`
- **Duration:** 50.3 seconds (under the 3-minute Kiroween limit)
- **Format:** 1280×800, H.264, 655 KB
- **Source:** Real local UI on `http://127.0.0.1:8768/` (server
  started for recording, stopped afterwards). It is a genuine
  recording of the local UI working — demo-house auto-scan,
  "Haunt the demo house", "Banish plan", "Haunt this repo itself"
  — not a fabricated demo.
- **Labels on the video itself:** "LOCAL DEMO ONLY" banner burned
  in at the bottom for the entire video; title card and end card
  repeat the local-only label, "no live Kiro, no live deployment",
  and "Kiroween winners around Feb 2027 — NOT December cash".
- **Status: INTERNAL DRAFT ONLY. DO NOT SUBMIT THIS VIDEO TO
  KIROWEEN. DO NOT UPLOAD IT AS THE SUBMISSION VIDEO.**

## 2. Why it must not be submitted — user video preference, 2026-11-03 evening

The user stated on 2026-11-03 evening, in plain terms: do not
make videos from screenshots / slides / assembled hold-frames —
that feel is bad. Submission videos must be a screen recording
of the ACTUAL LIVE UI LINK working, with at least one real action
on the live link. Local-only videos are internal drafts only and
must NEVER be submitted as a live demo.

This local video, however honestly labelled, is not a live-link
recording: there is no live Spec Ghost URL yet. Submitting it
would present a localhost demo as Kiroween evidence, which is
exactly what the user's preference and rulebook §7 both forbid.
The video is therefore kept as an internal preview of the UI
flow — useful for checking pacing and copy before the live
recording — and nothing more.

The same rule applies to any future video for this project: no
screenshot-assembled video, no slides-only video, no local-only
video presented as live proof.

## 3. What the submission video must be (when it is made)

1. Deploy to Render free tier (see
   `deployment/DEPLOYMENT_RUNBOOK.md`), verify the production
   URL from a fresh browser session, and freeze the release
   commit (record it in `deployment/RELEASE_MANIFEST.json`).
2. Record 60–120 seconds (Kiroween limit: under 3 minutes) from
   the verified production HTTPS URL, showing:
   - The user problem in one line (Kiro specs drift from code).
   - The live URL visibly in the browser.
   - The main journey on the live site: demo-house scan, rooms,
     ghost, unmarked corridor, stale portrait.
   - A real banish-plan action on the live site (plan only,
     deletes nothing).
   - The strongest differentiator: deterministic, no-LLM,
     spec↔code linkage for Kiro users.
   - The 3D experience, IF it has been implemented by then;
     otherwise, do not claim it, and do not fake it with
     footage of something else.
   - Sample/seeded data labelled as such (the demo house is
     bundled sample data, not a real user's repo).
   - A clear closing statement.
3. Review the recording for factual accuracy and secret leakage
   (there are no secrets in this app, but check anyway).
4. Upload only after the user has approved the publishing
   visibility and metadata, and verify the actual published
   URL by reading it back. Never invent a YouTube URL.
5. Record the production URL, release version, deployed commit
   SHA, and recording date in this file (section 4 below) —
   only at that point, with real values.

## 4. Submission video record (all fields null until a live recording exists)

- **Production URL recorded from:** `null` (no live URL yet)
- **Release version:** `null`
- **Deployed commit SHA:** `null`
- **Recording date:** `null`
- **Video file (submission):** `null`
- **Published video URL (verified):** `null`
- **Upload status:** `BLOCKED_AUTHORIZATION` in rulebook terms
  only insofar as no upload has been authorised or performed —
  more precisely: **NOT_ATTEMPTED**, because there is no live
  product to record yet. Do not relabel this as a publishing
  failure; the blocker is deployment, not authorisation.

## 5. Pending user taps before any submission video can exist

1. Render signup + service creation + live URL verification
   (stop at once if a card is asked).
2. Kiro credits request by 1 Dec 2026, 12:00 PT (stop if a
   card is asked) — needed for the real Kiro session, not for
   the deploy itself.
3. A real Kiro build session + "how Kiro was used" write-up
   (from that session, not from the README).
4. Live-URL demo recording + user-approved YouTube upload
   (Public, per Kiroween rules for the submission video).
5. Devpost submit by **5 Dec 2026, 03:30 IST** at
   https://kiroween.devpost.com/ with repo (including `/.kiro`),
   video, and Kiro write-up. Winners around Feb 2027 — NOT
   December cash; do not claim otherwise.
