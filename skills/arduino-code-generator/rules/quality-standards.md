# Quality Standards

All generated Arduino code must adhere to these quality standards for production readiness.

## Compilation Requirements
- ✅ **Compile without warnings** on Arduino IDE 1.8.x and 2.x
- ✅ **No deprecated function usage** (avoid old Arduino APIs)
- ✅ **Proper include guards** for custom headers
- ✅ **Correct preprocessor directives** (#ifdef, #define, etc.)

## Timing and Concurrency
- ✅ **Use unsigned long for millis() timing** - never signed types
- ✅ **Handle overflow conditions** - millis() wraps every ~49 days
- ✅ **Never use delay()** for timing-critical operations
- ✅ **Implement proper timing comparisons** with overflow protection

```cpp
// Correct timing implementation
unsigned long previousTime = 0;
const unsigned long INTERVAL = 1000;

void loop() {
  unsigned long currentTime = millis();
  if (currentTime - previousTime >= INTERVAL) {
    // Execute timed action
    previousTime = currentTime;
  }
}
```

## Memory Safety
- ✅ **Include bounds checking** for all array operations
- ✅ **Use const for read-only data** to prevent accidental modification
- ✅ **Define magic numbers as named constants**
- ✅ **Avoid buffer overflows** through proper sizing
- ✅ **Use F() macro** for strings on memory-constrained boards

```cpp
// Memory-safe implementations
#define BUFFER_SIZE 64
char buffer[BUFFER_SIZE];

const char* SENSOR_NAME = "DHT22";
const uint8_t PIN_LED = 13;

// Use F() macro on UNO
Serial.println(F("Sensor initialized"));
```

## Error Handling
- ✅ **Check return values** from peripheral initialization functions
- ✅ **Provide meaningful error messages** via Serial output
- ✅ **Implement fallback strategies** for missing hardware
- ✅ **Handle edge cases** gracefully (null pointers, invalid data)

```cpp
// Proper error handling
bool initializeSensor() {
  if (!sensor.begin()) {
    Serial.println(F("ERROR: Sensor initialization failed"));
    return false;
  }
  Serial.println(F("Sensor initialized successfully"));
  return true;
}
```

## Code Structure
- ✅ **Clear, descriptive variable names** following Arduino conventions
- ✅ **Consistent indentation** (2 or 4 spaces, or Arduino IDE default)
- ✅ **Logical function organization** with single responsibilities
- ✅ **Proper comment placement** explaining "why" not "what"

## Board Compatibility
- ✅ **Test compilation** on target boards (UNO, ESP32, RP2040)
- ✅ **Account for board-specific limitations** (memory, pins, features)
- ✅ **Use conditional compilation** for board-specific code
- ✅ **Document board requirements** and compatibility

## Performance Standards
- ✅ **Minimize blocking operations** in loop()
- ✅ **Optimize for power consumption** when applicable
- ✅ **Use appropriate data types** for the task
- ✅ **Avoid unnecessary computations** in tight loops

## Testing Requirements
- ✅ **Provide expected output** for verification
- ✅ **Include debugging Serial output** for troubleshooting
- ✅ **Document test procedures** and expected behavior
- ✅ **Handle common failure modes** gracefully

## Documentation Standards
- ✅ **Include setup instructions** with wiring diagrams
- ✅ **Document configuration options** and parameters
- ✅ **Explain integration points** with other patterns
- ✅ **Provide troubleshooting guidance** for common issues