---
name: ota-deployment-guardian
description: Use when users need safe over-the-air update workflows for ESP32-class boards or Arduino Uno R4 WiFi, including OTA sketch requirements, network port discovery failures, remote recovery planning, and rollout safety checks.
metadata: {triggers: "OTA, over-the-air update, rollback, remote recovery, deployment"}
---

# OTA Deployment Guardian

Use this skill when a device is updated remotely and losing the update path
would be expensive.

## Resources

- `references/ota-safe-sketch.md` - minimum sketch-side OTA contract and guardrails
- `references/discovery-and-network-ports.md` - IDE, mDNS, IP reachability, and disappearing network port triage
- `references/recovery-and-rollback.md` - rollout safety, rollback, and last-resort recovery planning
- `../../docs/board-support/uno-r4-family.md` - Uno R4 Minima and Uno R4 WiFi board-family caveats

## When to Use

Use this skill when the request involves:

- OTA uploads for ESP32, Nano ESP32, or Uno R4 WiFi
- network port appears briefly or disappears
- IDE can ping the device but cannot upload
- keeping a remote weather station or deployed board updateable
- avoiding self-bricking after an OTA deployment

Do not use this skill for ordinary bench USB uploads unless the user is clearly
preparing for later OTA deployment.

## Workflow

1. Confirm the board family:
   - ESP32 or Nano ESP32 -> open `references/ota-safe-sketch.md`
   - Uno R4 WiFi -> also open `../../docs/board-support/uno-r4-family.md`
2. Separate discovery failures from sketch failures:
   - ping works but network port disappears -> open
     `references/discovery-and-network-ports.md`
   - OTA works once, then disappears after the new sketch runs -> verify the new
     sketch still implements the OTA path in `ota-safe-sketch.md`
3. Before suggesting a rollout, check `references/recovery-and-rollback.md` for
   recovery path, rollback strategy, and what must stay available over USB.
4. Treat core-version changes as a possible variable when OTA previously worked
   and later became unreliable.

## Security And Maintenance Boundary

Use the router's connected-device security reference for secrets, signed images,
dependency versions, staged rollout, rollback, vulnerability response, and
decommissioning. This skill's board-specific OTA procedures do not prove that
the device has secure boot, authenticated updates, or a recoverable field
deployment; verify those controls on the exact target.

## Core Rules

- Never assume OTA remains available after a new sketch unless the sketch keeps
  the OTA path alive.
- Distinguish reachability from OTA discovery. Ping success does not prove the
  IDE can discover or upload.
- Keep at least one recovery path in reserve for high-cost remote devices.
- For Uno R4 WiFi, keep board-family caveats explicit. Its WiFi side is not the
  same operational model as a plain ESP32 board.

## Verification

- Confirm the sketch still connects to the intended network and services the OTA
  path after boot.
- Confirm whether the failure is discovery-only, upload-only, or full device
  reachability loss.
- For remote deployments, confirm the rollback or physical recovery plan before
  recommending an update.
- If board or core versions changed recently, capture the exact versions before
  concluding the failure is in user code.

## Integration

- Pair with `arduino-cli-skill` when the user needs command-line upload or port
  inspection.
- Pair with `field-power-and-connectivity-triager` when the OTA path fails only
  off USB or in field power conditions.
- Pair with `error-message-explainer` when the OTA sketch itself does not build.

## Shared Output Contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
