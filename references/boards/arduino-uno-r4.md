# Arduino Uno R4 Minima and Uno R4 WiFi

## Shared Renesas-side profile

- MCU: Renesas RA4M1, Arm Cortex-M4, 48 MHz.
- Board logic/operating voltage: 5 V.
- Input voltage listed by Arduino: 6-24 V. Treat this as a board input range,
  not as a regulated supply for external loads.
- Header I/O: 14 digital pins; PWM is available on the board's D3, D5, D6,
  D9, D10, and D11 positions.
- ADC: six analog inputs with up to 14-bit resolution in Arduino's board
  documentation. ADC effective accuracy and reference behavior remain
  application and core-version dependent.
- Memory: 256 KB flash, 32 KB SRAM, and 8 KB data flash/EEPROM as listed by
  Arduino.
- Default buses: UART D0/D1; I2C A4/A5; SPI on the ICSP header. CAN requires
  an external transceiver.
- Current: Arduino lists 8 mA DC per I/O pin. No universal safe total GPIO,
  5 V, or 3.3 V board-load budget was found; use the board schematic and
  supply measurement for attached loads.

## WiFi split

Uno R4 WiFi adds an ESP32-S3-MINI-1 connectivity MCU/module. Treat its
connectivity firmware, power, pins, and update path as a second domain. Do not
use the ESP32-S3 module's internal pins as if they were the Renesas header
GPIOs. Uno R4 Minima has no equivalent WiFi-side MCU.

## Pitfalls

- Do not apply ATmega328P register, timer, or memory assumptions to RA4M1.
- CAN needs a physical transceiver and correct termination.
- WiFi failures can be in the Renesas sketch, connectivity firmware, USB/serial
  bridge, power rail, or network path independently.
- `analogWrite()` is PWM; the RA4M1 DAC is a separate peripheral.

## Sources

1. [Arduino Uno R4 Minima](https://docs.arduino.cc/hardware/uno-r4-minima)
2. [Arduino Uno R4 WiFi](https://docs.arduino.cc/hardware/uno-r4-wifi)
3. [Uno R4 Minima pinout](https://docs.arduino.cc/resources/pinouts/ABX00080-full-pinout.pdf)
4. [Uno R4 WiFi pinout](https://docs.arduino.cc/resources/pinouts/ABX00083-full-pinout.pdf)

## Fact-to-source map

| Fact group | Primary source(s) | Status |
|---|---|---|
| Minima identity, voltage, memory, buses | 1 and 3 | verified against official Arduino product and pinout documents |
| WiFi identity and Renesas/connectivity split | 2 and 4 | verified against official Arduino product and pinout documents |
| Header PWM and analog positions | 3 and 4 | verified at board-header level; core-version behavior remains a compatibility check |
| RA4M1 electrical limits and aggregate load | exact RA4M1 and board schematic | gap beyond Arduino's listed 8 mA per I/O figure |

Source status: board identity, memory, voltage, and interface facts are from
Arduino's product and pinout documents checked on 2026-08-10. Pin electrical
and aggregate-current details beyond the board-listed 8 mA per I/O pin must be
checked against the exact board revision and the selected RA4M1
electrical-characteristics source; the public product pages do not expose an
immutable revision in their URL.
