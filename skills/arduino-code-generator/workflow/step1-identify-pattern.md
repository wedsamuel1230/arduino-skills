# Step 1: Identify Pattern Type

When a user requests Arduino code, first identify the core pattern category from their request:

## Pattern Categories

### Hardware Abstraction
- Multi-board configuration
- Pin definitions
- Memory management
- Board detection

**Keywords:** config, pins, setup, board, memory

### Sensor Reading & Filtering
- ADC noise reduction
- Sensor data processing
- Calibration and validation
- Environmental sensors (DHT22, BME280)

**Keywords:** sensor, read, temperature, humidity, filter, noise, adc

### Input Handling
- Button debouncing
- Edge detection
- Multi-button management
- User input processing

**Keywords:** button, press, input, debounce, switch

### Communication
- I2C device management
- SPI configuration
- UART/Serial protocols
- Data output (CSV)

**Keywords:** i2c, spi, serial, uart, communication, csv, data

### Timing & Concurrency
- Non-blocking timing
- Task scheduling
- State machines
- Event-driven programming

**Keywords:** timer, schedule, state machine, non-blocking, millis

### Hardware Detection
- Auto-detection
- Fallback strategies
- Adaptive configuration
- Resource monitoring

**Keywords:** detect, auto, fallback, adaptive

### Data Persistence
- EEPROM storage
- SD card logging
- Data validation
- Wear leveling

**Keywords:** eeprom, sd card, log, save, store, data

## Identification Process

1. **Scan request for keywords** from the categories above
2. **Determine primary pattern** (most relevant category)
3. **Note secondary patterns** that might be needed for integration
4. **Consider board constraints** (UNO vs ESP32 vs RP2040)

## Examples

**"Generate code to read a DHT22 sensor without blocking"**
→ Primary: Sensor Reading & Filtering + Timing & Concurrency

**"Create a button handler with long press detection"**
→ Primary: Input Handling

**"Make an I2C scanner for my Arduino"**
→ Primary: Communication (I2C)

**"Log data to SD card every 10 seconds"**
→ Primary: Data Persistence + Timing & Concurrency