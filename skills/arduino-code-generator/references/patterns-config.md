# Config.h Hardware Abstraction Pattern

## Basic Template

```cpp
// config.h
#ifndef CONFIG_H
#define CONFIG_H

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_NANO)
  #define BOARD_NAME "Arduino UNO"
  #define LED_PIN 13
  #define BUTTON_PIN 2
  #define I2C_SDA A4
  #define I2C_SCL A5
  #define SRAM_SIZE 2048

#elif defined(ESP32)
  #define BOARD_NAME "ESP32"
  #define LED_PIN 2
  #define BUTTON_PIN 4
  #define I2C_SDA 21
  #define I2C_SCL 22
  #define SRAM_SIZE 520000
  #define HAS_WIFI 1

#elif defined(ARDUINO_ARCH_RP2040)
  #define BOARD_NAME "RP2040"
  #define LED_PIN 25
  #define BUTTON_PIN 14
  #define I2C_SDA 4
  #define I2C_SCL 5
  #define SRAM_SIZE 264000

#else
  #error "Unsupported board!"
#endif

// Common constants
#define SERIAL_BAUD 115200
#define DEBOUNCE_DELAY 50
#define SENSOR_READ_INTERVAL 1000

#endif
```

## Usage
```cpp
#include "config.h"

void setup() {
  Serial.begin(SERIAL_BAUD);
  pinMode(LED_PIN, OUTPUT);
  Wire.begin(I2C_SDA, I2C_SCL);
}
```

## Key Points
- Use `#if defined()` for board detection
- Define all pins in config.h, never hardcode
- Include memory limits for adaptive code
- Add feature flags (HAS_WIFI, HAS_BLE) for capabilities
