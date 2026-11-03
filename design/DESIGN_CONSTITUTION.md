# Spec Ghost — Design Constitution

> Rulebook: `~/workspace/ABHI_22_GLOBAL_PROJECT_QUALITY_RULEBOOK.md` (v1.0, read
> 2026-11-03). This file is the project's design constitution. It does NOT
> duplicate the product's real Kiro steering and spec files — those live in
> `.kiro/steering/` (`product.md`, `tech.md`, `structure.md`) and
> `.kiro/specs/spec-ghost/` (`requirements.md`, `design.md`, `tasks.md`) and
> remain the authoritative product/technical record. This file covers only
> the visual identity, motion, layout, 3D plan, responsive and accessibility
> decisions the rulebook requires.

## 1. Product personality and emotional tone

- **Personality:** A watchful caretaker of a haunted house, not a horror
  show. Calm, candlelit, a little wry. The house is the codebase; the
  ghosts are questions, not bugs ("a ghost is a question, not a bug" —
  banish-plan wording in `app/specghost.py`).
- **Tone of copy:** Plain, honest, no AI hype. The UI itself says
  "No AI, no network — just files on disk, read honestly"
  (`app/index.html`). Every claim the UI makes is checkable by reading
  the scanned files.
- **Emotional register:** Curiosity first ("which specs are real?"),
  reassurance second (nothing is ever deleted, moved, or edited).

## 2. Target user, environment, context of use

- **User:** A solo developer or small team using Kiro's spec-driven
  workflow (steering, requirements, design, tasks), after a few weeks
  of specs piling up while code moves on.
- **Environment:** Their own repo on their own machine, or the bundled
  demo house. The tool is local-first: it never calls a network, a
  GitHub API, or an LLM, and the web UI may only scan `sample` and
  `.` — never an arbitrary path.
- **Context of use:** A quick check before a commit, a review, or a
  spec clean-up session. One page, one scan, four answers. No login,
  no account, no setup beyond `python3 run.py`.

## 3. Visual metaphor / central design idea

**A haunted house, used literally as the information architecture:**

| House element | Product meaning |
|---|---|
| Rooms (🏠 cards) | Covered specs — a spec referenced by at least one code file |
| Ghosts (👻) | Orphan specs — referenced by no code file |
| Unmarked corridors | Code files that reference no spec |
| Stale portraits | Specs mentioning a file path that no longer exists |

The metaphor is not decoration pasted on a dashboard: the four scan
categories *are* the four sections of the page, in the same order the
scanner computes them. If the metaphor were removed, the page would
lose its structure, not just its styling.

## 4. Colour palette (semantic roles, actual values from `app/index.html`)

| Role | Value | Used for |
|---|---|---|
| Background | `#0f0d0a` (near-black brown) | Page background — night in the house |
| Panel | `#1a150f` (dark brown) | Result sections |
| Candlelight amber (primary) | `#f5b942` | Headings, primary button, room borders' accent |
| Amber dim | `#c98f2e` | Room card borders |
| Text (warm parchment) | `#f2e8d5` | Body text |
| Muted text | `#a8987a` | Tagline, small print, spec→code mapping |
| Panel border | `#3a2c14` | Section borders |
| Code text | `#ffd98a` | File paths, spec→code JSON |

No purple gradient, no glassmorphism, no glow blobs, no floating
shapes. The only glow is a soft text-shadow on the title
(`0 0 18px rgba(245,185,66,.35)`), i.e. candlelight, not decoration.

## 5. Typography and type hierarchy

- **Headings and body:** Georgia, serif throughout (no webfont, no
  dependency). Title 36px, section headings 20px, tagline 17px,
  small print 14px.
- **Code/data:** `ui-monospace, monospace` at 13px for file paths,
  the spec→code mapping, and the banish-plan pre block.
- **Hierarchy:** One H1 (title) → H2 per result section → room/ghost
  chips and lists. The spec→code JSON is deliberately small print:
  evidence, not the headline.

## 6. Layout grid, spacing, page composition

- Single centred column, `max-width: 860px`, body padding
  `28px 16px`. No sidebar, no dashboard grid, no hero banner.
- One page, one route (`GET /`). Sections stack vertically:
  title → tagline → two scan buttons → safety note → scan result
  (house summary, rooms, ghosts with per-ghost Banish plan buttons,
  unmarked corridors, stale portraits, spec→code mapping) →
  banish-plan section (rendered below the result when requested).
- Sections are bordered panels with `16px` padding and `16px`
  vertical margin. Room chips are inline blocks with `4px` margin.
