# Board-Specific Optimization

Optimize Arduino code for specific board capabilities and constraints to maximize performance and reliability.

## Arduino UNO (ATmega328P)
**Memory:** 2KB SRAM, 32KB Flash, 1KB EEPROM
**Architecture:** 8-bit AVR, 16MHz clock
**Features:** Basic I/O, limited peripherals

### Memory Optimization
- Use `F()` macro for **all string literals** to store in flash memory
- Minimize global variables and buffers
- Prefer `char[]` arrays over `String` objects
- Use `PROGMEM` for read-only data tables

```cpp
// UNO-optimized string handling
Serial.println(F("Initializing sensor..."));
const char message[] PROGMEM = "Error: Sensor not found";

// Avoid String class
char buffer[32];
strncpy(buffer, "Sensor data", sizeof(buffer));
```

### Timing Considerations
- `millis()` resolution: ~16ms (due to 16MHz/1024 prescaler)
- Avoid microsecond-precision timing
- Use `delayMicroseconds()` sparingly for short delays

### Peripheral Limitations
- Limited interrupt pins (2 external interrupts)
- No hardware I2C/SPI buffering
- Basic ADC (10-bit, ~100μs conversion time)
- No native USB (uses serial-to-USB converter)

## ESP32 (ESP32-WROOM-32)
**Memory:** 520KB SRAM, 4MB+ Flash, 4KB EEPROM emulation
**Architecture:** 32-bit Xtensa LX6, dual-core, 240MHz
**Features:** WiFi, Bluetooth, extensive peripherals

### Advanced Features
- **FreeRTOS multitasking** - use tasks for concurrent operations
- **WiFi connectivity** - implement IoT patterns
- **Bluetooth/BLE** - wireless communication
- **Dual-core processing** - distribute workloads

```cpp
// ESP32-specific patterns
#include <WiFi.h>
#include <esp_task_wdt.h>

// Use FreeRTOS tasks
TaskHandle_t sensorTask;
void sensorTaskFunction(void *parameter) {
  for (;;) {
    readSensors();
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}
```

### Memory Management
- Larger buffers acceptable (up to KB range)
- Use PSRAM if available for large data structures
- Implement proper task stack sizing
- Monitor heap usage with `ESP.getFreeHeap()`

### Power Management
- Deep sleep modes for battery-powered applications
- Dynamic frequency scaling
- Peripheral power gating

## RP2040 (Raspberry Pi Pico)
**Memory:** 264KB SRAM, 2MB Flash
**Architecture:** Dual-core ARM Cortex-M0+, 133MHz
**Features:** PIO, USB host, extensive I/O

### PIO (Programmable I/O)
- **Custom protocols** for timing-critical applications
- **Precise timing** without CPU intervention
- **Parallel interfaces** for displays and sensors

```cpp
// RP2040 PIO example (conceptual)
#include <hardware/pio.h>

// PIO for precise timing
PIO pio = pio0;
uint offset = pio_add_program(pio, &timing_program);
pio_sm_config config = timing_program_get_default_config(offset);
```

### Multicore Features
- **Dual-core processing** with `Core1` for dedicated tasks
- **Inter-core communication** via FIFO or shared memory
- **Load balancing** for compute-intensive operations

```cpp
// RP2040 multicore
#include <pico/multicore.h>

void core1_entry() {
  while (true) {
    // Dedicated processing on core 1
    processData();
  }
}

void setup() {
  multicore_launch_core1(core1_entry);
}
```

### USB Capabilities
- **USB host mode** for connecting peripherals
- **High-speed data transfer**
- **Device emulation** for custom interfaces

### Performance Optimization
- **133MHz clock speed** for faster processing
- **Large SRAM** allows more complex algorithms
- **Hardware floating point** for mathematical operations

## Cross-Board Compatibility

### Conditional Compilation
Use preprocessor directives for board-specific code:

```cpp
#if defined(ARDUINO_AVR_UNO)
  // UNO-specific code
  Serial.println(F("UNO detected"));
#elif defined(ESP32)
  // ESP32-specific code
  WiFi.begin(ssid, password);
#elif defined(ARDUINO_ARCH_RP2040)
  // RP2040-specific code
  multicore_launch_core1(taskFunction);
#endif
```

### Runtime Detection
Implement runtime board detection for adaptive behavior:

```cpp
// Board detection patterns
bool isESP32() {
  #ifdef ESP32
    return true;
  #else
    return false;
  #endif
}

void adaptiveConfiguration() {
  if (isESP32()) {
    // ESP32 configuration
    enableWiFi();
  } else {
    // UNO/RP2040 configuration
    useSerialOnly();
  }
}
```

## Performance Benchmarks

### Memory Usage Guidelines
- **UNO:** Keep RAM usage under 1.5KB for stability
- **ESP32:** Up to 300KB RAM acceptable for most applications
- **RP2040:** Up to 200KB RAM available for user applications

### Timing Accuracy
- **UNO:** ±16ms for millis() timing
- **ESP32:** ±1ms with hardware timers
- **RP2040:** ±1μs with PIO for precise timing

### Power Consumption
- **UNO:** ~50mA active, ~20mA sleep
- **ESP32:** 80-240mA active, <1mA deep sleep
- **RP2040:** ~25mA active, ~1mA sleep