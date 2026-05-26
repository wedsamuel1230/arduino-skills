# Maker Pain Points Brainstorm

## Chosen Discovery Path

Used the `brainstorming` path.

Reason:

- the request is about opportunity discovery and prioritization
- the missing input is external maker pain, not internal repo terminology
- the repo already has enough context to judge overlap and implementation fit

## Scope Shift From The Earlier Embedded Pass

The earlier pass emphasized coding and toolchain pain:

- I2C bring-up
- library compatibility
- uploads and installs
- heap and runtime behavior

This pass shifts toward maker problems after the first prototype works:

- OTA and remote update safety
- calibration and trustworthy measurements
- power and connectivity drift in field conditions
- board-family support for newer boards like Uno R4

## External Maker Pain Signals

### 1. OTA is attractive to makers, but fragile in practice

Representative signals:

- Arduino Forum, November 8, 2025:
  https://forum.arduino.cc/t/ota-on-esp32-intermittently-drops-connection/1413055
  - OTA target is reachable by ping
  - IDE still loses the network port
  - workaround depends on mDNS behavior and an alternate programmer path
  - user needed OTA because the board was mounted on a roof weather station
- Arduino Forum, November 6, 2025:
  https://forum.arduino.cc/t/nano-esp32-ota-uploads-and-runs-once-then-network-port-disappears/1412654
  - OTA works once
  - network port disappears after the uploaded sketch runs
  - root cause was that OTA support must remain present in every uploaded sketch
- espressif/arduino-esp32 issue search result, October 22, 2025:
  https://github.com/espressif/arduino-esp32/issues
  - issue title indicates OTA update regression around core 3.3.2

Meaning:

- OTA problems are often workflow problems, not only code bugs
- makers need an "OTA-safe deployment" skill more than another generic upload
  guide

### 2. Makers struggle when the device leaves USB bench power

Representative signal:

- Arduino Forum, February 7, 2025:
  https://forum.arduino.cc/t/the-esp32-cannot-connect-to-wifi-using-a-power-source-other-than-usb/1351259
  - ESP32 connects on USB
  - fails to connect when powered from the intended supply path
  - likely pain centers on current peaks, voltage path, regulator quality, or
    wiring

Meaning:

- "works on USB, fails in deployment" is a strong maker-specific problem class
- this is only partly covered by generic debugging skills

### 3. Calibration and stable sensor behavior remain weak spots

Representative signals:

- Arduino Forum, June 16, 2025:
  https://forum.arduino.cc/t/project-update-and-sensor-help/1389274
  - CO2 readings became implausible
  - self-calibration expectations were not understood clearly
- Arduino Forum, January 23, 2025:
  https://forum.arduino.cc/t/s-type-load-cell-with-arduino-and-hx711/1346043
  - load-cell values are volatile during calibration
  - stability changes over time after warm-up
- Arduino Forum, May 17, 2025:
  https://forum.arduino.cc/t/magnetometer-easy-calibration/1382318
  - calibration method is constrained by the mechanical reality of the project,
    not only the code

Meaning:

- makers need workflows for warm-up, drift, reference points, persistence of
  calibration values, and validity checks
- the repo has code-generation support, but not calibration process support

### 4. Uno R4 support is a distinct opportunity, especially Uno R4 WiFi

Representative signals:

- Arduino issue listing shows open serial-monitor reconnect pain for Uno R4
  Minima:
  https://github.com/arduino/arduino/issues
- Arduino Forum, April 10, 2025:
  https://forum.arduino.cc/t/uno-r4-wifi-ota-with-ide/1372388/2
  - built-in IDE "network" port OTA is not officially supported for Uno R4 WiFi
- Arduino Forum, March 9, 2026:
  https://forum.arduino.cc/t/arduinoota-with-the-uno-r4-wifi-intermittent-network-port/1434538
  - network port appears only briefly
  - user had to patch local tool files and timing values
- Arduino Forum, September 23, 2023:
  https://forum.arduino.cc/t/ota-upload-to-uno-r4-wifi-is-working-a-post-from-a-beginner/1171442
  - OTA can work, but the workflow expectations are non-obvious and tied to
    cloud-compatible sketches
- Arduino Forum, July 13, 2023:
  https://forum.arduino.cc/t/uno-r4-wifi-is-not-recognized-or-wrong-recognized/1147781
  - device recognition and ESP-side firmware state can derail setup early

Meaning:

- Uno R4 is not only "one more board target"
- Uno R4 WiFi especially has a split personality: Renesas main MCU plus ESP32-S3
  connectivity side
- that makes it a high-value board-family support target

## Recommended Skill and Tool Opportunities

### 1. `ota-deployment-guardian`

Mission:

- preserve remote updateability and prevent accidental loss of the OTA path

Why it matters:

- OTA is a deployment workflow
- the cost of failure is higher than a normal bench upload

Likely assets:

- OTA-safe sketch checklist
- required code-path examples
- discovery vs reachability decision tree
- mDNS or network-port workaround reference
- rollback and "keep a serial recovery path" guidance

### 2. `sensor-calibration-workbench`

Mission:

- guide makers through calibration, stabilization, drift checks, and persistent
  coefficient handling

Likely assets:

- reusable calibration worksheet templates
- per-sensor-class references
- EEPROM or flash persistence patterns
- sanity-limit and outlier checks

### 3. `field-power-and-connectivity-triager`

Mission:

- explain why wireless or sensor-heavy maker projects work on USB but fail on
  the intended power path

Likely assets:

- current-peak and brownout checklist
- USB vs VIN vs 3V3 power-path matrix
- Wi-Fi startup instrumentation steps
- field wiring sanity flow

### 4. `i2c-bringup-diagnostician`

Mission:

- isolate wiring, voltage, address, library, and version causes in I2C bring-up

Why it stays on the list:

- makers hit this constantly
- still lower priority than OTA and calibration for the maker-first wave

## Uno R4 Support Recommendation

Do not start with a standalone `uno-r4-skill` unless the repo later adds
multiple board-family packs.

Recommended approach:

1. add Uno R4 Minima and Uno R4 WiFi support references into existing and new
   skills
2. create shared Uno R4 board-family references that can be used by:
   - `arduino-cli-skill`
   - `error-message-explainer`
   - `upload-path-recovery`
   - `ota-deployment-guardian`
   - `arduino-code-generator`
3. only create a dedicated Uno R4 support skill if the board-family references
   become too large or too operationally unique

Shared Uno R4 support should include:

- board split: Minima vs WiFi
- Renesas vs ESP32-S3 responsibilities
- OTA support caveats
- USB or serial-monitor quirks
- firmware bridge recovery references

## Priority Recommendation

If the repo should focus on maker agent skills and tools first:

1. `ota-deployment-guardian`
2. `sensor-calibration-workbench`
3. `field-power-and-connectivity-triager`
4. `i2c-bringup-diagnostician`

Cross-cutting board support work:

- add Uno R4 family support references alongside the first wave

Defer for later:

- broad library compatibility analysis
- board-manager install recovery
- heap-runtime investigation
- deep core-version regression triage
