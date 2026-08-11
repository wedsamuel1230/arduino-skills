# ESP32-C3-DevKitC-02

This profile targets Espressif ESP32-C3-DevKitC-02 with an
ESP32-C3-WROOM-02 or WROOM-02U module and the Arduino-ESP32 or ESP-IDF
framework. Check the exact module suffix and DevKit revision before wiring.

## Profile

- Logic: 3.3 V GPIO. The DevKit has a 5 V to 3.3 V LDO and can be powered from
  Micro-USB or the 5 V header; the 3V3 header is a regulated rail, not a 5 V
  signal input.
- CPU and memory: ESP32-C3 single-core RISC-V up to 160 MHz, 400 KB SRAM,
  and 4 MB SPI flash in the WROOM-02/02U module.
- Exposed GPIO: the official DevKit header exposes GPIO0-GPIO10 and GPIO18-
  GPIO21; GPIO11-GPIO17 are not treated as general-purpose header pins in this
  profile because flash/module reservations and board exposure must not be
  guessed from the SoC package.
- PWM: Arduino-ESP32 LEDC provides 6 channels. The GPIO matrix can route PWM
  to output-capable exposed pins, but GPIO2/GPIO8/GPIO9 boot straps, GPIO18/
  GPIO19 USB-JTAG, and GPIO20/GPIO21 UART use need an explicit decision first.
- ADC: Arduino-ESP32 maps A0-A5 to GPIO0-GPIO5; the ESP32-C3 ADC is 12-bit.
  GPIO5 is ADC2 on the Arduino map, so check the selected core's Wi-Fi/ADC2
  interaction and attenuation before using it for a connected sensor.
- Default buses from the pinned Arduino variant: UART RX/TX GPIO20/GPIO21;
  I2C SDA/SCL GPIO8/GPIO9; SPI SS/MOSI/MISO/SCK GPIO7/GPIO6/GPIO5/GPIO4.
- Per-pin current: the ESP32-C3 datasheet gives 40 mA high-level source and
  28 mA low-level sink at the stated 3.3 V maximum-drive test condition. Its
  default drive strengths vary by pin. These are SoC electrical
  characteristics, not safe LED, motor, DevKit regulator, USB, or total-board
  load limits.

## Pins to reserve or verify

- GPIO2, GPIO8, and GPIO9 are strapping pins. A connected sensor, pull-up,
  LED, or level shifter can change boot configuration.
- GPIO18/GPIO19 are USB D-/D+ and GPIO20/GPIO21 are the default UART pins.
  Reusing them can disable USB-JTAG or interfere with serial upload/debug.
- GPIO8 is also the DevKit's addressable RGB LED. GPIO4-GPIO7 carry the
  default SPI signals, and GPIO5 is both a SPI signal and ADC2 in the Arduino
  map.
- Do not use the 40 mA/28 mA figures to drive a load directly. Use a resistor,
  transistor, MOSFET, driver, or level shifter as the external circuit needs.

## Sources

1. [ESP32-C3-DevKitC-02 user guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c3/esp32-c3-devkitc-02/user_guide.html)
2. [ESP32-C3 series datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)
3. [ESP32-C3 GPIO API](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/gpio.html)
4. [Arduino-ESP32 C3 variant at commit d8a1bf6](https://github.com/espressif/arduino-esp32/blob/d8a1bf60d01aac021fc5f3cff30126f11d1e10a6/variants/esp32c3/pins_arduino.h)
5. [Arduino-ESP32 LEDC channel reference](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html)

## Fact-to-source map

| Fact group | Primary source(s) | Status |
|---|---|---|
| DevKit module, 4 MB flash, LDO, header exposure, USB, and RGB LED | 1 | verified against the official Espressif DevKit guide |
| ESP32-C3 GPIO, ADC, strapping, USB-JTAG, and electrical current data | 2 and 3 | verified against official Espressif sources; current figures are test limits, not load targets |
| Arduino analog and default UART/I2C/SPI maps | 4 | pinned to the Arduino-ESP32 commit above |
| Six LEDC channels and signal attachment behavior | 5 | verified against the Arduino-ESP32 API documentation |
| Aggregate DevKit current, clone/carrier behavior, and radio peak budget | 1 and the exact schematic/module | gap until the board revision and finished load are confirmed |

Source status: the DevKit guide, ESP32-C3 datasheet/API, pinned Arduino
variant, and LEDC reference were checked on 2026-08-11. GPIO2/8/9 and USB
18/19 must remain explicit in every pin assignment.
