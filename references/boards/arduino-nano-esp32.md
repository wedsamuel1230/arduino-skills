# Arduino Nano ESP32

This profile targets Arduino Nano ESP32 model ABX00083 with the NORA-W106
module and its ESP32-S3 inside. Confirm the board revision and Arduino-ESP32
core before using the map; a generic ESP32-S3 DevKit is not pin-compatible.

## Profile

- Logic: 3.3 V GPIO class. USB-C is a 5 V board input path; do not connect a
  5 V sensor signal to a mapped GPIO without level shifting or a verified
  interface.
- MCU and memory: NORA-W106 with ESP32-S3, Wi-Fi and Bluetooth, 16 MB board
  flash, and 512 KB internal ESP32-S3 SRAM. Filesystem, OTA, and application
  space depend on the selected partition and core version.
- Digital and analog map: D0-D13 and A0-A7 are exposed by the Nano form factor.
  The pinned variant maps D0/D1 to GPIO44/GPIO43, D2-D10 to GPIO5/6/7/8/9/10/
  17/18/21, D11-D13 to GPIO38/47/48, and A0-A7 to GPIO1/2/3/4/11/12/13/14.
- PWM: ESP32-S3 LEDC provides 8 channels and can route PWM to output-capable
  exposed GPIOs. The mapped GPIO, LED, UART, SPI, USB, flash, and PSRAM uses
  must be checked before selecting a PWM output; this is not a fixed AVR-style
  pin list.
- ADC: Arduino-ESP32 exposes 12-bit ADC behavior on the mapped analog GPIOs;
  calibration, attenuation, Wi-Fi interaction, and input range remain core
  and silicon dependent.
- Default buses from the pinned Nano variant: UART RX/TX D0/D1 = GPIO44/GPIO43;
  I2C SDA/SCL A4/A5 = GPIO11/GPIO12; SPI SS/MOSI/MISO/SCK D10/D11/D12/D13 =
  GPIO21/GPIO38/GPIO47/GPIO48. D13/GPIO48 is also the built-in LED path.
- Per-pin current: the ESP32-S3 datasheet gives 40 mA high-level source and
  28 mA low-level sink under its stated 3.3 V and maximum-drive test
  conditions. Default drive strengths vary by GPIO. These are SoC electrical
  characteristics, not a safe Nano board, regulator, USB, radio, or external
  load budget.

## Pins to reserve or verify

- GPIO43/GPIO44 are the default UART0 pins in the Nano map; keep them reserved
  if the serial console or upload path uses them.
- GPIO19/GPIO20 are USB pins on ESP32-S3 variants, while GPIO26-GPIO37 can be
  consumed by flash or PSRAM depending on the NORA/module population. Do not
  infer that an unlisted GPIO is free.
- GPIO0, GPIO3, GPIO45, and GPIO46 are ESP32-S3 strapping pins. The Nano
  profile's mapped pins still need boot-state review when a peripheral drives
  them through reset or power-up.
- A successful Arduino-ESP32 compile does not prove the board's USB mode,
  NORA firmware, radio, power rail, or external wiring is correct.

## Sources

1. [Arduino Nano ESP32 product page](https://docs.arduino.cc/hardware/nano-esp32)
2. [Arduino Nano ESP32 ABX00083 pinout](https://docs.arduino.cc/resources/pinouts/ABX00083-full-pinout.pdf)
3. [Arduino-ESP32 Nano NORA variant at commit d8a1bf6](https://github.com/espressif/arduino-esp32/blob/d8a1bf60d01aac021fc5f3cff30126f11d1e10a6/variants/arduino_nano_nora/pins_arduino.h)
4. [ESP32-S3 series datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)

## Fact-to-source map

| Fact group | Primary source(s) | Status |
|---|---|---|
| Nano ESP32 identity, NORA-W106, 16 MB flash, Wi-Fi, Bluetooth, and USB-C | 1 and 2 | verified against official Arduino sources |
| Header labels and board-level exposed pins | 2 and 3 | verified against the official pinout and pinned Arduino variant |
| Logical bus map, LED alias, and analog aliases | 3 | pinned to the Arduino-ESP32 commit above |
| ESP32-S3 ADC, strapping, USB, GPIO current, and flash/PSRAM reservations | 4 | verified at MCU level; exact NORA population and board behavior remain variant dependent |
| Aggregate Nano rail current, radio peak, and exact partition/application capacity | 1, 2, and exact board revision | gap until the board revision, schematic, and selected core partition are confirmed |

Source status: the product page, ABX00083 pinout, pinned variant, and ESP32-S3
datasheet were checked on 2026-08-11. This is a board-specific profile, not a
claim that every ESP32-S3 DevKit shares the same header map.
