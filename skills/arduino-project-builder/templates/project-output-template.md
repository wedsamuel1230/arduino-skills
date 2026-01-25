# Project Output Template

Standardized format for delivering complete Arduino projects.

## Template Structure

```
=== [PROJECT_NAME] for [BOARD_TYPE] ===

[BRIEF_DESCRIPTION]

## WIRING DIAGRAM
[ASCII_ART_OR_TEXT_BASED_WIRING]

Component Connections:
- [COMPONENT]: [PIN_ASSIGNMENT]
- [COMPONENT]: [PIN_ASSIGNMENT]
- [COMPONENT]: [PIN_ASSIGNMENT]

## UPLOAD INSTRUCTIONS
Board: [BOARD_TYPE]
Baud Rate: [BAUD_RATE]
Port: [AUTO_DETECT_OR_SPECIFY]

## CONFIGURATION
[CONFIGURABLE_PARAMETERS]
- Parameter: [DEFAULT_VALUE] ([DESCRIPTION])
- Parameter: [DEFAULT_VALUE] ([DESCRIPTION])

## USAGE
### Setup
1. [STEP_1]
2. [STEP_2]
3. [STEP_3]

### Operation
- [COMMAND]: [DESCRIPTION]
- [COMMAND]: [DESCRIPTION]
- [INDICATOR]: [MEANING]

### Serial Commands
- '[COMMAND]': [ACTION_DESCRIPTION]
- '[COMMAND]': [ACTION_DESCRIPTION]

## TROUBLESHOOTING
### Common Issues
- **Issue**: [DESCRIPTION]
  **Solution**: [STEP_BY_STEP_FIX]

- **Issue**: [DESCRIPTION]
  **Solution**: [STEP_BY_STEP_FIX]

### Error Codes
- **Code**: [NUMBER] - [DESCRIPTION] ([CAUSE])

## CODE
[COMPLETE_INO_FILE_CONTENT]
```

## Required Sections

### Project Header
- **Project Name:** Descriptive and specific
- **Board Type:** UNO, ESP32, Pico (with variant if applicable)
- **Brief Description:** One-sentence project summary

### Hardware Documentation
- **Wiring Diagram:** Clear, text-based representation
- **Component List:** All required parts with pin connections
- **Power Requirements:** Voltage and current specifications

### Software Documentation
- **Upload Instructions:** Board selection and configuration
- **Configuration Options:** User-modifiable parameters
- **Usage Guide:** Setup and operation procedures
- **Serial Interface:** Available commands and responses

### Support Documentation
- **Troubleshooting Guide:** Common problems and solutions
- **Error Codes:** Diagnostic information
- **Performance Notes:** Expected behavior and limitations

### Code Delivery
- **Complete Source:** Full .ino file content
- **Additional Files:** config.h, platformio.ini if applicable
- **Library Dependencies:** Required Arduino libraries

## Quality Standards

- [ ] All sections completed
- [ ] Wiring diagram accurate and clear
- [ ] Code compiles and runs on target board
- [ ] Instructions tested and verified
- [ ] Troubleshooting covers common issues
- [ ] Links to additional resources provided

## Example Implementation

```
=== Environmental Monitor for Arduino UNO ===

Multi-sensor data logger with temperature, humidity, and light monitoring.

## WIRING DIAGRAM
```
DHT22 → Pin 2
Photoresistor → A0
Button → Pin 3 (INPUT_PULLUP)
LED → Pin 13
```

Component Connections:
- DHT22 Temperature/Humidity Sensor: Digital Pin 2
- Photoresistor (Light Sensor): Analog Pin A0
- Push Button: Digital Pin 3 (with internal pull-up)
- Status LED: Digital Pin 13

## UPLOAD INSTRUCTIONS
Board: Arduino UNO
Baud Rate: 9600
Port: Auto-detect

## CONFIGURATION
- LOG_INTERVAL: 60 seconds (How often to log data)
- SENSOR_TIMEOUT: 5000ms (Sensor read timeout)
- LED_BLINK_RATE: 2000ms (Status LED blink interval)

## USAGE
### Setup
1. Connect sensors according to wiring diagram
2. Upload code to Arduino UNO
3. Open Serial Monitor at 9600 baud
4. Press button to start/stop logging

### Operation
- LED blinks every 2 seconds (heartbeat)
- Serial output shows sensor readings every 5 seconds
- Data logging occurs every 60 seconds when active

### Serial Commands
- 'd': Dump all logged CSV data
- 'c': Clear logged data
- 's': Show current sensor readings

## TROUBLESHOOTING
### Common Issues
- **No sensor readings**: Check wiring connections and power
  **Solution**: Verify DHT22 is connected to pin 2, photoresistor to A0

- **Compilation errors**: Ensure DHT library is installed
  **Solution**: Install "DHT sensor library" from Arduino IDE

### Error Codes
- **Code: 1** - DHT sensor read failure (Check wiring and power)
- **Code: 2** - SD card initialization failed (Check card insertion)

## CODE
[Full Arduino sketch content here]
```