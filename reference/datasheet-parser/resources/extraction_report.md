# Register Map Extraction Report Template

## Metadata
- **Component**: {{PART_NAME}}
- **Datasheet Version**: {{DATASHEET_VERSION}}
- **Datasheet Source**: {{DATASHEET_URL}}
- **Pages Referenced**: {{PAGE_NUMBERS}}
- **I2C Address (7-bit)**: 0x{{I2C_ADDRESS}}
- **Extraction Date**: {{DATE}}

## Device Information

### Device ID Register
- **WHO_AM_I**: Address 0x{{WHO_AM_I_ADDR}}, Expected Value: 0x{{EXPECTED_ID}}
- **Reference**: Datasheet p.{{PAGE}}, §{{SECTION}}

## Register Map Summary

Total Registers Extracted: {{TOTAL_COUNT}}
- Read-Only: {{RO_COUNT}}
- Write-Only: {{WO_COUNT}}
- Read-Write: {{RW_COUNT}}

## Detailed Register Definitions

### Configuration Registers

#### Register: {{REG_NAME_1}}
- **Address**: 0x{{HEX_ADDR}}
- **Access**: R/W
- **Reset Value**: 0x{{RESET_VAL}}
- **Reference**: Datasheet p.{{PAGE}}, §{{SECTION}}
- **Description**: {{DESCRIPTION}}

**Bitfield Layout:**

| Bit(s) | Name | Access | Reset | Description |
|--------|------|--------|-------|-------------|
| 7      | {{FIELD_NAME}} | R/W | {{VAL}} | {{DESCRIPTION}} |
| 6-4    | {{FIELD_NAME}} | R/W | {{VAL}} | {{DESCRIPTION}} |
| 3-0    | Reserved | - | 0 | Do not modify |

**Usage Notes**:
- {{NOTE_1}}
- {{NOTE_2}}

---

#### Register: {{REG_NAME_2}}
- **Address**: 0x{{HEX_ADDR}}
- **Access**: RO
- **Reset Value**: N/A (Read-only)
- **Reference**: Datasheet p.{{PAGE}}, §{{SECTION}}
- **Description**: {{DESCRIPTION}}

**Bitfield Layout:**

| Bit(s) | Name | Access | Description |
|--------|------|--------|-------------|
| 7-0    | {{FIELD_NAME}} | RO | {{DESCRIPTION}} |

---

### Data Registers

#### Register: {{DATA_REG_NAME}}
- **Address**: 0x{{HEX_ADDR}}
- **Access**: RO
- **Reference**: Datasheet p.{{PAGE}}, §{{SECTION}}
- **Description**: {{DESCRIPTION}}

