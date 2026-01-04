# Datasheet Parser Agent - Quick Reference

## Usage Pattern

When a user requests datasheet parsing, follow this sequence:

### 1. Gather Information
```
Required:
- PART_NAME: e.g., "MPU6050"
- DATASHEET_PDF: Path or URL to PDF
- TARGET_PLATFORM: "ARDUINO" (default) or "BARE_METAL"

Optional:
- Custom I2C address (if not using default)
```

### 2. Validate Datasheet
- Confirm PDF has selectable text
- Verify it's the official manufacturer version
- Check for register map section

### 3. I2C Address Confirmation (CRITICAL!)
```
If multiple addresses found:
❌ DON'T: Guess or pick arbitrarily
✅ DO: List all options and ask user to confirm

Example:
"Found 2 possible I2C addresses:
- 0x68 when AD0 pin is LOW
- 0x69 when AD0 pin is HIGH
Which configuration does your hardware use?"
```

### 4. Generate Extraction Report
Create `resources/extraction_report.md` with:
- All register addresses and bitfields
- Page references for every definition
- Reset values and access modes
- Initialization sequence
- Timing requirements

### 5. Generate Code Templates
Fill in templates with extracted data:
1. `src/{{part}}_regs.h` - Register definitions only
2. `src/{{part}}.h` - Main API interface
3. `src/{{part}}.cpp` - Business logic
4. `src/{{part}}_hal.cpp` - Platform-specific I2C
5. `examples/simple_test.ino` - Quick-start example
6. `README.md` - Documentation

## Template Variable Mapping

### Common Variables
- `{{PART_NAME}}`: Human-readable name (e.g., "MPU6050")
- `{{part}}`: lowercase for filenames (e.g., "mpu6050")
- `{{Part}}`: PascalCase for classes (e.g., "Mpu6050")
- `{{PART_UPPER}}`: UPPERCASE for macros (e.g., "MPU6050")
- `{{I2C_ADDRESS}}`: Confirmed 7-bit address (e.g., "68")
- `{{DEVICE_ID}}`: WHO_AM_I expected value (e.g., "71")
- `{{PAGE}}`: Datasheet page number
- `{{SECTION}}`: Datasheet section (e.g., "6.3.1")

### Register-Specific
- `{{REG_NAME}}`: Register name in uppercase
- `{{ADDR}}`: Register address in hex (without 0x)
- `{{RESET_VAL}}`: Reset value in hex
- `{{BITFIELD}}`: Bitfield name
- `{{BIT_POS}}`: Bit position
- `{{MASK}}`: Bit mask

### Configuration
- `{{ConfigParam1}}`: Configuration parameter name
- `{{EnumName}}`: Enum type name
- `{{VALUE_0}}`: Enum value name
- `{{DESC_0}}`: Description for enum value

### Data Types
- `{{DataType1}}`: Data type name (e.g., "Accel", "Temperature")
- `{{DATA_C_TYPE}}`: C type (e.g., "int16_t", "uint16_t")
- `{{UNIT}}`: Physical unit (e.g., "°C", "g", "°/s")
- `{{SCALE_FACTOR}}`: Conversion factor

## Code Generation Rules

### Register Definitions (`_regs.h`)
```cpp
// ✅ CORRECT
#define MPU6050_REG_CONFIG   0x1A  // Datasheet p.42, §6.3.1

enum class Mpu6050PowerMode : uint8_t {
    SLEEP = 0x00,     // Datasheet p.45
    NORMAL = 0x01,    // Datasheet p.45
    LOW_POWER = 0x02  // Datasheet p.45
};

// ❌ WRONG - No implementation in _regs.h
bool writeConfig(uint8_t val);  // This belongs in .h file
```

### Main API (`_hal.cpp` separation)
```cpp
// ✅ CORRECT in .cpp
bool Mpu6050::readAccel(int16_t* value) {
    uint8_t data[2];
    if (!readRegs(MPU6050_REG_ACCEL_H, data, 2)) {
        return false;  // HAL function failed
    }
    *value = (int16_t)((data[0] << 8) | data[1]);
    return true;
}

// ❌ WRONG - Direct I2C in .cpp
bool Mpu6050::readAccel(int16_t* value) {
    Wire.beginTransmission(_addr);  // NO! This belongs in HAL
    // ...
}
```

