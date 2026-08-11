# Classic ESP32 DevKit / ESP32-WROOM

"ESP32 DevKit" is not one electrical SKU. Confirm the exact DevKit revision,
ESP32-WROOM module suffix, flash population, and attached peripherals before
assigning pins.

## Profile

- Logic: 3.3 V class; ESP32-WROOM module supply is 3.0-3.6 V. A DevKit may
  accept 5 V on USB/VIN, but its GPIO is not 5 V tolerant.
- PWM: Arduino-ESP32 LEDC, up to 16 channels on classic ESP32; frequency and
  resolution are configured, so do not assume Uno timer behavior.
- ADC: 12-bit SAR. ADC1 is GPIO32-39. ADC2 covers GPIO0, GPIO2, GPIO4,
  GPIO12-15, GPIO25-27 and is unavailable/restricted while WiFi is active.
- Touch: GPIO0, GPIO2, GPIO4, GPIO12-15, GPIO27, GPIO32, GPIO33 in the
  classic Arduino-ESP32 mapping.
- Memory: 520 KB internal SRAM; WROOM flash varies by module, with 4 MB common
  but not universal.
- Default Arduino buses: UART0 TX/RX GPIO1/GPIO3; I2C SDA/SCL GPIO21/GPIO22;
  VSPI SS/MOSI/MISO/SCK GPIO5/GPIO23/GPIO19/GPIO18. APIs can remap them.
- GPIO current (SoC electrical characteristics, not a DevKit load budget): at
  3.3 V and maximum drive, the datasheet specifies 40 mA high-level source for
  VDD3P3_CPU/RTC pins, 20 mA for VDD_SDIO pins, and 28 mA low-level sink. The
  configurable drive settings are approximately 5, 10, 20, and 40 mA, with
  20 mA as the default. These are electrical test/drive characteristics, not
  safe LED, motor, or board-load targets; same-domain source current falls as
  more pins are loaded. The DevKit regulator, USB source, and radio-burst
  budget remain board-specific and require the module datasheet, schematic,
  and rail measurement.

## Pins to reserve or verify

- GPIO34-39 are input-only and have no internal pull-up/pull-down.
- GPIO6-11 are connected to SPI flash and are not general-purpose pins.
- Common strapping pins are GPIO0, GPIO2, GPIO5, GPIO12, and GPIO15; their
  reset levels affect boot or flash configuration.
- GPIO16/GPIO17 may be consumed by PSRAM on a module variant.

## Sources

1. [Espressif ESP32 GPIO API](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html)
2. [ESP32 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)
3. [ESP32-WROOM-32 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf)
4. [ESP32 DevKitC user guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html)
5. [Arduino-ESP32 classic pin variant at commit d8a1bf6](https://github.com/espressif/arduino-esp32/blob/d8a1bf60d01aac021fc5f3cff30126f11d1e10a6/variants/esp32/pins_arduino.h)

## Fact-to-source map

| Fact group | Primary source(s) | Status |
|---|---|---|
| GPIO direction, pulls, strapping, ADC and touch | 1 and 2 | verified against Espressif primary sources |
| Module supply and flash variation | 3 | verified for WROOM variants; exact suffix still required |
| DevKit USB/VIN and exposed header | 4 | verified for the named DevKitC revision; clones remain a gap |
| Arduino default bus map | 5 | pinned to commit d8a1bf60d01aac021fc5f3cff30126f11d1e10a6 |
| GPIO and total-board current | 2 and exact board schematic | SoC electrical figures verified; board load budget is a gap |

Source status: classic GPIO restrictions and default maps are primary-source
checked on 2026-08-10. Exact flash, PSRAM, regulator, and total-current values
remain module/board-specific.
