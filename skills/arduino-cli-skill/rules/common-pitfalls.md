# Common Pitfalls & Best Practices

- Do not hardcode device paths (COM3, /dev/ttyACM0) — detect ports at runtime or allow user override.
- Prefer `--format json` for programmatic parsing of `arduino-cli` output.
- Document minimum arduino-cli version required for specific flags.
- On Linux, prefer `/dev/serial/by-id` when available for stable device identifiers.
