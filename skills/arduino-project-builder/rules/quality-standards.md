# Quality Standards

All generated Arduino projects must adhere to these quality standards for production readiness.

## Core Requirements

### 1. Hardware Abstraction
- **config.h file:** Required for all projects with board detection and pin definitions
- **Conditional compilation:** Use #ifdef/#endif for board-specific code
- **Pin constants:** Define all pins as named constants, not magic numbers

### 2. Non-blocking Design
- **No delay() calls:** Use millis() timers for all timing requirements
- **EveryMs pattern:** Implement task scheduling without blocking
- **Responsive loop:** Main loop must complete within timing constraints

### 3. Error Handling
- **Sensor validation:** Check for NaN, out-of-range, and failure conditions
- **Graceful degradation:** Continue operation when non-critical components fail
- **Error states:** State machines must include error/default states

### 4. Diagnostics & Monitoring
- **Serial output:** Print status messages and sensor readings
- **Heartbeat indicators:** LED blinking or serial status updates
- **Debug levels:** Different verbosity levels for troubleshooting

### 5. Memory Safety
- **Bounds checking:** Validate array indices before access
- **CRC validation:** Use CRC for EEPROM and critical data storage
- **Memory monitoring:** Track SRAM usage on constrained boards

### 6. Documentation Standards
- **Wiring tables:** Clear text-based pin assignment documentation
- **Code comments:** Explain complex logic and hardware interactions
- **Usage instructions:** Include setup and operation procedures

### 7. Compilation Verification
- **Board compatibility:** Verify compilation for target board
- **Library dependencies:** Ensure all required libraries are available
- **Optimization flags:** Use appropriate compiler optimizations

## Code Quality Metrics

- **Cyclomatic complexity:** Keep functions under 10 complexity points
- **Function length:** Limit functions to 50 lines maximum
- **Global variables:** Minimize use, prefer local scope
- **Magic numbers:** Replace with named constants

## Testing Requirements

- **Unit testing:** Test individual components in isolation
- **Integration testing:** Verify component interactions
- **Performance testing:** Ensure timing requirements are met
- **Memory testing:** Validate memory usage under load