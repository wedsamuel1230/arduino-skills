# Board Source Ledger

Checked: 2026-08-11

This ledger records the primary-source basis for the board profiles. GitHub
variant and core references use immutable commits. Product pages and PDFs that
do not expose a revision are date-checked and explicitly marked as mutable.
The ledger is evidence for the documentation gate, not proof that a user's
clone, carrier, or populated module matches the reference board.

| Profile | Primary source set | Revision or access record | Remaining gap |
|---|---|---|---|
| Uno R3 | Arduino product page; Microchip ATmega328P online documentation and datasheet | Arduino product page and Microchip online documentation revision 12 were reachable when checked; legacy Microchip PDF is document 7810D and may return HTTP 403 to automated clients | Clone regulator, USB bridge, and aggregate load require the exact schematic |
| Uno R4 Minima/WiFi | Arduino product pages and ABX00080/ABX00083 pinout PDFs | Official Arduino URLs were reachable when checked; public product pages do not expose immutable revisions | RA4M1 electrical limits beyond the board-listed 8 mA and connectivity-firmware details require exact revisions |
| Mega 2560 Rev3 | Arduino Mega product page; Microchip ATmega2560 datasheet; ArduinoCore-avr Mega variant | Product page and Microchip PDF were reachable on 2026-08-11; variant pinned to `11b9130371e8447920edb65a75706a6c951e51fc` | Regulator, USB bridge, shield population, clone behavior, and aggregate board load require the exact schematic |
| Nano Every | Arduino Nano Every product page; Microchip ATmega4809 datasheet; ArduinoCore-megaavr `nona4809` variant | Product page and Microchip PDF were reachable on 2026-08-11; variant pinned to `bbdfd4b8c5f0c6bdaec4dc162460c32d993e7d4e` | The classic Nano map is not interchangeable; regulator, input protection, and aggregate load remain board-specific |
| Nano ESP32 | Arduino Nano ESP32 product page and ABX00083 pinout; Arduino-ESP32 Nano NORA variant; ESP32-S3 datasheet | Official Arduino PDFs were reachable on 2026-08-11; variant pinned to `d8a1bf60d01aac021fc5f3cff30126f11d1e10a6` | NORA population, USB mode, partition layout, radio peak, and aggregate rail load remain revision/core dependent |
| Classic ESP32 DevKit/WROOM | Espressif GPIO API, ESP32 and WROOM datasheets, DevKitC guide, Arduino-ESP32 variant | Arduino-ESP32 variant pinned to commit `d8a1bf60d01aac021fc5f3cff30126f11d1e10a6`; Espressif datasheet URL was reachable when checked | DevKit revision, regulator, flash/PSRAM population, and total load remain SKU-specific |
| ESP32-C3 DevKitC-02 | Espressif DevKit guide, ESP32-C3 datasheet/GPIO API, Arduino-ESP32 C3 variant, LEDC reference | Espressif pages/PDF and pinned variant were reachable on 2026-08-11; variant pinned to `d8a1bf60d01aac021fc5f3cff30126f11d1e10a6` | DevKit revision, module suffix, regulator load, USB/JTAG use, and aggregate current remain board-specific |
| ESP32-S3 DevKit | Espressif S3 GPIO API, S3 and WROOM-1 datasheets, DevKit guide, Arduino-ESP32 variant | Arduino-ESP32 variant pinned to commit `d8a1bf60d01aac021fc5f3cff30126f11d1e10a6`; Espressif datasheet URL was reachable when checked | DevKit revision, USB mode, flash/PSRAM, ADC calibration, and total load remain SKU-specific |
| Pico/Pico W | Raspberry Pi Pico and RP2040 datasheets, Pico documentation, Arduino-Pico README and variant | Raspberry Pi datasheet URLs were reachable when checked; Arduino-Pico sources pinned to commit `9a0bc35654e9af3eccfb88c54f9cc73f9e153ac6` | Exact flash population, carrier exposure, radio-burst rail, and aggregate board load remain product-specific |

## Verification rules

- Board identity, pin map, memory, voltage, and bus facts require at least two
  official sources where the vendor publishes them.
- A source URL returning an access error is not silently promoted to verified;
  use an accessible official mirror or mark the fact as a gap.
- SoC absolute maximums, configurable drive strengths, and product-level load
  budgets are separate facts. A per-pin figure never closes the board power
  gate.
- Refresh the ledger when the Arduino core, board package, module suffix, or
  source revision changes.
