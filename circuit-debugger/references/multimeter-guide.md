# Multimeter Usage Guide for Beginners

## Safety First
- **NEVER** measure current directly across a power source (creates short circuit!)
- Start with highest range, work down
- Discharge capacitors before measuring resistance
- Don't measure live mains voltage as a beginner

## Essential Measurements

### DC Voltage (Most Common)
**Setting:** V⎓ or VDC, 20V range for Arduino projects

```
How to measure:
1. Set dial to DC Voltage (V with straight line)
2. Select 20V range (covers 0-20V)
3. Black probe → Ground/Negative
4. Red probe → Point to measure
5. Read display

           Red probe here
                ↓
    VCC ───[component]─── GND
                          ↑
                    Black probe here
```

**Interpreting Results:**
| Reading | Meaning |
|---------|---------|
| 4.8-5.2V | Good 5V rail |
| 3.2-3.4V | Good 3.3V rail |
| 0V | No power or open circuit |
| Negative value | Probes reversed |
| Unstable/jumping | Floating or noisy |

### Continuity Test
**Setting:** Diode/Continuity symbol (sounds like ))) )

```
How to use:
1. Set dial to continuity (beep symbol)
2. Touch probes together → should beep
3. Test connections → beep = connected

Testing a wire:
    [====WIRE====]
     ↑          ↑
   Probe      Probe
   
   Beep = Good wire
   No beep = Broken wire
```

**Use For:**
- Checking if wires are connected
- Finding broken traces on PCB
- Verifying solder joints
- Finding shorts (unexpected beeps!)

### Resistance
**Setting:** Ω (Ohms)

```
IMPORTANT: Remove component from circuit first!
Otherwise you measure parallel paths, wrong value.

How to measure:
1. Set to Ω range (start with 20kΩ)
2. Touch probes to component leads
3. If shows "1" or "OL", increase range
4. Read value

Common resistor values:
- 330Ω = LED current limiter
- 4.7kΩ = I2C pull-up
- 10kΩ = Common pull-up/down
```

### Current (Advanced - Use Carefully!)
**Setting:** A or mA

```
⚠️ WARNING: Must break circuit and insert meter IN SERIES!

WRONG (will blow fuse or damage meter):
    VCC ──[A]── GND  ← SHORT CIRCUIT!

CORRECT:
    VCC ──[A]──[Load]── GND
         ↑
    Meter measures current
    flowing through load
```

**Current Measurement Setup:**
```
Before:
    VCC ─────[LED+R]───── GND

After (insert meter):
    VCC ──[mA]──[LED+R]── GND
          ↑
    Break wire here,
    insert meter in gap
```

## Troubleshooting with Multimeter

### "Nothing Powers On"
```
1. Check battery/power supply voltage
   - Fresh 9V battery: 9.0-9.6V
   - Drained 9V battery: <7V
   - USB power: 4.75-5.25V

2. Check voltage at MCU VCC pin
   - If 0V: trace back to power source
   - If correct: MCU may be damaged

3. Check for shorts
   - Continuity between VCC and GND
   - Should NOT beep! If it does = short circuit
```

### "Component Gets Hot"
```
1. Immediately disconnect power!
2. Check for reversed polarity
3. Check for short circuits
4. Verify component voltage rating
5. Calculate if current is excessive
```

### "Sensor Gives Wrong Values"
```
1. Verify VCC voltage at sensor
2. Check signal voltage levels
3. Test with known-good values
4. Check for noise (unstable readings)
```

## Quick Reference Card

| What to Measure | Setting | Probes | Expected |
|-----------------|---------|--------|----------|
| Arduino 5V rail | VDC 20V | Red=5V pin, Black=GND | 4.8-5.2V |
| Arduino 3.3V | VDC 20V | Red=3.3V, Black=GND | 3.2-3.4V |
| Battery | VDC 20V | Red=+, Black=- | Rated voltage |
| Wire intact? | Continuity | Both ends | Beep |
| Resistor value | Ω | Both leads | Marked value |
| LED polarity | Diode | Either way | Shows ~0.6-2V one way |
| I2C pull-up | Ω | SDA/SCL to VCC | ~4.7kΩ |

## Budget Multimeter Recommendations
- **Beginner:** Any $15-25 auto-ranging meter
- **Recommended:** AstroAI DM6000AR, Kaiweets HT118A
- **Pro:** Fluke 117 (expensive but lifetime tool)

Key features needed:
- Auto-ranging (easier to use)
- Continuity beeper
- DC voltage to 20V+
- Current measurement (mA range)
