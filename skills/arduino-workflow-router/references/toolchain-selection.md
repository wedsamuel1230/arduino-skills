# Toolchain And Compatibility Selection

Choose a toolchain from the project source of truth and the user's existing
environment. A skill may provide commands for one toolchain, but it must state
that boundary.

| Toolchain | Record before implementation | Typical proof |
|---|---|---|
| Arduino IDE | IDE version, board package, selected board, port, libraries | compile report, upload log, serial output |
| Arduino CLI | CLI version, core index/core version, FQBN, port, libraries | `compile`, `upload`, port and monitor evidence |
| PlatformIO | platform/framework versions, board ID, environment, `platformio.ini` or lock data | environment build, upload log, test/monitor evidence |
| Vendor-specific | SDK/tool version, flash layout, bootloader, probe, signing, recovery utility | vendor build/flash log and device identity |

## Compatibility Checks

- Pin the board package, framework, library, compiler, and upload tool versions
  when reproducibility matters.
- Check the library's supported architectures and transitive dependencies
  against the exact MCU and framework.
- Check API differences before translating an Arduino library to a vendor SDK or
  RTOS environment.
- Check memory map, partition, bootloader, and signing assumptions before upload.
- Keep toolchain-specific commands in separate branches; do not present one
  command as universal.
- Record the exact source revision, build flags, FQBN/environment, and image hash
  for any uploaded artifact.

## Safe Defaults

Prefer a dry-run, compile-only, or device discovery command before flashing.
Capture logs without tokens, Wi-Fi passwords, certificates, or private keys.
When versions are unknown, report the compatibility risk and ask for the
version output rather than installing or upgrading silently.