### HAL Layer (Platform Detection)
```cpp
// ✅ CORRECT - Platform-specific I2C
#ifdef MPU6050_PLATFORM_ARDUINO
    bool Mpu6050::writeReg(uint8_t reg, uint8_t val) {
        Wire.beginTransmission(_addr);
        Wire.write(reg);
        Wire.write(val);
        return (Wire.endTransmission() == 0);
    }
#else
    // Bare-metal implementation
    bool Mpu6050::writeReg(uint8_t reg, uint8_t val) {
        uint8_t data[2] = {reg, val};
        return i2c_write(_addr, data, 2);
    }
#endif
```

## Quality Checklist

Before delivering generated code:

- [ ] All registers have datasheet page references
- [ ] I2C address confirmed with user (if multiple options)
- [ ] Register definitions in `_regs.h` only (no implementation)
- [ ] Main logic in `.cpp` uses HAL functions (never direct I2C)
- [ ] HAL layer in `_hal.cpp` has both Arduino and bare-metal paths
- [ ] Example compiles for Arduino platform
- [ ] README includes troubleshooting section
- [ ] Extraction report complete with all registers
- [ ] Timing requirements documented
- [ ] Bitfield enumerations are type-safe

## Common Pitfalls to Avoid

### ❌ Don't Mix Concerns
```cpp
// BAD: I2C code in business logic
bool Mpu6050::readAccel(...) {
    Wire.beginTransmission(_addr);  // NO!
}
```

### ❌ Don't Skip Page References
```cpp
// BAD: No datasheet reference
#define MPU6050_REG_CONFIG  0x1A

// GOOD: With reference
#define MPU6050_REG_CONFIG  0x1A  // Datasheet p.42, §6.3.1
```

### ❌ Don't Hardcode Multiple Addresses
```cpp
// BAD: Using hardcoded address without confirmation
#define MPU6050_I2C_ADDR  0x68  // What if user has 0x69?

// GOOD: Document configuration
#define MPU6050_I2C_ADDR  0x68  // When AD0=LOW. Use 0x69 when AD0=HIGH
```

### ❌ Don't Put Implementation in Headers
```cpp
// BAD: Implementation in .h file
class Mpu6050 {
    bool readAccel(...) {
        // implementation here  // NO!
    }
};

// GOOD: Declaration only in .h
class Mpu6050 {
    bool readAccel(...);  // Implementation in .cpp
};
```

## File Structure Verification

After generation, verify this structure exists:

```
generated_library/
├── src/
│   ├── {{part}}_regs.h      ← Only definitions
│   ├── {{part}}.h            ← API declarations
│   ├── {{part}}.cpp          ← Business logic
│   └── {{part}}_hal.cpp      ← I2C platform code
├── examples/
│   └── simple_test.ino       ← Working Arduino example
├── resources/
│   └── extraction_report.md  ← Source of truth
└── README.md                 ← Complete documentation
```

## Testing Generated Code

### Minimum Validation
1. Check compilation for Arduino platform
2. Verify all #include statements resolve
3. Confirm no direct Wire calls in .cpp (only in _hal.cpp)
4. Validate all register definitions have page numbers

### Recommended Tests
1. I2C scanner finds device at correct address
2. WHO_AM_I returns expected value
3. Simple_test.ino compiles and uploads
4. Basic read operation returns reasonable values

## Support Questions

### "What if datasheet doesn't have WHO_AM_I?"
Generate without device ID check, add note in README.

### "What if device uses SPI, not I2C?"
This skill is I2C-focused. Suggest creating separate SPI variant.

### "What if register map spans 100+ pages?"
Extract incrementally, focus on essential registers first.

### "What if I don't have the datasheet?"
Cannot proceed - datasheet is mandatory for accurate code generation.

## Example Session

```
User: "Create driver for MPU6050"

Agent: 
1. "Please provide MPU6050 datasheet (PDF link or upload)"
2. User provides: mpu6050_datasheet_v4.2.pdf
3. "Found 2 I2C addresses: 0x68 (AD0=LOW), 0x69 (AD0=HIGH). Which?"
4. User: "0x68"
5. Generate extraction_report.md (125 registers found)
6. Generate all template files with filled data
7. Create README with wiring diagram and API docs
8. Summary: "Generated MPU6050 library with 125 registers, 8 APIs, datasheet references"
```

---

This quick reference should be consulted when using the skill to ensure consistency and quality!
