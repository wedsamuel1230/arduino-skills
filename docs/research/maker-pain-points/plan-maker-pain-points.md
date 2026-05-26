# Maker Pain-Point Skills Plan

**Goal:** Prioritize and prepare a maker-first wave of agent skills and shared
Uno R4 board support references.

## Task Group 1: Lock the first-wave scope

### Task 1.1

- Target files: `brainstorm-maker-pain-points.md`
- Action: confirm the first-wave priorities:
  - OTA
  - calibration
  - field power/connectivity
- Verification:
  - each has clear evidence and low overlap

### Task 1.2

- Target files: `prd-maker-pain-points.md`
- Action: encode the maker-first wave and Uno R4 support strategy
- Verification:
  - phases and slice seeds exist

## Task Group 2: Prepare first-wave skill specs

### Task 2.1

- Target output:
  - spec section per first-wave skill
- Action:
  - define `name`
  - define `description`
  - define workflow and support assets

### Task 2.2

- Target output:
  - overlap notes with current repo skills
- Action:
  - state why each skill is new instead of a subsection of an existing one

## Task Group 3: Prepare Uno R4 shared support pack

### Task 3.1

- Target output:
  - list of host skills that need Uno R4 references
- Action:
  - identify where Uno R4 support belongs today

### Task 3.2

- Target output:
  - shared reference topics
- Action:
  - define Minima vs WiFi split
  - define OTA, USB, serial-monitor, and firmware-bridge topics

## Future Implementation Order

1. Build `ota-deployment-guardian`
2. Build `sensor-calibration-workbench`
3. Build `field-power-and-connectivity-triager`
4. Add Uno R4 shared support references
5. Build `i2c-bringup-diagnostician`
