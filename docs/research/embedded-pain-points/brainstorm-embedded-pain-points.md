# Embedded and Arduino Pain Points Brainstorm

## Chosen Discovery Path

Used the `brainstorming` path rather than `grill-with-docs`.

Reason:

- the request is option exploration and prioritization
- the repository vocabulary is already stable enough after the recent
  canonicalization pass
- the critical missing input was external evidence of recurring user pain, not
  glossary clarification

## Current Repo Coverage

The repo already covers:

- generic code generation
- project scaffolding
- serial monitoring
- circuit debugging
- compiler error explanation
- Arduino CLI workflows
- FreeRTOS patterns
- datasheet extraction

The gaps are not broad "Arduino help" gaps. They are workflow-specific:

1. bus bring-up triage
2. library and board compatibility diagnosis
3. install or update recovery
4. upload and USB serial path recovery
5. runtime memory or heap investigation
6. core or board version regression triage

## External Pain Signals

### 1. I2C bring-up is still one of the highest-friction workflows

Representative signals:

- Arduino Forum, January 13, 2026:
  https://forum.arduino.cc/t/esp32-not-detecting-mlx90614esf-baa-i2c-scanner-fails/1425014
  - sensor reports nonsense values
  - multiple pull-up, voltage, and library combinations already tried
  - user linked multiple historical core issues because the failure is hard to
    localize
- espressif/arduino-esp32 issue #10685, opened December 4, 2024:
  https://github.com/espressif/arduino-esp32/issues/10685
  - dual I2C works on one ESP32 family but fails on another
  - user already isolated wiring and reproduced across boards and simulation
- espressif/arduino-esp32 issue #11787, opened September 2, 2025:
  https://github.com/espressif/arduino-esp32/issues/11787
  - version-specific I2C logging floods the serial output and hides application
    logs

What this means:

- current pain is not only "device not found"
- users need help distinguishing wiring faults, sensor faults, wrong voltage,
  wrong pins, bad pull-ups, library mismatch, and core regression

### 2. Library errors are often misread because the first visible message is not the root cause

Representative signal:

- Arduino Forum, March 16, 2026:
  https://forum.arduino.cc/t/multiple-libraries-were-found-for-wire-h/1435571
  - user focused on the "Multiple libraries were found" line
  - actual root cause was a board/library mismatch and missing `Serial` support
    on the selected target

What this means:

- users need root-cause extraction from verbose compile logs
- "warning vs real error" is a distinct workflow from generic compiler message
  explanation
- board architecture compatibility should be checked before line-by-line advice

### 3. Package install and board-manager updates fail in non-obvious ways

Representative signal:

- arduino-cli issue #3013, opened September 23, 2025:
  https://github.com/arduino/arduino-cli/issues/3013
  - large platform installs fail with `context deadline exceeded`
  - raising `network.connection_timeout` from `60s` to `240s` fixes it
  - the issue links a long chain of follow-on failures affecting IDE and CLI
    users

What this means:

- beginners experience install failure as "Arduino is broken"
- the recovery path depends on whether they use CLI or IDE, and on what
  platform package is being fetched
- there is a narrow but valuable automation opportunity here

### 4. Upload and serial workflows are fragile and often board-specific

Representative signals:

- Arduino issue #11996, opened October 21, 2024:
  https://github.com/arduino/arduino/issues/11996
  - Uno R4 serial monitor does not reconnect after reset
- Arduino Forum, September 30, 2025:
  https://forum.arduino.cc/t/port-not-recognized-properly-code-stuck-uploading/1408054
  - firmware flashing timed out until an unrelated USB headset was removed

What this means:

- users need a layered decision tree for USB mode, boot mode, board package,
  port protocol, hub or cable interference, and monitor state
- existing generic upload troubleshooting is too broad

### 5. Memory and heap behavior remains poorly understood

Representative signals:

- Arduino Forum, February 5, 2024:
  https://forum.arduino.cc/t/memory-fragmentation/1220388
  - user asked whether local variables fragment memory
  - response distinguished normal stack usage from `String`-driven heap problems
- repo-local evidence:
  `code-review-facilitator` and `error-message-explainer` already warn about
  `String`, RAM overflow, and heap issues, so the repo knows this is common

What this means:

- there is room for a focused runtime-memory skill, not just a static review
  checklist
