# Arduino Nano Every

This profile targets the official Nano Every using the ATmega4809 and the
Arduino megaAVR core. It is not a generic replacement for the classic Nano,
which has a different MCU and peripheral map.

## Profile

- Logic and operating voltage: 5 V class on the board. The ATmega4809 itself
  supports a wider VDD range, but the Nano Every rail, USB path, and external
  input path must be checked from the exact board documentation.
- Pins: 22 logical digital pins. D0-D13 are the header digital pins and A0-A7
  are mapped as logical pins D14-D21 by the pinned variant.
- PWM: D3, D5, D6, D9, and D10.
- ADC: 10-bit ADC with A0-A7 exposed by the board. ADC resolution is not ADC
  accuracy, input protection, or a substitute for checking the sensor range.
- Memory and CPU: ATmega4809, 48 KB flash, 6 KB SRAM, 256 bytes EEPROM, and
  a 20 MHz maximum operating clock at the board's 5 V supply.
- Default buses: SPI SS/MOSI/MISO/SCK D8/D11/D12/D13; I2C SDA/SCL D22/D23;
  header UART RX/TX D0/D1. The variant also reserves D24/D25 for the board's
  debug USART path, so do not assume every logical pin is a free header pin.
- Per-pin current: the ATmega4809 datasheet gives +/-40 mA as the absolute
  maximum I/O pin sink/source current. Use the board and library's lower
  operating guidance for real loads; do not treat the absolute maximum or the
  200 mA VDD/GND rating as a safe board power budget.

## Pins to reserve or verify

- D0/D1 are the primary hardware serial pins and D22/D23 are the hardware I2C
  pins; reserve them when those buses are required.
- D8-D13 are the hardware SPI pins. PWM is limited to the five variant pins,
  unlike the more flexible ESP32 LEDC peripheral.
- A0-A7 are logical aliases with an offset from the digital header. Use the
  core variant map rather than a classic Nano pin table.
- UPDI, debug USART, reset, oscillator, and internal-use pins are not free
  external GPIO merely because the MCU package has more physical pins.

## Sources

1. [Arduino Nano Every product page](https://docs.arduino.cc/hardware/nano-every)
2. [ATmega4808/4809 datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega4808-09-DataSheet-DS40002173C.pdf)
3. [Arduino megaAVR Nano Every variant at commit bbdfd4b](https://github.com/arduino/ArduinoCore-megaavr/blob/bbdfd4b8c5f0c6bdaec4dc162460c32d993e7d4e/variants/nona4809/pins_arduino.h)

## Fact-to-source map

| Fact group | Primary source(s) | Status |
|---|---|---|
| Board identity, ATmega4809, 48 KB flash, 20 MHz, and Nano form factor | 1 | verified on the official Arduino product page |
| VDD range, 10-bit ADC behavior, SRAM/EEPROM, and absolute I/O current | 2 | verified against the Microchip datasheet; absolute values are not board load limits |
| Logical D/A aliases, PWM, SPI, I2C, and serial maps | 3 | pinned to the ArduinoCore-megaavr commit above |
| Exact Nano Every regulator, input protection, and aggregate load | 1 and the exact board schematic | gap until the physical revision and power path are confirmed |

Source status: the official product page, Microchip datasheet, and pinned
megaAVR variant were checked on 2026-08-11. The classic Nano pin table must not
be reused for this board.
