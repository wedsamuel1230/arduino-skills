# Board And Hardware Intake

Use this reference whenever advice depends on a board, module, shield, sensor,
actuator, or power source.

## Required Facts

Record the exact board and revision, MCU, framework, bootloader, logic voltage,
input supply, memory/flash, reserved and boot pins, peripherals, buses,
protocols, current limits, and host/tool versions. Use the board profile template
as the record instead of relying on a product family name alone.

## Checks

1. Resolve the board identifier to the vendor's current pinout and datasheet.
2. Check pin multiplexing, ADC/PWM/timer availability, interrupt behavior,
   bootstrapping pins, debug pins, and USB/UART ownership.
3. Check flash/RAM usage, filesystem/partition layout, watchdog, brownout, and
   reset defaults against the requested features.
4. Check logic levels, pull-ups, level shifting, load current, peak current,
   thermal margin, and the complete power path.
5. Check bus addresses, chip selects, termination, pull-ups, cable length, and
   protocol/library compatibility.
6. Record the upload, boot, reset, debug-probe, and recovery path before making
   a firmware change.

## Decision Rule

If two boards share a marketing name but differ in MCU, connectivity, pinout,
or boot path, treat them as separate targets. If a value is inferred from a
similar board, label it as an assumption and require verification before
energizing or flashing the hardware.
