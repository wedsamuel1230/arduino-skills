# Measurement Checklist

Use this reference before concluding the problem is in firmware.

## Capture These Measurements

- source voltage
- board input voltage
- 3V3 rail voltage
- whether voltage changes during WiFi start or peripheral activity
- whether the board resets, hangs, or simply loses connectivity

## Evidence To Keep

- exact power source used
- exact connection point used on the board
- whether peripherals share the same source
- whether the behavior changes after warm-up

## Decision Hint

If the sketch is identical and only the power path changes, power integrity
deserves priority over code changes.
