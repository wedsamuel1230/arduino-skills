# Discovery And Network Port Triage

Use this reference when the board is reachable on the network but the IDE or
tooling cannot keep the OTA target visible.

## Common Failure Shapes

### Ping works, network port disappears

Likely causes:

- mDNS or network-port discovery instability
- IDE-side discovery issue
- board core or tool-version regression

Next checks:

- confirm the device remains reachable by IP
- confirm whether the failure is only discovery, not application reachability
- test a direct-IP or non-discovery-dependent workflow if available

### OTA works once, then vanishes after reboot

Likely cause:

- the uploaded sketch did not preserve OTA support or network initialization

Next checks:

- re-read `ota-safe-sketch.md`
- compare the working OTA sketch against the newly uploaded one

### Port appears only briefly after boot

Likely causes:

- startup timing issue
- board-family-specific OTA caveat
- toolchain or board package change

Next checks:

- capture exact board and tool versions
- on Uno R4 WiFi, open `../../docs/board-support/uno-r4-family.md`

## Notes For ESP32-Class Boards

- mDNS instability can look like a device failure even when the application is
  still running and reachable
- if a previous machine still discovers the device while a recently updated one
  does not, treat tool or core drift as a first-class suspect

## Notes For Uno R4 WiFi

- built-in IDE "network" port OTA is not an officially supported path in the
  same way it is on some ESP32 workflows
- third-party OTA flows can work, but they have extra constraints and timing
  sensitivity
