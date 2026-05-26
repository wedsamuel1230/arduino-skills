---
name: i2c-bringup-diagnostician
description: Use when users need to diagnose I2C bring-up failures on Arduino or ESP32-class boards, including no devices found, wrong readings, address conflicts, scanner-detects-but-library-fails cases, pull-up problems, or board-family-specific bus quirks.
---

# I2C Bringup Diagnostician

Use this skill when the sensor or device should be on the bus, but the I2C path
is still not trustworthy.

## Resources

- `references/bringup-flow.md` - ordered I2C fault-isolation workflow
- `references/scanner-vs-library.md` - what to do when the scanner finds the device but the library still fails
- `references/esp32-and-board-quirks.md` - ESP32-family and board-specific caveats
- `../../docs/board-support/uno-r4-family.md` - Uno R4 family board notes when relevant

## When to Use

Use this skill when the request includes:

- "no I2C devices found"
- scanner finds the address but the library cannot initialize the device
- two I2C devices conflict or one disappears
- ESP32 pin, bus, or second-channel confusion
- pull-up, wire-length, or voltage-level questions
- obviously wrong sensor values after basic detection succeeds

## Workflow

1. Establish the basic failure shape:
   - no scanner detection -> open `references/bringup-flow.md`
   - scanner detects but library fails -> open
     `references/scanner-vs-library.md`
   - ESP32-family multi-bus or pin issue -> open
     `references/esp32-and-board-quirks.md`
2. Confirm the electrical basics before library swapping:
   - power
   - common ground
   - SDA and SCL mapping
   - pull-ups
   - logic level compatibility
3. Only after the bus is electrically plausible, check address, device mode, and
   library expectations.
4. If the board is Uno R4 family and the failure involves board-specific I2C or
   support questions, also open `../../docs/board-support/uno-r4-family.md`.

## Core Rules

- Scanner success does not prove the library is using the device correctly.
- Library failure does not prove the sensor is dead.
- Bus voltage, pull-ups, and pin mapping must be explicit before changing code
  blindly.
- For ESP32-family boards, pin choices and multi-bus assumptions are not always
  portable across variants.

## Verification

- Confirm whether the scanner sees the expected address.
- Confirm whether a minimal register or identification read works.
- Confirm whether the failing behavior tracks a board family, bus instance, or
  library rather than the sensor alone.
- Confirm whether the final fix survives repeated scans and actual sensor reads.

## Integration

- Pair with `circuit-debugger` for deeper hardware isolation.
- Pair with `datasheet-interpreter` when the correct address, power, or timing
  details are not known.
- Pair with `arduino-code-generator` when the user needs a minimal test sketch or
  a cleaned-up bus probe.
