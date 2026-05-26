---
name: sensor-calibration-workbench
description: Use when makers need calibration workflows for sensors such as CO2 sensors, load cells, magnetometers, color sensors, or analog sensors, including warm-up behavior, reference measurements, coefficient storage, and drift checks.
---

# Sensor Calibration Workbench

Use this skill when the sensor technically works, but the readings are not yet
trustworthy enough for the project.

## Resources

- `references/calibration-flow.md` - end-to-end calibration workflow and evidence checklist
- `references/common-failure-patterns.md` - warm-up, scaling, drift, saturation, and environment mistakes
- `references/persistence-and-revalidation.md` - storing coefficients and deciding when recalibration is needed

## When to Use

Use this skill when the request involves:

- volatile or implausible sensor readings
- "how do I calibrate this sensor?"
- load-cell factor tuning
- CO2, magnetometer, or color-sensor calibration
- storing calibration coefficients in EEPROM or flash
- deciding whether the problem is calibration, hardware, or environment

Do not use this skill when the sensor is not detected at all. That should route
through hardware or bus bring-up first.

## Workflow

1. Confirm the measurement problem:
   - unstable -> open `references/common-failure-patterns.md`
   - offset or scaling error -> open `references/calibration-flow.md`
   - values good once but bad later -> open
     `references/persistence-and-revalidation.md`
2. Identify the calibration class:
   - one-point or zero-offset
   - two-point scale calibration
   - multi-orientation or environmental calibration
3. Collect reference evidence before changing coefficients:
   - known reference values
   - warm-up state
   - ambient conditions
   - sample stability
4. Decide how calibration values will persist and how revalidation will be
   triggered after reboot, firmware update, or field drift.

## Core Rules

- Calibration without a known reference is guesswork.
- Warm-up and stabilization time are part of calibration, not a side note.
- Do not mix hardware-fault symptoms with coefficient-tuning symptoms.
- Store both the calibration values and enough metadata to know when they became
  stale.

## Verification

- Confirm readings converge toward a known reference after calibration.
- Confirm the calibrated values stay stable across repeated samples.
- Confirm stored coefficients reload correctly after restart.
- If the project has operating thresholds, verify those thresholds against the
  calibrated output rather than the raw sensor value.

## Integration

- Pair with `i2c-bringup-diagnostician` or `circuit-debugger` when the sensor is
  not yet electrically trustworthy.
- Pair with `arduino-code-generator` when the user needs persistence or
  filtering code added to the sketch.
- Pair with `field-power-and-connectivity-triager` when sensor behavior changes
  only off USB or under field power conditions.
