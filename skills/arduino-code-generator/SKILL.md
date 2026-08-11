---
name: arduino-code-generator
description: Generate Arduino and embedded C++ snippets for sensors, actuators, buses, state machines, timing, data logging, and hardware abstraction. Use when a user requests implementation code and provide the exact board, framework, toolchain, pins, voltage, memory, and library versions first. Bundled templates target UNO, ESP32, and RP2040; document unsupported board or vendor-framework behavior instead of guessing.
metadata: {triggers: "generate Arduino code, C++, sensor, actuator, state machine"}
---

# Arduino Code Generator

Generate production-quality Arduino code snippets for sensors, actuators, communication, and embedded patterns.

## Quick Start

**Browse example sketches:**
```bash
# See 9 production-ready examples in examples/ folder
ls examples/
# config-example.ino, filtering-example.ino, buttons-example.ino,
# i2c-example.ino, csv-example.ino, scheduler-example.ino,
# state-machine-example.ino, hardware-detection-example.ino,
# data-logging-example.ino
```

**List available patterns:**
```bash
uv run --no-project scripts/generate_snippet.py --list
```

**Generate code for specific pattern and board:**
```bash
uv run --no-project scripts/generate_snippet.py --pattern i2c --board esp32
uv run --no-project scripts/generate_snippet.py --pattern buttons --board uno --output button.ino
```

**Interactive mode:**
```bash
uv run --no-project scripts/generate_snippet.py --interactive
```

## Target Gate

Read [the shared contract](../../docs/arduino-skill-contract.md) and the board
profile before selecting pins, APIs, or libraries. Keep board-specific branches
isolated, check memory and peripheral constraints, and state whether the result
has build proof only or also has upload, hardware, and system proof. The
generator's board flag is a template selector, not evidence that the generated
code works on a similar-looking board.

## Resources

- **examples/** - 9 production-ready example sketches (one per pattern category)
- **examples/README.md** - Detailed documentation for each example with wiring diagrams
- **scripts/generate_snippet.py** - CLI tool for code generation with 9 pattern templates
- **scripts/verify_patterns.ps1** - Compile examples for UNO/ESP32/RP2040 (PowerShell)
- **scripts/verify_patterns.sh** - Compile examples for UNO/ESP32/RP2040 (bash)
- **assets/workflow.mmd** - Mermaid diagram of code generation workflow

## Supported Patterns

### Hardware Abstraction
- Multi-board config.h with conditional compilation
- Pin definitions for UNO/ESP32/RP2040
- Memory budget tracking

See [patterns-config.md](references/patterns-config.md) | Example: [config-example.ino](examples/config-example.ino)

### Sensor Reading & Filtering
- ADC noise reduction (moving average, median, Kalman)
- DHT22, BME280, analog sensors
- Data validation and calibration

See [patterns-filtering.md](references/patterns-filtering.md) | Example: [filtering-example.ino](examples/filtering-example.ino)

### Input Handling
- Software button debouncing
- Edge detection (PRESSED/RELEASED/LONG_PRESS)
- Multi-button management

See [patterns-buttons.md](references/patterns-buttons.md) | Example: [buttons-example.ino](examples/buttons-example.ino)

### Communication
- I2C device scanning and diagnostics
- SPI configuration
- UART/Serial protocols
- CSV data output

See [patterns-i2c.md](references/patterns-i2c.md) and [patterns-csv.md](references/patterns-csv.md) | Examples: [i2c-example.ino](examples/i2c-example.ino), [csv-example.ino](examples/csv-example.ino)

### Timing & Concurrency
- Non-blocking millis() patterns
- Task scheduling without delay()
- Priority-based schedulers
- State machines

See [patterns-scheduler.md](references/patterns-scheduler.md) and [patterns-state-machine.md](references/patterns-state-machine.md) | Examples: [scheduler-example.ino](examples/scheduler-example.ino), [state-machine-example.ino](examples/state-machine-example.ino)

### Hardware Detection
- Auto-detect boards (UNO/ESP32/RP2040)
- SRAM usage monitoring
- Sensor fallback strategies
- Adaptive configuration

See [patterns-hardware-detection.md](references/patterns-hardware-detection.md) | Example: [hardware-detection-example.ino](examples/hardware-detection-example.ino)

### Data Persistence
- EEPROM with CRC validation
- SD card FAT32 logging
- Wear leveling for EEPROM
- Buffered writes

See [patterns-data-logging.md](references/patterns-data-logging.md) | Example: [data-logging-example.ino](examples/data-logging-example.ino)

## Code Generation Workflow

- [ ] **[Identify Pattern Type](workflow/step1-identify-pattern.md)** - Analyze user request to determine core pattern category
- [ ] **[Read Reference Documentation](workflow/step2-read-reference.md)** - Consult pattern-specific reference files for implementation details
- [ ] **[Generate Code](workflow/step3-generate-code.md)** - Create production-ready code following quality standards
- [ ] **[Provide Instructions](workflow/step4-provide-instructions.md)** - Include wiring diagrams and usage guidance
- [ ] **[Mention Integration](workflow/step5-mention-integration.md)** - Suggest combinations with other patterns when relevant

## Quality Standards & Rules

- [ ] **[Quality Standards](rules/quality-standards.md)** - Compilation, timing, memory safety, and error handling requirements
- [ ] **[Board Optimization](rules/board-optimization.md)** - UNO, ESP32, and RP2040 specific optimizations and features
- [ ] **[Common Pitfalls](rules/common-pitfalls.md)** - Critical mistakes to avoid in Arduino development

## Code Output Template

- [ ] **[Code Template](templates/code-output-template.md)** - Standardized structure for generated Arduino sketches

## Resources

- **examples/** - 9 production-ready example sketches (one per pattern category)
- **examples/README.md** - Detailed documentation for each example with wiring diagrams
- **scripts/generate_snippet.py** - CLI tool for code generation with 9 pattern templates
- **assets/workflow.mmd** - Mermaid diagram of code generation workflow
- **workflow/** - Step-by-step code generation process
- **rules/** - Quality standards and board-specific optimizations
- **templates/** - Code output templates and structure guidelines
- **references/** - Detailed pattern documentation and API references
- **references/README.md** - Reference structure and formatting guide

## Shared Output Contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
