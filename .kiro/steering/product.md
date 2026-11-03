# Product Steering — Spec Ghost

## What this product is
Spec Ghost is a small, local tool for developers who use Kiro specs.
It reads a repo's `.kiro/specs/` directory and its code files, and
answers four plain questions:
1. Which specs are covered by code? (rooms)
2. Which specs have no implementation? (ghosts / orphan specs)
3. Which code files reference no spec? (unmarked code)
4. Which specs mention files that no longer exist? (stale specs)

## Who it is for
A solo developer, or a small team, using Kiro's spec-driven workflow
(steering, requirements, design, tasks). They write specs, then code,
then more specs — and after a few weeks nobody remembers which specs
are real, which were abandoned, and which point at deleted files.

## What it is NOT
- Not an AI tool. There is no LLM call, no model, no inference.
  The scan is deterministic: the same files always give the same
  report, and any result can be verified by reading the files.
- Not a deleter, mover, or editor. The "banish ghost" action is a
  plan only. Spec Ghost never deletes, moves, or edits a file.
  A human decides, by hand, what to do with a ghost.
- Not a GitHub tool. It does not call the GitHub API, does not need
  a token, and does not know about pull requests or issues.
- Not a linter for code quality. It checks spec ↔ code linkage
  only, not whether the code is good.

## Product principles
1. Deterministic over clever: a result must be reproducible.
2. Honest over impressive: if a spec is a ghost, say so; do not
   invent a linkage.
3. Safe over powerful: the web UI scans only the demo house or
   this repo itself, never an arbitrary path a visitor asks for.
4. One screen: rooms, ghosts, unmarked code, stale specs, banish
   plan. No dashboard sprawl.
