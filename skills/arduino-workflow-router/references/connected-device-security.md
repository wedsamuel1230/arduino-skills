# Connected Device Security And Maintenance

Apply this reference to Wi-Fi, BLE, Ethernet, radio, USB-controlled, or
field-updateable devices. Security advice must match the board's actual
hardware and framework capabilities.

## Minimum Controls

- Keep API keys, Wi-Fi passwords, certificates, private keys, and signing keys
  out of source, examples, serial logs, crash dumps, and committed config.
- Use environment/config injection with redaction and least privilege; rotate
  secrets and credentials through an explicit operational procedure.
- Prefer signed firmware, authenticated transport, secure boot, protected
  storage, and rollback when the target supports them. State which controls are
  unavailable instead of implying they exist.
- Pin and review dependencies, record versions and provenance, and generate a
  component inventory or SBOM for releases where practical. Record each
  dependency explicitly in the release notes.

## Updates And Recovery

Define image identity, compatibility rules, staged rollout, health check,
watchdog behavior, failure timeout, rollback, physical recovery, and a stop
condition for unsafe updates. Test update failure and power loss, not only the
happy path.

## Maintainability And End Of Life

Keep a changelog, reproducible build inputs, board/toolchain versions, pin map,
configuration schema, diagnostic procedure, and owner. Define vulnerability
response, update support duration, credential revocation, data deletion, and
device decommissioning. Do not call a device production-ready without naming
these operational boundaries.
