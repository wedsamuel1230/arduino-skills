# Serial Port Detection (Cross-platform)

This reference lists commands to detect serial/COM ports on Windows, macOS, and Linux. Use these before running `arduino-cli upload`.

## Windows (PowerShell)

- List PnP devices with friendly name containing "COM":

  Get-PnpDevice -Class Ports | Where-Object { $_.FriendlyName -match 'COM' }

- WMI query (alternative):

  Get-WmiObject Win32_SerialPort | Select-Object DeviceID, Description

## Linux (bash)

- List tty devices:

  ls -l /dev/ttyUSB* /dev/ttyACM* /dev/serial/by-id || true

- Use udevadm to query properties:

  udevadm info -q all -n /dev/ttyACM0

## macOS (bash)

- List USB serial devices:

  ls /dev/tty.usb* /dev/cu.usb* || true

## Tips

- Use `arduino-cli board list --format json` to get arduino-cli's view of connected boards and ports.
- When scripting, prefer `/dev/serial/by-id` on Linux for stable identifiers.
