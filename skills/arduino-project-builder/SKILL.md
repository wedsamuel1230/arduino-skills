---
name: arduino-project-builder
description: Build complete, production-ready Arduino projects (environmental monitors, robot controllers, IoT devices, automation systems). Assembles multi-component systems combining sensors, actuators, communication protocols, state machines, data logging, and power management. Supports Arduino UNO, ESP32, and Raspberry Pi Pico with board-specific optimizations. Use this skill when users request complete Arduino applications, not just code snippets.
---

# Arduino Project Builder Skill

**Purpose:** Assemble complete, working Arduino projects from requirements. This skill combines multiple patterns (sensors, actuators, state machines, logging, communication) into cohesive systems.

**When to Use:** When user requests a complete project like "build an environmental monitor", "create a robot controller", "make an IoT temperature logger", or any multi-component Arduino application.

## Quick Start

**List available project types:**
```bash
uv run scripts/scaffold_project.py --list
```

**Create a complete project:**
```bash
uv run scripts/scaffold_project.py --type environmental --board esp32 --name "WeatherStation"
uv run scripts/scaffold_project.py --type robot --board uno --output ./my-robot
```

**Interactive mode:**
```bash
uv run scripts/scaffold_project.py --interactive
```

## Resources

- **scripts/scaffold_project.py** - CLI tool for project scaffolding (config.h, main.ino, platformio.ini, README)
- **assets/workflow.mmd** - Mermaid diagram of project assembly workflow

## Supported Project Types

1. **Environmental Monitors** - Multi-sensor data loggers (temperature, humidity, light, air quality)
2. **Robot Controllers** - Motor control, sensor fusion, obstacle avoidance, state machines
3. **IoT Devices** - WiFi/MQTT data transmission, cloud integration, remote monitoring
4. **Home Automation** - Relay control, scheduled tasks, sensor-triggered actions
5. **Data Acquisition Systems** - High-frequency sampling, SD card logging, real-time visualization

## Project Assembly Workflow

### 1. Requirements Gathering
- **User Intent:** Understand the project goal (what should it do?)
- **Hardware Inventory:** What sensors, actuators, and communication modules?
- **Board Selection:** Arduino UNO, ESP32, or Raspberry Pi Pico?
- **Constraints:** Power source, memory limits, real-time requirements

### 2. Architecture Design
- **Component Diagram:** Which sensors/actuators connect to which pins?
- **Data Flow:** How does data move through the system?
- **State Machine:** Does the project have distinct modes/states?
- **Timing Requirements:** What tasks run at what intervals?

### 3. Code Assembly
- **Pull patterns from references/** (environmental-monitor, robot-controller, iot-device)
- **Customize for user's hardware** (pin assignments, sensor types)
- **Integrate state machine** (if project has modes)
- **Add data logging** (Serial, SD card, or EEPROM)

### 4. Testing & Validation
- **Compilation Check:** Does it compile for the target board?
- **Memory Usage:** Within board limits? (UNO has only 2KB SRAM)
- **Pin Conflicts:** No duplicate pin assignments?
- **Timing Analysis:** All tasks fit within loop execution time?

### 5. Documentation
- **Wiring Diagram:** Pin connections in text/ASCII format
- **Usage Instructions:** How to upload, configure, and run
- **Serial Commands:** What commands trigger actions?
- **Troubleshooting:** Common issues and fixes

## Board-Specific Considerations

**Arduino UNO/Nano (ATmega328P):**
- 2KB SRAM → Keep arrays small, use F() macro for strings
- 10-bit ADC → Range 0-1023
- No WiFi → Use Serial or add external module

**ESP32:**
- 327KB SRAM → Can use large buffers
- 12-bit ADC → Range 0-4095
- Built-in WiFi/Bluetooth → Ideal for IoT projects
- Dual-core → Can run tasks in parallel

**Raspberry Pi Pico (RP2040):**
- 262KB SRAM → Plenty of room
- 12-bit ADC → Range 0-4095
- No WiFi (unless Pico W) → Serial or add module
- Dual-core → Advanced task scheduling

## Quality Standards

All generated projects must include:
1. **config.h** - Hardware abstraction (board detection, pin definitions)
2. **Non-blocking code** - No delay() calls, use EveryMs timers
3. **Error handling** - Check for sensor failures, out-of-range values
4. **Serial diagnostics** - Print status messages, sensor readings
5. **Memory safety** - Bounds checking on arrays, CRC for stored data
6. **Wiring documentation** - Clear pin assignment table
7. **Compilation testing** - Verify it compiles for target board

## Integration Checklist

Before delivering a project, verify:
- [ ] All sensor readings validated (NaN checks, range checks)
- [ ] Button inputs debounced (50ms minimum)
- [ ] I2C devices scanned and detected
- [ ] CSV logging includes headers
- [ ] State machine has default/error states
- [ ] EEPROM writes include CRC validation
- [ ] WiFi reconnection logic (ESP32 projects)
- [ ] LED indicators for system status
- [ ] Serial baud rate matches board (9600 for UNO, 115200 for ESP32)
- [ ] F() macro used for all string literals

## Common Project Patterns

**1. Sensor → Filter → Display → Log**
- Read sensor with EveryMs timer
- Apply MovingAverageFilter or MedianFilter
- Print to Serial every 5 seconds
- Log CSV every 60 seconds

**2. Button → State Machine → Actuator**
- DebouncedButton detects input
- State machine transitions modes
- Actuator (motor, relay, LED) responds to state

**3. Sensor → Threshold → Action**
- Continuous sensor monitoring
- If value exceeds threshold, trigger action
- Hysteresis to prevent oscillation

**4. Multi-Sensor → Data Logger → SD Card**
- Multiple EveryMs timers for different sensors
- Aggregate data into struct
- Buffered SD card writes (flush every 10 entries)

**5. IoT: Sensor → WiFi → MQTT → Cloud**
- ESP32 connects to WiFi
- Read sensors every 60 seconds
- Publish JSON to MQTT broker
- Reconnect logic if connection drops

## Project References

See `references/` directory for complete project examples:
- `project-environmental-monitor.md` - Multi-sensor data logger
- `project-robot-controller.md` - Button-controlled robot with obstacle avoidance
- `project-iot-device.md` - ESP32 temperature/humidity logger with WiFi
- `project-home-automation.md` - Relay controller with scheduled tasks
- `project-data-acquisition.md` - High-speed ADC sampling with SD logging

## Communication & Output

**Present projects as:**
1. **Full .ino file** (ready to upload)
2. **Wiring table** (pin connections)
3. **Upload instructions** (board selection, baud rate)
4. **Usage guide** (Serial commands, expected output)

**Example Output Format:**
```
=== Environmental Monitor for Arduino UNO ===

WIRING:
DHT22 → Pin 2
Photoresistor → A0
Button → Pin 3 (INPUT_PULLUP)
LED → Pin 13

UPLOAD:
Board: Arduino UNO
Baud Rate: 9600

USAGE:
- Press button to start/stop logging
- Send 'd' to dump CSV data
- LED blinks every 2 seconds (heartbeat)

CODE:
[Full .ino file here]
```

---

**Next Steps:** When user requests a project, ask clarifying questions about:
1. Hardware components (what sensors/actuators?)
2. Target board (UNO, ESP32, Pico?)
3. Data output (Serial, SD card, WiFi?)
4. Special requirements (battery power, waterproof enclosure?)

Then assemble the project using patterns from references/, customize for their hardware, and deliver a complete, tested system.
