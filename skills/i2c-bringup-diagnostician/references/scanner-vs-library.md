# Scanner Sees Device But Library Fails

Use this reference when the address appears on the bus but the library says the
device cannot be found or returns nonsense data.

## What Scanner Success Proves

- the device answered at an address
- the bus is at least partially alive

## What Scanner Success Does Not Prove

- correct device identity
- correct power mode
- correct register access sequence
- correct library assumptions
- healthy sensor readings

## Next Checks

- verify the expected address from datasheet or board docs
- verify the library matches the exact device variant
- try a minimal identification or register read
- check if the sensor requires startup delay, mode configuration, or a different
  voltage environment

## Common Causes

- compatible-looking breakout with wrong or damaged sensor
- library written for a variant with different registers
- wrong initialization sequence
- bus present but sensor returning invalid data
