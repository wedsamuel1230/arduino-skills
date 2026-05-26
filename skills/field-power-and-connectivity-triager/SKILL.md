---
name: field-power-and-connectivity-triager
description: Use when maker projects work on USB bench power but fail on their intended supply path, especially for WiFi or sensor-heavy boards such as ESP32, including brownout, current-peak, regulator, and wiring-path diagnosis.
---

# Field Power And Connectivity Triager

Use this skill when the project works on the bench but breaks when powered the
way it will be used in the real world.

## Resources

- `references/power-path-triage.md` - USB vs VIN vs 3V3 diagnosis workflow
- `references/wifi-and-peak-current.md` - WiFi startup, brownout, and current-peak behavior
- `references/measurement-checklist.md` - what to measure before blaming the code
- `../../docs/board-support/uno-r4-family.md` - Uno R4 family board caveats where relevant

## When to Use

Use this skill when the request includes:

- "works on USB but not on my power supply"
- WiFi connects on the bench but not in deployment
- field-only resets, brownouts, or sensor instability
- suspected regulator or wiring-path weakness
- battery, VIN, or 3V3 supply-path questions

## Workflow

1. Reproduce the split:
   - USB works
   - intended power path fails
2. Open `references/power-path-triage.md` to classify the supply path.
3. If WiFi or radio startup is involved, open
   `references/wifi-and-peak-current.md`.
4. Capture actual measurements from `references/measurement-checklist.md`
   before assuming the failure is in user code.
5. If the target is Uno R4 WiFi, open `../../docs/board-support/uno-r4-family.md`
   and keep the connectivity-side hardware split explicit.

## Core Rules

- "Works on USB" is evidence about the power path, not proof the code is sound.
- WiFi startup current peaks are first-class suspects on ESP32-class boards.
- Diagnose the supply path before tuning network code blindly.
- Treat sensor instability under field power as a possible power-integrity issue
  until measurements say otherwise.

## Verification

- Confirm the failure reproduces only on the intended power path.
- Confirm voltage and current conditions during the failing phase, not only at
  idle.
- Confirm whether the failure happens at boot, during WiFi association, or later
  under load.
- Confirm whether the same sketch behaves consistently once the power path is
  corrected.

## Integration

- Pair with `power-budget-calculator` when the issue may be under-sized source
  capacity.
- Pair with `ota-deployment-guardian` when OTA fails only under field power.
- Pair with `circuit-debugger` when the board wiring itself is suspect.
