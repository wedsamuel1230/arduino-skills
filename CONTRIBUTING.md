# Contributing to Arduino Skills

Thank you for your interest in contributing to Arduino Skills! This repository provides professional Arduino/embedded systems skills for educational use. Contributions should focus on creating high-quality, well-tested skills that follow our design principles.

## Before You Start

**Read the Design Principles First:**
- [arduino-skills.md](arduino-skills.md) — Core rules, platform support, code quality standards

**Understand the Skill Framework:**
- [README.md](README.md#how-skills-work) — Skill structure and Agent Skills
- Examine an existing skill folder (for example, `skills/battery-selector/`) for reference
- [docs/plugin-distribution.md](docs/plugin-distribution.md) — Host packaging and install commands

**Use the creator guidance when changing the skill surface:**
- The Agent Skills `skill-creator` guidance informs concise frontmatter, progressive
  disclosure, and fresh-context forward testing.
- The Codex `plugin-creator` guidance informs `.codex-plugin/plugin.json`, marketplace
  policy fields, and manifest validation.
- `skills-lock.json` records the creator companions used for this repository:
  `anthropics/skills@skill-creator`, `openai/skills@cli-creator`, and
  `openai/skills@plugin-creator`.

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
└── assets/               # Optional: Output assets and templates
```

Do not add a per-skill `README.md` or installation guide unless a packaging
consumer explicitly requires it; keep activation guidance in `SKILL.md` and
load-on-demand detail in `references/`, `scripts/`, or `assets/`.

### 2. Write Your SKILL.md

Every skill requires YAML frontmatter + body.

```yaml
---
name: skill-name
description: Explain what the skill does and when to use it. Include likely trigger phrases and problem types.
compatibility: Optional. Mention product, runtime, or tool requirements only when needed.
---
```

Recommended body shape:

- short overview
- task-oriented workflow or checklist
- targeted examples
- explicit references to `references/...`, `scripts/...`, or `assets/...`
- verification notes and common failure cases

Authoring rules:

- `name` must match the skill directory name
- keep `SKILL.md` focused and move bulk detail into `references/`, `scripts/`,
  or `assets/`
- avoid legacy top-level keys like `id`, `title`, `category`, `platforms`, and
  `whenToUse`
- use shallow relative file references from the skill root

### Universal Embedded Workflow Contract

For board-dependent skills, use [the shared contract](docs/arduino-skill-contract.md)
and [board profile](docs/board-support/board-profile-template.md). Name the
exact board/revision, framework, pins, memory, peripherals, voltage/current,
protocols, host, and versions before giving implementation advice. Support
Arduino IDE, Arduino CLI, PlatformIO, or vendor-specific tools only when the
branch and compatibility boundary are explicit.
For combined firmware, electronics, power, networking, enclosure, or deployment
work, start with `embedded-project-loop` when the task is physical or spans
sessions, then use `arduino-workflow-router` and load specialists on demand.

Every response must distinguish build, upload, hardware, system, and
deployment proof. Include assumptions, required tools and versions,
implementation steps, tests/evidence, known limitations, and recovery/security
notes. Never put secrets in source, examples, generated configuration, or logs.

### Plugin Source And Distribution

Keep all skill content under `skills/`; do not copy `SKILL.md` files into
`.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/`, or host wrapper files.
Update the provider adapter only when its manifest schema requires it, then
validate every host surface. The supported install paths are documented in
[docs/plugin-distribution.md](docs/plugin-distribution.md), including:

- `npx skills add wedsamuel1230/arduino-skills` for the complete shared tree
- `npx skills add wedsamuel1230/arduino-skills --skill pin-assignment` for one skill
- the local Codex, Claude Code, and Cursor plugin adapters

Do not add a second skill when an existing skill already owns the trigger. For
example, structured serial runtime debugging belongs to `arduino-serial-monitor`.
Record deliberate deduplication or host-schema conflicts in `CHANGELOG.md`.

### 3. Checklist Before Submitting

**Code Quality:**
- [ ] Code compiles without warnings (Arduino IDE or PlatformIO)
- [ ] Uses `unsigned long` for millis() timing
- [ ] Bounds checking on all arrays
- [ ] F() macro for string constants on UNO
- [ ] No hardcoded pins (use config.h pattern)
- [ ] Memory-safe (no buffer overflows)

**Documentation:**
- [ ] `name` and `description` are present and valid
- [ ] `name` matches the skill folder name
- [ ] No legacy top-level frontmatter keys remain
- [ ] `SKILL.md` stays focused and loads details on demand
- [ ] Code examples include comments where they add real value

**Testing (Platforms):**
- [ ] Tested on the exact target (or documented limitation)
- [ ] Board profile covers pins, memory, peripherals, voltage, current, and protocols
- [ ] Toolchain and library versions are recorded
- [ ] Build, upload, hardware, and system evidence are labeled separately
- [ ] Recovery path is documented for upload, boot, power, or firmware faults
- [ ] Platform and toolchain support boundaries are clear in SKILL.md
- [ ] Physical or multi-session workflows use `embedded-project-loop` as the
      first entry and preserve one next todo plus an evidence gate

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
   - Test on the exact target or document the limitation
   ```

3. **Create a Pull Request** with:
   - Title: `feat(skill): my-skill-name — [short description]`
   - Description:
     ```markdown
     ## Skill: My Skill Name
     
     **Category:** arduino | maker | project-builder
     **Target and toolchain:** [exact board/revision, framework, IDE/CLI/PlatformIO/vendor tool]
     
     **Solves:** [Problem statement]
     
     **Verification:**
     - [ ] Compiles without warnings
     - [ ] Tested on the exact target or limitation documented
     - [ ] Evidence stages are labeled and reproducible
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

- Use the repo-local validator to check active skill conformance:
  ```bash
  python3 scripts/validate_agent_skills.py
  python3 scripts/validate_arduino_skill_contract.py
  python3 scripts/validate_arduino_plugin.py
  python3 scripts/run_arduino_evals.py
  git diff --check
```

The evaluation suite must include a loop-engine case with both a valid durable
state/ledger fixture and an invalid fixture that is rejected fail-closed.

- Use **markdownlint** for Markdown consistency:
  ```bash
  markdownlint SKILL.md
  ```

- Keep lines ≤100 characters when practical
- Use consistent heading hierarchy (#, ##, ###)
- Use relative links for in-repo skill references

## Design Principles Reference

From [arduino-skills.md](arduino-skills.md):

### Core Rules
1. **Verifiable Output** — Code output must be observable (Serial.print, LED, motor spin)
2. **Avoid delay() Blocking** — Non-blocking patterns only (millis(), state machines)
3. **Hardware Abstraction** — Pin definitions in config.h, not hardcoded
4. **Universal Intake** — Record board, pins, memory, peripherals, voltage/current, protocols, toolchain, and versions
5. **Evidence Separation** — Compile, upload, hardware, system, and deployment proof are distinct

### Reference Hardware
- **Arduino UNO:** 2 KB SRAM, 32 KB Flash
- **ESP32:** 520 KB SRAM, WiFi/BLE/RTOS
- **RP2040:** 264 KB SRAM, Dual-core

All skills must document exact target and toolchain support, compatibility
versions, known limitations, and recovery or security boundaries.

### Code Quality

- No warnings on Arduino IDE compile
- Memory-safe (bounds checking)
- Timing-safe (unsigned long, not delay())
- Pin-safe (config.h, not hardcoded)

## Questions?

- **Existing issues:** Search [GitHub Issues](https://github.com/wedsamuel1230/arduino-skills/issues)
- **Feature requests:** Open a [new issue](https://github.com/wedsamuel1230/arduino-skills/issues/new)
- **Design questions:** Use [GitHub Discussions](https://github.com/wedsamuel1230/arduino-skills/discussions) or file an issue with a clear design question

## License

By contributing, you agree that your code will be licensed under the **MIT** license, consistent with the rest of this repository.

---

**Thank you for contributing to Arduino Skills!** 🎓
