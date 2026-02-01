# Examples — Arduino CLI Workflows

This folder contains concise, production-ready command sequences for common Arduino CLI workflows.

## Windows PowerShell — Detect board and upload

```powershell
# 1. Detect COM ports
Get-PnpDevice -Class Ports | Where-Object { $_.FriendlyName -match 'COM' }

# 2. Compile
arduino-cli compile --fqbn arduino:avr:uno C:\path\to\sketch

# 3. Upload (replace COM3 with detected port)
arduino-cli upload -p COM3 --fqbn arduino:avr:uno C:\path\to\sketch
```

## Linux — Use stable serial by-id

```bash
# List devices
ls -l /dev/serial/by-id

# Compile
arduino-cli compile --fqbn arduino:avr:uno /home/user/sketch

# Upload (use /dev/serial/by-id/…)
arduino-cli upload -p /dev/serial/by-id/usb-... --fqbn arduino:avr:uno /home/user/sketch

## Notes

- Replace the sketch path with your local project folder.
- Prefer stable `/dev/serial/by-id` paths on Linux to avoid port changes between reboots.
- For scripted workflows, consider `arduino-cli ... --format json` for machine-readable output.
```