- This single-column composition is itself part of the identity:
  it is deliberately unlike the multi-panel dashboards of the
  sibling projects (see §13).

## 7. Navigation and information architecture

There is no navigation: one page, no menu, no tabs, no routes for
the user to get lost in. The only "navigation" is the choice of
what to haunt:

1. `Haunt the demo house` (bundled `sample/`, the default — the page
   auto-scans it on load).
2. `Haunt this repo itself` (the Spec Ghost repo root, `.`).

Every other destination is an API route (`/health`, `/api/scan`,
`/api/banish-plan`), not a user-facing page. See
`qa/INTERACTION_INVENTORY.md` for the full control list.

## 8. Component behaviour and interaction patterns

- **Scan buttons:** Amber solid (demo house) vs amber outline
  (this repo). Clicking re-renders the whole result section from
  the fresh JSON; there is no incremental update and no cached
  result shown as fresh.
- **Banish plan buttons:** One per ghost, rendered inside the ghost
  list, amber outline. Clicking POSTs the ghost name and renders a
  plan section below the result. The plan always states, in the UI
  and in the JSON (`deletes_anything: false`), that nothing is
  deleted, moved, or edited — approval is by hand, always.
- **States:** There is no loading skeleton (scans are local and
  fast), no success toast, and no fake progress. Failure modes are
  the honest HTTP ones: 400 for a disallowed target, 404 for an
  unknown route. See the inventory for the one soft spot: a
  malformed POST body is silently treated as `{}`, not rejected.
- **Escaping:** All spec/file names rendered into the page go
  through an `esc()` HTML-escape helper in the inline script.

## 9. Motion language

- Exactly one animation exists: the title candle flicker
  (`@keyframes flicker`, 3s, opacity 1 → .85 → .95). It signals
  "candlelit house" and nothing else.
- No hover animations, no transitions, no scroll effects, no
  animated charts. Motion communicates one thing — atmosphere —
  and never delays the scan or the plan.
- **GAP (honest, not yet fixed):** there is no
  `@media (prefers-reduced-motion)` rule in `app/index.html`. The
  flicker is low-amplitude (opacity only, no movement), so it is
  unlikely to cause vestibular discomfort, but the rulebook's
  reduced-motion requirement is NOT yet met. Fix before release:
  add a reduced-motion media query that disables the flicker.
  Status: FAIL (minor, tracked in §14).

## 10. 3D concept — PLANNED ONLY, does NOT exist yet

> **Status: PLANNED. No 3D code exists in this project as of
> 2026-11-03. Do not claim otherwise in any submission, video,
> or README. This section is the plan the rulebook requires, not
> a description of a shipped feature.**

**Concept — "Walk the house": a spatial rooms map.**
The scanned repo becomes a small explorable house rendered in the
browser (CSS 3D first; WebGL only if the house grows beyond what
CSS 3D can carry):

- Each **room** is a module (a spec's directory / the code files
  that reference it). Room size grows with the number of code
  files referencing the spec; rooms are arranged along corridors
  that follow the repo's directory layout, so the map *is* the
  architecture.
- Each **ghost** is a translucent figure standing in an empty room
  — a spec with no code. Clicking a ghost opens the same banish
  plan the 2D UI already shows; the 3D view never deletes anything.
- Each **stale portrait** hangs crooked on a wall, labelled with
  the missing path; clicking it shows which spec mentions it.
- **Unmarked corridors** are dim passages (code with no spec)
  connecting rooms; walking one highlights the code file.
