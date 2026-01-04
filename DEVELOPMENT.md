# Development Guide

Welcome! This guide explains how to set up the Arduino Skills workspace, run automation scripts, create skills, and contribute to the project.

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/arduino-skills.git
cd arduino-skills
```

### 2. Install Dependencies

Arduino Skills uses Python automation scripts with `uv` for dependency management.

**Option A: Using uv (Recommended)**
```bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run scripts with uv (no setup required)
uv run arduino-code-generator/scripts/generate_snippet.py --board uno --pattern timer
uv run arduino-project-builder/scripts/scaffold_project.py --type environmental-monitor --board esp32
```

**Option B: Using Python directly**
```bash
python arduino-code-generator/scripts/generate_snippet.py --board uno --pattern timer
python arduino-project-builder/scripts/scaffold_project.py --type environmental-monitor --board esp32
```

### 3. Verify Installation

```bash
# Test code generator
python arduino-code-generator/scripts/generate_snippet.py --help

# Test project builder
python arduino-project-builder/scripts/scaffold_project.py --help
```

## Workspace Structure

```
arduino-skills/
├── README.md                    # Main documentation
├── CONTRIBUTING.md              # Contribution guidelines
├── CODE_OF_CONDUCT.md          # Community standards
├── DEVELOPMENT.md              # This file
├── SECURITY.md                 # Security policy
├── LICENSE                     # MIT license
├── CHANGELOG.md                # Version history
│
├── arduino-skills.md           # Design principles & constraints
│
├── Arduino Core Skills (9)
├── battery-selector/
├── bom-generator/
├── circuit-debugger/
│   ├── SKILL.md                # Skill documentation
│   ├── scripts/                # Python generators (PEP 723)
│   └── references/             # Example implementations
├── code-review-facilitator/
├── datasheet-interpreter/
├── enclosure-designer/
├── error-message-explainer/
├── power-budget-calculator/
├── readme-generator/
│
├── .github/
│   ├── workflows/
│   │   └── release.yml         # Automated GitHub releases
│   ├── ISSUE_TEMPLATE/         # Issue templates
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   ├── skill_proposal.md
│   │   └── discussion.md
│   └── pull_request_template.md
│
├── docs/                       # Documentation assets
│   └── diagrams/
│
├── memory-bank/                # Session history & context
│   ├── projectbrief.md
│   ├── activeContext.md
│   └── SESSION.md
│
└── reference/                  # Reference implementations
    └── datasheet-parser/       # Example pattern library
```

## Creating a New Skill

### Step 1: Plan Your Skill

Answer these questions:
- **Problem:** What does this skill teach or solve?
- **Platforms:** UNO, ESP32, RP2040 (or subset)?
- **Complexity:** Beginner, intermediate, or advanced?
- **Dependencies:** What libraries or hardware required?

### Step 2: Create the Folder

```bash
mkdir -p skills/my-skill-name/scripts
mkdir -p skills/my-skill-name/references
```

### Step 3: Write SKILL.md

Use this template (also in [CONTRIBUTING.md](CONTRIBUTING.md)):

```yaml
---
id: my-skill-name
title: My Skill Title
category: arduino|maker|project-builder
platforms:
  - uno
  - esp32
  - rp2040
whenToUse: |
  When users ask for [specific problem].
---

## Overview
Clear, concise description.

## Core Principles
1. Why this approach works
2. Design decisions

## Implementation
Complete, compile-ready code.

## Verification Steps
✅ Expected output
❌ Common mistakes

## Common Pitfalls
- Issue 1
- Issue 2

## Advanced Patterns
Extension ideas.

## Engineering Rationale
Technical deep-dive.

## Integration Notes
How this works with other skills.

## References
Datasheets, links, code samples.
```

### Step 4: Add Code Examples

Place working code in `SKILL.md` Implementation section. Ensure:
- ✅ Compiles without warnings
- ✅ Uses `unsigned long` for timing
- ✅ Bounds checking on arrays
- ✅ F() macro on UNO for strings
- ✅ No hardcoded pins (use config.h)

### Step 5: Create Python Scripts (Optional)

If adding automation scripts:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",  # Add dependencies here
# ]
# ///

"""Generate my-skill artifacts."""
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate my-skill code")
    parser.add_argument("--board", choices=["uno", "esp32", "rp2040"], required=True)
    args = parser.parse_args()
    
    print(f"Generating for {args.board}...")
    # Your logic here

if __name__ == "__main__":
    main()
```

**Key points:**
- PEP 723 frontmatter with inline dependencies
- No external `requirements.txt`
- Run with: `uv run script.py` or `python script.py`
- Always include `--help` support

### Step 6: Test Thoroughly

Before submitting:

```bash
# Test code compiles
# Copy code from SKILL.md into Arduino IDE
# Test on each supported platform

# For Python scripts
uv run scripts/generate_example.py --help
python scripts/generate_example.py --board uno
```

### Step 7: Submit a Pull Request

