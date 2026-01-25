# Common Pitfalls to Avoid

Critical mistakes that can cause Arduino projects to fail, crash, or behave unexpectedly.

## ❌ Timing Pitfalls

### Never use `delay()` for timing
**Problem:** `delay()` blocks all execution, preventing other tasks from running.

```cpp
// WRONG - blocks everything
void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);  // Nothing else can happen here
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}
```

```cpp
// CORRECT - non-blocking timing
unsigned long lastBlink = 0;
const unsigned long BLINK_INTERVAL = 1000;

void loop() {
  unsigned long currentTime = millis();
  if (currentTime - lastBlink >= BLINK_INTERVAL) {
    digitalToggle(LED_PIN);
    lastBlink = currentTime;
  }
  // Other code can run here
}
```

### Never use signed types for millis() comparisons
**Problem:** `int` overflows at 32,767ms (~32 seconds), causing timing failures.

```cpp
// WRONG - will fail after 32 seconds
int startTime = millis();
if (millis() - startTime > 5000) { ... }

// CORRECT - use unsigned long
unsigned long startTime = millis();
if (millis() - startTime > 5000) { ... }
```

### Never ignore millis() overflow
**Problem:** `millis()` wraps to 0 every ~49 days, breaking timing calculations.

```cpp
// WRONG - fails when millis() overflows
if (millis() > previousTime + INTERVAL) { ... }

// CORRECT - handles overflow properly
if (millis() - previousTime >= INTERVAL) { ... }
```

## ❌ Hardware Initialization Pitfalls

### Never forget to call `begin()` on peripherals
**Problem:** Sensors and communication modules won't work without initialization.

```cpp
// WRONG - sensor won't respond
DHT dht(DHT_PIN, DHT_TYPE);
// Missing: dht.begin();

// CORRECT
DHT dht(DHT_PIN, DHT_TYPE);
dht.begin();  // Required initialization
```

### Never assume hardware is present without checking
**Problem:** Code crashes or hangs when hardware is missing.

```cpp
// WRONG - assumes sensor is connected
float temp = dht.readTemperature();
if (isnan(temp)) {
  // Handle error
}

// BETTER - check hardware availability
if (dht.begin()) {
  float temp = dht.readTemperature();
  // Use temperature
} else {
  Serial.println(F("DHT sensor not found"));
}
```

## ❌ Memory Management Pitfalls

### Never use String class on memory-constrained boards
**Problem:** String concatenation causes heap fragmentation on UNO.

```cpp
// WRONG on UNO - causes memory issues
String message = "Temperature: ";
message += String(temp);
Serial.println(message);

// CORRECT - use char arrays
char buffer[32];
snprintf(buffer, sizeof(buffer), "Temperature: %.1f", temp);
Serial.println(buffer);
```

### Never forget F() macro for strings on UNO
**Problem:** String literals consume precious RAM instead of flash.

```cpp
// WRONG - uses 20 bytes of RAM
Serial.println("Initializing sensor...");

// CORRECT - stores in flash memory
Serial.println(F("Initializing sensor..."));
```

## ❌ Input Handling Pitfalls

### Never mix polling and interrupt-based input
**Problem:** Inconsistent behavior and missed events.

```cpp
// WRONG - mixing approaches
volatile bool buttonPressed = false;

void buttonISR() {
  buttonPressed = true;
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {  // Polling
    // Handle press
  }
  if (buttonPressed) {  // Interrupt flag
    // Handle press again?
  }
}

// CORRECT - choose one approach
// Either pure polling with debouncing, or pure interrupt-driven
```

### Never debounce buttons incorrectly
**Problem:** False triggers from contact bounce.

```cpp
// WRONG - no debouncing
if (digitalRead(BUTTON_PIN) == LOW) {
  // Button press detected (but might be bounce)
}

// CORRECT - software debouncing
unsigned long lastDebounceTime = 0;
const unsigned long DEBOUNCE_DELAY = 50;
bool lastButtonState = HIGH;
bool buttonState;

void loop() {
  bool reading = digitalRead(BUTTON_PIN);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
  
  if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY) {
    if (reading != buttonState) {
      buttonState = reading;
      if (buttonState == LOW) {
        // Valid button press
      }
    }
  }
  lastButtonState = reading;
}
```

## ❌ Communication Pitfalls

### Never ignore I2C/SPI initialization failures
**Problem:** Silent failures lead to debugging nightmares.

```cpp
// WRONG - no error checking
Wire.begin();
Wire.beginTransmission(0x68);
Wire.write(0x00);
Wire.endTransmission();

// CORRECT - check for errors
Wire.begin();
Wire.beginTransmission(0x68);
byte error = Wire.endTransmission();
if (error == 0) {
  // Success - device found
} else {
  Serial.print(F("I2C error: "));
  Serial.println(error);
}
```

### Never use blocking Serial operations in time-critical code
**Problem:** `Serial.print()` can block for milliseconds.

```cpp
// WRONG in timing-critical sections
void loop() {
  unsigned long start = micros();
  // Time-critical operation
  Serial.println(micros() - start);  // Blocks execution
}

// CORRECT - buffer or use non-blocking approaches
char buffer[32];
snprintf(buffer, sizeof(buffer), "Time: %lu", micros() - start);
Serial.println(buffer);
```

## ❌ Data Handling Pitfalls

### Never access arrays without bounds checking
**Problem:** Buffer overflows corrupt memory.

```cpp
// WRONG - potential buffer overflow
char buffer[10];
for (int i = 0; i < 20; i++) {
  buffer[i] = data[i];  // Overflows buffer
}

// CORRECT - bounds checking
char buffer[10];
int copyLength = min(sizeof(buffer) - 1, dataLength);
memcpy(buffer, data, copyLength);
buffer[copyLength] = '\0';
```

### Never use floating point in interrupt service routines
**Problem:** Floating point operations are not reentrant and slow.

```cpp
// WRONG in ISR
volatile float temperature;
void sensorISR() {
  temperature = readSensor();  // Floating point in ISR
}

// CORRECT - use integer math in ISRs
volatile int32_t temperatureRaw;
void sensorISR() {
  temperatureRaw = analogRead(SENSOR_PIN);
}
// Convert to float in main code
```

## ✅ Best Practices Summary

- **Always use millis()** for non-blocking timing
- **Always check hardware initialization** return values
- **Always use F() macro** for strings on UNO
- **Always debounce buttons** properly
- **Always check array bounds** before access
- **Always handle millis() overflow** in timing calculations
- **Never use delay()** in production code
- **Never mix input handling strategies**
- **Never ignore error conditions**
- **Never use String class** on memory-constrained boards