---
name: memory-budgeting
description: Use when Arduino or embedded projects hit SRAM, flash, heap, stack, partition, JSON-buffer, or performance limits, or when reviewing String use, F() placement, OTA slots, FreeRTOS stacks, or memory margin.
metadata:
  triggers: "memory budget, SRAM, flash, heap, stack, fragmentation, F macro, String, partition"
  attribution: "Adapted from embedded memory-safety practice and the shared Arduino board-profile contract."
---

# Memory Budgeting

Make memory a measured budget, not a nominal board label. The implementation is
embedded C/C++; scripts may parse build or runtime logs when that is the useful
deterministic tool.

## Intake

Record exact board/module, flash/RAM/EEPROM/PSRAM, bootloader and partition
layout, framework, compiler flags, libraries, static buffers, task stacks,
filesystem/OTA needs, peak protocol sizes, and available measurement output.

## Process

1. Separate static data, code/flash, heap, task stacks, interrupt state,
   filesystem, bootloader, and OTA/update slots.
2. Establish a numeric budget and minimum margin for every category. Use board
   references rather than copying a family-level number into a project claim.
3. Capture compiler size output and map changes to a feature or dependency.
4. Measure runtime free heap, largest block, stack high-water marks, and reset/
   allocation failures under representative load where the framework exposes
   them.
5. On AVR, keep literals in flash with `F()` where appropriate, prefer bounded buffers and fixed-size storage, and avoid unbounded dynamic `String` use. On ESP32/RP2040,
   still bound buffers and distinguish heap, stack, flash, and filesystem.
6. Re-run the stress case after each memory-affecting change and record the
   tradeoff.

## Anti-rationalization

| Shortcut | Response |
|---|---|
| "The datasheet says 520 KB, so memory is fine." | Separate usable heap, stacks, reserved regions, and radio/RTOS use. |
| "It compiled." | Inspect size output and exercise runtime allocation paths. |
| "Make the buffer bigger." | Bound the protocol and prove the required maximum. |
| "Use String everywhere." | Check fragmentation and lifetime; use bounded alternatives where needed. |
| "OTA only needs the application image." | Budget both update slots, bootloader, metadata, and rollback image. |

## Verification

- Build-size output and runtime memory evidence name the exact target/version.
- Each budget has a margin and a failure response.
- Stress tests cover peak message, sensor, logging, radio, and task load as
  applicable.
- Optimization does not remove bounds, safety checks, or recovery behavior.

## Shared output contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
