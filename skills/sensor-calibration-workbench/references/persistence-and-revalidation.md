# Persistence And Revalidation

Use this reference when the user needs calibration values to survive reset or
be rechecked over time.

## What To Persist

- calibration coefficients
- sensor mode assumptions
- reference conditions if they matter
- timestamp or firmware version if useful

## Where To Persist

- EEPROM for small, simple values
- flash-backed preferences or equivalent on platforms that support it

## Revalidation Triggers

Recheck calibration when:

- firmware changes the measurement pipeline
- power path changes
- sensor mounting changes
- environment changes significantly
- readings cross sanity limits unexpectedly

## Verification

- reboot and confirm coefficients reload
- compare one known reference before and after reboot
- log whether the stored values are being used or replaced
