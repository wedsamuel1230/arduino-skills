# Arduino Skills Design Principles

This document defines the core design principles and constraints for all skills in the **arduino-skills** repository.

## Core Rules

All skills MUST follow these three fundamental rules:

### 1. Verifiable Output
Every code example must include:
- **Test Procedures:** Step-by-step instructions to verify the code works
- **Expected Results:** Specific outputs (serial messages, LED patterns, sensor readings)
- **Acceptance Criteria:** Clear pass/fail conditions

**Example:**
```cpp
// Expected output:
// Button pressed!
// Button released!
```

### 2. Avoid delay() Blocking
Use non-blocking timing patterns:
- **millis()-based timers** with `unsigned long` overflow handling
- **State machines** for sequential operations
- **Event-driven architectures** instead of polling loops

**Anti-pattern:**
```cpp
❌ delay(1000);  // Blocks all other code
```

**Correct pattern:**
```cpp
✅ if (millis() - lastTime >= 1000) {
    lastTime = millis();
    // Execute periodic task
}
```

### 3. Hardware Abstraction
All board-specific code must be isolated in `config.h` using conditional compilation:

```cpp
// config.h
#if defined(ARDUINO_AVR_UNO)
  #define LED_PIN 13
  #define BAUD_RATE 9600
#elif defined(ESP32)
  #define LED_PIN 2
  #define BAUD_RATE 115200
#elif defined(ARDUINO_ARCH_RP2040)
  #define LED_PIN 25
  #define BAUD_RATE 115200
#endif
```

**Never hardcode pins in main logic:**
```cpp
❌ digitalWrite(13, HIGH);      // Hardcoded UNO pin
✅ digitalWrite(LED_PIN, HIGH);  // Abstracted from config.h
```

---

## Supported Platforms

| Platform | SRAM | Flash | Baud Rate | Special Features |
|----------|------|-------|-----------|------------------|
| **Arduino UNO/Nano** | 2 KB | 32 KB | 9600 | F() macro required for strings |
| **ESP32 DevKit** | 520 KB | 4 MB | 115200 | WiFi, BLE, dual-core, FreeRTOS |
| **RP2040 (Pico)** | 264 KB | 2 MB | 115200 | Dual-core, PIO, USB host |

---

## Code Quality Standards

### Memory Safety
- ✅ Bounds checking on all arrays
- ✅ Use `constexpr` or `const` for fixed sizes
- ✅ F() macro for string literals on UNO (SRAM conservation)
- ✅ No dynamic allocation (`new`/`malloc`) without explicit justification

### Timing Safety
- ✅ Use `unsigned long` for `millis()` timestamps (handles overflow)
- ✅ Check for overflow: `if (now - last >= interval)`
- ❌ Never cast `millis()` to `int` or `long`

### Compilation
- ✅ Compiles without warnings on Arduino IDE 2.x
- ✅ Compiles without warnings on PlatformIO
- ✅ No platform-specific extensions (unless isolated in `#ifdef`)

---

## Skill Structure Requirements

Every active skill must use the current Agent Skills frontmatter contract:

```yaml
---
name: skill-name
description: Explain what the skill does and when to use it.
compatibility: Optional. Mention runtime or tool constraints only when needed.
---
```

Body sections are flexible. The main requirement is that `SKILL.md` stays
focused enough to load cleanly at activation time.

Recommended structure:

1. **Overview** — Short statement of purpose
2. **Workflow** — The core steps the agent should follow
3. **Verification** — How to confirm the output is correct
4. **References** — Explicit pointers to `references/`, `scripts/`, or `assets/`

Progressive-disclosure rule:

- Keep `SKILL.md` focused and under 500 lines
- Move heavy examples, deep troubleshooting, lookup tables, and long reference
  material into support files
- Tell the agent when to open each referenced file

---

## Pattern Library

### Available Patterns (arduino-code-generator)
- `config` — Hardware abstraction layer
- `buttons` — Debounced button handling
- `i2c` — I2C scanner and diagnostics
- `scheduler` — Non-blocking multi-task coordination
- `csv` — Structured data output for logging
- `filtering` — ADC noise reduction (moving average, median, Kalman)
- `state-machine` — Enum-based finite state machines
- `hardware-detection` — Board and sensor auto-detection
- `data-logging` — EEPROM/SD card persistence

### Project Templates (arduino-project-builder)
- `environmental` — Multi-sensor data logger (DHT22, light, SD card)
- `robot` — Motor control with obstacle avoidance
- `iot` — WiFi-connected sensor with MQTT publishing

---

## Testing & Verification

### Verification Checklist
- [ ] Code compiles without warnings
- [ ] Serial output matches expected results
- [ ] Timing is non-blocking (no `delay()` in main loop)
- [ ] Memory usage documented (SRAM/Flash percentages)
- [ ] Works on target platform (UNO/ESP32/RP2040)
- [ ] Edge cases handled (overflow, disconnected sensors, etc.)

### Manual Testing Protocol
1. Upload code to target board
2. Open Serial Monitor at correct baud rate
3. Verify startup messages
4. Test normal operation
5. Test error conditions (disconnect sensor, press button rapidly, etc.)
6. Monitor for memory leaks or crashes (run for 5+ minutes)

---

## Educational Focus

Skills are designed for teaching:
- **Progressive complexity:** Beginner → Intermediate → Advanced
- **Explain "why" not just "how":** Include rationale for design decisions
- **Real-world relevance:** Use practical examples (sensor logging, robot control, IoT)
- **Safe patterns:** Teach memory-safe, timing-safe, maintainable code

---

## Constraints

### What's NOT Allowed
- ❌ Proprietary cloud services (Arduino.cc Web Editor)
- ❌ External dependencies without PEP 723 inline declarations (Python scripts)
- ❌ Hardcoded board assumptions (use config.h abstraction)
- ❌ Blocking code (delay() in main loop)
- ❌ Unsafe string handling (use F() macro on UNO)

### License
All skills are MIT-licensed for development, research, and prototyping.

---

## Script Execution

All Python automation scripts use **uv** for dependency management:

```bash
# List available patterns
uv run skills/arduino-code-generator/scripts/generate_snippet.py --list

# Generate code
uv run skills/arduino-code-generator/scripts/generate_snippet.py \
    --pattern i2c --board esp32

# Scaffold project
uv run skills/arduino-project-builder/scripts/scaffold_project.py \
    --type environmental --board esp32 --name "WeatherStation"
```

Scripts use PEP 723 inline dependencies (no separate requirements.txt needed).

---

## References

- [Arduino Language Reference](https://www.arduino.cc/reference/en/)
- [ESP32 Arduino Core](https://github.com/espressif/arduino-esp32)
- [RP2040 Arduino Core](https://github.com/earlephilhower/arduino-pico)
- [PlatformIO Documentation](https://docs.platformio.org/)

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-04  
**Maintainer:** arduino-skills repository