- **Why 3D helps here (the rulebook's test):** spec↔code drift is
  a spatial problem — "where does this spec live, and what touches
  it?" A map answers that faster than four lists, and a ghost
  standing alone in an empty room is instantly legible in a demo
  in a way a table row is not.

**Interaction:** Orbit/pan with mouse or touch, keyboard
arrow-key movement between rooms as the accessible alternative,
click a room/ghost/portrait to select it and show the same
detail panel as the 2D UI. No control may exist only in 3D: every
3D action must have a 2D equivalent (the current lists), so the
tool stays fully usable without WebGL.

**Loading, error, fallback:** Lazy-load the 3D scene only after
the 2D scan has rendered (never block the primary workflow).
If WebGL is unavailable, performance is low, or the user prefers
reduced motion, fall back to the current 2D lists with no loss
of information — the 2D UI is the fallback, by design.

**Mobile / low-power:** Cap the scene (few rooms, no textures,
no shadows) and offer a "2D only" toggle. Test on a normal laptop
and a mobile viewport before claiming the gate.

**Reduced motion:** In reduced-motion mode the 3D scene is
static (no flicker, no camera drift); the user moves only by
explicit key/click steps.

## 11. Responsive behaviour

- Viewport meta tag is present; the single column and wrapping
  room chips reflow to narrow widths without horizontal overflow
  (no fixed-width elements except the 860px max-width cap).
- **GAP (honest):** No tablet/mobile viewport test has been
  recorded for this UI as of 2026-11-03. The layout is simple
  enough that a mobile break is unlikely, but the rulebook's
  responsive gate is NOT passed on assumption. Record a
  desktop/tablet/mobile check before release. Status: BLOCKED
  (untested, not known-broken).

## 12. Accessibility

- **Done:** Semantic structure (single `main`, H1/H2 hierarchy),
  real `<button>` elements (keyboard-focusable by default),
  high-contrast warm text on near-black (`#f2e8d5` on `#0f0d0a`),
  no information conveyed by colour alone (ghosts also have the
  👻 glyph and the word "Ghosts"; rooms also have the 🏠 glyph
  and the word "Rooms").
- **Gaps (honest):**
  - No `prefers-reduced-motion` handling (see §9) — FAIL (minor).
  - No focus-visible styling beyond the browser default — the
    default outline is present but not deliberately designed.
  - No keyboard alternative for the planned 3D scene yet — the
    3D plan in §10 includes one, but it does not exist.
  - Emoji glyphs (🕯️🏠👻) are decorative aids, not the sole
    carriers of meaning, but no `aria-hidden`/`aria-label`
    treatment has been applied to them.
- Overall accessibility status: IN_PROGRESS, not PASS.

## 13. Distinctiveness vs the three most recent sibling projects

Comparison required by the rulebook (identity, not just accent
colour). All three comparisons are against projects in
`~/workspace/hackathons/` as of 2026-11-03:

| Project | Identity | How Spec Ghost differs |
|---|---|---|
| CageCheck (Vultr) | Paper/ink/stamp: warm off-white `#F7F4ED`, ink `#1A1A18`, stamp red/green/amber, serif headings + mono receipts, single 720px column, one stamp-landing animation | Spec Ghost inverts the palette (near-black brown + candlelight amber), replaces the stamp/receipt metaphor with rooms/ghosts, and replaces a verdict stamp with a four-category house report |
| ChatBoss (TwitchCon) | Dark game gradient, animated HP bars, shield pill, event feed, medal leaderboard, collapsed sim controls | Spec Ghost has no game HUD, no leaderboard, no gradient, no animated bars — one static column, one candle flicker, and a report that reads like a house tour, not a battle |
| NoteVault (Otari) | Local-first notes agent, routing panel + budget meter web UI (light, tool-like) | Spec Ghost is a single-purpose scanner with a narrative metaphor throughout (rooms/ghosts/corridors/portraits), not a tool dashboard with panels and meters |

Verdict: **UI_DISTINCTIVENESS PASS** — recognisably different in
concept, metaphor, palette direction, layout purpose, and motion
(a single flicker vs stamp-landing vs game HUD), not merely in
accent colour. The shared trait is engineering style (stdlib,
honest limits, no fake claims), not visual identity — which is
exactly what the rulebook asks for.

## 14. Design references — BLOCKED (honest)

The rulebook requires five inspected design references per
project. **No design-reference research was performed for Spec
Ghost in this session, and none is claimed here.** No URLs are
listed, because listing URLs that were not inspected would
violate the rulebook's own honesty rule. The haunted-house
identity was designed from the product's own problem (spec drift
as an abandoned house), not from a cited reference set.

- Status: GATE A (research) is BLOCKED on this item. Before a
  release claim, either perform the five-reference research
  (two same-category, one interaction/motion, one typography/
  hierarchy, one 3D/spatial) with inspected dates and learnings,
  or record an approved exception. Do not backfill invented
  references.
- The `.kiro` steering/spec files are product research, not a
  substitute for design references, and are not presented as such.

## 15. Open design gaps (checklist before any COMPLETE claim)

1. [ ] Reduced-motion media query disabling the candle flicker.
2. [ ] Desktop / tablet / mobile viewport checks recorded.
3. [ ] Five design references researched, or exception approved.
4. [ ] 3D "Walk the house" implemented, or an approved exception
       for omitting it (rulebook §3: explain the conflict, do
       not silently omit).
5. [ ] Focus-visible styling designed, not just browser default.
6. [ ] Interaction inventory (companion file) kept in sync with
       the UI whenever a control is added or removed.
