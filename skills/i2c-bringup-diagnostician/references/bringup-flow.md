# I2C Bringup Flow

Use this reference when nothing on the bus is behaving yet.

## Step 1: Basic Electrical Plausibility

Check:

- device power
- common ground
- correct SDA and SCL pins
- pull-ups present where needed
- logic voltage compatibility

If these are unknown, do not move to library debugging yet.

## Step 2: Minimal Detection

Run a minimal scanner or equivalent probe.

Possible results:

- nothing found
- one address found
- multiple addresses found
- intermittent detection

## Step 3: Interpret The Result

### Nothing Found

Suspect:

- swapped pins
- missing power or ground
- wrong bus instance
- missing pull-ups
- incompatible level or dead module

### Address Found

Move to minimal device interaction before jumping into full application code.

### Intermittent Detection

Suspect:

- weak pull-ups
- long or noisy wires
- unstable power
- board-specific bus behavior
