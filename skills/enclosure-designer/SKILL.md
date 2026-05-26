---
name: enclosure-designer
description: Use when users need a 3D-printable enclosure for an Arduino, ESP32, or RP2040 project and need help with measurements, cutouts, print settings, or environmental protection.
---

# Enclosure Designer

Use this skill to design practical enclosures without loading a full mechanical
guide up front.

## Resources

- `assets/basic-template.scad` - starting OpenSCAD template
- `scripts/generate_enclosure.py` - enclosure generator script
- `references/design-workflow.md` - measurement, parameter, and generator
  workflow
- `references/dimensions.md` - common board and module dimensions
- `references/print-and-protection.md` - wall thickness, print settings,
  ventilation, and waterproofing

## When to Use

Use this skill when the user asks for:

- an enclosure, case, box, or housing
- mounting holes or cutout placement
- OpenSCAD-based enclosure generation
- board fit checks for Arduino, ESP32, or Pico-class boards
- print-material or weather-resistance guidance

## Workflow

1. Gather the minimum physical inputs:
   - board dimensions
   - tallest component
   - connector locations
   - mounting method
   - environmental constraints
2. Open `references/design-workflow.md` for the parameterization flow.
3. Open `references/dimensions.md` if the user does not already have exact
   measurements.
4. Open `references/print-and-protection.md` for material, wall, ventilation,
   or moisture guidance.
5. Use `assets/basic-template.scad` or `scripts/generate_enclosure.py` when the
   user needs a concrete starting model.

## Core Rules

- Treat user measurements as authoritative over reference dimensions.
- Add clearance deliberately for connectors, wiring, and print tolerance.
- Separate fit problems from printability problems.
- Do not promise waterproofing from geometry alone.

## Verification

- The board and connectors fit with explicit clearance.
- Mounting points and cable exits are reachable.
- The selected material and wall thickness match the use environment.
- Print orientation and support strategy are named before finalizing the design.

## Integration

- Pair with `battery-selector` or `power-budget-calculator` if battery size
  drives the enclosure volume.
- Pair with `readme-generator` when the enclosure should be documented for a
  project repo.
