# OTA-Safe Sketch Contract

Use this reference when the question is whether the uploaded sketch itself can
continue to accept OTA updates.

## Minimum Contract

The updated sketch must continue to:

- initialize the intended network path
- initialize OTA support
- keep servicing OTA in the main runtime path
- avoid blocking the event path for long periods

If the old sketch supported OTA but the new sketch does not, OTA may work once
and then disappear after reboot. Treat that as expected behavior, not as a
mystery transport bug.

## Guardrails

- keep credentials and network mode explicit
- verify the board actually joins the network before assuming OTA is available
- avoid long blocking sections early in boot that starve network startup
- avoid assuming example code for one board family is correct for another

## Evidence To Collect

- does the device still get an IP address after the new sketch boots?
- does the device respond over the expected network path?
- is OTA service initialized in the new sketch?
- is OTA handling still exercised regularly enough to remain usable?

## High-Risk Cases

- updating a deployed device without recent USB recovery access
- changing Wi-Fi credentials, network mode, or boot flow in the same rollout
- switching board core versions at the same time as sketch behavior changes
- trying Uno R4 WiFi OTA without checking board-family-specific caveats
