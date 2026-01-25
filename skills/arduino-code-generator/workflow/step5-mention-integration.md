# Step 5: Mention Integration

When relevant, suggest how the generated code can integrate with other patterns for more complex projects.

## Integration Patterns

### Environmental Monitor
**Combines:** Filtering + Scheduler + CSV + Data Logging

**Use Case:** Collect sensor data over time and log to SD card
**Components:** DHT22/BME280 sensors + SD card module + real-time clock

**Integration Points:**
- Use Scheduler for periodic readings
- Apply Filtering for noise reduction
- Format data as CSV for logging
- Use Data Logging for persistent storage

### Button-Controlled Robot
**Combines:** Buttons + State Machine + Scheduler

**Use Case:** Robot with button controls and different operational modes
**Components:** Multiple buttons + motor drivers + state indicators

**Integration Points:**
- Buttons trigger state transitions
- State Machine manages robot behavior
- Scheduler handles timing-critical motor control

### IoT Data Logger
**Combines:** Hardware Detection + WiFi + Data Logging + CSV

**Use Case:** Remote environmental monitoring with cloud connectivity
**Components:** ESP32 board + sensors + WiFi module + SD card

**Integration Points:**
- Hardware Detection for sensor availability
- WiFi for data transmission
- Data Logging as backup when offline
- CSV for structured data format

### Sensor Hub
**Combines:** I2C + Filtering + Scheduler + Hardware Detection

**Use Case:** Multiple I2C sensors with coordinated readings
**Components:** Multiple I2C sensors + microcontroller with I2C bus

**Integration Points:**
- I2C for sensor communication
- Filtering for each sensor type
- Scheduler for coordinated sampling
- Hardware Detection for plug-and-play sensors

## Integration Guidelines

### When to Suggest Integration
- **User requests complex functionality** requiring multiple patterns
- **Hardware setup** naturally combines different components
- **Project scope** involves data flow between subsystems
- **Performance requirements** need coordinated timing

### How to Present Integration
1. **Identify the primary pattern** from the user's request
2. **Suggest complementary patterns** that enhance functionality
3. **Explain the benefits** of combining patterns
4. **Provide integration examples** from the examples/ folder
5. **Note any constraints** or considerations

### Integration Examples

**"I want to log temperature data"**
→ Primary: Data Logging
→ Integration: Add Filtering for noise reduction, Scheduler for timing

**"Build a smart button interface"**
→ Primary: Buttons
→ Integration: Add State Machine for complex interactions, Scheduler for timeouts

**"Create a wireless sensor network"**
→ Primary: Communication (WiFi/I2C)
→ Integration: Add Hardware Detection for robustness, Data Logging for offline operation

## Cross-Pattern Considerations

### Shared Resources
- **Pins:** Ensure no conflicts between integrated patterns
- **Memory:** Account for combined memory usage
- **Timing:** Coordinate timing requirements between patterns
- **Power:** Consider power consumption of combined components

### Code Organization
- **Modular Functions:** Keep patterns in separate functions
- **Shared Constants:** Define common pins/constants once
- **Error Handling:** Integrate error handling across patterns
- **Initialization Order:** Ensure proper startup sequence

### Testing Strategy
- **Individual Testing:** Test each pattern separately first
- **Integration Testing:** Verify combined functionality
- **Edge Cases:** Test interactions between patterns
- **Resource Limits:** Verify memory and timing constraints

## Documentation Links

For detailed integration examples, see:
- [examples/README.md](examples/README.md) - Complete project examples
- Individual pattern references in [references/](references/) folder
- [assets/workflow.mmd](assets/workflow.mmd) - Integration workflow diagram