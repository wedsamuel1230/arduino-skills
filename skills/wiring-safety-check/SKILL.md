---
name: wiring-safety-check
description: Use when wiring an Arduino, ESP32, ESP32-S3, Pico, or Pico W to sensors, LEDs, motors, relays, buses, or external supplies, especially when 5 V and 3.3 V logic, current limits, pull-ups, level shifting, inductive loads, or safe defaults matter.
metadata:
  triggers: "wire sensor, connect 5V, level shifting, current limit, pull-up, power rail, GPIO safety"
  attribution: "Adapted from the shared Arduino safety contract and Agent Skills task-fragility guidance."
---

# Wiring Safety Check

Check the electrical contract before code or power is applied. A board's input
voltage or per-pin maximum does not prove that a connected signal or total rail
is safe.

## Intake

Record the exact board/module and logic voltage, sensor/actuator part number,
each rail, signal direction, VIH/VIL/input maximum, current and startup peak,
pull-up location/value, ground path, cable length, protection, default state,
and whether a level shifter, driver, flyback path, fuse, or current limiter is
present.

## Process

1. Draw a rail and ground map, including USB/VIN/VSYS/3V3 paths and regulators.
2. Check every signal in both directions. A 5 V supply does not imply 5 V-safe
   I/O; a 3.3 V MCU input must not receive an out-of-range high level.
3. Calculate steady and peak current with regulator, connector, wiring, and
   thermal margin. Do not add per-pin absolute maxima into a board budget.
4. Check pull-ups for bus voltage, value, rise time, fanout, and duplicate
   resistors. Check I2C/SPI/UART default pins against the board profile.
5. Add level shifting, divider, transistor/MOSFET driver, flyback protection,
   decoupling, or isolation when the electrical contract requires it.
6. Define safe reset and fault states before enabling an output or motor.
7. Stop at the physical gate until continuity, polarity, rail, and load
   measurements are captured.

## Required 5 V to ESP32 result

When a user says only "wire a 5 V sensor to ESP32", flag the missing level
compatibility immediately: ESP32 GPIO is 3.3 V class and is not generally 5 V
tolerant. Ask for the sensor's actual I/O levels and require a suitable level
shifter or divider for any 5 V signal entering the ESP32. A shared ground does not solve level incompatibility. Check whether the sensor accepts a 3.3 V supply
and whether its output is open-drain before choosing the circuit.

## Anti-rationalization

| Shortcut | Response |
|---|---|
| "It is a 5 V sensor, so its data pin is safe." | Inspect the sensor datasheet and flag level shifting for a 5 V high. |
| "A shared ground fixes it." | Ground reference is necessary but does not change logic thresholds. |
| "20 mA per pin is the board budget." | Check rail, regulator, connector, total load, and peak current. |
| "The LED or motor is small." | Check inrush, stall current, inductive kick, and driver topology. |
| "I already powered it." | Stop, inspect, and record measurements; do not infer safety from survival. |

## Verification

- Wiring table names source/destination, voltage, direction, and protection.
- Level-shifting and pull-up decisions cite a datasheet or are explicitly
  unresolved.
- Continuity/polarity and unloaded/load rail measurements are captured.
- Build/upload evidence is not promoted to hardware or system proof.

## Shared output contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
