# Common Datasheet Parameters Reference

Quick reference for understanding component datasheets.

## Electrical Ratings

### Voltage Parameters
| Parameter | Symbol | Meaning |
|-----------|--------|---------|
| Operating Voltage | VCC, VDD | Normal supply voltage range |
| Max Voltage | Vmax | Absolute maximum (do not exceed!) |
| Logic High | VIH | Minimum voltage for logic HIGH |
| Logic Low | VIL | Maximum voltage for logic LOW |
| Output High | VOH | Output voltage when HIGH |
| Output Low | VOL | Output voltage when LOW |

### Current Parameters
| Parameter | Symbol | Meaning |
|-----------|--------|---------|
| Operating Current | ICC, IDD | Normal current draw |
| Standby Current | ISB | Current in sleep/standby mode |
| Max Current | Imax | Maximum safe continuous current |
| Source Current | IOH | Max current pin can source (output HIGH) |
| Sink Current | IOL | Max current pin can sink (output LOW) |

## Communication Interface Parameters

### I2C
| Parameter | Typical Value | Notes |
|-----------|---------------|-------|
| Standard Mode | 100 kHz | Basic speed |
| Fast Mode | 400 kHz | Common for sensors |
| Fast Mode+ | 1 MHz | Higher performance |
| High Speed | 3.4 MHz | Requires special setup |
| Pull-up | 2.2kΩ-10kΩ | Required on SDA/SCL |

### SPI
| Parameter | Range | Notes |
|-----------|-------|-------|
| Clock Speed | 1-20+ MHz | Device dependent |
| Modes | 0, 1, 2, 3 | CPOL/CPHA settings |
| Bit Order | MSB/LSB first | Check datasheet |

### UART
| Parameter | Common Values | Notes |
|-----------|---------------|-------|
| Baud Rate | 9600, 115200 | Must match both ends |
| Data Bits | 8 | Standard |
| Stop Bits | 1 | Standard |
| Parity | None | Unless specified |

## Timing Parameters

| Parameter | Symbol | Meaning |
|-----------|--------|---------|
| Startup Time | tPU | Time from power-on to ready |
| Conversion Time | tCONV | ADC/sensor measurement time |
| Response Time | tRESP | Time to respond to input |
| Refresh Rate | - | How often output updates |

## Temperature Ratings

| Range | Min | Max | Notes |
|-------|-----|-----|-------|
| Commercial | 0°C | 70°C | Consumer devices |
| Industrial | -40°C | 85°C | Robust applications |
| Extended | -40°C | 125°C | Automotive/harsh |

## Common Unit Conversions

| From | To | Multiply by |
|------|----|-------------|
| mA | µA | 1000 |
| µA | mA | 0.001 |
| mW | W | 0.001 |
| MHz | kHz | 1000 |
| ms | µs | 1000 |
| µs | ms | 0.001 |

## Absolute Maximum Ratings ⚠️

**CRITICAL**: These are DAMAGE LIMITS, not operating conditions!
- Never exceed these values even momentarily
- Recommended operating conditions are LOWER
- No safety margin included

## Interpreting Accuracy Specs

### ±X% vs ±X Units
- **±5%**: Error is percentage of reading
- **±2°C**: Error is fixed amount regardless of reading

### Full Scale (FS) vs Reading
- **±1% FS**: Error relative to maximum range
- **±1% rdg**: Error relative to actual reading

## Common Gotchas

1. **5V vs 3.3V Logic**
   - Many modern sensors are 3.3V ONLY
   - Check "Absolute Maximum" voltage
   - Use level shifters if needed

2. **I2C Addresses**
   - May be shown as 7-bit or 8-bit
   - 7-bit: 0x3C, 8-bit: 0x78 (same device)
   - Some addresses are configurable

3. **Current Draw**
   - Datasheet shows typical, actual may vary
   - Add 20% margin for design
   - Check peak vs average current

4. **Pin Names**
   - VCC/VDD = Power positive
   - VSS/GND = Ground
   - NC = Not Connected
   - DNC = Do Not Connect

## Quick Lookup: Popular Components

| Component | Voltage | Interface | Address |
|-----------|---------|-----------|---------|
| DHT22 | 3.3-5V | 1-Wire | N/A |
| BME280 | 3.3V | I2C/SPI | 0x76/0x77 |
| SSD1306 | 3.3V | I2C/SPI | 0x3C/0x3D |
| MPU6050 | 3.3V | I2C | 0x68/0x69 |
| DS3231 | 3.3-5V | I2C | 0x68 |
| nRF24L01 | 3.3V | SPI | N/A |
