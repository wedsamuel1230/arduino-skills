# Arduino CLI Commands Reference

Basic `arduino-cli` commands commonly used in automation and agent-driven workflows.

## Board discovery

- List all installed boards:

  arduino-cli board list --format json

- List all available platforms and cores:

  arduino-cli core search
  arduino-cli core update-index

## Library management

- Search for a library:

  arduino-cli lib search "WiFi"

- Install a library:

  arduino-cli lib install "Adafruit Unified Sensor"

- List installed libraries:

  arduino-cli lib list

## Compile and upload

- Compile a sketch for a board FQBN:

  arduino-cli compile --fqbn arduino:avr:uno /path/to/sketch

- Upload to a port:

  arduino-cli upload -p COM3 --fqbn arduino:avr:uno /path/to/sketch

## Validation notes

- These command forms are stable across recent arduino-cli releases. For authoritative and up-to-date syntax consult the official reference: https://arduino.github.io/arduino-cli/latest/commands/arduino-cli
- Verify your installed CLI version before running scripts: `arduino-cli version`.
- If you rely on machine-readable output in scripts, prefer `--format json` when available and confirm the CLI version supports it.

## Additional flags

- Use `--format json` on list commands for machine-readable output.
- Use `--verify` to only compile and check without producing an upload.
