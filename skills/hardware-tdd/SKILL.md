---
name: hardware-tdd
description: Use when planning tests for Arduino, ESP32, ESP32-S3, Pico, or Pico W firmware; deciding what can run off-target; using Wokwi or simulation; writing host fakes; or accepting a physical hardware feature without confusing compile proof with system proof.
metadata:
  triggers: "hardware test, embedded TDD, Wokwi, simulation, host test, acceptance test, hardware regression"
  attribution: "Adapted from Agent Skills eval integrity guidance and the shared Arduino evidence-stage contract."
---

# Hardware TDD

Build the test ladder before claiming a feature is complete. Pure behavior can
often be tested off-target; voltage, pin mux, timing under load, and physical
assembly still require target evidence.

## Intake

Record exact board/revision, framework/toolchain, hardware invariants, safety
inhibits, simulator model, available instruments, test fixtures, and the proof
stage required by the user.

## Process

1. Turn requirements into observable behavior and safety invariants.
2. Write host tests for pure C/C++ logic using fakes for time, serial, sensors,
   and actuators. Keep hardware adapters thin.
3. Use Wokwi or another simulator only for peripherals and timing that its model
   actually represents; record model limitations.
4. Run an exact-board compile and static checks with the selected toolchain.
5. Create a one-change target checklist: power-off continuity, controlled
   power-up, input observation, output inhibit, reset/recovery, and logs.
6. Ask a physical gate for measurements, photos, or serial output. Do not infer
   target success from a host test or compile log.
7. Record failures as evidence and keep the next test bounded.

## Test matrix

| Layer | Example | Proves | Does not prove |
|---|---|---|---|
| Host | debounce/state/packet parser | deterministic logic | pin voltage or wiring |
| Simulation | modeled sensor/LED/UART | modeled interactions | regulator, clone, EMI, thermal behavior |
| Build | exact FQBN/environment | source and dependency compile | upload or behavior |
| Target | serial, meter, scope, photo | observed hardware behavior | field reliability unless loaded |
| System | integrated load/failure case | requirement under scenario | future deployment safety |

## Anti-rationalization

| Shortcut | Response |
|---|---|
| "The unit test passed." | Keep all physical and system stages open. |
| "Wokwi matches the board." | List what the model omits and verify those items on hardware. |
| "The sketch compiled." | Require upload identity and target observations separately. |
| "The photo proves it works." | Require board identity, measurement context, and observed result. |
| "Mark it done and test later." | Keep the loop item blocked or `needs-review` until evidence exists. |

## Verification

- Every requirement maps to a test, proof stage, and artifact path.
- Host/simulation/build/target/system results are labeled separately.
- Physical-only steps emit the concrete `Physical gate` format from
  `embedded-project-loop`.
- Failed and unverified cases remain visible in the report.

## Shared output contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