- users need instrumentation, not only advice

## Proposed Skill Opportunities

## Option A: Build one large "embedded-troubleshooter" skill

Pros:

- single entry point
- easy discovery for beginners

Cons:

- conflicts with progressive disclosure
- duplicates existing repo coverage
- becomes hard to maintain because upload, I2C, memory, and package management
  evolve independently

Verdict:

- not recommended

## Option B: Extend existing skills only

Pros:

- low surface growth
- reuses current inventory

Cons:

- pushes unrelated workflows into already broad skills
- makes discovery less precise
- some problems deserve a dedicated workflow, not a subsection

Verdict:

- partially recommended, but not sufficient

## Option C: Add a narrow set of high-signal specialist skills

Pros:

- best fit for the repo's current structure
- aligns to real user failure modes
- easiest to keep current as toolchains change

Cons:

- adds more skill folders
- needs careful overlap control

Verdict:

- recommended

## Recommended Skill Shortlist

### 1. `i2c-bringup-diagnostician`

Mission:

- isolate whether an I2C failure is caused by wiring, voltage, address,
  pull-ups, board pin mapping, core version, or library mismatch

Why it is not covered well today:

- `circuit-debugger` is too generic
- `datasheet-interpreter` extracts specs but does not drive fault isolation
- `arduino-code-generator` can emit an I2C scanner, but not a decision tree

Likely assets:

- bus checklist
- address and voltage sanity matrix
- generated minimal probe sketches
- "scanner sees device but library fails" branch
- ESP32-family pin and second-bus caveat reference

### 2. `library-compatibility-auditor`

Mission:

- read verbose compile output and determine whether the real problem is board
  mismatch, architecture incompatibility, duplicate library confusion, example
  version drift, or a real code error

Why it is not covered well today:

- `error-message-explainer` explains compiler errors line-by-line
- it does not explicitly rank likely root causes across board, library, and
  architecture metadata

Likely assets:

- compile log parser
- library.properties reader
- compatibility decision tree
- "warning line vs root-cause line" workflow

### 3. `board-manager-install-recovery`

Mission:

- recover from board or library package install failures in Arduino IDE and
  `arduino-cli`

Why it is not covered well today:

- `arduino-cli-skill` gives commands, but not a full recovery flow for timeout,
  package index, proxy, or cache problems

Likely assets:

- timeout tuning guide
- cache and index reset checklist
- IDE vs CLI branch
- large-platform download troubleshooting

### 4. `upload-path-recovery`

Mission:

- fix upload, boot mode, COM port, DFU mode, monitor interference, and USB-path
  failures

Why it is not covered well today:

- `error-message-explainer` includes some upload fixes
- `arduino-cli-skill` covers commands
- neither gives a full board-family-specific recovery tree

Likely assets:

- board-family upload matrix
- protocol mapping: serial, DFU, UF2, bootloader
- port and cable sanity checklist
- serial monitor conflict checks

### 5. `heap-runtime-investigator`

Mission:

- instrument and explain RAM, heap, stack headroom, `String` churn, and
  long-run instability

Why it is not covered well today:

- `code-review-facilitator` catches static smells
- there is no focused runtime-investigation workflow

Likely assets:

- probe macros for AVR and ESP32
- min-free-heap logging workflow
- stack headroom checks
- static vs dynamic allocation triage

### 6. `core-version-regression-triager`

Mission:

- detect when a failure is caused by a board core or toolchain version change
  rather than user code or wiring

Why it matters:

- the ESP32 I2C logging issue and ESP32-C6 dual-I2C issue both show that
  version-specific regressions can look like user mistakes

Likely assets:

- minimal reproduction workflow
- version bisect checklist
- known-bad and known-good matrix format
- downgrade or pinning guidance

## Priority Recommendation

If only three skills should be built first:

1. `i2c-bringup-diagnostician`
2. `library-compatibility-auditor`
3. `upload-path-recovery`

Reason:

- highest pain concentration
- least overlap with current repo
- strongest beginner and intermediate value

If a fourth is added:

4. `board-manager-install-recovery`

If a fifth is added:

5. `heap-runtime-investigator`

Keep `core-version-regression-triager` as a narrower advanced skill unless the
repo starts targeting more ESP32-family maintenance work.
