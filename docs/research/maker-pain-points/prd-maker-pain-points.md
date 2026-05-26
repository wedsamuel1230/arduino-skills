# PRD: Maker-Focused Agent Skills and Uno R4 Support

## Problem Statement

The repository already helps with Arduino code and tooling, but maker pain
often appears after the prototype first works. OTA workflows break, field power
paths behave differently from USB bench power, calibration is improvised, and
newer boards like Uno R4 WiFi have support quirks that are broader than a
single compile error or upload message. The repo needs a maker-first skill wave
that helps projects survive deployment and iteration, not only initial coding.

## Solution

Add a maker-focused first wave of skills and board-family support:

Primary skills:

- `ota-deployment-guardian`
- `sensor-calibration-workbench`
- `field-power-and-connectivity-triager`
- `i2c-bringup-diagnostician`

Cross-cutting board support initiative:

- add Uno R4 Minima and Uno R4 WiFi support references into relevant skills
- treat Uno R4 board support as a shared support pack first, not a standalone
  skill

## AI Translation Layer

- Mission: shift the repo toward maker workflows that matter after first boot,
  especially OTA, calibration, field power, and Uno R4 support.
- Core behavior contract: the first new skills should help makers keep devices
  updateable, readings trustworthy, and boards supportable in real conditions.
- Constraints: do not duplicate current generic skills, keep top-level skills
  narrow, and use shared board-family references when possible.
- Definition of done: the repo has a clear first-wave maker-skill backlog and a
  concrete Uno R4 support strategy.

## User Stories

1. As a maker with a remote ESP32 device, I want OTA to remain recoverable, so
   that I do not lose my remote maintenance path.
2. As a maker calibrating a CO2 sensor, load cell, or compass, I want a guided
   calibration workflow, so that my readings become trustworthy.
3. As a maker moving from USB power to real deployment power, I want help
   diagnosing field-only failures, so that my project works off the bench.
4. As a Uno R4 user, I want board-specific support references, so that I can
   understand WiFi, OTA, USB, and firmware bridge quirks.
5. As a maintainer, I want Uno R4 support to be shared across skills, so that I
   do not create a redundant board-only mega-skill prematurely.

## Execution Phases

### Phase 1: Maker-first scope lock

- Goal: finalize the maker-first wave and Uno R4 support strategy
- Acceptance criteria:
  - first-wave skills are prioritized
  - Uno R4 support is framed as shared references
  - overlap with existing repo skills is documented
- Dependencies: discovery research
- Exit condition: no major scope ambiguity remains

### Phase 2: Design first-wave maker skills

- Goal: produce implementation-ready designs for:
  - `ota-deployment-guardian`
  - `sensor-calibration-workbench`
  - `field-power-and-connectivity-triager`
- Acceptance criteria:
  - each skill has a `name`, `description`, workflow outline, references list,
    and verification concept
- Dependencies: Phase 1
- Exit condition: each skill can be implemented without rediscovery

### Phase 3: Add shared Uno R4 support map

- Goal: define the shared board-family reference pack for Uno R4 Minima and
  Uno R4 WiFi
- Acceptance criteria:
  - relevant host skills are identified
  - the shared references cover OTA, USB, serial-monitor, and firmware-bridge
    considerations
- Dependencies: Phase 2
- Exit condition: Uno R4 support can be implemented as cross-cutting references

### Phase 4: Second-wave engineering skills

- Goal: scope `i2c-bringup-diagnostician` and later engineering-focused skills
- Acceptance criteria:
  - second-wave ordering is explicit
- Dependencies: maker-first design complete
- Exit condition: later work is backlog-ready

## Writing Plan Handoff

- Recommended plan objective: implement the maker-first skill wave and shared
  Uno R4 support references
- Major task groups:
  - design first-wave skills
  - define Uno R4 shared support pack
  - implement skill folders and references
  - validate repo conformance
- Dependencies that must stay ordered:
  - maker-first skill definitions before file creation
  - Uno R4 support mapping before editing multiple skills

## Executing Plan Handoff

- Recommended execution mode: one maker skill at a time, then shared Uno R4
  support references
- Expected batch order:
  1. `ota-deployment-guardian`
  2. `sensor-calibration-workbench`
  3. `field-power-and-connectivity-triager`
  4. Uno R4 shared support references
  5. `i2c-bringup-diagnostician`

## Implementation Decisions

- Prefer maker workflow skills over additional generic compiler guidance.
- Keep Uno R4 support as shared references first.
- Treat Uno R4 WiFi as operationally distinct from Uno R4 Minima.

## Testing Decisions

- Good tests later should verify that each skill routes high-risk maker failures
  to distinct next steps.
- Uno R4 support references should be checked for cross-skill consistency.

## TDD Slice Seeds

- Behavior under test: OTA skill distinguishes IDE discovery failure from
  missing OTA implementation in the uploaded sketch
- Expected red evidence: both route to the same generic retry step
- Minimum green target: explicit branches with concrete next checks

- Behavior under test: calibration skill distinguishes warm-up, scaling, and
  persistence problems
- Expected red evidence: one generic checklist handles all failures badly
- Minimum green target: at least one clear branch per failure class

- Behavior under test: field-power skill distinguishes software failure from
  power-path failure
- Expected red evidence: USB-only success is treated like a WiFi code bug
- Minimum green target: explicit power-path branch and next measurements

- Behavior under test: Uno R4 support stays shared rather than fragmented
- Expected red evidence: conflicting advice appears in multiple skills
- Minimum green target: one shared Uno R4 support map consumed by multiple
  skills

## Out of Scope

- Implementing all later engineering skills in the same wave
- Creating a standalone Uno R4 mega-skill before shared references are tried

## Further Notes

- Discovery evidence is recorded in `brainstorm-maker-pain-points.md`.
