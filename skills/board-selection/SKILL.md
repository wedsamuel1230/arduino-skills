---
name: board-selection
description: Use when choosing or replacing an Arduino Uno, Uno R4, ESP32, ESP32-S3, Raspberry Pi Pico, Pico W, or another embedded board from project requirements. Compare exact board constraints, toolchains, libraries, power, memory, peripherals, recovery, and lifecycle fit before implementation.
metadata:
  triggers: "choose a board, board recommendation, replace MCU, Arduino vs ESP32 vs Pico, hardware selection"
  attribution: "Adapted from Agent Skills progressive-disclosure and verification guidance; board facts live in the repository reference index."
---

# Board Selection

Choose a concrete board target from requirements rather than a marketing family
name. This skill produces a decision record that downstream skills can consume.

## Boundary With Board Support

Use `board-support` when the user has named a board and needs its exact profile,
capabilities, pin hazards, source status, or framework compatibility. Use this
skill when the user is choosing, replacing, or comparing boards against project
requirements. Consume the board-support profile instead of repeating or
guessing its facts.

## Intake

Capture required voltage and rails, inputs/outputs, PWM/ADC/timers, buses and
protocols, memory/flash/PSRAM, radio/USB, timing, power source and peak load,
physical constraints, production quantity, toolchain, library constraints,
security/update needs, and recovery access.

Read `../../references/boards/README.md` and use `../board-support/SKILL.md` for
the relevant exact profile. If the board is not covered, use the vendor product
page, MCU/module datasheet, board schematic, and selected framework variant
source. Label inferred values.

## Process

1. Turn requirements into hard constraints and preferences.
2. Eliminate candidates that fail voltage, pin direction, peripheral, memory,
   power, or recovery constraints.
3. Compare remaining boards across exact SKU, framework/core, toolchain,
   library architecture, upload path, security/update support, availability,
   and maintenance horizon.
4. Record the selected board, rejected alternatives, reasons, open risks, and
   the exact build identifier/FQBN/environment.
5. Hand the board profile to `pin-assignment`, `wiring-safety-check`,
   `library-selection`, `memory-budgeting`, and `hardware-tdd` as applicable.

## Output

Return a compact table with `requirement`, `constraint`, `candidate result`,
`source`, and `verification status`, followed by the decision and open risks.
Do not present a board-family fact as a board-revision guarantee.

## Anti-rationalization

| Shortcut | Response |
|---|---|
| "ESP32" is precise enough. | Ask for module suffix, DevKit revision, flash/PSRAM, and USB use. |
| "The board has enough memory." | Separate nominal memory, application memory, heap/stack, filesystem, and OTA partitions. |
| "USB power will run it." | Check rail voltage, regulator headroom, startup peaks, and external loads. |
| "Any Arduino library will work." | Check architecture, framework, version, API, and dependency compatibility. |
| "It compiles, so it is the right board." | Keep electrical, hardware, system, and deployment proof open. |

## Verification

- The exact board/revision, MCU/module, framework, toolchain, and version are
  recorded.
- Every chosen value has a primary source or is marked `to verify`.
- A compile-only or dry-run path exists for the selected target.
- Rejected alternatives and unresolved risks remain visible.

## Shared output contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
