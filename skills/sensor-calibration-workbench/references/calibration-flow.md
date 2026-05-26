# Calibration Flow

Use this reference for the core calibration procedure.

## Step 1: Define The Measurement Contract

Before calibrating, write down:

- what quantity is being measured
- the expected range
- the acceptable error
- the operating environment

If the project cannot state those four items, the calibration target is not yet
clear enough.

## Step 2: Prepare Known References

Examples:

- load cell -> known masses
- CO2 sensor -> fresh air baseline or controlled environment
- color sensor -> defined white and black references
- magnetometer -> known orientation or established calibration routine

Do not tune coefficients against unknown or drifting references.

## Step 3: Stabilize First

Capture:

- warm-up time
- power source used during calibration
- whether readings are still drifting over time
- whether sampling noise is random or systematic

If the sensor is still drifting strongly, fix that before final coefficient
changes.

## Step 4: Apply The Right Calibration Class

- offset-only when the scale is correct but the zero point is wrong
- two-point when both offset and scale need correction
- multi-orientation or environmental calibration when geometry or physics
  changes the response surface

## Step 5: Validate After Applying Coefficients

Check:

- same reference again
- at least one different reference value
- threshold behavior in the actual project logic

If the second check fails, the calibration model is incomplete or the hardware
is still unstable.
