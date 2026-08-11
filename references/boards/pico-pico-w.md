# Raspberry Pi Pico and Pico W with Arduino-Pico

This profile assumes RP2040 Pico/Pico W boards and the Earle Philhower
Arduino-Pico core, not RP2350 boards or the Pico SDK.

## Profile

- Logic: 3.3 V GPIO. VSYS accepts 1.8-5.5 V; USB VBUS is nominally 5 V.
  VSYS is not a regulated 3.3 V peripheral rail.
- PWM: RP2040 has 8 PWM slices with two channels each; pins sharing a slice
  share timing configuration. Arduino-Pico maps `analogWrite()` to hardware
  PWM.
- ADC: GPIO26-GPIO29 are ADC0-ADC3; the internal temperature sensor is ADC4;
  the converter is 12-bit.
- PIO/CPU: two Cortex-M0+ cores; two PIO blocks with four state machines each.
  Arduino-Pico exposes multicore and PIO APIs, but shared resources still need
  explicit coordination.
- Memory: 264 KB SRAM. Standard Pico and Pico W boards commonly carry 2 MB
  external QSPI flash; verify the product revision.
- Default Arduino-Pico buses: Wire0 SDA/SCL GPIO4/GPIO5; Wire1 GPIO26/GPIO27;
  SPI0 MISO/MOSI/SCK/SS GPIO16/GPIO19/GPIO18/GPIO17; SPI1
  GPIO12/GPIO15/GPIO14/GPIO13; Serial1 TX/RX GPIO0/GPIO1 and Serial2
  GPIO8/GPIO9. The core permits alternate routing.
- GPIO current: RP2040 provides nominal 2, 4, 8, and 12 mA output-drive modes.
  The datasheet explicitly says these are not hard limits; actual source or
  sink current depends on load and the selected voltage guarantee. Its maximum
  total IOVDD current and total VSS current due to GPIO/QSPI IO are each 50 mA.
  Do not use a drive setting as a safe LED, motor, or board-load target. Size
  the regulator and Pico W radio-burst supply from the board schematic and
  measure the complete load.

## Pitfalls

- Only GPIO26-29 are external ADC inputs; ADC resolution is not accuracy.
- PWM slices are shared; two pins can interfere even though both are PWM-capable.
- QSPI flash pins are not user GPIO.
- Pico W wireless operation changes power and timing constraints; do not assume
  a Pico sketch and a Pico W sketch have identical resource headroom.

## Sources

1. [Raspberry Pi Pico datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)
2. [RP2040 datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)
3. [Raspberry Pi Pico documentation](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)
4. [Arduino-Pico core README at commit 9a0bc35](https://github.com/earlephilhower/arduino-pico/blob/9a0bc35654e9af3eccfb88c54f9cc73f9e153ac6/README.md)
5. [Arduino-Pico pin definitions at commit 9a0bc35](https://github.com/earlephilhower/arduino-pico/blob/9a0bc35654e9af3eccfb88c54f9cc73f9e153ac6/variants/rpipico/pins_arduino.h)

## Fact-to-source map

| Fact group | Primary source(s) | Status |
|---|---|---|
| Board supply, flash and exposed GPIO | 1 and 3 | verified for the named Pico/Pico W board family; clone/carrier gaps remain |
| RP2040 PWM, ADC, PIO, dual core and current characteristics | 2 | verified against the MCU datasheet |
| Arduino-Pico default buses and alternate routing | 4 and 5 | pinned to commit 9a0bc35654e9af3eccfb88c54f9cc73f9e153ac6 |
| Pico W radio load and product-specific regulator behavior | 1 and exact board schematic | board-specific; measure the finished rail |

Source status: MCU, board supply, PIO, ADC, and bus facts are source-backed
and were checked on 2026-08-10. Exact flash population, total-current budget,
and carrier exposure remain board-specific.
