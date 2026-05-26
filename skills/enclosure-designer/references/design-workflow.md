# Enclosure Design Workflow

Use this reference when you need the step-by-step enclosure process.

## Step 1: Gather Measurements

Minimum dimensions to capture:

- board length, width, and height
- tallest component
- USB, barrel jack, antenna, or terminal block positions
- mounting-hole locations and screw size
- cable bend room

If the project already exists physically, measure the assembled unit instead of
the bare board.

## Step 2: Choose Design Parameters

Decide:

- internal clearance
- wall thickness
- lid style
- mounting strategy
- cutout style
- ventilation needs

Prefer a parameterized design so these choices can be changed without redrawing
the enclosure.

## Step 3: Generate a Starting Model

Choose one path:

- `assets/basic-template.scad` for manual OpenSCAD editing
- `scripts/generate_enclosure.py` for script-assisted generation
- an online box generator when the geometry is simple and speed matters

## Step 4: Review Fit Risk

Check:

- connector clearance
- screw boss interference
- lid overlap
- wiring paths
- print orientation effects on openings
