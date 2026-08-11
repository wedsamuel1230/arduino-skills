# Arduino Skills Design Principles

This document defines the core design principles and constraints for all skills in the **arduino-skills** repository.

## Core Rules

All skills MUST follow these rules. The router and shared contract provide the
cross-skill workflow; specialists keep domain-specific detail focused.

### Stable Pin Declaration Convention

When a pin declaration is requested, emit raw C++ declarations in the user's
fixed logical order, for example:

```cpp
constexpr int btn_esc = 101;
constexpr int btn_enter = 102;
```

Do not replace this with an enum, macro, array, or explanatory wrapper. Keep the
logical IDs separate from the board's physical GPIO map, which still requires
board-specific input/output, strapping, flash/PSRAM, USB, voltage, pull, and
current checks.

### Composable Guardrails

Use `board-support` for named-board profile lookup, capabilities, source status,
identity-contract checks, and exact pin-risk intake. Use `board-selection` before choosing an exact target,
`pin-assignment` and
`wiring-safety-check` before wiring, `library-selection` and `memory-budgeting`
before adding dependencies, `non-blocking-patterns` for timing, and
`hardware-tdd` plus `embedded-project-loop` when physical evidence is needed.

### Recommended Lifecycle Entry

Use `embedded-project-loop` first for any physical, recovery, measurement, or
multi-session request. It owns the durable goal, one next todo, append-only
experiment evidence, rollback boundary, and user-owned physical gate. Continue
through `arduino-workflow-router` for board, toolchain, wiring, firmware, test,
and deployment specialists. A heartbeat or compile result never closes a later
proof stage.

### 0. Universal Intake And Routing

Before board-dependent advice, resolve a named board through `board-support` or
record the exact board/revision, MCU, pins,
memory, peripherals, voltage/current, protocols, framework, toolchain, and
versions. Use `arduino-workflow-router` when the request crosses firmware,
electronics, power, networking, enclosure, deployment, or maintenance.
The supported toolchain branches are Arduino IDE, Arduino CLI, PlatformIO, and
vendor-specific tools; do not merge their commands or compatibility claims.

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

## Reference Platforms

These profiles are examples, not a guarantee for every board in the family.
The exact target and revision always win over a remembered platform table.

| Platform | SRAM | Flash | Baud Rate | Special Features |
|----------|------|-------|-----------|------------------|
| **Arduino UNO/Nano** | 2 KB | 32 KB | 9600 | F() macro required for strings |
| **ESP32 DevKit** | 520 KB | 4 MB | 115200 | WiFi, BLE, dual-core, FreeRTOS |
| **RP2040 (Pico)** | 264 KB | 2 MB | 115200 | Dual-core, PIO, USB host |

Exact board profiles additionally cover Arduino Mega 2560 Rev3, Nano Every,
Nano ESP32, and ESP32-C3-DevKitC-02. Read `references/boards/index.json` and
the selected profile before assigning pins or making voltage/current claims.
For repository work, use `scripts/resolve_board_profile.py` and stop on a
`needs-disambiguation` result for variant-sensitive advice.

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

Every active skill also links `docs/arduino-skill-contract.md` and reports
assumptions, required tools and versions, implementation steps, tests/evidence,
known limitations, and recovery/security notes.

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
- [ ] Works on the exact target board and toolchain (or limitation is documented)
- [ ] Edge cases handled (overflow, disconnected sensors, etc.)
- [ ] Multi-session or physical work has a durable loop state, one next todo,
      append-only ledger, and explicit physical gate

Label each result as build, upload, hardware, system, or deployment proof.
Compilation success alone is not hardware or system success.

Run `python3 scripts/run_arduino_evals.py` before release. The loop-engine
scenario must accept complete durable artifacts and reject incomplete state or
ledger fixtures.

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
- ❌ Secrets, API keys, private keys, or passwords in source, examples, or logs
- ❌ Unpinned dependency/toolchain claims presented as reproducible results

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
