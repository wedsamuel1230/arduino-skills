---
name: arduino-serial-monitor
description: Read and analyze Arduino or embedded serial output for structured runtime debugging across Arduino IDE, Arduino CLI, PlatformIO, and vendor-specific monitor tools. Use when boot output, sensor data, resets, communication failures, timing symptoms, or field behavior need evidence rather than compile-only reasoning.
metadata:
  triggers: "serial monitor, runtime logs, boot output, reset reason, sensor logs, structured debug, field symptoms"
  attribution: "Refined from the existing Arduino serial monitor skill; no separate serial-debugging skill is installed."
---

# Arduino Serial Monitor

This skill provides advanced tools for reading and analyzing serial monitor data from Arduino boards, enhancing the debugging experience beyond the basic Arduino IDE serial monitor.

## Features

- **Real-time Serial Monitoring**: Connect to Arduino serial ports and display data in real-time
- **Data Logging**: Save serial output to files with timestamps for later analysis
- **Filtering & Pattern Matching**: Filter output by keywords, regex patterns, or data types
- **Error Detection**: Automatically highlight common error patterns and warnings
- **Multiple Format Support**: Handle different data formats (text, JSON, CSV, binary)
- **Cross-platform**: Works with Windows, macOS, and Linux serial ports

## Structured Debugging Workflow

1. Record the exact board/revision, firmware/image identifier, toolchain and
   versions, port, baud, reset cause if known, and timestamp source.
2. Prefer one line per event with stable fields such as
   `t_ms=123 level=INFO event=sensor_read value=...`; keep secrets and tokens
   out of output.
3. Capture the unfiltered log before filtering. Preserve the first boot lines,
   reset/brownout/watchdog messages, and the transition that reproduces the
   symptom.
4. Label conclusions as build, upload, hardware, system, or deployment
   evidence. Report the result by proof stages. A clean serial stream is not proof that pins, power, or the full
   system are correct.
5. Pair with `hardware-tdd` for a test matrix and `embedded-project-loop` when
   the next observation must come from a user-operated board.

## Recommended C++ Event Format

```cpp
Serial.print("t_ms=");
Serial.print(millis());
Serial.print(" level=INFO event=ready board=");
Serial.println(BOARD_ID);
```

Use a fixed, bounded format appropriate to the board's memory budget. Do not
log Wi-Fi passwords, API keys, certificates, tokens, or private data.

## Usage

### Basic Serial Monitoring

```bash
# Monitor serial port with default settings (9600 baud)
uv run --no-project scripts/monitor_serial.py --port COM3

# Specify baud rate and output file
uv run --no-project scripts/monitor_serial.py --port /dev/ttyACM0 --baud 115200 --output debug.log

# Filter for specific patterns
uv run --no-project scripts/monitor_serial.py --port COM3 --filter "ERROR|WARNING"
```

### Advanced Debugging

```bash
# Parse JSON data from serial
uv run --no-project scripts/monitor_serial.py --port COM3 --format json --pretty

# Monitor with timestamp and color coding
uv run --no-project scripts/monitor_serial.py --port COM3 --timestamp --color

# Detect common Arduino errors
uv run --no-project scripts/monitor_serial.py --port COM3 --detect-errors
```

## Script Options

- `--port`: Serial port (e.g., COM3, /dev/ttyACM0)
- `--baud`: Baud rate (default: 9600)
- `--output`: Output file for logging
- `--filter`: Regex pattern to filter lines
- `--format`: Data format (text, json, csv, binary)
- `--timestamp`: Add timestamps to output
- `--color`: Enable color-coded output
- `--detect-errors`: Highlight common error patterns
- `--timeout`: Connection timeout in seconds

## Common Arduino Debugging Scenarios

### Memory Issues
```
Filter for: "low memory|stack overflow|heap"
```

### Sensor Data Validation
```
Filter for: "sensor|reading|value"
Format as: json
```

### Timing Analysis
```
Enable: --timestamp
Filter for: "start|end|duration"
```

### Communication Errors
```
Filter for: "timeout|failed|error"
Enable: --detect-errors
```

## Integration with Arduino CLI

```bash
# Compile and upload, then monitor
arduino-cli compile --fqbn arduino:avr:uno sketch/
arduino-cli upload -p COM3 --fqbn arduino:avr:uno sketch/
uv run --no-project scripts/monitor_serial.py --port COM3
```

## Troubleshooting

### Port Not Found
- Check `arduino-cli board list` for available ports
- Ensure Arduino is connected and drivers are installed
- Try different port names (COM1-COM99 on Windows, /dev/ttyACM* on Linux)

### No Data Received
- Verify baud rate matches Arduino sketch (`Serial.begin(9600)`)
- Check USB cable connection
- Reset Arduino board while monitoring

### Permission Errors (Linux/macOS)
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER
# Logout and login again
```

## Evidence And Privacy

Record the board, firmware/image version, toolchain, baud, port, reset cause,
and timestamp source. Label serial output as hardware or system evidence only
when it was captured on the target. Redact Wi-Fi passwords, API keys,
certificates, tokens, and personal data before saving logs or sharing them.

## Dependencies

- Python 3.8+
- `uv` 0.4+ (the script declares `pyserial` and `colorama` inline)
- Run the self-contained helper with `uv run --no-project scripts/monitor_serial.py --help`.

## Examples

### Basic Temperature Sensor Monitoring

```python
// Arduino sketch
void setup() {
  Serial.begin(9600);
}

void loop() {
  float temp = analogRead(A0) * 0.488;
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println(" C");
  delay(1000);
}
```

```bash
uv run --no-project scripts/monitor_serial.py --port COM3 --filter "Temperature" --timestamp
```

### JSON Data Parsing

```python
// Arduino sketch with JSON output
#include <ArduinoJson.h>

void setup() {
  Serial.begin(115200);
}

void loop() {
  StaticJsonDocument<200> doc;
  doc["temperature"] = analogRead(A0) * 0.488;
  doc["humidity"] = analogRead(A1) * 0.146;
  doc["timestamp"] = millis();
  serializeJson(doc, Serial);
  Serial.println();
  delay(2000);
}
```

```bash
uv run --no-project scripts/monitor_serial.py --port COM3 --format json --pretty
```

## Shared Output Contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
