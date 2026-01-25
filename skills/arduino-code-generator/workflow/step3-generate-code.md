# Step 3: Generate Code

Generate production-ready Arduino code following these comprehensive rules and best practices.

## Code Generation Rules

### 1. Include Statements
- Include all necessary `#include` statements at the top
- Use angle brackets for standard libraries: `#include <Wire.h>`
- Use quotes for custom headers: `#include "config.h"`
- Group includes logically (standard, then third-party, then custom)

### 2. Configuration Management
- Define pins in config.h style with conditional compilation
- Use `#ifdef` for board-specific configurations
- Define constants for magic numbers
- Group related constants together

### 3. Timing Patterns
- **Never use `delay()`** - always use `millis()` for non-blocking timing
- Use `unsigned long` for all time variables
- Handle millis() overflow (wraps every ~49 days)
- Implement proper timing comparisons

### 4. Memory Management
- Use `F()` macro for string literals on memory-constrained boards
- Avoid `String` class on UNO - use char arrays
- Implement bounds checking for all arrays
- Use `const` for read-only data
- Minimize global variables

### 5. Error Handling
- Check return values from peripheral initialization
- Provide meaningful error messages via Serial
- Implement fallback strategies for missing hardware
- Use appropriate error codes or states

### 6. Debugging Support
- Add Serial output for debugging at key points
- Include status messages during initialization
- Log errors and unusual conditions
- Comment "why" decisions were made, not "what" the code does

### 7. Code Structure
- Use clear, descriptive variable names
- Implement proper indentation and spacing
- Add comments for complex logic
- Separate concerns into functions
- Follow Arduino naming conventions

## Board-Specific Considerations

### Arduino UNO (ATmega328P, 2KB SRAM)
```cpp
// Use F() macro for all strings
Serial.println(F("Initializing sensor..."));

// Prefer char arrays over String
char buffer[32];

// Minimize buffer sizes
#define BUFFER_SIZE 64
```

### ESP32 (520KB SRAM, WiFi/BLE capable)
```cpp
// Can use larger buffers
#define BUFFER_SIZE 1024

// Leverage FreeRTOS
TaskHandle_t sensorTask;

// Enable WiFi patterns
#include <WiFi.h>
```

### RP2040 (264KB SRAM, dual-core)
```cpp
// Use PIO for timing-critical tasks
// Support USB host mode
// Multicore patterns available
```

## Code Template Structure

```cpp
// 1. Includes
#include <Wire.h>
#include <SPI.h>
#include "config.h"

// 2. Constants and Configuration
#define PIN_LED 13
#define INTERVAL_MS 1000
const char* DEVICE_NAME = "SensorNode";

// 3. Global Variables
unsigned long lastUpdate = 0;
bool sensorActive = false;

// 4. Function Declarations
void initializeHardware();
void updateSensor();
void handleErrors();

// 5. Setup Function
void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for serial on Leonardo/UNO
  
  Serial.println(F("Initializing..."));
  initializeHardware();
  Serial.println(F("Ready"));
}

// 6. Main Loop
void loop() {
  unsigned long currentTime = millis();
  
  // Handle millis() overflow
  if (currentTime - lastUpdate >= INTERVAL_MS) {
    updateSensor();
    lastUpdate = currentTime;
  }
  
  handleErrors();
}

// 7. Implementation Functions
void initializeHardware() {
  // Hardware initialization with error checking
}

void updateSensor() {
  // Sensor reading and processing
}

void handleErrors() {
  // Error detection and recovery
}
```

## Quality Assurance

Before finalizing code:
- ✅ Verify compilation on target board
- ✅ Check memory usage estimates
- ✅ Validate timing calculations
- ✅ Test error conditions
- ✅ Review against common pitfalls