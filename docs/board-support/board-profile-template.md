# Board Profile Template

Fill this profile before board-dependent code, wiring, power, upload, or
recovery advice. Unknown values stay `unknown` until verified from the board
documentation, project files, or measurements.

## Identity

| Field | Value |
|---|---|
| Board family and exact model/revision | `unknown` |
| MCU and architecture | `unknown` |
| Bootloader / ROM boot mode | `unknown` |
| Board package or SDK | `unknown` |
| Framework | Arduino / ESP-IDF / Pico SDK / vendor / other |
| Host OS and architecture | `unknown` |
| Toolchain and version | `unknown` |

## Hardware Contract

| Field | Value |
|---|---|
| Logic voltage and tolerances | `unknown` |
| Input supply range | `unknown` |
| Peak and continuous current budget | `unknown` |
| Flash / RAM / storage limits | `unknown` |
| Reserved, boot, strapping, or debug pins | `unknown` |
| Available GPIO, ADC, PWM, timers, and interrupts | `unknown` |
| USB, UART, I2C, SPI, CAN, Ethernet, Wi-Fi, BLE | `unknown` |
| Reset, watchdog, brownout, and safe-output behavior | `unknown` |

## Peripheral Map

For each device record its bus/protocol, address or chip select, voltage,
pull-ups/termination, interrupt/reset pins, library, and maximum rate. Check
that the selected pins are valid on this exact board and do not conflict with
boot or debug behavior.

## Verification Checklist

- [ ] Board and revision match the source documentation or a clear photo.
- [ ] Pin numbers are mapped to the exact package, not a similar board.
- [ ] Memory, flash layout, and required runtime features fit the target.
- [ ] Peripheral voltage and current are compatible with the board and supply.
- [ ] Protocol wiring, addresses, pull-ups, termination, and level shifting are
      accounted for.
- [ ] Board package, framework, library, and tool versions are recorded.
- [ ] Upload, boot, reset, and recovery paths are known before flashing.
- [ ] Any unverified field is called out in the final limitations.

Record the selected peripherals and communication protocols explicitly; do not
leave either as an implied property of the board family.
