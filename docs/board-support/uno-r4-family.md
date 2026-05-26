# Uno R4 Family Support Notes

Use this shared reference when a skill needs Uno R4-specific support guidance.

## Board Split

The Uno R4 family is not one operational target:

- **Uno R4 Minima** - Renesas RA4M1 board without the WiFi connectivity side
- **Uno R4 WiFi** - Renesas RA4M1 main MCU plus an ESP32-S3 connectivity side

Advice that is correct for Minima is not automatically correct for WiFi.

## Why It Matters

Uno R4 WiFi issues often cross boundaries:

- sketch behavior on the Renesas side
- connectivity behavior on the ESP32-S3 side
- USB or firmware bridge state
- OTA workflow limitations in IDE tooling

## OTA Caveats

- Arduino IDE built-in "network" port OTA is not an officially supported path
  for Uno R4 WiFi in the same way it is for some ESP32 flows.
- Third-party `ArduinoOTA`-style workflows can work, but discovery can be
  intermittent and timing-sensitive.
- If the user mentions brief network-port visibility, disappearing OTA targets,
  or patched local tool files, keep Uno R4 WiFi-specific behavior in play.

## USB And Serial Quirks

- serial-monitor and reconnect behavior can differ from classic Uno expectations
- board recognition problems may involve the connectivity-side firmware state,
  not only the sketch

## Recommended Host Skills

Reference this file from:

- `ota-deployment-guardian`
- `arduino-cli-skill`
- `error-message-explainer`
- future upload or firmware-recovery skills

## Evidence To Capture

When troubleshooting Uno R4 family boards, capture:

- Minima vs WiFi
- board package version
- IDE or CLI version
- whether the failure is USB, serial monitor, OTA, or connectivity firmware
  related
