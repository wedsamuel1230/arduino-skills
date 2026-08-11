---
name: arduino-cli-skill
description: Use when users need Arduino CLI commands for board discovery, library installation, compilation, upload, or serial-port troubleshooting on Windows, macOS, or Linux. Use it as the CLI branch of a broader workflow when the project also involves Arduino IDE, PlatformIO, vendor tools, hardware, power, or deployment.
metadata: {triggers: "Arduino CLI, board discovery, compile, upload, serial port"}
---

# Arduino CLI Skill

Provide cross-platform `arduino-cli` workflows and command references.

## Resources

- `references/commands.md` - board, core, library, compile, and upload commands
- `references/serial-ports.md` - OS-specific serial port discovery
- `rules/common-pitfalls.md` - common command mistakes and recovery guidance
- `examples/README.md` - runnable command sequences
- `../../docs/board-support/uno-r4-family.md` - Uno R4 Minima and Uno R4 WiFi support notes

## Workflow

1. Identify the user's platform and target board.
2. Open `references/serial-ports.md` if the task depends on port discovery.
3. Open `references/commands.md` for the exact command family you need.
4. Check `rules/common-pitfalls.md` before suggesting upload or compile fixes.
5. If the target is Uno R4 family and the problem touches WiFi, firmware bridge,
   or OTA-related setup, open `../../docs/board-support/uno-r4-family.md`.
6. Prefer `arduino-cli` JSON output when the result will be parsed or reused.

## Compatibility And Proof Boundary

Record `arduino-cli version`, the core/index version, FQBN, libraries, host OS,
and port before changing commands. Check library architecture support and board
package compatibility. A successful `compile` is build proof only; an accepted
upload is upload proof and does not establish hardware or system success. For
IDE, PlatformIO, or vendor-specific commands, route to the appropriate branch
instead of silently translating them.

## Quick Start

```bash
arduino-cli board list
arduino-cli core list
arduino-cli compile --fqbn arduino:avr:uno path/to/sketch
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno path/to/sketch
```

## Verification

- Confirm the `fqbn` matches the target board.
- Confirm the selected serial port exists before upload.
- Prefer command output over remembered defaults when troubleshooting.

See `references/commands.md` and `references/serial-ports.md` for detailed examples.

## Shared Output Contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
