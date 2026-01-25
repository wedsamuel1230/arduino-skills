# Step 2: Read Relevant Reference File

After identifying the pattern type, read the corresponding reference documentation to understand implementation details.

## Reference File Mapping

| Pattern Category | Reference File | Location |
|------------------|----------------|----------|
| Hardware Abstraction | patterns-config.md | references/ |
| Sensor Reading & Filtering | patterns-filtering.md | references/ |
| Input Handling | patterns-buttons.md | references/ |
| Communication (I2C) | patterns-i2c.md | references/ |
| Communication (SPI) | patterns-spi.md | references/ |
| Communication (CSV) | patterns-csv.md | references/ |
| Timing & Concurrency (Scheduler) | patterns-scheduler.md | references/ |
| Timing & Concurrency (State Machine) | patterns-state-machine.md | references/ |
| Hardware Detection | patterns-hardware-detection.md | references/ |
| Data Persistence | patterns-data-logging.md | references/ |

## Reading Process

1. **Locate the reference file** based on pattern mapping
2. **Read the complete file** to understand:
   - Required libraries and includes
   - Pin configurations
   - Function signatures
   - Error handling patterns
   - Board-specific considerations
   - Example implementations

3. **Extract key implementation details**:
   - Data structures used
   - Timing constraints
   - Memory requirements
   - Initialization sequences
   - Common pitfalls

4. **Note integration points** with other patterns

## Reference File Structure

Each reference file contains:
- **Overview**: Pattern description and use cases
- **API Reference**: Function signatures and parameters
- **Implementation Guide**: Step-by-step coding instructions
- **Board-Specific Notes**: UNO/ESP32/RP2040 differences
- **Examples**: Code snippets and usage patterns
- **Integration**: How to combine with other patterns

## Fallback Strategy

If a specific reference file doesn't exist:
1. Check for similar patterns in existing files
2. Use general Arduino best practices
3. Consult the quality standards and common pitfalls
4. Generate code following established patterns