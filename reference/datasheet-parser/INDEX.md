# Datasheet Parser Agent Skill - File Index

## Quick Navigation

### 📖 Start Here
- **[README.md](README.md)** - Complete overview and summary
- **[SKILL.md](SKILL.md)** - Main skill instructions (required reading)

### 🎓 Learning Materials
- **[EXAMPLE.md](EXAMPLE.md)** - Complete MPU6050 driver generation example
- **[QUICKREF.md](QUICKREF.md)** - Quick reference for using the skill

### 🛠️ Templates
All templates are in the `templates/` directory:

#### Source Code Templates
- **[part_regs.h.tmpl](templates/src/part_regs.h.tmpl)** - Register definitions (single source of truth)
- **[part.h.tmpl](templates/src/part.h.tmpl)** - Main API interface declarations
- **[part.cpp.tmpl](templates/src/part.cpp.tmpl)** - Business logic implementation
- **[part_hal.cpp.tmpl](templates/src/part_hal.cpp.tmpl)** - Hardware abstraction layer (I2C)

#### Example Templates
- **[simple_test.ino.tmpl](templates/examples/simple_test.ino.tmpl)** - Arduino quick-start example

#### Documentation Templates
- **[README.md.tmpl](templates/README.md.tmpl)** - Complete library documentation template

### 📋 Resources
- **[extraction_report.md](resources/extraction_report.md)** - Template for datasheet register extraction

---

## File Purposes

### Documentation Files (4 files)

#### README.md (11.2 KB)
**Purpose**: Comprehensive skill overview  
**Contents**:
- Skill features and capabilities
- Architecture overview
- Usage workflow
- Quality metrics
- Success criteria
- Example session

**When to read**: First introduction to the skill

---

#### SKILL.md (15.9 KB) ⭐ MOST IMPORTANT
**Purpose**: Complete skill instructions for Claude  
**Contents**:
- Persona and objectives
- 4-phase workflow (gathering, extraction, generation, delivery)
- Template structures with detailed specs
- Coding standards
- Critical rules and constraints
- Quality requirements

**When to read**: Before using the skill; reference during execution

---

#### QUICKREF.md (7.8 KB)
**Purpose**: Quick reference guide  
**Contents**:
- Usage patterns
- Template variable mapping
- Code generation rules
- Quality checklist
- Common pitfalls
- Troubleshooting

**When to read**: During skill execution for quick lookups

---

#### EXAMPLE.md (12.8 KB)
**Purpose**: Complete working example  
**Contents**:
- Full MPU6050 driver generation
- Real register definitions
- Generated API code
- Working Arduino example
- Statistics and metrics

**When to read**: To understand output quality and structure

---

### Template Files (6 files)

All templates use `{{VARIABLE}}` syntax for placeholders.

#### part_regs.h.tmpl (8.3 KB)
**Purpose**: Register definitions only  
**Contains**:
- I2C address definitions
- Register address constants
- Bitfield definitions
- Enumerations
- Timing constants
- NO implementation code

**Key principle**: Single source of truth for hardware definitions

---

#### part.h.tmpl (11.3 KB)
**Purpose**: Main API interface  
**Contains**:
- Class declaration
- Public API methods
- Data structures
- Private HAL function declarations
- Doxygen documentation

**Key principle**: API declarations only, no implementation

---

#### part.cpp.tmpl (8.5 KB)
**Purpose**: Business logic implementation  
**Contains**:
- All public API implementations
- Device initialization sequence
- Configuration methods
- Data reading functions
- Helper functions

**Key principle**: Never calls I2C directly, only uses HAL functions

---

