# ESP32 And Board Quirks

Use this reference when the I2C behavior depends on board family rather than
only the sensor.

## ESP32 Family

Watch for:

- non-portable default pins across variants
- assumptions about a second I2C bus
- differences between board families even when similar code worked elsewhere
- core-version-specific behavior

If multi-bus or variant behavior is involved, capture the exact board and core
version before assuming wiring fault.

## Known Diagnostic Questions

- which ESP32 family is this exactly?
- which pins are assigned to each bus?
- is the same sketch known to work on a different ESP32 variant?
- did the behavior change after a core update?

## Uno R4 Family

Uno R4 is not a generic ESP32-style board. If the user is conflating board
families or bus assumptions, open `../../docs/board-support/uno-r4-family.md`
and reset the board-specific expectations first.
