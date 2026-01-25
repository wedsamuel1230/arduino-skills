# Code Output Template

Standardized template for generating Arduino code snippets with consistent structure and documentation.

## Template Structure

```cpp
/*
 * [Pattern Name] - [Brief Description]
 * Generated for [Board Type] using Arduino Code Generator
 *
 * Features:
 * - [List key features]
 * - [List capabilities]
 *
 * Hardware Requirements:
 * - [Board type]
 * - [List required components]
 *
 * Connections:
 * [ASCII wiring diagram]
 *
 * Usage:
 * 1. Upload this sketch to your Arduino
 * 2. Open Serial Monitor at 9600 baud
 * 3. [Expected behavior description]
 *
 * Expected Output:
 * [Sample Serial output]
 */

#include <[Required Libraries]>

// Configuration
#define [PIN_NAME] [PIN_NUMBER]
#define [CONSTANT_NAME] [VALUE]

// Timing constants
const unsigned long [INTERVAL_NAME] = [VALUE_MS];

// Global variables
unsigned long [timing_variable] = 0;
[Other global variables]

// Function declarations
void [function_name]();
[Other function declarations]

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  #if defined(ARDUINO_ARCH_AVR)
    while (!Serial); // Wait for serial on Leonardo/UNO
  #endif

  Serial.println(F("[Initialization message]"));

  // Hardware initialization
  [hardware_init_code]

  // Verify initialization
  if ([init_check_condition]) {
    Serial.println(F("[Success message]"));
  } else {
    Serial.println(F("[Error message]"));
    while (1); // Halt on critical error
  }
}

void loop() {
  // Non-blocking timing
  unsigned long currentTime = millis();

  // Handle millis() overflow
  if (currentTime - [timing_variable] >= [INTERVAL_NAME]) {
    [timed_action_code]
    [timing_variable] = currentTime;
  }

  // Main logic
  [main_logic_code]

  // Error handling
  [error_handling_code]
}

// Implementation functions
void [function_name]() {
  [function_implementation]
}

[Additional helper functions]
```

## Template Customization Guide

### Header Comments
- **Pattern Name**: Descriptive name (e.g., "DHT22 Temperature Sensor")
- **Board Type**: Target board (UNO, ESP32, RP2040)
- **Features List**: 3-5 bullet points of capabilities
- **Hardware Requirements**: Specific components needed
- **Connections**: ASCII art wiring diagram
- **Usage Steps**: Numbered steps for user
- **Expected Output**: Sample Serial monitor output

### Include Section
- Group standard libraries first (`<Wire.h>`, `<SPI.h>`)
- Then third-party libraries (`<DHT.h>`)
- Finally custom headers (`"config.h"`)

### Configuration Section
- Use `#define` for pin numbers and constants
- Group related constants together
- Use descriptive names in ALL_CAPS

### Timing Section
- Define timing intervals as `const unsigned long`
- Use milliseconds for all time values
- Name intervals descriptively (e.g., `READ_INTERVAL_MS`)

### Global Variables
- Initialize timing variables to 0
- Use descriptive names
- Minimize global scope

### Setup Function
- Always initialize Serial first
- Use F() macro for strings on UNO
- Include hardware initialization checks
- Provide clear success/error messages

### Loop Function
- Implement proper millis() timing with overflow protection
- Keep loop() responsive (no blocking operations)
- Include error checking and recovery

### Function Organization
- Declare all functions at top (Arduino requirement)
- Implement functions after loop()
- Use clear, descriptive names
- Single responsibility per function

## Board-Specific Templates

### Arduino UNO Template
```cpp
// Memory-optimized for 2KB SRAM
#define BUFFER_SIZE 64
char buffer[BUFFER_SIZE];

// Use F() macro for all strings
Serial.println(F("UNO-optimized output"));
```

### ESP32 Template
```cpp
// WiFi-capable with FreeRTOS
#include <WiFi.h>

// Task for concurrent operations
TaskHandle_t sensorTask;
```

### RP2040 Template
```cpp
// Dual-core capable
#include <pico/multicore.h>

// PIO for precise timing if needed
```

## Error Handling Template

```cpp
// Standardized error handling
bool initializeHardware() {
  if (![init_success_condition]) {
    Serial.println(F("ERROR: Hardware initialization failed"));
    return false;
  }
  return true;
}

void handleErrors() {
  static unsigned long lastErrorCheck = 0;
  const unsigned long ERROR_CHECK_INTERVAL = 5000;

  if (millis() - lastErrorCheck >= ERROR_CHECK_INTERVAL) {
    if ([error_condition]) {
      Serial.println(F("WARNING: [specific error]"));
      [recovery_action]
    }
    lastErrorCheck = millis();
  }
}
```

## Integration Template

When combining patterns, use this structure:

```cpp
// Primary pattern includes
#include <[primary_pattern_libs]>

// Secondary pattern includes
#include <[secondary_pattern_libs]>

// Shared configuration
#define SHARED_PIN [pin_number]

// Primary pattern variables
[primary_variables]

// Secondary pattern variables
[secondary_variables]

// Initialize both patterns
void setup() {
  initPrimaryPattern();
  initSecondaryPattern();
}

void loop() {
  updatePrimaryPattern();
  updateSecondaryPattern();
}
```

## Testing Template

Include this testing section for validation:

```cpp
// Testing and debugging
#define DEBUG_MODE true

void debugOutput() {
  #if DEBUG_MODE
    Serial.print(F("Debug: "));
    Serial.println([debug_value]);
  #endif
}

// Call debugOutput() at key points
```

## Documentation Standards

- **Comments**: Explain "why" decisions, not "what" code does
- **Variable Names**: descriptive and consistent
- **Function Names**: verb-based (readSensor, updateDisplay)
- **Constants**: ALL_CAPS_WITH_UNDERSCORES
- **Indentation**: 2 spaces (Arduino IDE default)