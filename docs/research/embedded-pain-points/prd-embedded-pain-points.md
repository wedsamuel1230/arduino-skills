# PRD: Discovery-Backed Embedded Pain-Point Skills

## Problem Statement

The repository already has broad Arduino and embedded skills, but current
real-world user pain is clustering around narrower failure workflows that are
not well served by generic debugging or code-generation skills. Users struggle
to isolate I2C bring-up failures, understand library or board compatibility,
recover from board-manager install problems, fix upload or USB serial path
issues, and investigate runtime memory instability. These problems are common,
repetitive, and highly structured, which makes them strong candidates for
specialist agent skills.

## Solution

Create a focused set of specialist skills that tackle the highest-signal,
highest-repeat Arduino and embedded pain points:

- `i2c-bringup-diagnostician`
- `library-compatibility-auditor`
- `upload-path-recovery`
- optional follow-ons:
  - `board-manager-install-recovery`
  - `heap-runtime-investigator`
  - `core-version-regression-triager`

Each skill should be workflow-first, evidence-driven, and designed around
progressive disclosure with minimal top-level instructions and supporting
references or scripts for deeper branches.

## AI Translation Layer

- Mission: turn discovery-backed embedded pain points into a small set of
  sharply scoped skills that solve recurring real-world failures.
- Core behavior contract: each skill should guide diagnosis, eliminate the most
  likely false leads, and produce actionable next steps or minimal test code.
- Constraints: avoid overlap with existing skills, keep the top-level file
  narrow, and anchor behavior in actual ecosystem failure patterns.
- Definition of done: the repo has a prioritized implementation map for the new
  skills and each candidate has a clear scope boundary, assets list, and test
  strategy.

## User Stories

1. As an Arduino beginner, I want help isolating I2C failures, so that I can
   stop guessing between wiring, voltage, addresses, and bad libraries.
2. As an intermediate maker, I want compile logs translated into board and
   library compatibility guidance, so that I can fix the real issue instead of
   chasing warnings.
3. As a user installing ESP32 or other large board packages, I want recovery
   steps for installation failures, so that I can get back to a working tool
   chain quickly.
4. As a board user stuck on uploads, I want a USB, boot mode, and port decision
   tree, so that I can recover without random cable swapping.
5. As an embedded developer, I want runtime memory instrumentation patterns, so
   that I can catch heap depletion and stack pressure before a crash.
6. As a maintainer, I want each new skill to fill a distinct gap, so that the
   repo grows by coverage, not by duplication.
7. As an agent consumer, I want concise skill entrypoints and deeper references
   only when needed, so that discovery and activation stay efficient.
8. As a maintainer, I want the first implementation wave prioritized, so that
   effort goes into the highest-pain and lowest-overlap opportunities first.

## Execution Phases

### Phase 1: Define skill boundaries and overlap policy

- Goal: lock down which new skills are distinct enough to justify their own
  folders.
- Acceptance criteria:
  - each candidate skill has a one-sentence mission
  - overlap with existing repo skills is documented
  - top-three implementation priority is agreed
- Dependencies: discovery research and repo inventory
- Exit condition: no candidate remains fuzzy or redundant

### Phase 2: Design the first three skills

- Goal: produce implementation-ready designs for:
  - `i2c-bringup-diagnostician`
  - `library-compatibility-auditor`
  - `upload-path-recovery`
- Acceptance criteria:
  - each skill has a proposed `name` and `description`
  - each skill has a workflow outline
  - supporting references and scripts are enumerated
  - failure boundaries are explicit
- Dependencies: Phase 1
- Exit condition: each priority skill can be implemented without rediscovery

### Phase 3: Design follow-on skills

- Goal: scope the second wave:
  - `board-manager-install-recovery`
  - `heap-runtime-investigator`
  - `core-version-regression-triager`
- Acceptance criteria:
  - each skill has a justification for being separate rather than merged
  - each skill has a minimal v1 surface
- Dependencies: Phase 2
- Exit condition: follow-on skills are backlog-ready

### Phase 4: Implementation and validation

- Goal: add the first wave to the repo using the current Agent Skills contract
- Acceptance criteria:
  - skills validate structurally
  - supporting references are present
  - any scripts have runnable `--help`
  - overlap with older skills is still acceptable