#### part_hal.cpp.tmpl (9.8 KB)
**Purpose**: Hardware abstraction layer  
**Contains**:
- Platform detection (#ifdef)
- Arduino implementation (Wire library)
- Bare-metal implementation (user functions)
- I2C communication primitives
- Platform-specific notes

**Key principle**: Only file with direct I2C code

---

#### simple_test.ino.tmpl (7.1 KB)
**Purpose**: Arduino quick-start example  
**Contains**:
- Hardware wiring diagram
- Basic initialization
- Simple data reading
- Serial output
- Helper functions (commented)

**Key principle**: Beginner-friendly, works out-of-box

---

#### README.md.tmpl (12.1 KB)
**Purpose**: Generated library documentation  
**Contains**:
- Installation instructions
- Hardware connections
- Quick start guide
- Complete API reference
- Architecture explanation
- Troubleshooting section
- License

**Key principle**: Complete user documentation for generated library

---

### Resource Files (1 file)

#### extraction_report.md (5.7 KB)
**Purpose**: Template for datasheet register extraction  
**Contains**:
- Metadata section
- Register map summary
- Detailed register tables
- Bitfield layouts
- Enumeration definitions
- Special notes
- References

**Key principle**: "Source of truth" for register data before code generation

---

## Workflow File Usage

### Phase 1: Information Gathering
**Files Used**: SKILL.md (workflow section)

### Phase 2: Register Extraction
**Files Created**: `extraction_report.md` (based on template)  
**Files Referenced**: SKILL.md (extraction rules)

### Phase 3: Code Generation
**Templates Used**:
1. `part_regs.h.tmpl` → Fill with register data
2. `part.h.tmpl` → Fill with API definitions
3. `part.cpp.tmpl` → Fill with implementation
4. `part_hal.cpp.tmpl` → Select platform, fill I2C code
5. `simple_test.ino.tmpl` → Fill with example usage
6. `README.md.tmpl` → Fill with documentation

**Files Referenced**: QUICKREF.md (variable mapping)

### Phase 4: Delivery
**Files Generated**: Complete library directory  
**Files Referenced**: EXAMPLE.md (for quality comparison)

---

## File Dependencies

```
SKILL.md (Master Instructions)
    ↓
    ├─→ QUICKREF.md (Quick Reference)
    ├─→ EXAMPLE.md (Quality Benchmark)
    └─→ Templates/
         ├─→ extraction_report.md
         ├─→ part_regs.h.tmpl
         ├─→ part.h.tmpl
         ├─→ part.cpp.tmpl
         ├─→ part_hal.cpp.tmpl
         ├─→ simple_test.ino.tmpl
         └─→ README.md.tmpl
```

---

## File Size Summary

| File | Size | Lines | Purpose |
|------|------|-------|---------|
| SKILL.md | 15.9 KB | 503 | Master instructions |
| README.md | 11.2 KB | ~350 | Skill overview |
| EXAMPLE.md | 12.8 KB | ~400 | Complete example |
| QUICKREF.md | 7.8 KB | ~250 | Quick reference |
| extraction_report.md | 5.7 KB | ~200 | Register template |
| part_regs.h.tmpl | 8.3 KB | ~280 | Register definitions |
| part.h.tmpl | 11.3 KB | ~380 | API interface |
| part.cpp.tmpl | 8.5 KB | ~290 | Implementation |
| part_hal.cpp.tmpl | 9.8 KB | ~330 | HAL layer |
| simple_test.ino.tmpl | 7.1 KB | ~240 | Arduino example |
| README.md.tmpl | 12.1 KB | ~410 | Library docs |
| **Total** | **110.5 KB** | **~3,630** | Complete skill |

---

## Essential Reading Order

1. **[README.md](README.md)** - Get overview (5 min)
2. **[SKILL.md](SKILL.md)** - Understand workflow (15 min)
3. **[EXAMPLE.md](EXAMPLE.md)** - See complete example (10 min)
4. **[QUICKREF.md](QUICKREF.md)** - Reference during use (as needed)

---

## Template Usage Examples

### Variable Naming Convention

```
{{PART_NAME}}    → "MPU6050"           (Human readable)
{{part}}         → "mpu6050"           (Lowercase for filenames)
{{Part}}         → "Mpu6050"           (PascalCase for classes)
{{PART_UPPER}}   → "MPU6050"           (Uppercase for macros)
```

### Common Template Variables

- `{{I2C_ADDRESS}}` - Confirmed I2C address (e.g., "68")
- `{{DEVICE_ID}}` - WHO_AM_I expected value
- `{{PAGE}}` - Datasheet page number
- `{{SECTION}}` - Datasheet section (e.g., "6.3.1")
- `{{REG_NAME}}` - Register name in uppercase
- `{{ADDR}}` - Register address in hex (no 0x prefix)
- `{{DataType1}}` - Data type name (e.g., "Accel")
- `{{UNIT}}` - Physical unit (e.g., "g", "°C")

---

## Support and Help

### Problem: Don't know where to start
**Solution**: Read README.md first, then SKILL.md

### Problem: Need quick variable lookup
**Solution**: Check QUICKREF.md "Template Variable Mapping" section

### Problem: Want to see real output
**Solution**: Read EXAMPLE.md for complete MPU6050 example

### Problem: Code generation failing
**Solution**: Check QUICKREF.md "Quality Checklist" and "Common Pitfalls"

### Problem: Template syntax unclear
**Solution**: Look at template files directly, they have inline comments

---

## Maintenance Notes

### Adding New Templates
1. Create `.tmpl` file in appropriate directory
2. Use `{{VARIABLE}}` syntax for placeholders
3. Add documentation header
4. Update this INDEX.md
5. Add example usage in EXAMPLE.md

### Updating Existing Templates
1. Maintain backward compatibility
2. Update SKILL.md if workflow changes
3. Update QUICKREF.md if new variables added
4. Update EXAMPLE.md if output format changes

### Version Control
- All files are plain text (Markdown)
- Easy to diff and track changes
- Templates are independent (can update separately)

---

**Last Updated**: 2026-01-04  
**Skill Version**: 1.0.0  
**Status**: Production Ready ✅
