---
name: code-review-facilitator
description: Automated code review for Arduino/ESP32/RP2040 projects focusing on best practices, memory safety, and common pitfalls. Use when user wants code feedback, says "review my code", needs help improving code quality, or before finalizing a project. Generates actionable checklists and specific improvement suggestions.
metadata: {triggers: "review embedded code, Arduino code quality, memory safety, code feedback"}
---

# Code Review Facilitator

Provides systematic code review for microcontroller projects.

## Resources

This skill includes bundled tools:

- **scripts/analyze_code.py** - Static analyzer detecting 15+ common Arduino issues

## Quick Start

**Analyze a file:**
```bash
uv run --no-project scripts/analyze_code.py sketch.ino
```

**Analyze entire project:**
```bash
uv run --no-project scripts/analyze_code.py --dir /path/to/project
```

**Interactive mode (paste code):**
```bash
uv run --no-project scripts/analyze_code.py --interactive
```

**Filter by severity:**
```bash
uv run --no-project scripts/analyze_code.py sketch.ino --severity warning
```

## When to Use
- "Review my code"
- "Is this code okay?"
- "How can I improve this?"
- Before publishing to GitHub
- After completing a feature
- When code "works but feels wrong"

---

## Review Categories

### 1. 🏗️ Structure & Organization

**Check For:**
```
□ Single responsibility - each function does ONE thing
□ File organization - separate concerns (config, sensors, display, network)
□ Consistent naming convention (camelCase for variables, UPPER_CASE for constants)
□ Reasonable function length (< 50 lines ideally)
□ Header comments explaining purpose
```

**Common Issues:**

| Issue | Bad | Good |
|-------|-----|------|
| God function | 200-line `loop()` | Split into `readSensors()`, `updateDisplay()`, etc. |
| Mixed concerns | WiFi code in sensor file | Separate network.cpp/h |
| Unclear names | `int x, temp1, val;` | `int sensorReading, temperatureC;` |

**Example Refactoring:**
```cpp
// ❌ Bad: Everything in loop()
void loop() {
  // 50 lines of sensor reading
  // 30 lines of display update
  // 40 lines of network code
}

// ✅ Good: Organized functions
void loop() {
  SensorData data = readAllSensors();
  updateDisplay(data);
  if (shouldTransmit()) {
    sendToServer(data);
  }
  handleSleep();
}
```

---

### 2. 💾 Memory Safety

**Critical Checks:**
```
□ No String class in time-critical code (use char arrays)
□ Buffer sizes declared as constants
□ Array bounds checking
□ No dynamic memory allocation in loop()
□ Static buffers for frequently used strings
```

**Memory Issues Table:**

| Issue | Problem | Solution |
|-------|---------|----------|
| String fragmentation | Heap corruption over time | Use char arrays, snprintf() |
| Stack overflow | Large local arrays | Use static/global, reduce size |
| Buffer overflow | strcpy without bounds | Use strncpy, snprintf |
| Memory leak | malloc without free | Avoid dynamic allocation |

**Safe String Handling:**
```cpp
// ❌ Dangerous: String class in loop
void loop() {
  String msg = "Temp: " + String(temp) + "C";  // Fragments heap
  Serial.println(msg);
}

// ✅ Safe: Static buffer with snprintf
void loop() {
  static char msg[32];
  snprintf(msg, sizeof(msg), "Temp: %.1fC", temp);
  Serial.println(msg);
}

// ✅ Safe: F() macro for flash strings
Serial.println(F("This string is in flash, not RAM"));
```

**Memory Monitoring:**
```cpp
// Add to setup() for debugging
Serial.print(F("Free heap: "));
Serial.println(ESP.getFreeHeap());

// Periodic check in loop()
if (ESP.getFreeHeap() < 10000) {
  Serial.println(F("WARNING: Low memory!"));
}
```

---

### 3. 🔢 Magic Numbers & Constants

**Check For:**
```
□ No unexplained numbers in code
□ Pin assignments in config.h
□ Timing values named
□ Threshold values documented
```

