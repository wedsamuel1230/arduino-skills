# Arduino Mega 2560 Rev3

This profile targets the official Mega 2560 Rev3 with the ATmega2560 and the
Arduino AVR core. Clones, different bootloaders, regulator revisions, and
shield populations require their own checks.

## Profile

- Logic and operating voltage: 5 V class. Arduino documents 7-12 V as the
  recommended external input range; use the exact board power path before
  applying VIN or barrel-jack limits.
- Pins: 54 logical digital pins, 16 analog inputs, and 15 PWM outputs. The
  pinned AVR variant exposes analog aliases A0-A15 as logical pins 54-69.
- PWM: D2-D13 and D44-D46 in the pinned Arduino AVR variant.
- ADC: 10-bit AVR ADC on A0-A15; ADC resolution is not input accuracy or a
  safe voltage claim outside the board and MCU supply range.
- Memory and CPU: ATmega2560, 256 KB flash, 8 KB SRAM, 4 KB EEPROM, and a
  16 MHz clock on the board.
- Default buses: UART0 RX/TX D0/D1; UART1 RX/TX D19/D18; UART2 RX/TX D17/D16;
  UART3 RX/TX D15/D14; I2C SDA/SCL D20/D21; SPI SS/MOSI/MISO/SCK D53/D51/D50/D52.
- Per-pin current: the ATmega2560 datasheet gives 40 mA as the absolute
  maximum DC current per I/O pin and 200 mA through VCC/GND pins. Arduino's
  product specification gives a lower 20 mA operating figure. Treat neither
  number as a safe LED, motor, shield, or total-board load budget.

## Pins to reserve or verify

- D0-D3 and D14-D19 are used by the four hardware UARTs when those ports are
  enabled; reserve the selected port pins in the project map.
- D20/D21 are the hardware I2C pins and D50-D53 are the hardware SPI pins.
- D2-D13 and D44-D46 share timer resources with PWM; timer libraries can
  change the waveform or disable PWM on related pins.
- Analog aliases are separate from the digital header numbering. Do not
  substitute a Nano or Uno alias map.
- The 40 mA and 200 mA values are MCU electrical/absolute limits, not a power
  budget for the board regulator, USB bridge, shields, or external loads.

## Sources

1. [Arduino Mega 2560 product page](https://docs.arduino.cc/hardware/mega-2560)
2. [ATmega640/1280/1281/2560/2561 datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega640-1280-1281-2560-2561-Datasheet-DS40002211A.pdf)
3. [Arduino AVR Mega variant at commit 11b9130](https://github.com/arduino/ArduinoCore-avr/blob/11b9130371e8447920edb65a75706a6c951e51fc/variants/mega/pins_arduino.h)

## Fact-to-source map

| Fact group | Primary source(s) | Status |
|---|---|---|
| Board identity, 54 digital, 16 analog, 15 PWM, 4 UART, 16 MHz | 1 | verified on the official Arduino product page |
| Flash, SRAM, EEPROM, operating limits, and MCU current ratings | 2 | verified against the Microchip datasheet; current values are not board load limits |
| Arduino logical aliases, PWM set, and default SPI/I2C map | 3 | pinned to the ArduinoCore-avr commit above |
| Exact regulator, USB bridge, shield load, and aggregate board current | 1 and the exact board schematic | gap until the physical revision and schematic are confirmed |

Source status: the named board and core maps were checked on 2026-08-11.
Product-page input and operating figures are board documentation; MCU absolute
ratings must not be substituted for a measured or designed board power budget.
