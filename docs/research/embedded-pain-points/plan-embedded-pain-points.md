# Embedded Pain-Point Skills Plan

**Goal:** Turn the researched Arduino and embedded failure hotspots into a
prioritized specialist-skill backlog.

**Scope:** Design and planning only in this pass. Do not implement the new
skills yet.

## Task Group 1: Finalize the first-wave scope

### Task 1.1

- Target files: `brainstorm-embedded-pain-points.md`
- Action: review first-wave candidates and keep the top three
- Verification:
  - confirm each chosen skill has a distinct mission and overlap note

### Task 1.2

- Target files: `prd-embedded-pain-points.md`
- Action: encode first-wave priority and follow-on backlog structure
- Verification:
  - confirm execution phases and TDD slice seeds exist

## Task Group 2: Convert skill ideas into implementation-ready specs

### Task 2.1

- Target output:
  - one spec section per first-wave skill
- Action:
  - define `name`
  - define concise `description`
  - define workflow outline
  - list references and scripts needed
- Verification:
  - each skill can be implemented without rediscovery

### Task 2.2

- Target output:
  - overlap matrix against current skills
- Action:
  - state whether each idea is new, an extension, or a wrapper around an
    existing skill
- Verification:
  - no candidate silently duplicates repo coverage

## Task Group 3: Prepare future implementation slices

### Task 3.1

- Target files: `tests-map-embedded-pain-points.md`
- Action: define future validation expectations for new skills and any helper
  scripts
- Verification:
  - structural, behavior, and script checks are all represented

### Task 3.2

- Target output:
  - future per-skill task list
- Action:
  - order future implementation as
    1. I2C skill
    2. compatibility skill
    3. upload recovery skill
- Verification:
  - order matches pain severity and overlap analysis

## Future Implementation Phases

1. Build `i2c-bringup-diagnostician`
2. Build `library-compatibility-auditor`
3. Build `upload-path-recovery`
4. Reassess whether install recovery or heap investigation should come next

## Stop Conditions

- stop if a proposed skill cannot be separated cleanly from an existing one
- stop if the evidence for a pain point is too weak or too one-off
- stop if the design starts expanding into a generic mega-skill
