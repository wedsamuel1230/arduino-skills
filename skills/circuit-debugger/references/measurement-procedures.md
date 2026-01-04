# Circuit Debugging Measurement Procedures

## Multimeter Basics

### Safety First
- Never measure resistance in a powered circuit
- Start with highest range when unknown
- Check meter leads for damage before use
- Use proper probes (not worn/broken tips)

### Common Measurements

## 1. Continuity Testing

**Purpose:** Check if two points are electrically connected

**Procedure:**
1. Turn off/disconnect power
2. Set multimeter to continuity mode (🔊 symbol)
3. Touch probes to two points
4. Beep = connected, No beep = open

**When to Use:**
- Verify solder joints
- Check for broken traces
- Test switches/buttons
- Find shorts

**Expected Results:**
| Component | Should Beep? |
|-----------|--------------|
| Wire | Yes |
| Closed switch | Yes |
| Open switch | No |
| Diode (forward) | Yes (with resistance) |
| Diode (reverse) | No |
| Capacitor | Brief beep, then no |

---

## 2. DC Voltage Measurement

**Purpose:** Measure voltage between two points

**Procedure:**
1. Set meter to DC voltage (V⎓)
2. Select appropriate range (or auto-range)
3. Black probe to ground/reference
4. Red probe to measurement point
5. Read display

**Common Voltages:**
| Source | Expected |
|--------|----------|
| USB | 4.75-5.25V |
| LiPo battery | 3.0-4.2V |
| 3.3V regulator | 3.2-3.4V |
| 5V regulator | 4.9-5.1V |
| Arduino 5V pin | 4.5-5.5V |
| Arduino 3.3V pin | 3.1-3.5V |

**Troubleshooting:**
- 0V = No power, broken connection
- Lower than expected = Overloaded, bad regulator
- Higher than expected = Check regulator, source

---

## 3. Current Measurement

**Purpose:** Measure current flowing through circuit

**Procedure:**
1. **BREAK** the circuit where you want to measure
2. Set meter to DC current (A⎓)
3. Connect meter IN SERIES (current flows through meter)
4. Red to upstream, black to downstream
5. Read display

**⚠️ WARNING:**
- Never connect ammeter in parallel!
- Use correct port (mA vs 10A)
- Start with highest range

**Typical Currents:**
| State | Current |
|-------|---------|
| Arduino Uno idle | 40-50mA |
| ESP32 WiFi active | 80-250mA |
| ESP32 deep sleep | 10-150µA |
| LED (typical) | 10-20mA |
| Servo idle | 10-20mA |
| Servo moving | 100-500mA |

---

## 4. Resistance Measurement

**Purpose:** Measure resistance of component or connection

**Procedure:**
1. **POWER OFF** - Never measure resistance in live circuit!
2. Set meter to Ω (ohms)
3. Touch probes to component leads
4. Read display

**Component Values:**
| Component | Typical Resistance |
|-----------|-------------------|
| Wire/trace | <1Ω |
| LED (forward) | 20-200Ω |
| Pull-up resistor | 1kΩ-10kΩ |
| Potentiometer | Varies with position |
| Thermistor | Varies with temp |
| Open circuit | OL (overload) |
| Short circuit | 0Ω |

---

## 5. Diode/LED Testing

**Purpose:** Test diode functionality and forward voltage

**Procedure:**
1. Set meter to diode test mode (▷|)
2. Red probe to anode (+), black to cathode (-)
3. Read forward voltage drop
4. Reverse probes - should show OL

**Expected Forward Voltages:**
| Diode Type | Forward Voltage |
|------------|-----------------|
| Silicon (1N4148) | 0.6-0.7V |
| Schottky | 0.2-0.4V |
| Red LED | 1.8-2.2V |
| Green LED | 2.0-2.4V |
| Blue/White LED | 3.0-3.4V |
| Zener (reverse) | Zener voltage |

---

## Common Debug Scenarios

### Scenario 1: Device Not Powering On

**Checklist:**
```
□ Check power source voltage
□ Check regulator input voltage
□ Check regulator output voltage
□ Check for shorts (0Ω between VCC and GND)
□ Feel for hot components
□ Check fuse/polyfuse if present
```

### Scenario 2: Intermittent Operation

**Checklist:**
```
□ Check all solder joints (cold joints?)
□ Wiggle wires while measuring voltage
□ Check connector seating
□ Look for loose screws/standoffs touching traces
□ Check power under load vs idle
```

### Scenario 3: Sensor Not Working

**Checklist:**
```
□ Verify power at sensor VCC pin
□ Check I2C/SPI connections with scope/logic analyzer
□ Run I2C scanner to find address
□ Verify pull-up resistors present for I2C
□ Check signal levels match MCU voltage
```

### Scenario 4: Motor/Actuator Issues

**Checklist:**
```
□ Measure motor supply voltage
□ Check driver IC is getting logic power
□ Verify PWM signal present
□ Check for proper ground connection
□ Test motor directly with power supply
□ Check current - motor might be stalled
```

---

## Logic Level Reference

| Logic Family | LOW | HIGH | Note |
|--------------|-----|------|------|
| 5V TTL | 0-0.8V | 2.0-5V | Arduino Uno |
| 5V CMOS | 0-1.5V | 3.5-5V | ATmega328 |
| 3.3V CMOS | 0-1.0V | 2.3-3.3V | ESP32, RP2040 |
| 1.8V CMOS | 0-0.6V | 1.2-1.8V | Some sensors |

**Level Shifting Required When:**
- 5V Arduino ↔ 3.3V sensor
- 3.3V MCU ↔ 5V display
- Any mixed-voltage I2C bus

---

## Oscilloscope Quick Reference

### When Multimeter Isn't Enough:

Use oscilloscope for:
- PWM signal verification
- Serial communication debugging
- Timing-critical signals
- Noise analysis
- I2C/SPI bus issues

### Common Signals:

**PWM:**
- Square wave
- Check frequency and duty cycle
- Look for clean edges

**I2C:**
- SDA: Data, bidirectional
- SCL: Clock, master-driven
- Both idle HIGH (pull-ups)
- Look for ACK bits

**UART/Serial:**
- Idle HIGH
- Start bit (LOW)
- 8 data bits
- Stop bit (HIGH)

---

## Quick Debug Commands (Arduino Serial)

```cpp
// Print all pin states
void debugPins() {
    for (int i = 0; i < 14; i++) {
        Serial.print("D"); Serial.print(i);
        Serial.print(": "); Serial.println(digitalRead(i));
    }
    for (int i = 0; i < 6; i++) {
        Serial.print("A"); Serial.print(i);
        Serial.print(": "); Serial.println(analogRead(i));
    }
}

// Measure execution time
unsigned long start = micros();
// ... code to measure ...
unsigned long duration = micros() - start;
Serial.print("Duration: "); Serial.print(duration); Serial.println(" µs");

// Memory check
extern int __heap_start, *__brkval;
int freeMemory() {
    int v;
    return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}
```
