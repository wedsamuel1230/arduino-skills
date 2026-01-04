# Arduino Code Generator - Example Sketches

This directory contains **9 production-ready example sketches** demonstrating each pattern category in the arduino-code-generator skill. All examples follow best practices from `arduino-skills.md`.

## 📁 Available Examples

### 1. **config-example.ino** - Hardware Configuration Pattern
**Purpose:** Board-agnostic hardware abstraction using compile-time configuration

**Demonstrates:**
- Multi-board support (UNO/ESP32/RP2040) with automatic pin mapping
- Compile-time board detection using preprocessor directives
- Single codebase for multiple platforms

**Boards:** Arduino UNO, ESP32, RP2040

---

### 2. **filtering-example.ino** - ADC Filtering & Signal Processing
**Purpose:** Clean noisy sensor readings using multiple filtering techniques

**Demonstrates:**
- Moving average filter (10-sample window)
- Exponential moving average (EMA) with alpha = 0.15
- Median filter (3-sample spike rejection)
- CSV output format for data analysis

**Boards:** All (uses analog input A0)

---

### 3. **buttons-example.ino** - Debounced Button Input
**Purpose:** Robust button handling with debouncing and event detection

**Demonstrates:**
- Hardware debouncing (50ms threshold)
- Press/release event detection
- Long-press detection (1 second)
- Non-blocking state machine implementation

**Boards:** Arduino UNO (pin 2), ESP32 (pin 4), RP2040 (pin 10)

---

### 4. **i2c-example.ino** - I2C Communication & Device Scanner
**Purpose:** I2C bus scanning with device identification

**Demonstrates:**
- 7-bit address scanning (0x08-0x77)
- Board-specific SDA/SCL pin configuration
- Error detection and reporting
- Common device identification (OLED, RTC, IMU, sensors)

**Boards:** Arduino UNO (A4/A5), ESP32 (21/22), RP2040 (4/5)

---

### 5. **csv-example.ino** - CSV Data Output Pattern
**Purpose:** Structured data logging in CSV format for analysis

**Demonstrates:**
- Timestamp + multi-channel sensor data
- F() macro for PROGMEM string storage
- Proper CSV formatting with headers
- Data suitable for Excel/Python analysis

**Boards:** All (simulated sensors)

---

### 6. **scheduler-example.ino** - Non-Blocking Task Scheduler
**Purpose:** Cooperative multitasking without delay()

**Demonstrates:**
- Lightweight task scheduler (millis() based)
- 5 independent tasks with different intervals
- Task enable/disable control
- Execution tracking and status reporting

**Boards:** All

---

### 7. **state-machine-example.ino** - Finite State Machine (FSM)
**Purpose:** Traffic light controller using explicit state machine

**Demonstrates:**
- State enumeration and transition logic
- Timing-based state changes (non-blocking)
- State-specific behavior and LED outputs
- 4-state cycle: RED → RED+YELLOW → GREEN → YELLOW

**Boards:** Arduino UNO (pins 9/10/11), ESP32 (pins 25/26/27)

---

### 8. **hardware-detection-example.ino** - Runtime Board Detection
**Purpose:** Detect board capabilities and report system information

**Demonstrates:**
- Compile-time board identification
- Memory capacity detection (Flash/SRAM)
- Clock speed and ADC resolution reporting
- Feature flags (WiFi, Bluetooth)

**Boards:** UNO, Mega 2560, ESP32, RP2040, SAMD21

---

### 9. **data-logging-example.ino** - EEPROM Persistent Data Storage
**Purpose:** Long-term sensor data logging with EEPROM

**Demonstrates:**
- Circular buffer implementation (20 entries)
- EEPROM wear leveling (write minimization)
- Data retrieval and playback
- Sensor data persistence across reboots

**Boards:** All (uses EEPROM library)

---

## 🚀 Quick Start

### Upload an Example

1. **Open Arduino IDE**
2. **Select your board:**
   - Tools → Board → Arduino UNO / ESP32 / RP2040
3. **Open example:**
   - File → Open → `arduino-code-generator/examples/<example>.ino`
4. **Upload:**
   - Click Upload (or Ctrl+U)
5. **Open Serial Monitor:**
   - Tools → Serial Monitor (or Ctrl+Shift+M)
   - Set baud rate (9600 for UNO, 115200 for ESP32/RP2040)

### Generate Custom Code

Use the `generate_snippet.py` script to create custom variations:

```bash
# Generate config pattern for ESP32
uv run scripts/generate_snippet.py --pattern config --board esp32

# Generate button handler for UNO on pin 3
uv run scripts/generate_snippet.py --pattern buttons --board uno --pin 3

# Interactive mode
uv run scripts/generate_snippet.py --interactive
```

---

## 📚 Pattern Reference Documentation

Each example corresponds to a detailed reference file in `references/`:

| Example | Reference File |
|---------|---------------|
| config-example.ino | [patterns-config.md](../references/patterns-config.md) |
| filtering-example.ino | [patterns-filtering.md](../references/patterns-filtering.md) |
| buttons-example.ino | [patterns-buttons.md](../references/patterns-buttons.md) |
| i2c-example.ino | [patterns-i2c.md](../references/patterns-i2c.md) |
| csv-example.ino | [patterns-csv.md](../references/patterns-csv.md) |
| scheduler-example.ino | [patterns-scheduler.md](../references/patterns-scheduler.md) |
| state-machine-example.ino | [patterns-state-machine.md](../references/patterns-state-machine.md) |
| hardware-detection-example.ino | [patterns-hardware-detection.md](../references/patterns-hardware-detection.md) |
| data-logging-example.ino | [patterns-data-logging.md](../references/patterns-data-logging.md) |

---

## 🛠️ Design Principles

All examples follow arduino-skills best practices:

✅ **No `delay()`** - All timing uses `millis()` for non-blocking execution  
✅ **F() macros** - String literals stored in PROGMEM to save RAM  
✅ **Board-agnostic** - Compile for UNO/ESP32/RP2040 without code changes  
✅ **Modular classes** - Reusable components with clear interfaces  
✅ **Serial output** - Verifiable behavior for testing/debugging  
✅ **Production-ready** - Proper error handling and edge cases

---

## 📊 Testing & Verification

Each example includes:

- **Serial output** for runtime verification
- **Compile-time board detection** for hardware compatibility
- **Non-blocking loops** for responsive systems
- **Documentation** explaining pattern rationale

To verify an example compiles for all boards:

```bash
# Verify UNO compilation
arduino-cli compile --fqbn arduino:avr:uno config-example.ino

# Verify ESP32 compilation
arduino-cli compile --fqbn esp32:esp32:esp32 config-example.ino

# Verify RP2040 compilation
arduino-cli compile --fqbn rp2040:rp2040:rpipico config-example.ino
```

---

## 🤝 Contributing

To add a new example:

1. Follow the template structure (header comment, configuration, classes, setup, loop)
2. Ensure board compatibility (UNO/ESP32/RP2040 minimum)
3. Add documentation to this README
4. Create corresponding reference file in `references/`
5. Test compilation on all target boards

---

## 📄 License

MIT License - See [LICENSE](../../LICENSE) for details

**Generated by:** arduino-code-generator v1.0.0  
**Last Updated:** January 2025
