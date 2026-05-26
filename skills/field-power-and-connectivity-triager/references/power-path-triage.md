# Power Path Triage

Use this reference to classify the real supply path before deeper debugging.

## Identify The Path

- USB port
- VIN pin
- regulated 3V3 input
- battery plus onboard regulation
- external regulator feeding peripherals and board together

Each path has different risk points.

## Common Failure Shapes

### USB Works, VIN Fails

Possible causes:

- weak external source
- wrong VIN voltage
- poor wiring path
- regulator headroom or heat issues

### USB Works, 3V3 Injection Fails

Possible causes:

- bypassing the board's intended regulation path
- unstable external 3V3 rail
- insufficient transient response

### Sensors Drift Only Off USB

Possible causes:

- noisier supply
- grounding differences
- regulator interaction with analog front ends

## First Measurements

- supply voltage at source
- voltage at board input during load
- voltage at 3V3 rail during radio or sensor activity
- whether the board resets or just fails to connect
