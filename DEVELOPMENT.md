# Development Guide

Welcome! This guide explains how to set up the Arduino Skills workspace, run automation scripts, create skills, and contribute to the project.

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/wedsamuel1230/arduino-skills.git
cd arduino-skills
```

### 2. Install Dependencies

Arduino Skills uses Python automation scripts with `uv` for dependency management.

**Option A: Using uv (Recommended)**
```bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run scripts with uv (no setup required)
uv run skills/arduino-code-generator/scripts/generate_snippet.py --board uno --pattern timer
uv run skills/arduino-project-builder/scripts/scaffold_project.py --type environmental-monitor --board esp32
```

**Option B: Using Python directly**
```bash
python skills/arduino-code-generator/scripts/generate_snippet.py --board uno --pattern timer
python skills/arduino-project-builder/scripts/scaffold_project.py --type environmental-monitor --board esp32
```

### 3. Verify Installation

```bash
# Test code generator
python skills/arduino-code-generator/scripts/generate_snippet.py --help

# Test project builder
python skills/arduino-project-builder/scripts/scaffold_project.py --help

# Validate Agent Skills structure and the shared Arduino workflow contract
python3 scripts/validate_agent_skills.py
python3 scripts/validate_arduino_skill_contract.py
python3 scripts/validate_arduino_plugin.py
python3 scripts/run_arduino_evals.py
git diff --check
```

The forward suite includes `loop-engine-evidence-contract` and the board-support
identity, resolver, routing, and trigger-corpus checks. It currently passes
18/18 cases and validates a complete durable loop state and append-only ledger,
while proving that an incomplete fixture is rejected. This is contract evidence
only; it does not replace user-supplied measurements or target-board tests.

## Workspace Structure

```
arduino-skills/
├── README.md                    # Main documentation
├── CONTRIBUTING.md              # Contribution guidelines
├── DEVELOPMENT.md               # This file
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT license
├── arduino-skills.md            # Design principles & constraints
├── docs/
│   ├── board-support/           # Shared board-family references
│   ├── diagrams/                # Documentation assets
│   ├── research/                # Archived discovery notes
│   └── workflows/               # Archived PRD/plan/test-map artifacts
├── scripts/
│   ├── validate_agent_skills.py # Agent Skills schema validator
│   ├── validate_arduino_skill_contract.py # Cross-skill workflow validator
│   ├── validate_arduino_plugin.py # Plugin, reference, and fixture validator
│   ├── resolve_board_profile.py # Exact board lookup and identity gate
│   └── run_arduino_evals.py     # Deterministic behavioral fixture runner
├── evals/                       # Scenarios, fixtures, results, fresh review
├── references/boards/           # Board-family facts and source links
└── skills/
    ├── arduino-workflow-router/
    ├── arduino-code-generator/
    ├── arduino-project-builder/
    ├── arduino-cli-skill/
    └── ...                      # Each skill owns its own SKILL.md/resources
```

## Plugin Packaging And Evaluation

`skills/` is the only content source of truth. The root `plugin.json`,
`.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/`, marketplace manifests,
and `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` files are host adapters or routing
wrappers. Do not duplicate skill bodies in them. See
[docs/plugin-distribution.md](docs/plugin-distribution.md) for install commands.

For local development, validate the package before publishing:

```bash
python3 scripts/validate_agent_skills.py
python3 scripts/validate_arduino_skill_contract.py
python3 scripts/validate_arduino_plugin.py
python3 scripts/run_arduino_evals.py --output evals/eval-results.json
git diff --check
```

The deterministic suite covers ordered raw pin declarations, ESP32 output-pin
constraints, 5 V-to-3.3 V wiring warnings, blocked physical-world gates,
combined-workflow routing, board selection, non-blocking timing, library and
memory checks, hardware test stages, and structured serial evidence. It does
not prove that a physical board was wired, flashed, measured, or deployed.

When the OpenAI Codex plugin creator is available, run its independent manifest
validator as an additional host check:

```bash
UV_CACHE_DIR=/private/tmp/arduino-skills-uv-cache uv run --no-project --with pyyaml \
  ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

If that local system skill is unavailable, record the omission rather than
claiming Codex manifest validation. Keep fresh-context semantic review results
in `evals/fresh-review.md` and repair only the failed evaluator family.

