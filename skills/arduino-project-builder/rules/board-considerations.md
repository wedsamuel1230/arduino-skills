# Board-Specific Considerations

Hardware and software optimizations for different Arduino-compatible boards.

## Arduino UNO/Nano (ATmega328P)

### Memory Constraints
- **SRAM:** 2KB total - Keep arrays small, monitor usage constantly
- **Flash:** 32KB - Code size limited, optimize for space
- **EEPROM:** 1KB - Use sparingly, implement wear leveling

### Hardware Features
- **ADC:** 10-bit resolution (0-1023 range)
- **PWM:** 6 pins (3, 5, 6, 9, 10, 11)
- **Interrupts:** Only 2 external (pins 2, 3)
- **I2C:** Software implementation, slower than hardware

### Optimization Strategies
- Use F() macro for all string literals to save RAM
- Avoid large arrays and complex data structures
- Implement simple filtering algorithms
- Use interrupt-driven inputs sparingly

### Communication
- No built-in WiFi/Bluetooth
- Serial communication at 9600 baud recommended
- External modules required for wireless connectivity

## ESP32 (ESP32-WROOM-32)

### Memory Resources
- **SRAM:** 327KB+ - Can use large buffers and complex structures
- **Flash:** 4MB+ - Ample space for code and data
- **PSRAM:** Optional external RAM for large datasets

### Hardware Features
- **ADC:** 12-bit resolution (0-4095 range), 18 channels
- **PWM:** 16 channels with adjustable frequency
- **Interrupts:** Multiple GPIO pins support interrupts
- **I2C/SPI:** Hardware accelerated, multiple buses

### Advanced Capabilities
- **Dual-core:** Run tasks in parallel on CPU0/CPU1
- **WiFi/Bluetooth:** Built-in 802.11 b/g/n WiFi, Bluetooth 4.2
- **Deep sleep:** Ultra-low power consumption modes
- **RTC:** Real-time clock with battery backup

### IoT Optimization
- Implement WiFi reconnection with exponential backoff
- Use FreeRTOS tasks for concurrent operations
- Leverage deep sleep for battery-powered applications
- Implement OTA (Over-The-Air) updates

## Raspberry Pi Pico (RP2040)

### Memory Resources
- **SRAM:** 262KB - Good balance between UNO and ESP32
- **Flash:** 2MB - Sufficient for most applications
- **No EEPROM:** Use flash for persistent storage

### Hardware Features
- **ADC:** 12-bit resolution (0-4095 range), 5 channels
- **PWM:** 16 channels, 8 slices
- **PIO:** Programmable I/O for custom protocols
- **Interrupts:** All GPIO pins support interrupts

### Advanced Features
- **Dual-core:** Cortex-M0+ cores for parallel processing
- **PIO State Machines:** Hardware-accelerated custom protocols
- **USB:** Full-speed USB 1.1 with device/host support
- **High-speed interfaces:** SPI, I2C, UART with DMA

### Performance Optimization
- Utilize PIO for timing-critical operations
- Implement DMA for high-speed data transfer
- Use both cores for computationally intensive tasks
- Leverage USB for high-bandwidth communication

## Cross-Board Compatibility

### Conditional Compilation
```cpp
#ifdef ARDUINO_AVR_UNO
  // UNO-specific code
#elif defined(ESP32)
  // ESP32-specific code
#elif defined(ARDUINO_ARCH_RP2040)
  // Pico-specific code
#endif
```

### Hardware Detection
- Implement runtime board detection
- Use conditional compilation for optimal performance
- Provide fallback implementations for missing features

### Memory Management
- Monitor memory usage across all platforms
- Implement different strategies for different memory sizes
- Use heap allocation carefully on constrained boards

### Communication Abstraction
- Abstract communication interfaces (WiFi, Serial)
- Provide board-specific implementations
- Gracefully degrade when features unavailable