**Examples:**
```cpp
// ❌ Bad: Magic numbers everywhere
if (analogRead(A0) > 512) {
  digitalWrite(4, HIGH);
  delay(1500);
}

// ✅ Good: Named constants
// config.h
#define MOISTURE_SENSOR_PIN     A0
#define PUMP_RELAY_PIN          4
#define MOISTURE_THRESHOLD      512   // ~50% soil moisture
#define PUMP_RUN_TIME_MS        1500  // 1.5 second watering

// main.ino
if (analogRead(MOISTURE_SENSOR_PIN) > MOISTURE_THRESHOLD) {
  digitalWrite(PUMP_RELAY_PIN, HIGH);
  delay(PUMP_RUN_TIME_MS);
}
```

---

### 4. ⚠️ Error Handling

**Check For:**
```
□ Sensor initialization verified
□ Network connections have timeouts
□ File operations check return values
□ Graceful degradation when components fail
□ User feedback for errors (LED, serial, display)
```

**Error Handling Patterns:**
```cpp
// ❌ Bad: Assume everything works
void setup() {
  bme.begin(0x76);  // What if it fails?
}

// ✅ Good: Check and handle failures
void setup() {
  Serial.begin(115200);
  
  if (!bme.begin(0x76)) {
    Serial.println(F("BME280 not found!"));
    errorBlink(ERROR_SENSOR);  // Visual feedback
    // Either halt or continue without sensor
    sensorAvailable = false;
  }
  
  // WiFi with timeout
  WiFi.begin(SSID, PASSWORD);
  unsigned long startAttempt = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startAttempt > WIFI_TIMEOUT_MS) {
      Serial.println(F("WiFi failed - continuing offline"));
      wifiAvailable = false;
      break;
    }
    delay(500);
  }
}
```

---

### 5. ⏱️ Timing & Delays

**Check For:**
```
□ No blocking delay() in main loop (except simple projects)
□ millis() overflow handled (after 49 days)
□ Debouncing for buttons/switches
□ Rate limiting for sensors/network
```

**Non-Blocking Pattern:**
```cpp
// ❌ Bad: Blocking delays
void loop() {
  readSensor();
  delay(1000);  // Blocks everything for 1 second
}

// ✅ Good: Non-blocking with millis()
unsigned long previousMillis = 0;
const unsigned long INTERVAL = 1000;

void loop() {
  unsigned long currentMillis = millis();
  
  // Handle button immediately (responsive)
  checkButton();
  
  // Sensor reading at interval
  if (currentMillis - previousMillis >= INTERVAL) {
    previousMillis = currentMillis;
    readSensor();
  }
}

// ✅ millis() overflow safe (works after 49 days)
// The subtraction handles overflow automatically with unsigned math
```

**Debouncing:**
```cpp
// Button debouncing
const unsigned long DEBOUNCE_MS = 50;
unsigned long lastDebounce = 0;
int lastButtonState = HIGH;
int buttonState = HIGH;

void checkButton() {
  int reading = digitalRead(BUTTON_PIN);
  
  if (reading != lastButtonState) {
    lastDebounce = millis();
  }
  
  if ((millis() - lastDebounce) > DEBOUNCE_MS) {
    if (reading != buttonState) {
      buttonState = reading;
      if (buttonState == LOW) {
        handleButtonPress();
      }
    }
  }
  lastButtonState = reading;
}
```

---

### 6. 🔌 Hardware Interactions

**Check For:**
```
□ Pin modes set in setup()
□ Pull-up/pull-down resistors considered
□ Voltage levels compatible (3.3V vs 5V)
□ Current limits respected
□ Proper power sequencing
```

**Pin Configuration:**
```cpp
// ❌ Bad: Missing or incorrect pin modes
digitalWrite(LED_PIN, HIGH);  // Works by accident on some boards

// ✅ Good: Explicit configuration
void setup() {
  // Outputs
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  
  // Inputs with pull-up (button connects to GND)
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // Analog input (no pinMode needed but document it)
  // SENSOR_PIN is analog input - no pinMode required
  
  // Set safe initial states
  digitalWrite(RELAY_PIN, LOW);  // Relay off at start
}
```

---

### 7. 📡 Network & Communication

**Check For:**
```
□ Credentials not hardcoded (use config file)
□ Connection retry logic
□ Timeout handling
□ Secure connections (HTTPS where possible)
□ Data validation
```

