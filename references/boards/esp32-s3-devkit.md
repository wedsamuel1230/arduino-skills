# ESP32-S3 DevKit

Confirm the exact DevKitC board, ESP32-S3-WROOM module suffix, flash/PSRAM
population, USB mode, and Arduino-ESP32 core version.

## Profile

- Logic: 3.3 V class; ESP32-S3-WROOM supply is 3.0-3.6 V. GPIO is not 5 V
  tolerant.
- PWM: Arduino-ESP32 LEDC exposes up to 8 channels on ESP32-S3.
- ADC: 12-bit SAR; generic Arduino mapping exposes A0-A19 as GPIO1-GPIO20,
  but board exposure and USB use must be checked.
- Touch: Arduino-ESP32 generic mapping exposes T1-T14 as GPIO1-GPIO14.
- Memory: 512 KB internal SRAM; flash and PSRAM vary by WROOM suffix.
- Default generic Arduino buses: UART0 TX/RX GPIO43/GPIO44; I2C SDA/SCL
  GPIO8/GPIO9; SPI SS/MOSI/MISO/SCK GPIO10/GPIO11/GPIO13/GPIO12. Board
  variants can intentionally use different defaults.
- GPIO current (SoC electrical characteristics, not a DevKit load budget): at
  3.3 V and maximum PAD_DRIVER, the datasheet specifies 40 mA high-level source
  and 28 mA low-level sink. Default drive strengths are 10 mA on GPIO17/18,
  40 mA on GPIO19/20, and 20 mA on other pins. These are electrical
  characteristics, not safe LED, motor, or board-load targets; the 1500 mA
  cumulative IO figure is an absolute stress rating. Module population, USB
  use, radio bursts, regulator capacity, and the finished 3.3 V rail remain
  board-specific.

## Pins to reserve or verify

- GPIO0, GPIO3, GPIO45, and GPIO46 are strapping pins.
- GPIO19/GPIO20 are USB-JTAG/USB pins by default; using them as GPIO can disable
  USB behavior.
- GPIO26-GPIO32 are normally SPI flash/PSRAM pins. GPIO33-GPIO37 can also be
  reserved with octal flash/PSRAM. Do not assign them without the exact module
  datasheet and board schematic.
- Do not carry the classic ESP32 GPIO34-39 input-only rule into S3 without
  checking the S3 GPIO table; S3 capability and board reservation differ.

## Sources

1. [Espressif ESP32-S3 GPIO API](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/gpio.html)
2. [ESP32-S3 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)
3. [ESP32-S3-WROOM-1 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
4. [ESP DevKit documentation](https://docs.espressif.com/projects/esp-dev-kits/en/latest/)
5. [Arduino-ESP32 S3 pin variant at commit d8a1bf6](https://github.com/espressif/arduino-esp32/blob/d8a1bf60d01aac021fc5f3cff30126f11d1e10a6/variants/esp32s3/pins_arduino.h)

## Fact-to-source map

| Fact group | Primary source(s) | Status |
|---|---|---|
| GPIO direction, strapping, USB and ADC | 1 and 2 | verified against Espressif primary sources |
| Module supply, flash and PSRAM reservations | 3 | verified for WROOM-1 variants; exact suffix still required |
| DevKit exposure and USB mode | 4 | board-revision and USB-configuration dependent |
| Arduino default bus and touch map | 5 | pinned to commit d8a1bf60d01aac021fc5f3cff30126f11d1e10a6 |
| GPIO and total-board current | 2 and exact board schematic | SoC electrical figures verified; board load budget is a gap |

Source status: S3 strapping, USB, flash/PSRAM reservations, and variant maps
are source-backed and were checked on 2026-08-10. Exact board exposure, ADC
calibration, and current limits remain revision/module-dependent.
