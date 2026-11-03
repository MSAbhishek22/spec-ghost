# Requirements — Spec Ghost

## Introduction
Spec Ghost helps a Kiro user see which of their specs are alive,
which are ghosts, and which point at files that no longer exist —
before the spec folder becomes a haunted house nobody dares to clean.

## Glossary
- **Spec:** a directory under `.kiro/specs/<name>/` (or a single
  `.md` file under `.kiro/specs/`), containing requirements/design/
  tasks prose.
- **Covered spec (room):** a spec referenced by at least one code file.
- **Ghost spec (orphan):** a spec referenced by no code file.
- **Unmarked code:** a code file referencing no spec.
- **Stale spec:** a spec mentioning a file path that does not exist
  under the scanned root.
- **Banish plan:** a plan-only response for a ghost spec. It never
  deletes, moves, or edits files.

## Requirements

### Requirement 1: Discover specs
**User Story:** As a Kiro user, I want Spec Ghost to find all my
specs, so that I can see the whole house at once.

#### Acceptance Criteria
1. WHEN a folder contains `.kiro/specs/<name>/` directories with
   `.md` files, THEN Spec Ghost SHALL list each directory name as
   a spec.
2. WHEN a `.md` file sits directly under `.kiro/specs/`, THEN Spec
   Ghost SHALL list its stem as a spec.
3. WHEN a folder contains no `.kiro/specs/` directory, THEN Spec
   Ghost SHALL report zero specs, not crash.

### Requirement 2: Discover code files
**User Story:** As a Kiro user, I want Spec Ghost to find my code
files, so that linkage can be checked.

#### Acceptance Criteria
1. WHEN scanning, THEN Spec Ghost SHALL include `.py`, `.js`,
   `.ts`, `.tsx`, `.jsx`, `.html`, `.css`, and `.json` files.
2. WHEN scanning, THEN Spec Ghost SHALL skip `.git`,
   `__pycache__`, `node_modules`, `.venv`, `venv`, and `runs`.
3. WHEN scanning, THEN Spec Ghost SHALL NOT count files under
   `.kiro/specs/` themselves as code files.

### Requirement 3: Covered vs ghost specs
**User Story:** As a Kiro user, I want to know which specs are
implemented and which are ghosts, so that I can decide what to keep.

#### Acceptance Criteria
1. WHEN a code file contains the spec name (case-insensitive,
   hyphens/underscores equivalent) or an explicit `spec: <name>`
   marker, THEN that spec SHALL be covered.
2. WHEN no code file references a spec, THEN that spec SHALL be
   listed as a ghost.
3. WHEN the same scan runs twice on unchanged files, THEN the
   covered/ghost lists SHALL be identical.

### Requirement 4: Unmarked code
**User Story:** As a Kiro user, I want to know which code files
reference no spec, so that I can spec them or accept them as unmarked.

#### Acceptance Criteria
1. WHEN a code file references no spec, THEN it SHALL be listed
   as unmarked.
2. WHEN a code file references at least one spec, THEN it SHALL
   NOT be listed as unmarked.

### Requirement 5: Stale specs
**User Story:** As a Kiro user, I want to know when a spec points
at a deleted file, so that I can update or retire the spec.

#### Acceptance Criteria
1. WHEN a spec mentions a file path containing a slash that does
   not exist under the scanned root, THEN that spec SHALL be
   listed as stale with the missing path named.
2. WHEN every file a spec mentions exists, THEN that spec SHALL
   NOT be listed as stale.

### Requirement 6: Banish plan (plan only)
**User Story:** As a Kiro user, I want a plan for a ghost spec,
so that I can decide by hand what to do with it.

#### Acceptance Criteria
1. WHEN a banish plan is requested for a ghost spec, THEN Spec
   Ghost SHALL return a plan with concrete steps and SHALL NOT
   delete, move, or edit any file.
2. WHEN a banish plan is requested for a non-ghost name, THEN
   Spec Ghost SHALL say so and SHALL NOT invent a plan.

### Requirement 7: Web UI and safety
**User Story:** As a Kiro user, I want a one-screen haunted-house
view of the report, so that I can understand it in seconds.

#### Acceptance Criteria
1. WHEN the web UI loads, THEN it SHALL show rooms (covered),
   ghosts (orphan), unmarked code, and stale specs.
2. WHEN the web UI is asked to scan, THEN it SHALL accept only
   the demo house (`sample`) and this repo itself (`.`), and
   SHALL reject any other target with an error.
3. WHEN a banish plan is requested from the UI, THEN the UI
   SHALL label it as plan-only and SHALL NOT present it as a
   deletion.

### Requirement 8: No LLM, no network
**User Story:** As a Kiro user, I want the scan to be checkable
by reading files, so that I can trust it without trusting a model.

#### Acceptance Criteria
1. WHEN scanning, THEN Spec Ghost SHALL make no network call
   and SHALL NOT call any LLM or model API.
2. WHEN the report is shown, THEN it SHALL NOT claim any AI,
   model, or inference was used.
