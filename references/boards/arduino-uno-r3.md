# Arduino Uno R3

## Profile

- MCU: ATmega328P, 8-bit AVR, 16 MHz.
- Logic and operating voltage: 5 V.
- External input: 7-12 V recommended; 6-20 V input limit. The limit is not a
  promise of a cool regulator or adequate peripheral current.
- Digital I/O: D0-D13; PWM on D3, D5, D6, D9, D10, D11.
- ADC: A0-A5, 10-bit. A4/A5 are also the default I2C pins.
- Memory: 32 KB flash (0.5 KB bootloader), 2 KB SRAM, 1 KB EEPROM.
- Default buses: UART D0/D1; I2C/TWI A4/A5; SPI D10 SS, D11 MOSI, D12 MISO,
  D13 SCK. ICSP exposes the SPI signals.
- Current: Arduino lists 20 mA DC per I/O pin and 50 mA maximum for the 3.3 V
  pin. Do not sum per-pin values into a board load budget. The ATmega328P
  absolute maximum of 40 mA per pin is not a design target.

## Pitfalls

- 5 V outputs can damage 3.3 V-only sensors and radios.
- D0/D1 are shared with USB serial; D13 drives the onboard LED.
- `analogWrite()` is timer PWM, not an analog voltage.
- Avoid dynamic `String` use and keep literals in flash with `F()` when SRAM
  pressure is material.

## Sources

1. [Arduino Uno Rev3 technical specifications](https://docs.arduino.cc/hardware/uno-rev3)
2. [ATmega328P Microchip online documentation, revision 12](https://onlinedocs.microchip.com/oxy/GUID-0EC909F9-8FB7-46B2-BF4B-05290662B5C3-en-US-12/index.html)
3. [ATmega328P datasheet PDF, document 7810D](https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega328P-7810D-AVR-8-bit-Microcontroller-Datasheet.pdf)
4. [Arduino language reference](https://docs.arduino.cc/language-reference/en/functions/analog-io/analogWrite/)

## Fact-to-source map

| Fact group | Primary source(s) | Status |
|---|---|---|
| Board voltage, headers, PWM, memory | 1 | verified against the official product page |
| ADC, UART, I2C, SPI, absolute pin limits | 2 and 3 | verified against Microchip documentation; PDF fetch may be blocked by automated clients |
| `analogWrite()` behavior | 4 | verified against the Arduino reference |
| Clone regulator, USB bridge, and aggregate load | exact board schematic | gap; do not infer from the reference board |

Source status: board values are product-page facts; absolute pin limits come
from the MCU documentation. Exact clone regulator and connector behavior
remains board-specific. Product-page content was checked on 2026-08-10 and
does not expose an immutable revision in its public URL.
