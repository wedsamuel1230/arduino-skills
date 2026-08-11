# Board Expansion Research

Checked: 2026-08-11

## Decision

Keep four additions for this bounded loop:

- Arduino Mega 2560 Rev3: expands 5 V AVR coverage to the high-pin-count
  ATmega2560 family.
- Arduino Nano Every: covers the ATmega4809/megaAVR Nano form factor without
  confusing it with the classic ATmega328P Nano.
- Arduino Nano ESP32: covers an official Arduino ESP32-S3 board with a
  board-specific NORA-W106 header map.
- ESP32-C3-DevKitC-02: covers a mainstream RISC-V ESP32 DevKit with explicit
  USB, strapping, ADC2, and LEDC constraints.

The existing five profiles remain protected. The additions reach the loop
target of nine source-backed profiles without making a board-family claim for
unlisted clones or carrier boards.

## Primary source checks

All URLs below returned successfully during the direct source pass unless the
profile explicitly calls out a mutable product page. Product pages are
date-checked because their URLs do not expose immutable revisions.

### Mega 2560 Rev3

- [Arduino product page](https://docs.arduino.cc/hardware/mega-2560): 54
  digital pins, 16 analog inputs, 15 PWM outputs, four UARTs, ATmega2560, and
  16 MHz board facts.
- [Microchip ATmega2560 datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega640-1280-1281-2560-2561-Datasheet-DS40002211A.pdf): 256 KB
  flash, 8 KB SRAM, 4 KB EEPROM, operating and absolute I/O ratings.
- [Pinned Arduino AVR Mega variant](https://github.com/arduino/ArduinoCore-avr/blob/11b9130371e8447920edb65a75706a6c951e51fc/variants/mega/pins_arduino.h): logical aliases, PWM set, UART, SPI, and I2C defaults.

### Nano Every

- [Arduino product page](https://docs.arduino.cc/hardware/nano-every):
  ATmega4809, 48 KB CPU flash, and 20 MHz board facts.
- [Microchip ATmega4808/4809 datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega4808-09-DataSheet-DS40002173C.pdf): 6 KB SRAM,
  256-byte EEPROM, VDD range, 10-bit ADC, and +/-40 mA absolute I/O rating.
- [Pinned Arduino megaAVR `nona4809` variant](https://github.com/arduino/ArduinoCore-megaavr/blob/bbdfd4b8c5f0c6bdaec4dc162460c32d993e7d4e/variants/nona4809/pins_arduino.h): 22 logical pins, PWM, I2C, SPI, and serial aliases.

### Nano ESP32

- [Arduino product page](https://docs.arduino.cc/hardware/nano-esp32): NORA-W106,
  ESP32-S3, 16 MB flash, Wi-Fi, Bluetooth, and USB-C.
- [Official ABX00083 pinout](https://docs.arduino.cc/resources/pinouts/ABX00083-full-pinout.pdf): physical board header and alternate-function map.
- [Pinned Arduino-ESP32 Nano NORA variant](https://github.com/espressif/arduino-esp32/blob/d8a1bf60d01aac021fc5f3cff30126f11d1e10a6/variants/arduino_nano_nora/pins_arduino.h): D/A aliases and default UART/I2C/SPI maps.
- [ESP32-S3 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf): 512 KB internal SRAM, ADC/GPIO behavior, strapping, USB, and GPIO electrical characteristics.

### ESP32-C3-DevKitC-02

- [Official DevKit guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c3/esp32-c3-devkitc-02/user_guide.html): WROOM-02/02U, 4 MB flash,
  5 V to 3.3 V LDO, exposed headers, USB, RGB LED GPIO8, and strapping pins.
- [ESP32-C3 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf): 400 KB SRAM, 12-bit ADC, GPIO current
  test conditions, USB/boot behavior, and default drive strengths.
- [ESP32-C3 GPIO API](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/gpio.html): GPIO matrix, pull behavior,
  strapping, USB-JTAG, and drive-capability API.
- [Pinned Arduino-ESP32 C3 variant](https://github.com/espressif/arduino-esp32/blob/d8a1bf60d01aac021fc5f3cff30126f11d1e10a6/variants/esp32c3/pins_arduino.h): Arduino analog and default bus aliases.
- [Arduino-ESP32 LEDC reference](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html): six LEDC channels on ESP32-C3 and signal attachment behavior.

## Deferred candidates

- Arduino GIGA R1 WiFi: official board sources exist, but the board has a
  broader STM32H747 peripheral, display, Ethernet, Wi-Fi, and power surface.
  It is deferred rather than represented by a shallow profile.
- ESP32-C6-DevKitC-1: official sources exist, but a distinct RISC-V, Wi-Fi 6,
  802.15.4, USB, and current Arduino-core map needs its own bounded review.

## Evidence boundary

This research proves source accessibility and documentation consistency only.
No physical board was wired, compiled, uploaded, powered under load, measured,
or deployed during this loop. The board profiles keep MCU electrical ratings
separate from board-level current budgets and mark revision, module, clone,
partition, and aggregate-load gaps explicitly.
