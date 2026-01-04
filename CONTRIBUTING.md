# Contributing to Arduino Skills

Thank you for your interest in contributing to Arduino Skills! This repository provides professional Arduino/embedded systems skills for educational use. Contributions should focus on creating high-quality, well-tested skills that follow our design principles.

## Before You Start

**Read the Design Principles First:**
- [arduino-skills.md](arduino-skills.md) — Core rules, platform support, code quality standards

**Understand the Skill Framework:**
- [README.md](README.md#how-skills-work) — Skill structure and ACP (Agent Context Protocol)
- Examine an existing skill folder (e.g., `battery-selector/`) for reference

## Submitting a New Skill

### 1. Create a Skill Folder

```
your-skill-name/
├── SKILL.md              # Required: Main skill documentation
├── scripts/              # Optional: Python automation scripts
│   └── generate_*.py     # PEP 723 inline dependencies
├── references/           # Optional: Reference implementations
│   ├── example-*.md
│   └── pattern-*.md
└── README.md             # Optional: Quick reference
```

### 2. Write Your SKILL.md

Every skill requires YAML frontmatter + body. Minimum sections:

```yaml
---
id: skill-name
title: Skill Title
category: arduino|maker|project-builder
platforms:
  - uno      # Arduino UNO
  - esp32    # ESP32
  - rp2040   # RP2040
whenToUse: |
  When users ask for [specific problem].
  Triggers: keywords, phrases, problem descriptions.
---

## Overview
Clear, concise description.

## Core Principles
1. Explain WHY this approach works
2. Design decisions and trade-offs

## Implementation
Complete, compile-ready code with comments.

## Verification Steps
✅ Expected output / behavior
❌ Common mistakes

## Common Pitfalls
- Issue 1
- Issue 2

## Advanced Patterns
For users who want to extend the skill.

## Engineering Rationale
Technical deep-dive for educators.

## Integration Notes
How this skill works with others.

## References
Links to datasheets, articles, code.
```

### 3. Checklist Before Submitting

**Code Quality:**
- [ ] Code compiles without warnings (Arduino IDE or PlatformIO)
- [ ] Uses `unsigned long` for millis() timing
- [ ] Bounds checking on all arrays
- [ ] F() macro for string constants on UNO
- [ ] No hardcoded pins (use config.h pattern)
- [ ] Memory-safe (no buffer overflows)

**Documentation:**
- [ ] SKILL.md has all required sections
- [ ] YAML frontmatter is valid (use `yamllint` to verify)
- [ ] Code examples include comments
- [ ] Verification steps have ✅/❌ comparisons
- [ ] At least 2 advanced patterns documented

**Testing (Platforms):**
- [ ] Tested on Arduino UNO (or documented limitation)
- [ ] Tested on ESP32 (or documented limitation)
- [ ] Tested on RP2040 (or documented limitation)
- [ ] Platform support clearly marked in SKILL.md

**Scripts (If Included):**
- [ ] PEP 723 inline dependencies (no requirements.txt)
- [ ] Runs with: `uv run script.py` or `python script.py`
- [ ] Has `--help` output
- [ ] Generates valid code that compiles

### 4. Pull Request Workflow

1. **Fork the repository** and create a feature branch: `git checkout -b skills/my-skill-name`

2. **Commit with clear messages:**
   ```
   feat(skill): add my-skill-name
   
   - Implement core skill logic
   - Add verification examples
   - Test on UNO, ESP32, RP2040
   ```

3. **Create a Pull Request** with:
   - Title: `feat(skill): my-skill-name — [short description]`
   - Description:
     ```markdown
     ## Skill: My Skill Name
     
     **Category:** arduino | maker | project-builder
     **Platforms:** UNO, ESP32, RP2040
     
     **Solves:** [Problem statement]
     
     **Verification:**
     - [ ] Compiles without warnings
     - [ ] Tested on all platforms
     - [ ] Checklist items complete
     - [ ] SKILL.md sections present
     ```

4. **PR Validation:**
   - Automated checks verify YAML syntax
   - Code compilation tests (if applicable)
   - Markdown linting

## Code Quality Standards

All contributions must follow these standards:

### Arduino Code

- **Timing:** Use `unsigned long` for millis() to avoid overflow bugs:
  ```cpp
  unsigned long lastTime = 0;
  const unsigned long INTERVAL = 1000; // ms
  
  if (millis() - lastTime >= INTERVAL) {
    lastTime = millis();
    // Do work here
  }
  ```

- **Memory Safety:** Always bounds-check arrays:
  ```cpp
  const int BUFFER_SIZE = 100;
  char buffer[BUFFER_SIZE];
  
  void addToBuffer(const char* data, int len) {
    if (len > BUFFER_SIZE - 1) len = BUFFER_SIZE - 1;
    strncpy(buffer, data, len);
    buffer[len] = '\0';
  }
  ```

- **String Constants on UNO:** Use F() macro to save RAM:
  ```cpp
  Serial.println(F("Low memory warning"));  // ✅ String in PROGMEM
  Serial.println("Low memory warning");     // ❌ String in RAM
  ```

- **Hardware Abstraction:** Never hardcode pins. Use config.h:
  ```cpp
  // config.h
  #ifdef ARDUINO_AVR_UNO
    #define LED_PIN 13
    #define BUTTON_PIN 2
  #elif ARDUINO_ESP32_DEV
    #define LED_PIN 2
    #define BUTTON_PIN 4
  #endif
  
  // main sketch
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  ```

### Python Scripts

- Use **PEP 723 inline dependencies:**
  ```python
  #!/usr/bin/env python3
  # /// script
  # requires-python = ">=3.8"
  # dependencies = [
  #   "requests",
  # ]
  # ///
  
  import requests
  ```

- **No external requirements.txt** — all dependencies inline
- Run with: `uv run script.py` or `python script.py`
- Include `--help` usage:
  ```bash
  $ python script.py --help
  usage: script.py [-h] [--board {uno,esp32,rp2040}]
  
  Generate Arduino code...
  ```

### Markdown & Documentation

- Use **yamllint** to validate SKILL.md frontmatter:
  ```bash
  yamllint SKILL.md
  ```

- Use **markdownlint** for Markdown consistency:
  ```bash
  markdownlint SKILL.md
  ```

- Keep lines ≤100 characters
- Use consistent heading hierarchy (#, ##, ###)
- Link to references with full URLs

## Design Principles Reference

From [arduino-skills.md](arduino-skills.md):

### 3 Core Rules
1. **Verifiable Output** — Code output must be observable (Serial.print, LED, motor spin)
2. **Avoid delay() Blocking** — Non-blocking patterns only (millis(), state machines)
3. **Hardware Abstraction** — Pin definitions in config.h, not hardcoded

### Platform Support
- **Arduino UNO:** 2 KB SRAM, 32 KB Flash
- **ESP32:** 520 KB SRAM, WiFi/BLE/RTOS
- **RP2040:** 264 KB SRAM, Dual-core

All skills must document which platforms they support.

### Code Quality

- No warnings on Arduino IDE compile
- Memory-safe (bounds checking)
- Timing-safe (unsigned long, not delay())
- Pin-safe (config.h, not hardcoded)

## Questions?

- **Existing issues:** Search [GitHub Issues](../../issues)
- **Feature requests:** Open a [new issue](../../issues/new)
- **Design questions:** File an issue with `[discussion]` prefix
- **Security concerns:** See [SECURITY.md](SECURITY.md)

## License

By contributing, you agree that your code will be licensed under the **MIT** license, consistent with the rest of this repository.

---

**Thank you for contributing to Arduino Skills!** 🎓