## Creating a New Skill

### Step 1: Plan Your Skill

Answer these questions:
- **Problem:** What does this skill teach or solve?
- **Exact target:** board/revision, MCU, pins, memory, peripherals, voltage,
  current, protocols, and recovery path?
- **Toolchain:** Arduino IDE, Arduino CLI, PlatformIO, or vendor-specific tool?
- **Versions:** host, framework/board package, compiler, libraries, and upload tool?
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
name: my-skill-name
description: Explain what the skill does and when to use it. Include concrete trigger phrases when helpful.
compatibility: Optional. Include only if the skill has specific runtime or tool requirements.
---
```

Recommended body shape:

- concise overview
- workflow or checklist
- examples
- targeted references to `references/...`, `scripts/...`, or `assets/...`
- verification and failure notes

Use [the shared Arduino skill contract](docs/arduino-skill-contract.md) for
assumptions, required tools and versions, implementation steps, evidence stages,
limitations, recovery, and security. Keep detailed board or toolchain branches
in directly linked references.

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
3. Run the repo-local validator and any affected scripts before opening the PR
4. Wait for review and feedback

See [CONTRIBUTING.md](CONTRIBUTING.md#pull-request-workflow) for full details.

## Running Automation Scripts

### Code Generator

Generate Arduino code snippets for common patterns:

```bash
# Interactive mode (prompts for options)
uv run skills/arduino-code-generator/scripts/generate_snippet.py

# Batch mode (specify all options)
uv run skills/arduino-code-generator/scripts/generate_snippet.py \
  --board esp32 \
  --pattern "wifi-state-machine" \
  --output my_sketch.ino

# List supported patterns
uv run skills/arduino-code-generator/scripts/generate_snippet.py --help
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
uv run skills/arduino-project-builder/scripts/scaffold_project.py

# Batch mode
uv run skills/arduino-project-builder/scripts/scaffold_project.py \
  --type "environmental-monitor" \
  --board "esp32" \
  --output "my_project"

# List supported types
uv run skills/arduino-project-builder/scripts/scaffold_project.py --help
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

1. **Build proof:**
   ```bash
   # Copy code into Arduino IDE
   # Select board: Tools > Board > [Your Board]
   # Click Verify (Ctrl+R)
   # Record the exact target, versions, build flags, and output.
   ```

2. **Upload and hardware proof:**
   ```bash
   # Upload to board
   # Open Serial Monitor (Tools > Serial Monitor, 9600 baud)
   # Verify output matches expected behavior
   ```

3. **System and deployment proof:**
   - Test representative integrated behavior and failure conditions
   - Test update, rollback, and recovery when the device is connected or field deployed
   - Document every unverified stage and exact target limitation

### Linting (Optional)

If you have linting tools:

```bash
# YAML validation
python3 scripts/validate_agent_skills.py
python3 scripts/validate_arduino_skill_contract.py

# Markdown validation
markdownlint SKILL.md

# Python linting
python -m pylint scripts/generate_*.py
```

## Common Development Tasks

### Adding a Skill Variant

To add a new platform variant to an existing skill:

1. Update the `description` and any required support references
2. Add platform-specific code in #ifdef blocks
3. Test on new platform
4. Update Integration Notes

### Updating Documentation

1. Edit the file directly
2. Test Markdown rendering: `markdownlint file.md`
3. Commit and create PR

### Reporting Issues

Found a bug? Help us improve:

1. Check [existing issues](https://github.com/wedsamuel1230/arduino-skills/issues)
2. Open a new issue or discussion with the relevant reproduction details
3. Include platform, board, and reproduction steps

## Frequently Asked Questions

**Q: Can I use delay() for timing?**
A: No. Use millis() and state machines instead. delay() blocks all other code.

**Q: What's config.h?**
A: A header file with board-specific pin definitions. Prevents hardcoding pins.

**Q: Do I need to test on all board families?**
A: No. Test the exact target and toolchain in scope, then document every
unverified board, framework, and proof stage clearly.

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

- Check existing [issues](https://github.com/wedsamuel1230/arduino-skills/issues)
- Read [CONTRIBUTING.md](CONTRIBUTING.md#questions)
- Ask in a GitHub [discussion](https://github.com/wedsamuel1230/arduino-skills/discussions)

---

**Happy developing!** 🚀
