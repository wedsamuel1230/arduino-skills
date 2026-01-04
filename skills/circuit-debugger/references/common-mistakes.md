# Common Hardware Mistakes Gallery

## Beginner Hall of Fame (We've All Done These!)

### 1. Reversed LED Polarity
```
WRONG:                      CORRECT:
  [Short leg]─R─VCC         [Long leg]─R─VCC
  [Long leg]──GND           [Short leg]──GND

Remember: Long leg = Anode = Positive = +
Flat side of LED body = Cathode = Negative = -
```
**Symptom:** LED doesn't light up
**Fix:** Flip the LED around

### 2. Missing Current-Limiting Resistor
```
WRONG (will burn out LED):
  GPIO ──────[LED]────── GND

CORRECT:
  GPIO ──[330Ω]──[LED]── GND
```
**Symptom:** LED very bright then dies, or GPIO pin damaged
**Fix:** Always use 220Ω-1kΩ resistor with LEDs

### 3. Breadboard Power Rails Not Connected
```
Many breadboards have SPLIT power rails!

    [+]─────────  [+]─────────
    [-]─────────  [-]─────────
              ↑
          GAP HERE - not connected!
          
Add jumper wire to connect both halves
```
**Symptom:** Components on one side work, other side dead
**Fix:** Bridge the gap with jumper wires

### 4. Wrong Breadboard Row
```
Component leads must be in DIFFERENT rows:

WRONG (shorted):         CORRECT:
    A B C D E               A B C D E
 1 [===LED===]           1 [LED]
                         2     [LED]
Both legs in row 1       Legs in rows 1 and 2
= short circuit          = proper connection
```
**Symptom:** Component doesn't work or gets hot
**Fix:** Ensure leads span multiple rows

### 5. Forgetting Pull-Up Resistors on I2C
```
I2C REQUIRES pull-ups!

           VCC
            │
           [4.7kΩ]
            │
MCU SDA ───┴─── Sensor SDA
            
(Same for SCL line)
```
**Symptom:** I2C scanner finds nothing, or intermittent communication
**Fix:** Add 4.7kΩ pull-ups from SDA and SCL to VCC

### 6. 5V Sensor on 3.3V MCU (or vice versa)
```
ESP32 is 3.3V logic!

WRONG:
5V sensor ──────────→ ESP32 GPIO
                      (can damage ESP32!)

CORRECT:
5V sensor ──[Level Shifter]──→ ESP32 GPIO
```
**Symptom:** Erratic behavior, sensor works briefly then MCU dies
**Fix:** Use level shifter or voltage divider

### 7. Motor Connected Directly to GPIO
```
WRONG (will damage MCU):
GPIO ───────[MOTOR]─── GND
      ↑
  Motors need more current
  than GPIO can provide!

CORRECT:
GPIO ──[Driver]──[MOTOR]─── Motor Power
          │
        Separate power supply
```
**Symptom:** Motor doesn't move, MCU resets, or GPIO burns out
**Fix:** Use motor driver (L298N, TB6612, L293D)

### 8. Missing Flyback Diode on Inductive Loads
```
Motors/relays generate voltage spikes when turned off!

CORRECT (with flyback diode):
    ┌────[DIODE]────┐
    │    ← stripe   │
    └──[MOTOR/RELAY]┘
    │               │
  Driver          GND
```
**Symptom:** Random resets, erratic behavior, damaged components
**Fix:** Add flyback diode (1N4001-1N4007) across motor/relay

### 9. Servo Power from Arduino 5V Pin
```
WRONG:
Arduino 5V ──→ Servo VCC
               (can cause brownouts!)

CORRECT:
External 5V ──→ Servo VCC
             └─→ Arduino GND (connect grounds!)
```
**Symptom:** Servo jitters, Arduino resets, erratic behavior
**Fix:** Use external 5V power supply for servos

### 10. Floating Input Pins
```
WRONG:
Button ──────→ GPIO (set as INPUT)
              ↑
          Pin floats when button open
          Reads random HIGH/LOW

CORRECT:
         VCC
          │
       [10kΩ] Pull-up
          │
Button ───┴──→ GPIO (INPUT)
  │
 GND

Or use INPUT_PULLUP mode:
  pinMode(BUTTON_PIN, INPUT_PULLUP);
```
**Symptom:** Random triggering, noise-sensitive inputs
**Fix:** Use INPUT_PULLUP or external pull-up/down resistor

## Intermediate Mistakes

### 11. Ground Loops
```
Multiple ground paths can create noise:

WRONG:                    CORRECT:
MCU ─┬─ Sensor          MCU ────┬─ Sensor
     └─ Motor Driver            │
     └─ Power GND        Star ground
                         all to one point
```
**Symptom:** Noisy sensor readings, especially when motors run
**Fix:** Use star grounding, separate analog/digital grounds

### 12. Inadequate Decoupling Capacitors
```
Every IC needs decoupling!

      VCC
       │
   [100nF] ← Close to IC!
       │
    [IC]
       │
      GND
```
**Symptom:** Occasional glitches, communication errors, resets
**Fix:** Add 100nF ceramic capacitor close to every IC's VCC pin

### 13. Long I2C Wires
```
I2C is designed for short distances (<30cm)

Long wires = increased capacitance = signal degradation

Solutions:
1. Shorter wires
2. Lower I2C speed (Wire.setClock(100000))
3. Stronger pull-ups (2.2kΩ instead of 4.7kΩ)
4. Use I2C extender chip for long runs
```
**Symptom:** I2C works close, fails when wires extended
**Fix:** Keep I2C wires short, or use I2C bus extender

### 14. PWM Frequency Mismatch
```
Some components need specific PWM frequencies:

- LEDs: Any frequency >100Hz (no flicker)
- Motors: 1-20kHz typical
- Servos: 50Hz (20ms period) required!
- ESCs: Varies, check datasheet
```
**Symptom:** Component behaves strangely, servo jitters
**Fix:** Match PWM frequency to component requirements

### 15. Shared SPI Without Proper CS Handling
```
Multiple SPI devices need separate Chip Select:

      CS1  CS2
       │    │
      [A]  [B]
       ↑    ↑
      MOSI/MISO/SCK shared

IMPORTANT: Only ONE CS low at a time!
```
**Symptom:** SPI devices interfere with each other
**Fix:** Ensure all CS pins HIGH before selecting device

## Debug Checklist Template

```
□ Power LED on MCU lit?
□ Correct voltage at VCC?
□ All grounds connected?
□ Correct pin assignments in code?
□ Component polarity correct?
□ Resistors where needed?
□ Pull-ups on I2C?
□ Level shifters for mixed voltage?
□ Decoupling caps near ICs?
□ Flyback diodes on motors/relays?
□ External power for high-current loads?
□ No floating input pins?
```