- Dependencies: approved designs and plan artifacts
- Exit condition: first-wave skills are live and validated

## Writing Plan Handoff

- Recommended plan objective: implement the first wave of discovery-backed
  specialist Arduino pain-point skills
- Major task groups:
  - convert shortlist into final skill specs
  - create skill folders and top-level `SKILL.md` files
  - write references and helper scripts
  - validate conformance and runnable script surfaces
- Dependencies that must stay ordered:
  - first-wave scoping before writing files
  - top-level workflow before deeper references
  - structural validation after each skill is added
- Expected artifacts:
  - three new skill folders for the first wave
  - supporting references and optional scripts
  - refreshed README inventory if the skills are implemented
- Plan-level verification expectations:
  - repo validator passes
  - each new skill has clear overlap notes
  - scripts run with `--help` where present

## Executing Plan Handoff

- Recommended execution mode: one skill at a time, with validation after each
  addition
- Expected batch or slice order:
  1. `i2c-bringup-diagnostician`
  2. `library-compatibility-auditor`
  3. `upload-path-recovery`
  4. optional second-wave skills
- Checkpoints that require review or proof:
  - each skill's scope boundary against existing skills
  - any scripted diagnostics that parse logs or generate probe sketches
  - final structural validation
- Likely blocked states:
  - scope creep into generic debugging
  - accidental duplication with `error-message-explainer` or
    `arduino-cli-skill`
  - missing examples for board-family-specific branches
- Verification gates before completion:
  - new skills validate structurally
  - added scripts expose working CLI help
  - README inventory updates are consistent if the repo surface changed

## Implementation Decisions

- Prefer narrow specialist skills over one large troubleshooting umbrella skill.
- Keep existing repo skills intact; fill gaps rather than merging everything.
- Treat I2C diagnosis, compatibility diagnosis, and upload recovery as the first
  wave because they combine high pain with low overlap.
- Defer version-regression triage unless more ESP32-family maintenance work is
  desired.
- Keep all new skills aligned to the current Agent Skills schema and
  progressive-disclosure rules.

## Testing Decisions

- Good tests should prove that each skill can guide the correct branch of a
  failure workflow, not just that the markdown exists.
- Modules to test later:
  - any compile-log parser
  - any generated probe-sketch helper
  - any install or upload checklist references that encode deterministic commands
- Prior art:
  - existing repo validator for structure
  - existing CLI-style helper scripts in the repo for `--help` expectations

## TDD Slice Seeds

### Phase 2 skill designs

- Behavior under test: the I2C skill routes "scanner sees address but library
  fails" to the correct decision path
- Expected red evidence: missing or ambiguous branch in the initial workflow
- Minimum green target: explicit branch with next-step probes and likely root
  causes
- Likely refactor boundary: shared reference for voltage, address, and pull-up
  checks

- Behavior under test: the compatibility skill distinguishes warning lines from
  actual compile-failure lines
- Expected red evidence: sample log is summarized incorrectly
- Minimum green target: workflow identifies the true error class and next action
- Likely refactor boundary: reusable log-scan rules

- Behavior under test: the upload recovery skill separates board protocol, boot
  mode, and USB path problems
- Expected red evidence: decision tree collapses unrelated failures into one path
- Minimum green target: at least one board-family-aware recovery branch
- Likely refactor boundary: shared USB and serial monitor troubleshooting table

### Phase 3 follow-ons

- Behavior under test: the install-recovery skill identifies timeout vs cache vs
  board index failures
- Expected red evidence: all install failures route to one generic retry step
- Minimum green target: distinct recovery paths with deterministic commands
- Likely refactor boundary: reusable CLI and IDE split

- Behavior under test: the heap skill emits runtime instrumentation guidance
- Expected red evidence: only static "avoid String" advice exists
- Minimum green target: board-specific runtime measurement workflow
- Likely refactor boundary: AVR vs ESP32 instrumentation references

## Out of Scope

- Implementing all proposed skills immediately
- Refactoring unrelated existing skills during this discovery effort
- Adding CI or publishing automation
- Writing broad embedded theory skills unrelated to the researched pain points

## Further Notes

- Discovery evidence is recorded in `brainstorm-embedded-pain-points.md`.
- This PRD is intentionally a roadmap artifact, not an implementation claim.