**Multi-byte Read**:
- {{DATA_REG_NAME}}_H: 0x{{ADDR_H}} (MSB)
- {{DATA_REG_NAME}}_L: 0x{{ADDR_L}} (LSB)
- Data Format: {{FORMAT}} (e.g., 16-bit 2's complement)
- Conversion: {{FORMULA}}

---

### Control Registers

#### Register: {{CTRL_REG_NAME}}
- **Address**: 0x{{HEX_ADDR}}
- **Access**: R/W
- **Reset Value**: 0x{{RESET_VAL}}
- **Reference**: Datasheet p.{{PAGE}}, §{{SECTION}}
- **Description**: {{DESCRIPTION}}

**Bitfield Layout:**

| Bit(s) | Name | Access | Values | Description |
|--------|------|--------|--------|-------------|
| 7      | ENABLE | R/W | 0=Disable, 1=Enable | Enable/disable function |
| 6-5    | MODE | R/W | 00=Mode0, 01=Mode1, 10=Mode2, 11=Mode3 | Operating mode |
| 4      | Reserved | - | 0 | Must write 0 |
| 3-0    | SETTING | R/W | 0x0-0xF | Configuration value |

---

## Register Categories

### Initialization Sequence
Required register writes for device initialization (Datasheet p.{{PAGE}}, §{{SECTION}}):

1. Write 0x{{VAL}} to {{REG_NAME}} - {{DESCRIPTION}}
2. Wait {{TIME}}ms
3. Write 0x{{VAL}} to {{REG_NAME}} - {{DESCRIPTION}}
4. Verify {{REG_NAME}} reads 0x{{VAL}}

### Power Management
Registers related to power modes:
- {{PWR_REG_1}}: 0x{{ADDR}} - {{DESCRIPTION}}
- {{PWR_REG_2}}: 0x{{ADDR}} - {{DESCRIPTION}}

### Measurement Configuration
Registers for configuring measurements:
- {{MEAS_REG_1}}: 0x{{ADDR}} - {{DESCRIPTION}}
- {{MEAS_REG_2}}: 0x{{ADDR}} - {{DESCRIPTION}}

### Interrupt Configuration
Registers for interrupt control:
- {{INT_REG_1}}: 0x{{ADDR}} - {{DESCRIPTION}}
- {{INT_REG_2}}: 0x{{ADDR}} - {{DESCRIPTION}}

## Bitfield Enumerations

### {{ENUM_NAME_1}}
From Register: {{REG_NAME}} (Datasheet p.{{PAGE}})

```cpp
enum class {{EnumName}} : uint8_t {
    VALUE_0 = 0x00,  // {{DESCRIPTION}}
    VALUE_1 = 0x01,  // {{DESCRIPTION}}
    VALUE_2 = 0x02,  // {{DESCRIPTION}}
    VALUE_3 = 0x03   // {{DESCRIPTION}}
};
```

### {{ENUM_NAME_2}}
From Register: {{REG_NAME}} (Datasheet p.{{PAGE}})

```cpp
enum class {{EnumName}} : uint8_t {
    OPTION_A = (1 << 0),  // {{DESCRIPTION}}
    OPTION_B = (1 << 1),  // {{DESCRIPTION}}
    OPTION_C = (1 << 2),  // {{DESCRIPTION}}
    OPTION_D = (1 << 3)   // {{DESCRIPTION}}
};
```

## Special Notes

### Reserved Bits
- Always write 0 to reserved bits unless datasheet specifies otherwise
- Reading reserved bits may return undefined values

### Multi-byte Reads
- For 16-bit values, read high byte first (most sensors auto-increment address)
- Check if datasheet requires specific read order
- Some devices require dummy read after address write

### I2C Communication Notes
- **Clock Speed**: Max {{SPEED}} kHz (Datasheet p.{{PAGE}})
- **Address Auto-increment**: {{YES/NO}} (when reading multiple registers)
- **Repeated Start**: {{REQUIRED/OPTIONAL}} (Datasheet p.{{PAGE}})

### Timing Requirements
- **Power-on Reset Time**: {{TIME}}ms (Datasheet p.{{PAGE}})
- **Soft Reset Time**: {{TIME}}ms (Datasheet p.{{PAGE}})
- **Measurement Time**: {{TIME}}ms (Datasheet p.{{PAGE}})

## Validation Checklist

- [ ] All register addresses verified against datasheet
- [ ] All bitfield positions verified
- [ ] Reset values documented
- [ ] Access modes (R/W/RO) confirmed
- [ ] Reserved bits identified
- [ ] Page references included for all definitions
- [ ] Initialization sequence documented
- [ ] Multi-byte read order specified
- [ ] Timing requirements noted
- [ ] I2C address confirmed with user

## References

### Datasheet Sections
- Register Map: §{{SECTION}}, p.{{PAGES}}
- Electrical Characteristics: §{{SECTION}}, p.{{PAGES}}
- I2C Timing: §{{SECTION}}, p.{{PAGES}}
- Application Notes: §{{SECTION}}, p.{{PAGES}}

### Related Documents
- {{DOC_1}}
- {{DOC_2}}

---

*This report serves as the "Source of Truth" for generating `{{part}}_regs.h`*