1. Push to your fork: `git push origin skills/my-skill-name`
2. Create PR with title: `feat(skill): my-skill-name — [description]`
3. Complete checklist in [pull_request_template.md](.github/pull_request_template.md)
4. Wait for review and feedback

See [CONTRIBUTING.md](CONTRIBUTING.md#pull-request-workflow) for full details.

## Running Automation Scripts

### Code Generator

Generate Arduino code snippets for common patterns:

```bash
# Interactive mode (prompts for options)
uv run arduino-code-generator/scripts/generate_snippet.py

# Batch mode (specify all options)
uv run arduino-code-generator/scripts/generate_snippet.py \
  --board esp32 \
  --pattern "wifi-state-machine" \
  --output my_sketch.ino

# List supported patterns
uv run arduino-code-generator/scripts/generate_snippet.py --help
```

**Patterns:**
- timer, scheduler, state-machine, adc-filter
- button-debounce, i2c-scanner, csv-logger
- eeprom-manager, wifi, hardware-detect

**Boards:**
- uno (Arduino UNO/Nano, 2KB SRAM)
- esp32 (ESP32, 520KB SRAM)
- rp2040 (RP2040, 264KB SRAM)

### Project Builder

Scaffold complete Arduino projects:

```bash
# Interactive mode
uv run arduino-project-builder/scripts/scaffold_project.py

# Batch mode
uv run arduino-project-builder/scripts/scaffold_project.py \
  --type "environmental-monitor" \
  --board "esp32" \
  --output "my_project"

# List supported types
uv run arduino-project-builder/scripts/scaffold_project.py --help
```

**Project Types:**
- environmental-monitor (sensors + data logging)
- robot-controller (motors + sensors + state machine)
- iot-device (WiFi + cloud communication)

## Design Principles Reference

All code must follow the 3 core rules in [arduino-skills.md](arduino-skills.md):

### Rule 1: Verifiable Output
- Code must produce observable results
- Serial.print/println for text
- LED blinking for visual feedback
- Motor spinning for physical feedback

### Rule 2: Avoid delay() Blocking
- Only non-blocking patterns
- Use millis() for timing
- Use state machines for sequences
- Use event-driven architecture

### Rule 3: Hardware Abstraction
- Pin definitions in config.h, never hardcoded
- Platform-specific code in #ifdef blocks
- Graceful degradation on limited platforms

## Testing Your Changes

### Manual Verification

1. **Code Compilation:**
   ```bash
   # Copy code into Arduino IDE
   # Select board: Tools > Board > [Your Board]
   # Click Verify (Ctrl+R)
   # Expected: "Compilation complete."
   ```

2. **Code Execution:**
   ```bash
   # Upload to board
   # Open Serial Monitor (Tools > Serial Monitor, 9600 baud)
   # Verify output matches expected behavior
   ```

3. **Platform Coverage:**
   - Test on UNO (or document limitation)
   - Test on ESP32 (or document limitation)
   - Test on RP2040 (or document limitation)

### Linting (Optional)

If you have linting tools:

```bash
# YAML validation
yamllint SKILL.md

# Markdown validation
markdownlint SKILL.md

# Python linting
python -m pylint scripts/generate_*.py
```

## Common Development Tasks

### Adding a Skill Variant

To add a new platform variant to an existing skill:

1. Update SKILL.md `platforms:` section
2. Add platform-specific code in #ifdef blocks
3. Test on new platform
4. Update Integration Notes

### Updating Documentation

1. Edit the file directly
2. Test Markdown rendering: `markdownlint file.md`
3. Commit and create PR

### Reporting Issues

Found a bug? Help us improve:

1. Check [existing issues](../../issues)
2. Create new issue using appropriate template
   - [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)
   - [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)
3. Include platform, board, and reproduction steps

## Frequently Asked Questions

**Q: Can I use delay() for timing?**
A: No. Use millis() and state machines instead. delay() blocks all other code.

**Q: What's config.h?**
A: A header file with board-specific pin definitions. Prevents hardcoding pins.

**Q: Do I need to test on all 3 platforms?**
A: Ideally yes. If your skill only works on some platforms, document the limitation clearly.

**Q: Can I use external libraries (e.g., Adafruit)?**
A: Yes, but document in SKILL.md and verify they work on target platforms.

**Q: How do I handle memory constraints on UNO?**
A: Use F() macro for strings, limit arrays, avoid serial prints in loops.

## Resources

- **[README.md](README.md)** — Main project documentation
- **[arduino-skills.md](arduino-skills.md)** — Design principles
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)** — Version history
- **[Arduino Reference](https://www.arduino.cc/reference/)** — Arduino API docs
- **[PlatformIO](https://platformio.org/)** — Alternative IDE with better testing

## Need Help?

- Check existing [issues](../../issues)
- Read [CONTRIBUTING.md](CONTRIBUTING.md#questions)
- Ask in a GitHub [discussion](../../discussions)

---

**Happy developing!** 🚀
