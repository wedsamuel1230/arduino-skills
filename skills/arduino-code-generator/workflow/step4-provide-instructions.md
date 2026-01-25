# Step 4: Provide Usage Instructions

After generating code, provide comprehensive usage instructions including wiring diagrams, configuration steps, and expected behavior.

## Instruction Components

### 1. Hardware Requirements
- **Components List**: Specific sensors, actuators, or modules needed
- **Board Compatibility**: Which Arduino boards are supported
- **Power Requirements**: Voltage and current specifications
- **Additional Hardware**: Cables, resistors, breadboards, etc.

### 2. Wiring Instructions
- **Pin Connections**: Clear mapping between Arduino pins and component pins
- **Circuit Diagrams**: ASCII art or reference to visual diagrams
- **Pull-up/Pull-down Resistors**: When and where to use them
- **Power Connections**: VCC, GND, and signal pins

### 3. Software Setup
- **Library Installation**: Which Arduino libraries to install via Library Manager
- **Board Selection**: How to select the correct board in Arduino IDE
- **Configuration**: Any settings or parameters to modify
- **Dependencies**: Other code or configurations required

### 4. Usage Instructions
- **Initialization**: What happens during setup()
- **Operation**: How the code behaves during normal operation
- **User Interaction**: Buttons to press, sensors to trigger, etc.
- **Output**: What to expect on Serial monitor, LEDs, displays

### 5. Testing and Validation
- **Expected Output**: Sample Serial output or LED patterns
- **Error Conditions**: What to look for if something goes wrong
- **Debugging Tips**: How to troubleshoot common issues
- **Performance Metrics**: Expected timing or resource usage

## Wiring Diagram Format

Use clear ASCII art for wiring diagrams:

```
Arduino UNO          DHT22 Sensor
-----------          ------------
  5V      --------->   VCC
  GND     --------->   GND
  D2      --------->   DATA
                     (with 10K pull-up resistor)
```

Or reference existing diagrams:
- See examples/README.md for detailed wiring diagrams
- Check Fritzing diagrams in assets/ folder

## Example Instructions Template

### Hardware Required
- Arduino UNO, ESP32, or RP2040 board
- DHT22 temperature/humidity sensor
- 10KΩ pull-up resistor
- Jumper wires

### Wiring
```
Arduino Pin  | DHT22 Pin | Notes
-------------|-----------|--------
5V          | VCC       | Power supply
GND         | GND       | Ground
D2          | DATA      | Data signal (with 10K pull-up to 5V)
```

### Setup Steps
1. Install DHT sensor library: `Sketch > Include Library > Manage Libraries > "DHT sensor library"`
2. Select your board: `Tools > Board > Arduino UNO`
3. Upload the sketch
4. Open Serial Monitor: `Tools > Serial Monitor`

### Expected Output
```
Initializing DHT22 sensor...
DHT22 initialized successfully
Temperature: 23.50°C, Humidity: 45.20%
Temperature: 23.52°C, Humidity: 45.15%
...
```

### Troubleshooting
- **No readings**: Check wiring and power connections
- **Invalid readings**: Ensure proper pull-up resistor on data pin
- **Slow response**: DHT22 sensors can take up to 2 seconds between readings

## Integration Notes

When combining with other patterns:
- Mention how wiring integrates with existing circuits
- Note any pin conflicts or shared resources
- Explain how multiple components work together
- Provide combined wiring diagrams for complex projects