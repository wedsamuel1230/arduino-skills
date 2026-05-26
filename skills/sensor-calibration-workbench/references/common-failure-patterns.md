# Common Calibration Failure Patterns

Use this reference when the user knows the sensor is present but the numbers are
wrong.

## Warm-Up And Stabilization

Symptoms:

- readings improve after a few minutes
- early readings are much noisier than later readings

Common with:

- load cells and HX711 setups
- gas sensors
- analog front ends

## Wrong Reference Assumptions

Symptoms:

- coefficients seem to "work" only for one point
- readings are obviously clipped or nonsensical at another point

Typical cause:

- calibrating against an uncertain baseline
- assuming the environment is already stable

## Saturation Or Scaling Errors

Symptoms:

- values pin at zero or max
- calibrated values exceed expected bounds dramatically

Typical cause:

- wrong mapping range
- wrong gain setting
- unit mismatch

## Environment-Coupled Drift

Symptoms:

- values change with temperature, supply path, mounting, or nearby materials

Typical cause:

- the sensor is reacting to the real environment and the model ignores it

## Hardware Fault Masquerading As Calibration

Symptoms:

- calibration values change wildly between runs
- impossible readings remain impossible after coefficient tuning

Typical cause:

- poor wiring
- noisy supply
- wrong sensor mode
- damaged module
