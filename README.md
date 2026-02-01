# arduino-skills

![Status](https://img.shields.io/badge/version-1.2.0-blue)
![Skills](https://img.shields.io/badge/skills-21%20complete-brightgreen)
![Platform](https://img.shields.io/badge/platform-Arduino%20|%20ESP32%20|%20RP2040-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Marketplace](https://img.shields.io/badge/marketplace-claude%20%26%20gemini-orange)

> Professional Arduino/embedded systems skills and maker tools for development, education, and prototyping.  
> **v1.2.0:** Added arduino-serial-monitor skill for enhanced debugging with real-time monitoring, data logging, and error detection. Comprehensive project development workflow with board-specific considerations, integration checklist, and quality standards.

## 📋 Table of Contents

- [arduino-skills](#arduino-skills)
  - [📋 Table of Contents](#-table-of-contents)
  - [🔍 Overview](#-overview)
  - [🤖 How Skills Work](#-how-skills-work)
  - [📦 Installation](#-installation)
    - [📍 Marketplace Configuration](#-marketplace-configuration)
    - [Claude Code](#claude-code)
    - [Google Gemini CLI](#google-gemini-cli)
    - [VS Code Copilot](#vs-code-copilot)
  - [🚀 Quick Start](#-quick-start)
    - [Generate Code Snippets](#generate-code-snippets)
    - [Scaffold Complete Projects](#scaffold-complete-projects)
  - [🔧 Arduino Core Skills](#-arduino-core-skills)
    - [Pattern Relationships](#pattern-relationships)
  - [🛠️ Maker Tools](#️-maker-tools)
    - [Tool Scripts](#tool-scripts)
  - [🏗️ Project Builders](#️-project-builders)
    - [Code Generator Workflow](#code-generator-workflow)
    - [Project Builder Workflow](#project-builder-workflow)
  - [📱 Platform Support](#-platform-support)
    - [Board-Specific Optimization](#board-specific-optimization)
  - [🏛️ Architecture](#️-architecture)
    - [Directory Structure](#directory-structure)
    - [Marketplace Configuration](#marketplace-configuration)
    - [Design Principles](#design-principles)
  - [🤝 Contributing](#-contributing)
    - [Quick Submission Checklist](#quick-submission-checklist)
  - [📖 Documentation](#-documentation)
  - [📄 License](#-license)
  - [📋 Changelog](#-changelog)

---

## 🔍 Overview

This collection provides **21 production-ready skills** for Arduino and maker projects:

- **11 Arduino Core Skills** - Hardware patterns, timing, communication, FreeRTOS
- **10 Maker Tools** - Debugging, serial monitoring, BOM generation, power planning, documentation, diagrams
- **2 Project Builders** - Code generation and project scaffolding with automation scripts

All skills follow a consistent structure with:
- ✅ Copy-paste ready code that compiles without warnings
- ✅ Verification steps with expected outputs
- ✅ Common pitfalls with corrections
- ✅ Engineering rationale explaining "why"

---

## 🤖 How Skills Work

**arduino-skills** uses the **Agent Context Protocol (ACP)** — a standard for self-contained, interoperable skill packages for AI/ML agents. Each skill is a folder containing:

- **SKILL.md** — Instructions with YAML frontmatter (name, description, trigger conditions)
- **scripts/** — Python automation tools with PEP 723 inline dependencies
- **references/** — Code examples, patterns, and templates
- **assets/** — Diagrams, datasheets, and resources


---

## 📦 Installation

| Agent | Setup | Marketplace | Docs |
|-------|-------|-------------|------|
| **Claude Code** | `/plugin marketplace add arduino-skills` | ✅ Configured (v1.2.0) | [Docs](https://code.claude.com/docs/en/skills) |
| **Google Gemini CLI** | `gemini extensions install` | ✅ Converted (11 extensions) | [Docs](https://geminicli.com/docs/) |
| **VS Code Copilot** | Copy to `.github/skills/` folder | ⚠️ Manual setup | [Docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills) |

### 📍 Marketplace Configuration

All skills include marketplace metadata for discovery and installation:
- **Claude Code:** `.claude-plugin/marketplace.json` — Enables `/plugin marketplace search` discovery
- **Gemini CLI:** `gemini-extension.json` — Auto-generated from skill-porter conversion (see `d:/projects/gemini-extensions/`)

Each marketplace file includes:
- ✅ Skill name and description (50+ characters)
- ✅ Version (1.2.0), license (MIT), and category tags
- ✅ Plugin metadata for discovery
- ✅ Compatible with skill-porter universal conversion tool

### Claude Code

**Requirements:** `marketplace.json` present in each skill's `.claude-plugin/` directory

```bash
# Register marketplace
/plugin marketplace add arduino-skills

# Install a skill (auto-discovers all 11)
/plugin install arduino-code-generator@arduino-skills

# Search available skills
/plugin search arduino
```

**What's configured:**
- ✅ All skills have marketplace metadata
- ✅ Descriptions, tags, license, and version included
- ✅ Ready for official marketplace publication

### Google Gemini CLI

**Requirements:** Gemini extensions generated via skill-porter conversion (at `d:/projects/gemini-extensions/`)

```bash
# Install from local directory
gemini extensions install ./gemini-extensions/arduino-code-generator --consent

# Install from GitHub
gemini extensions install https://github.com/yourusername/arduino-skills/tree/main/gemini-extensions/arduino-code-generator --consent

# List installed extensions
gemini extensions list
```

**What's included:**
- ✅ 11 Gemini CLI extensions (auto-generated from skill-porter)
- ✅ Universal `gemini-extension.json` manifest format
- ✅ Full compatibility with Gemini's extension system

**Note on Multi-Platform Support:** This repository uses [skill-porter](https://github.com/jduncan-rva/skill-porter) to automatically convert between Claude SKILL.md and Gemini extension.json formats. Both versions are kept in sync.

### VS Code Copilot

Enable the chat.useAgentSkills setting to use Agent Skills

**Copy skill folder to extensions directory:**
```bash
mkdir -p .github/skills
cp -r arduino-code-generator .github/skills/arduino-code-generator
```

VS Code supports two locations:
- **Recommended:** `~/.github/skills/` (shared location)
- **Legacy:** `~/.claude/skills/` (backward compatible)

---

## 🚀 Quick Start

### Generate Code Snippets

```bash
# List available patterns
uv run arduino-code-generator/scripts/generate_snippet.py --list

# Generate I2C scanner for ESP32
uv run arduino-code-generator/scripts/generate_snippet.py --pattern i2c --board esp32

# Interactive mode
uv run arduino-code-generator/scripts/generate_snippet.py --interactive
```

### Scaffold Complete Projects

```bash
# List project types
uv run arduino-project-builder/scripts/scaffold_project.py --list

# Create environmental monitor for ESP32
uv run arduino-project-builder/scripts/scaffold_project.py \
    --type environmental --board esp32 --name "WeatherStation"

# Interactive mode
uv run arduino-project-builder/scripts/scaffold_project.py --interactive
```

---

## 🔧 Arduino Core Skills

| Pattern | Path | Description |
|-------|------|-------------|
| Button Debouncing | `arduino-code-generator/` | Software debouncing with press/release/long-press detection |
| Config Management | `arduino-code-generator/` | Multi-board hardware abstraction with conditional compilation |
| CSV Output | `arduino-code-generator/` | Structured data logging for Serial/SD/Excel analysis |
| Data Logging | `arduino-code-generator/` | EEPROM with CRC, SD card CSV, wear leveling |
| ADC Filtering | `arduino-code-generator/` | Moving average, median, and Kalman filters for noisy sensors |
| Hardware Detection | `arduino-code-generator/` | Auto-detect boards, sensors, adaptive configuration |
| I2C Communication | `arduino-code-generator/` | Device scanning, address detection, bus diagnostics |
| Non-blocking Scheduler | `arduino-code-generator/` | millis()-based timing, priority task scheduling |
| State Machine | `arduino-code-generator/` | Enum-based FSM for complex behavior control |

### Pattern Relationships

```mermaid
%%{init: {
  "theme": "neutral",
  "themeVariables": {
    "primaryColor": "#df9696ff",
    "primaryTextColor": "#0f8cf3ff",
    "lineColor": "#4A77B5"
  }
}}%%
mindmap
  root((Arduino Patterns))
    Hardware
      Config Management
      Hardware Detection
      I2C Communication
    Input
      Button Debouncing
      ADC Filtering
    Timing
      Non-blocking Scheduler
      State Machine
    Output
      CSV Output
      Data Logging
    Projects
      Environmental Monitor
      Robot Controller
      IoT Device
```

---

## 🛠️ Maker Tools

| Skill | Path | Description |
|-------|------|-------------|
| Circuit Debugger | `circuit-debugger/` | 5-phase hardware debugging with multimeter guide |
| Error Explainer | `error-message-explainer/` | Compiler error interpretation with fixes |
| BOM Generator | `bom-generator/` | Bill of materials with supplier links, Excel export |
| Power Calculator | `power-budget-calculator/` | Current draw estimation, battery sizing |
| Battery Selector | `battery-selector/` | Chemistry comparison, charging solutions |
| Enclosure Designer | `enclosure-designer/` | OpenSCAD parametric templates, 3D print settings |
| README Generator | `readme-generator/` | Professional GitHub documentation |
| Code Review | `code-review-facilitator/` | 8-category review, code smell detection |
| Datasheet Interpreter | `datasheet-interpreter/` | PDF spec extraction from URLs |
| **Serial Monitor** | `arduino-serial-monitor/` | Enhanced serial debugging with real-time monitoring, data logging, filtering, and error detection |
| **Mermaid Generator** | `mermaid-diagram-generator/` | Visual documentation: state machines, timing, FreeRTOS |
| **Serial Monitor** | `arduino-serial-monitor/` | Real-time monitoring, data logging, filtering, and pattern matching for debugging |

### Tool Scripts

All tools include Python scripts with PEP 723 inline dependencies:

```bash
# Serial monitoring with filtering and error detection
uv run arduino-serial-monitor/scripts/monitor_serial.py --port COM3 --detect-errors

# Power budget calculation
uv run power-budget-calculator/scripts/calculate_power.py --interactive

# BOM generation to Excel
uv run bom-generator/scripts/generate_bom.py --output bom.xlsx

# Extract specs from datasheet PDF
uv run datasheet-interpreter/scripts/extract_specs.py \
    --url "https://example.com/sensor-datasheet.pdf"
```

---

## 🏗️ Project Builders

### Code Generator Workflow

```mermaid
flowchart TD
    A["User Request: Generate Arduino Code"] --> B{"Pattern Type?"}
    
    B -->|config| C1["patterns-config.md"]
    B -->|buttons| C2["patterns-buttons.md"]
    B -->|i2c| C3["patterns-i2c.md"]
    B -->|other| C4["..."]
    
    C1 & C2 & C3 & C4 --> D["Template Engine generate_snippet.py"]
    
    D --> E{"Board Type?"}
    
    E -->|Arduino UNO| F1["2KB SRAM 9600 baud"]
    E -->|ESP32| F2["520KB SRAM WiFi/BLE"]
    E -->|RP2040| F3["264KB SRAM Dual-core"]
    
    F1 & F2 & F3 --> G["Generated .ino Code"]
```

### Project Builder Workflow

```mermaid
flowchart TD
    A["📋 Requirements"] --> B["🔧 Hardware Inventory"]
    B --> C["🎯 Board Selection"]
    C --> D{"Project Type?"}
    
    D -->|Environmental| E1["DHT22, Light, Logging, SD Card"]
    D -->|Robot| E2["Ultrasonic, Motors, Servo"]
    D -->|IoT| E3["BME280, WiFi, MQTT"]
    
    E1 & E2 & E3 --> F["📦 Pattern Assembly scaffold_project.py"]
    
    F --> G["📁 Project Structure"]
    
    G --> H1["src/config.h"]
    G --> H2["src/main.ino"]
    G --> H3["platformio.ini"]
    G --> H4["README.md"]
    
    H1 & H2 & H3 & H4 --> I["✅ Complete Project"]
```

---

## 📱 Platform Support

| Platform | SRAM | Features | Skills Supported |
|----------|------|----------|------------------|
| **Arduino UNO/Nano** | 2KB | Basic I/O, ADC | All (with F() macro) |
| **ESP32** | 520KB | WiFi, BLE, dual-core, FreeRTOS | All + IoT projects |
| **RP2040 (Pico)** | 264KB | Dual-core, PIO, USB host | All (no WiFi unless Pico W) |

### Board-Specific Optimization


|Arduino UNO (2KB)     |ESP32 (520KB)       |RP2040(264KB)   |
|----------------------|--------------------|----------------|
| F() for strings      | WiFi/BLE patterns  | Multicore tasks|
| Small buffers        | FreeRTOS tasks     | PIO for timing |
| Avoid String class   | Large JSON buffers | USB host mode  |
| 9600 baud            | 115200 baud        | 115200 baud    |


---

## 🏛️ Architecture

### Directory Structure

```
skills/
├── arduino-code-generator/           # Code snippet generation
│   ├── SKILL.md
│   ├── .claude-plugin/
│   │   └── marketplace.json          # Claude marketplace config (v1.2.0)
│   ├── references/                   # 9 pattern files
│   └── scripts/generate_snippet.py
│
├── arduino-project-builder/          # Project scaffolding
│   ├── SKILL.md
│   ├── .claude-plugin/
│   │   └── marketplace.json          # Claude marketplace config (v1.2.0)
│   ├── references/                   # 3 project templates
│   └── scripts/scaffold_project.py
│
├── arduino-serial-monitor/           # Serial debugging tool (NEW v1.2.0)
│   ├── SKILL.md
│   └── scripts/monitor_serial.py     # Real-time monitoring & logging
│
├── [arduino-*]/                      # Core skills (9 folders)
│   └── .claude-plugin/
│       └── marketplace.json          # Claude marketplace config (v1.2.0)
│
├── [maker-tools]/                    # Maker tools (10 folders)
│   ├── .claude-plugin/
│   │   └── marketplace.json          # Claude marketplace config (v1.2.0)
│   └── scripts/*.py                  # Automation scripts
│
├── gemini-extensions/                # Gemini CLI extensions (v1.2.0)
│   └── [skill-name]/
│       ├── gemini-extension.json
│       └── GEMINI.md
│
├── docs/
│   └── diagrams/                     # Mermaid diagram sources
│
└── memory-bank/                      # Project tracking
    ├── projectbrief.md
    ├── activeContext.md
    └── SESSION.md
```

### Marketplace Configuration

**v1.2.0 Feature Release:** All 21 skills include marketplace metadata for discovery on Claude Code and Gemini CLI. arduino-code-generator includes 9 production-ready example sketches with comprehensive documentation. New arduino-serial-monitor skill added for enhanced debugging with real-time monitoring, data logging, and error detection.

Each skill's `.claude-plugin/marketplace.json` includes:
```json
{
  "name": "skill-name",
  "metadata": {
    "description": "Full skill description (50+ characters)",
    "version": "1.2.0",
    "license": "MIT",
    "author": "arduino-skills contributors",
    "tags": ["arduino", "embedded-systems", "..."],
    "category": "embedded-systems | maker-tools"
  },
  "plugins": [
    {
      "name": "skill-name",
      "description": "Brief one-liner for discovery",
      "enabled": true
    }
  ]
}
```

**Multi-Platform Conversion:** Gemini extensions are auto-generated from these marketplace files using [skill-porter](https://github.com/jduncan-rva/skill-porter), which transforms:
- Claude `SKILL.md` → Gemini `gemini-extension.json`
- `allowed-tools` (whitelist) → `excludeTools` (blacklist)
- YAML metadata → JSON manifest

Both versions are validated and kept in sync via CI/CD.

### Design Principles

All skills follow these rules from `arduino-skills.md`:

1. **Verifiable Output** - Every example includes test procedures and expected results
2. **Avoid delay() Blocking** - Use `millis()` and state machines for timing
3. **Hardware Abstraction** - All board-specific code in `config.h` with `#if defined()`

---

## 🤝 Contributing

We welcome contributions! Before you start, please read:

- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Skill submission process, code quality checklist, pull request workflow
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** — Community standards and expectations
- **[DEVELOPMENT.md](DEVELOPMENT.md)** — Setup guide, skill creation walkthrough, automation scripts

### Quick Submission Checklist

- [ ] Compiles without warnings on Arduino IDE
- [ ] Uses `unsigned long` for millis() timing
- [ ] Bounds checking on all arrays
- [ ] F() macro for string constants on UNO
- [ ] No hardcoded pins (use config.h)
- [ ] SKILL.md has complete sections and YAML frontmatter
- [ ] Tested on Arduino UNO, ESP32, RP2040 (or documented limitation)

See [CONTRIBUTING.md](CONTRIBUTING.md#submitting-a-new-skill) for the complete process.

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Main project documentation (this file) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Skill submission guidelines and checklist |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Setup, skill creation, automation scripts |
| [SECURITY.md](SECURITY.md) | Security vulnerability reporting |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards |
| [arduino-skills.md](arduino-skills.md) | Design principles and constraints |
| [CHANGELOG.md](CHANGELOG.md) | Version history and release notes |

---

## 📄 License

These skills are provided under the **MIT** license.  
Suitable for development, research, and prototyping.
See [LICENSE](LICENSE) for details.

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for the complete version history and release notes.

---
