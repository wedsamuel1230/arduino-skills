# Arduino Skills Refinement Tests Map

## Contract Coverage

- Intent: ensure the review comment is represented by observable repository
  structure and not only by prose.
- Check: `python3 scripts/validate_arduino_skill_contract.py`
- Expected: 8/8 review themes pass and every active skill links the shared
  output contract.

## Agent Skills Conformance

- Intent: prevent frontmatter and progressive-disclosure drift.
- Check: `python3 scripts/validate_agent_skills.py`
- Expected: 0 errors and 0 warnings.

## Forward Prompt Contract Cases

1. "Build a battery-powered ESP32 sensor node in PlatformIO, then add secure
   OTA updates and a recovery plan."
   - Expected routing: board/toolchain intake, datasheet, power, builder,
     generator, build/upload evidence, OTA, security, maintenance.
2. "My Uno R4 WiFi compiles but upload intermittently fails and the board
   disappears from the serial port."
   - Expected routing: board-family caveat, CLI/IDE discovery, serial, error,
     power/USB checks, boot recovery, and explicit proof-stage separation.
3. "Create a multi-board I2C sensor sketch that works in Arduino IDE or
   PlatformIO, but do not assume pins or voltage."
   - Expected routing: board profile first, datasheet and I2C bringup, code
     generation, toolchain-specific build instructions, limitations.
4. "Design the firmware, power budget, enclosure, and deployment checklist for
   a connected robot controller."
   - Expected routing: combined workflow with builder, power, circuit, code,
     serial, enclosure, OTA, security, and maintenance.

The cases are declared in `evals/evals.json` and consumed by
`scripts/run_arduino_evals.py`. The local harness validates the prompt, expected
route, route precedence, required output-contract sections, and fixture-backed
behavior for every assertion. It is deliberately not presented as a model
invocation; `evals/fresh-review.md` is the independent semantic evaluation.

## Documentation Checks

- Confirm README, `arduino-skills.md`, CONTRIBUTING, and DEVELOPMENT mention the
  router and all four toolchain families.
- Confirm every referenced file exists.
- Confirm the largest active SKILL.md remains below 500 lines.
- Confirm every active frontmatter includes `metadata.triggers`.
- Confirm every board profile has a fact-to-source map and the source ledger is
  current for the checked date.
