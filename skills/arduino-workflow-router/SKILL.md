---
name: arduino-workflow-router
description: Route Arduino and embedded-system requests across Arduino IDE, Arduino CLI, PlatformIO, and vendor-specific tools. Use when a request combines firmware, board constraints, electronics, power, networking, calibration, enclosure, upload, debugging, OTA, or maintenance, or when the exact board or toolchain is not yet clear.
metadata: {triggers: "combined Arduino workflow, embedded routing, board intake, toolchain selection"}
---

# Arduino Workflow Router

Use this skill as the concise entrypoint for complete or cross-discipline
embedded work. For a focused task with a confirmed board and one stage, load the
specialist skill directly.

## Recommended lifecycle entry

For any physical or multi-session request, load `embedded-project-loop` first.
It establishes the goal, one next action, evidence boundary, rollback path, and
user-owned physical gate. Then return here for board and toolchain routing.

## Load First

1. Read `../../docs/arduino-skill-contract.md`.
2. If the work spans sessions or physical actions, `embedded-project-loop` is
   the recommended first skill; create its goal/next-todo state before
   implementation and keep it open until the evidence gate is satisfied.
3. Fill `../../docs/board-support/board-profile-template.md` or state why it is
   unnecessary.
4. When a named board or board family must be resolved, load
   `../board-support/SKILL.md` and its indexed profile before selecting pins.
5. Read `references/board-intake.md` for board and hardware checks.
6. Read `references/toolchain-selection.md` for IDE, CLI, PlatformIO, or vendor
   version and library compatibility.
7. Select specialist skills from the routing table below.
8. Read `references/failure-recovery.md` before upload, boot, power, or firmware
   recovery actions; read `references/connected-device-security.md` for any
   networked or updateable device.

This is the load-first order. Load on demand: references are loaded only when
their trigger applies, so the router stays under 500 lines and detailed
variants remain progressive disclosure.

## Trigger precedence

- For combined, underspecified, or cross-discipline requests, this router owns
  the first route. Load it before any overlapping specialist, including
  `arduino-project-builder` or `board-selection`.
- For physical or multi-session requests, load `embedded-project-loop` before
  this router, then return to this router for the combined specialist route.
- For a single-stage request with a confirmed board and toolchain, load the
  narrowest specialist directly.
- For a named-board reference or capability lookup, `board-support` owns the
  exact identity and source-backed profile. `board-selection` owns choosing or
  replacing a board from requirements and may consume its handoff.
- A board-choice request without implementation, wiring, or lifecycle work may
  start at `board-selection`; once another discipline appears, return to this
  router and preserve the combined-workflow order.
- Do not load both `arduino-serial-monitor` and a second serial-debugging skill;
  the existing serial monitor owns structured runtime evidence.

## Intake Gate

Do not invent a pin, voltage, current limit, memory size, peripheral, protocol,
library version, or upload command. Ask for the missing value or proceed with a
clearly labeled assumption and a verification step. Record the exact board,
framework, toolchain, host, dependency versions, and desired proof stage.

## Routing Table

| Need | Load next | Evidence focus |
|---|---|---|
| Requirements or board choice | `board-selection`, then `board-support`, then `arduino-project-builder` | decision and design |
| Named board reference or capability lookup | `board-support`, then the relevant specialist | exact identity and source-backed constraints |
| Pin map or GPIO declarations | `board-support`, then `pin-assignment`, then `wiring-safety-check` | board constraints and hardware |
| Wiring, voltage, current, or pull-ups | `wiring-safety-check`, `power-budget-calculator`, `circuit-debugger` | hardware |
| Code pattern or board abstraction | `arduino-code-generator`, `non-blocking-patterns`, `memory-budgeting` | build and memory |
| Library or framework dependency | `library-selection`, then the code/project skill | compatibility and memory |
| Datasheet, component, or protocol uncertainty | `datasheet-interpreter`, `i2c-bringup-diagnostician` | hardware assumptions |
| Compile, board discovery, upload, or port | `arduino-cli-skill` plus `error-message-explainer` | build and upload |
| Runtime logs or field symptoms | `arduino-serial-monitor`, `error-message-explainer`, `hardware-tdd` | hardware and system |
| Timing, blocking, or watchdog risk | `non-blocking-patterns`, `hardware-tdd` | build and system |
| Memory or footprint risk | `memory-budgeting`, `library-selection` | build and runtime |
| Calibration or sensor drift | `sensor-calibration-workbench` after detection is proven | system |
| Complete application | `arduino-project-builder`, then the relevant domain skills | design and build |
| Connected update or field deployment | `ota-deployment-guardian` plus the security reference | deployment |
| Parts, PCB-adjacent, or enclosure work | `bom-generator`, `enclosure-designer`, `readme-generator` | design and maintenance |
| Host/simulation/target test plan | `hardware-tdd` and `embedded-project-loop` when physical work is pending | evidence |
| Multi-session, physical, or recovery work | `embedded-project-loop` first, then this router | durable state and user-owned gate |

## Combined Workflows

Skills **can be used together**. Keep one owner for each decision and pass its
artifacts to the next skill. For a combined request, use this concise default
order:

`loop (if long-running) -> board selection/intake -> wiring safety ->
library/memory -> project/code/timing -> toolchain build/upload -> serial and
hardware tests -> system/calibration -> deployment/security/maintenance`

Default combined order: `arduino-workflow-router` -> `board-selection` ->
`board-support` -> `pin-assignment` -> `wiring-safety-check` -> `non-blocking-patterns` ->
`arduino-serial-monitor` -> `hardware-tdd`. Start with
`embedded-project-loop` when the work spans sessions or physical gates, then
keep its next-todo and evidence ledger open through the later stages.

If the user already supplied an exact, supported board identity, skip
`board-selection` and begin with `board-support`; never skip `board-support`
before pin or electrical advice.

- **Battery-powered Wi-Fi sensor**: board intake -> datasheet -> power ->
  project builder -> code generator -> toolchain -> serial/calibration -> OTA
  security -> maintenance README.
- **Uno R4 WiFi upload incident**: board-family reference -> IDE/CLI discovery
  -> serial and error diagnosis -> USB/power checks -> boot recovery -> upload
  proof -> runtime/system proof. See `../../docs/board-support/uno-r4-family.md`.
- **Robot controller**: board intake -> project builder -> power/BOM -> circuit
  and code -> serial/system tests -> enclosure -> signed update and rollback.
- **Multi-board sensor library**: board profiles -> datasheets/protocol bringup
  -> code generator -> IDE/CLI/PlatformIO branches -> per-board build proof and
  documented unsupported behavior.
- **Four-button ESP32 controller**: board selection -> pin assignment -> wiring
  safety -> non-blocking debounce -> code generator -> build proof -> hardware
  gate -> serial/system evidence.

Do not treat a table row as proof that a skill was run. Report which skills were
actually used, which artifacts they produced, and which evidence stages remain
unverified.

## Output Contract

Use `../../docs/arduino-skill-contract.md`: state assumptions, required tools and
versions, implementation steps, tests/evidence by proof stage, known
limitations, and recovery/security notes.
