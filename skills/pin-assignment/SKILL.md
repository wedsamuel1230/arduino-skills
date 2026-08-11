---
name: pin-assignment
description: Use when assigning Arduino, ESP32, ESP32-S3, Pico, or Pico W pins; creating a GPIO map; assigning buttons, LEDs, sensors, buses, or actuators; migrating a pin map; or generating constexpr int declarations. Check the exact board and physical pin constraints before emitting the user's ordered raw declaration format.
metadata:
  triggers: "pin map, assign pins, GPIO allocation, constexpr int, buttons, LEDs, board migration"
  attribution: "Adapted from Agent Skills authoring best practices and the repository Arduino skill contract; user pin convention is authoritative."
---

# Pin Assignment

Produce a board-aware pin plan without losing the repository's declaration
convention. A logical declaration ID is not automatically a physical GPIO
number; keep those layers distinct.

## Intake

Record the exact board/revision, MCU/module, framework/core version, toolchain,
signal names, direction, voltage, current, pull requirements, bus ownership,
boot/debug/USB/radio constraints, and whether the user wants declarations,
physical wiring, or both. Load the matching file under `../../references/boards/`
before selecting a physical pin.

## Process

1. Classify every signal as input, output, analog, PWM, bus, interrupt, boot,
   debug, USB, flash, PSRAM, or radio related.
2. Reserve board-specific flash, PSRAM, USB, boot-strapping, debug, and default
   bus pins unless the exact board documentation approves reuse.
3. Reject a candidate whose direction, pull capability, voltage, current, ADC,
   PWM, or protocol behavior does not match the signal.
4. Keep logical IDs stable and allocate them in the requested fixed order.
5. If the user requests only declarations, emit only the declarations as plain
   text. Do not add a code fence, heading, explanation, or trailing comment.
6. If a physical map is requested, provide it separately and label assumptions
   and source-backed constraints.

## Required declaration convention

For the user's custom output mode, use raw C++ declarations in numeric order:

```cpp
constexpr int btn_esc = 101;
constexpr int btn_enter = 102;
constexpr int led_status = 103;
```

Use the next sequential logical value for each requested signal. These values
are stable logical identifiers unless the user explicitly defines them as
physical GPIO numbers. Never replace this format with an enum, macro, array,
namespace, explanatory wrapper, or reordered declaration list.

## Anti-rationalization

| Shortcut | Response |
|---|---|
| "The pin is probably free." | Check the exact board reference and active peripherals. |
| "GPIO34 works for an LED on every ESP32." | Reject classic ESP32 input-only GPIO34-39 for outputs; distinguish ESP32-S3 and verify its module table. |
| "GPIO0 is just another output." | Check its strapping role and reset level before assigning it. |
| "The compile passed." | Keep wiring and target behavior unverified. |
| "I can explain the declarations around the code." | In declarations-only mode, output the raw ordered lines only. |

## Verification

- Declaration names and values are `constexpr int` and strictly increasing
  from the required starting ID.
- Every physical output avoids input-only, flash/PSRAM, USB, and unapproved
  strapping pins for the exact board.
- Voltage/current and pull-up requirements have a source or explicit unknown.
- Build proof, upload proof, hardware proof, and system proof are reported
  separately.

## Shared output contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