**Secure Credential Handling:**
```cpp
// ❌ Bad: Credentials in main code
WiFi.begin("MyNetwork", "password123");

// ✅ Good: Separate config file (add to .gitignore)
// config.h
#ifndef CONFIG_H
#define CONFIG_H

#define WIFI_SSID     "your-ssid"
#define WIFI_PASSWORD "your-password"
#define API_KEY       "your-api-key"

#endif

// .gitignore
config.h
```

---

### 8. 🔋 Power Efficiency

**Check For:**
```
□ Unused peripherals disabled
□ Appropriate sleep modes used
□ WiFi off when not needed
□ LED brightness reduced (PWM)
□ Sensor power controlled
```

**Power Optimization:**
```cpp
// ESP32 power management
void goToSleep(int seconds) {
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  btStop();
  
  esp_sleep_enable_timer_wakeup(seconds * 1000000ULL);
  esp_deep_sleep_start();
}

// Sensor power control
#define SENSOR_POWER_PIN 25

void readSensorWithPowerControl() {
  digitalWrite(SENSOR_POWER_PIN, HIGH);  // Power on
  delay(100);  // Stabilization time
  
  int value = analogRead(SENSOR_PIN);
  
  digitalWrite(SENSOR_POWER_PIN, LOW);   // Power off
  return value;
}
```

---

## Review Checklist Generator

Generate project-specific checklist:

```markdown
## Code Review Checklist for [Project Name]

### Critical (Must Fix)
- [ ] Memory: No String in loop()
- [ ] Safety: All array accesses bounds-checked
- [ ] Error: Sensor init failures handled

### Important (Should Fix)
- [ ] No magic numbers
- [ ] Non-blocking delays where possible
- [ ] Timeouts on all network operations

### Nice to Have
- [ ] F() macro for string literals
- [ ] Consistent naming convention
- [ ] Comments for complex logic

### Platform-Specific (ESP32)
- [ ] WiFi reconnection logic
- [ ] Brownout detector consideration
- [ ] Deep sleep properly configured
```

---

## Code Smell Detection

### Automatic Red Flags

| Pattern | Severity | Action |
|---------|----------|--------|
| `String +` in loop() | 🔴 Critical | Replace with snprintf |
| `delay(>100)` in loop() | 🟡 Warning | Consider millis() |
| `while(1)` without yield() | 🔴 Critical | Add yield() or refactor |
| Hardcoded credentials | 🔴 Critical | Move to config.h |
| `malloc/new` without `free/delete` | 🔴 Critical | Track allocations |
| `sprintf` (not snprintf) | 🟡 Warning | Use snprintf for safety |
| Global variables without `volatile` for ISR | 🔴 Critical | Add volatile keyword |

---

## Review Response Template

```markdown
## Code Review Summary

**Overall Assessment:** ⭐⭐⭐☆☆ (3/5)

### 🔴 Critical Issues (Fix Before Use)
1. **Memory leak in line 45** - String concatenation in loop()
   - Current: `String msg = "Value: " + String(val);`
   - Fix: Use `snprintf(buffer, sizeof(buffer), "Value: %d", val);`

### 🟡 Important Issues (Fix Soon)
1. **Missing error handling** - BME280 init not checked
2. **Magic number** - `delay(1500)` unexplained

### 🟢 Suggestions (Nice to Have)
1. Consider adding F() macro to Serial.print strings
2. Function `readAllSensors()` could be split

### ✅ Good Practices Found
- Clear variable naming
- Consistent formatting
- Good use of constants in config.h

### Recommended Next Steps
1. Fix critical memory issue first
2. Add sensor error handling
3. Run memory monitoring to verify fix
```

---

## Quick Reference Commands

```cpp
// Memory debugging
Serial.printf("Free heap: %d bytes\n", ESP.getFreeHeap());
Serial.printf("Min free heap: %d bytes\n", ESP.getMinFreeHeap());

// Stack high water mark (FreeRTOS)
Serial.printf("Stack remaining: %d bytes\n", uxTaskGetStackHighWaterMark(NULL));

// Find I2C devices
void scanI2C() {
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.printf("Found device at 0x%02X\n", addr);
    }
  }
}
```

## Shared Output Contract
See [the shared Arduino skill contract](../../docs/arduino-skill-contract.md).
