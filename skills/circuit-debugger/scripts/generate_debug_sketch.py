#!/usr/bin/env python3
"""
Debug Sketch Generator - Creates diagnostic Arduino sketches

Generates diagnostic code for common debugging tasks:
- I2C bus scanner
- SPI device tester
- GPIO pin tester
- Serial loopback test
- Voltage/ADC checker
- PWM output tester
- Interrupt tester

Usage:
    uv run generate_debug_sketch.py --i2c
    uv run generate_debug_sketch.py --gpio --pins 2,3,4,5
    uv run generate_debug_sketch.py --adc --pins A0,A1,A2
    uv run generate_debug_sketch.py --all --output debug_suite.ino
"""

import argparse
from typing import List, Optional

# =============================================================================
# Sketch Templates
# =============================================================================

I2C_SCANNER = '''/*
 * I2C Bus Scanner
 * Scans for all connected I2C devices and reports addresses
 * 
 * Wiring:
 *   SDA -> A4 (Uno) or 21 (Mega) or GPIO21 (ESP32) or GP4 (Pico)
 *   SCL -> A5 (Uno) or 20 (Mega) or GPIO22 (ESP32) or GP5 (Pico)
 *   
 * Common I2C addresses:
 *   0x27, 0x3F - LCD displays
 *   0x3C, 0x3D - OLED displays (SSD1306)
 *   0x68 - DS3231 RTC, MPU6050
 *   0x76, 0x77 - BME280/BMP280
 *   0x48-0x4F - PCF8591, ADS1115
 *   0x20-0x27 - PCF8574 I/O expander
 *   0x50-0x57 - EEPROM (24LC256)
 */

#include <Wire.h>

void setup() {
    Serial.begin(115200);
    while (!Serial) delay(10);  // Wait for serial (Leonardo/ESP32)
    
    Wire.begin();
    
    Serial.println();
    Serial.println("========================================");
    Serial.println("         I2C Bus Scanner v1.0          ");
    Serial.println("========================================");
    Serial.println();
    
    scanI2C();
}

void loop() {
    Serial.println("\\nPress any key to scan again...");
    while (!Serial.available()) delay(100);
    while (Serial.available()) Serial.read();
    scanI2C();
}

void scanI2C() {
    byte deviceCount = 0;
    byte error;
    
    Serial.println("Scanning I2C bus (0x03 to 0x77)...");
    Serial.println();
    
    // Print header
    Serial.print("     ");
    for (byte i = 0; i < 16; i++) {
        Serial.print(" ");
        if (i < 16) Serial.print(i, HEX);
    }
    Serial.println();
    
    for (byte row = 0; row < 8; row++) {
        Serial.print(row, HEX);
        Serial.print("0: ");
        
        for (byte col = 0; col < 16; col++) {
            byte addr = (row << 4) | col;
            
            if (addr < 0x03 || addr > 0x77) {
                Serial.print(" --");
            } else {
                Wire.beginTransmission(addr);
                error = Wire.endTransmission();
                
                if (error == 0) {
                    Serial.print(" ");
                    if (addr < 16) Serial.print("0");
                    Serial.print(addr, HEX);
                    deviceCount++;
                } else {
                    Serial.print(" --");
                }
            }
        }
        Serial.println();
    }
    
    Serial.println();
    Serial.print("Found ");
    Serial.print(deviceCount);
    Serial.println(" device(s)");
    
    if (deviceCount > 0) {
        Serial.println("\\nDevice details:");
        for (byte addr = 0x03; addr <= 0x77; addr++) {
            Wire.beginTransmission(addr);
            if (Wire.endTransmission() == 0) {
                Serial.print("  0x");
                if (addr < 16) Serial.print("0");
                Serial.print(addr, HEX);
                Serial.print(" - ");
                Serial.println(identifyDevice(addr));
            }
        }
    }
}

String identifyDevice(byte addr) {
    // Common device identification
    switch(addr) {
        case 0x27: case 0x3F: return "LCD I2C (PCF8574)";
        case 0x3C: case 0x3D: return "OLED SSD1306";
        case 0x68: return "DS3231 RTC or MPU6050";
        case 0x69: return "MPU6050 (ALT)";
        case 0x76: case 0x77: return "BME280/BMP280";
        case 0x48: return "ADS1115/PCF8591";
        case 0x50: return "EEPROM 24LC256";
        case 0x57: return "MAX30102 Pulse Sensor";
        case 0x1E: return "HMC5883L Compass";
        case 0x53: return "ADXL345 Accelerometer";
        case 0x40: return "INA219 Current Sensor or HTU21D";
        case 0x44: return "SHT31 Humidity";
        case 0x29: return "VL53L0X ToF Sensor";
        default:
            if (addr >= 0x20 && addr <= 0x27) return "PCF8574 I/O Expander";
            if (addr >= 0x50 && addr <= 0x57) return "EEPROM";
            return "Unknown device";
    }
}
'''

GPIO_TESTER = '''/*
 * GPIO Pin Tester
 * Tests digital I/O functionality
 * 
 * Features:
 * - Output test (LED blink pattern)
 * - Input test with pullup
 * - Measures pin capacitance indication
 * 
 * Test pins: {pins}
 */

const int TEST_PINS[] = {{{pins_array}}};
const int NUM_PINS = {num_pins};

void setup() {{
    Serial.begin(115200);
    while (!Serial) delay(10);
    
    Serial.println();
    Serial.println("========================================");
    Serial.println("         GPIO Pin Tester v1.0          ");
    Serial.println("========================================");
    Serial.println();
    
    Serial.println("Testing pins: {pins}");
    Serial.println();
    
    // Test each pin
    for (int i = 0; i < NUM_PINS; i++) {{
        testPin(TEST_PINS[i]);
    }}
    
    Serial.println("\\nOutput test - watch for LED blink pattern...");
    outputTest();
}}

void loop() {{
    // Continuous input monitoring
    Serial.println("\\nMonitoring inputs (press any key to restart)...");
    
    while (!Serial.available()) {{
        for (int i = 0; i < NUM_PINS; i++) {{
            pinMode(TEST_PINS[i], INPUT_PULLUP);
        }}
        
        Serial.print("Inputs: ");
        for (int i = 0; i < NUM_PINS; i++) {{
            Serial.print("D");
            Serial.print(TEST_PINS[i]);
            Serial.print("=");
            Serial.print(digitalRead(TEST_PINS[i]));
            Serial.print(" ");
        }}
        Serial.println();
        delay(500);
    }}
    
    while (Serial.available()) Serial.read();
    
    Serial.println("\\n--- Restarting test ---\\n");
    for (int i = 0; i < NUM_PINS; i++) {{
        testPin(TEST_PINS[i]);
    }}
    outputTest();
}}

void testPin(int pin) {{
    Serial.print("Pin D");
    Serial.print(pin);
    Serial.print(": ");
    
    // Test as output
    pinMode(pin, OUTPUT);
    digitalWrite(pin, HIGH);
    delay(1);
    digitalWrite(pin, LOW);
    
    // Test as input with pullup
    pinMode(pin, INPUT_PULLUP);
    delay(1);
    int pullupVal = digitalRead(pin);
    
    // Test as input without pullup
    pinMode(pin, INPUT);
    delay(1);
    int floatVal = digitalRead(pin);
    
    Serial.print("pullup=");
    Serial.print(pullupVal);
    Serial.print(" float=");
    Serial.print(floatVal);
    
    // Diagnosis
    if (pullupVal == HIGH && floatVal == LOW) {{
        Serial.println(" [OK - normal]");
    }} else if (pullupVal == HIGH && floatVal == HIGH) {{
        Serial.println(" [OK - pulled high externally]");
    }} else if (pullupVal == LOW) {{
        Serial.println(" [WARNING - pulled low or shorted to GND]");
    }} else {{
        Serial.println(" [OK]");
    }}
}}

void outputTest() {{
    // Set all as outputs
    for (int i = 0; i < NUM_PINS; i++) {{
        pinMode(TEST_PINS[i], OUTPUT);
    }}
    
    // Blink pattern
    for (int cycle = 0; cycle < 5; cycle++) {{
        // All on
        for (int i = 0; i < NUM_PINS; i++) {{
            digitalWrite(TEST_PINS[i], HIGH);
        }}
        delay(200);
        
        // All off
        for (int i = 0; i < NUM_PINS; i++) {{
            digitalWrite(TEST_PINS[i], LOW);
        }}
        delay(200);
    }}
    
    // Sequential chase
    for (int cycle = 0; cycle < 3; cycle++) {{
        for (int i = 0; i < NUM_PINS; i++) {{
            digitalWrite(TEST_PINS[i], HIGH);
            delay(100);
            digitalWrite(TEST_PINS[i], LOW);
        }}
    }}
    
    Serial.println("Output test complete");
}}
'''

ADC_CHECKER = '''/*
 * ADC / Analog Input Checker
 * Reads and displays analog values with voltage calculation
 * 
 * Test pins: {pins}
 * Reference: {vref}V (10-bit = 0-1023)
 */

const int ADC_PINS[] = {{{pins_array}}};
const int NUM_PINS = {num_pins};
const float VREF = {vref};  // Reference voltage
const int ADC_MAX = 1023;   // 10-bit ADC

void setup() {{
    Serial.begin(115200);
    while (!Serial) delay(10);
    
    Serial.println();
    Serial.println("========================================");
    Serial.println("        ADC Analog Checker v1.0        ");
    Serial.println("========================================");
    Serial.println();
    
    Serial.print("Reference voltage: ");
    Serial.print(VREF);
    Serial.println("V");
    Serial.print("Testing pins: {pins}");
    Serial.println();
    Serial.println();
    
    // Print header
    printHeader();
}}

void loop() {{
    // Read and display all channels
    for (int i = 0; i < NUM_PINS; i++) {{
        int raw = analogRead(ADC_PINS[i]);
        float voltage = (raw * VREF) / ADC_MAX;
        float percent = (raw * 100.0) / ADC_MAX;
        
        // Pin label
        Serial.print("A");
        Serial.print(ADC_PINS[i] - A0);
        Serial.print(": ");
        
        // Raw value (padded)
        if (raw < 1000) Serial.print(" ");
        if (raw < 100) Serial.print(" ");
        if (raw < 10) Serial.print(" ");
        Serial.print(raw);
        
        Serial.print(" | ");
        
        // Voltage
        Serial.print(voltage, 3);
        Serial.print("V | ");
        
        // Percentage bar
        int bars = percent / 5;  // 20 chars max
        Serial.print("[");
        for (int b = 0; b < 20; b++) {{
            if (b < bars) Serial.print("#");
            else Serial.print(" ");
        }}
        Serial.print("] ");
        Serial.print(percent, 1);
        Serial.println("%");
    }}
    
    Serial.println("----------------------------------------");
    delay(500);
}}

void printHeader() {{
    Serial.println("Pin  | Raw  | Voltage | Level");
    Serial.println("----------------------------------------");
}}
'''

PWM_TESTER = '''/*
 * PWM Output Tester
 * Tests PWM output on specified pins with varying duty cycles
 * 
 * PWM Pins by board:
 *   Uno/Nano: 3, 5, 6, 9, 10, 11
 *   Mega: 2-13, 44-46
 *   ESP32: Any GPIO (LEDC)
 *   Pico: Any GPIO
 * 
 * Test pins: {pins}
 */

const int PWM_PINS[] = {{{pins_array}}};
const int NUM_PINS = {num_pins};

int currentDuty = 0;
int direction = 1;
bool fadeMode = true;

void setup() {{
    Serial.begin(115200);
    while (!Serial) delay(10);
    
    Serial.println();
    Serial.println("========================================");
    Serial.println("         PWM Output Tester v1.0        ");
    Serial.println("========================================");
    Serial.println();
    Serial.println("Testing pins: {pins}");
    Serial.println();
    Serial.println("Commands:");
    Serial.println("  0-255: Set specific duty cycle");
    Serial.println("  f: Toggle fade mode");
    Serial.println("  s: Stop all outputs");
    Serial.println();
    
    // Initialize pins
    for (int i = 0; i < NUM_PINS; i++) {{
        pinMode(PWM_PINS[i], OUTPUT);
    }}
}}

void loop() {{
    // Check for serial commands
    if (Serial.available()) {{
        String cmd = Serial.readStringUntil('\\n');
        cmd.trim();
        
        if (cmd == "f") {{
            fadeMode = !fadeMode;
            Serial.print("Fade mode: ");
            Serial.println(fadeMode ? "ON" : "OFF");
        }} else if (cmd == "s") {{
            for (int i = 0; i < NUM_PINS; i++) {{
                analogWrite(PWM_PINS[i], 0);
            }}
            Serial.println("All PWM stopped");
            fadeMode = false;
        }} else {{
            int duty = cmd.toInt();
            if (duty >= 0 && duty <= 255) {{
                currentDuty = duty;
                fadeMode = false;
                for (int i = 0; i < NUM_PINS; i++) {{
                    analogWrite(PWM_PINS[i], currentDuty);
                }}
                Serial.print("Set duty cycle: ");
                Serial.print(currentDuty);
                Serial.print(" (");
                Serial.print((currentDuty * 100) / 255);
                Serial.println("%)");
            }}
        }}
    }}
    
    // Fade mode - smooth ramp up/down
    if (fadeMode) {{
        currentDuty += direction * 5;
        if (currentDuty >= 255) {{
            currentDuty = 255;
            direction = -1;
        }} else if (currentDuty <= 0) {{
            currentDuty = 0;
            direction = 1;
        }}
        
        for (int i = 0; i < NUM_PINS; i++) {{
            analogWrite(PWM_PINS[i], currentDuty);
        }}
        
        // Display
        Serial.print("PWM: ");
        Serial.print(currentDuty);
        Serial.print(" [");
        int bars = currentDuty / 12;  // ~21 chars
        for (int b = 0; b < 21; b++) {{
            if (b < bars) Serial.print("=");
            else Serial.print(" ");
        }}
        Serial.println("]");
        
        delay(30);
    }}
}}
'''

SERIAL_LOOPBACK = '''/*
 * Serial Loopback Tester
 * Tests serial communication by sending and receiving
 * 
 * For loopback test: Connect TX to RX directly
 * For device test: Connect to external serial device
 * 
 * Tests:
 * 1. Self loopback (wire TX to RX)
 * 2. Baud rate validation
 * 3. Data integrity
 */

// Test configuration
const long BAUD_RATES[] = {9600, 19200, 38400, 57600, 115200};
const int NUM_BAUDS = 5;

void setup() {
    Serial.begin(115200);
    while (!Serial) delay(10);
    
    Serial.println();
    Serial.println("========================================");
    Serial.println("      Serial Loopback Tester v1.0      ");
    Serial.println("========================================");
    Serial.println();
    Serial.println("Connect TX -> RX for loopback test");
    Serial.println("Or connect to target device");
    Serial.println();
    Serial.println("Commands:");
    Serial.println("  t - Run loopback test");
    Serial.println("  s - Send test string");
    Serial.println("  m - Monitor incoming data");
    Serial.println();
}

void loop() {
    if (Serial.available()) {
        char cmd = Serial.read();
        while (Serial.available()) Serial.read();  // Clear buffer
        
        switch (cmd) {
            case 't':
            case 'T':
                loopbackTest();
                break;
            case 's':
            case 'S':
                sendTestString();
                break;
            case 'm':
            case 'M':
                monitorMode();
                break;
        }
    }
}

void loopbackTest() {
    Serial.println("\\n--- Loopback Test ---");
    Serial.println("Ensure TX is connected to RX");
    Serial.println();
    
    // Wait for any existing data
    delay(100);
    while (Serial.available()) Serial.read();
    
    // Test string
    const char* testStr = "LOOPBACK_TEST_12345";
    int testLen = strlen(testStr);
    
    Serial.print("Sending: ");
    Serial.println(testStr);
    
    // Send test string (will echo back through loopback)
    Serial.print(testStr);
    Serial.flush();
    
    // Wait for response
    delay(100);
    
    char response[50];
    int received = 0;
    unsigned long start = millis();
    
    while (received < testLen && (millis() - start) < 1000) {
        if (Serial.available()) {
            response[received++] = Serial.read();
        }
    }
    response[received] = '\\0';
    
    Serial.print("Received: ");
    Serial.println(response);
    
    // Compare
    if (received == testLen && strcmp(response, testStr) == 0) {
        Serial.println("Result: PASS - Loopback OK");
    } else if (received == 0) {
        Serial.println("Result: FAIL - No response (check TX-RX connection)");
    } else {
        Serial.print("Result: FAIL - Received ");
        Serial.print(received);
        Serial.print(" of ");
        Serial.print(testLen);
        Serial.println(" bytes");
    }
}

void sendTestString() {
    Serial.println("\\n--- Sending Test Pattern ---");
    
    // ASCII printable range
    Serial.println("ASCII printable characters:");
    for (char c = 32; c < 127; c++) {
        Serial.print(c);
    }
    Serial.println();
    
    // Numbers
    Serial.println("\\nNumber sequence:");
    for (int i = 0; i < 10; i++) {
        Serial.print(i);
    }
    Serial.println();
    
    Serial.println("\\nTest complete");
}

void monitorMode() {
    Serial.println("\\n--- Monitor Mode ---");
    Serial.println("Displaying incoming bytes (press any key to exit)...");
    Serial.println();
    
    int byteCount = 0;
    unsigned long lastPrint = 0;
    
    while (true) {
        // Check for exit (data from USB serial)
        // This is tricky in loopback mode...
        
        // Display any received data
        while (Serial.available()) {
            char c = Serial.read();
            
            // Print as hex and ASCII
            if (c >= 32 && c < 127) {
                Serial.print(c);
            } else {
                Serial.print("[");
                Serial.print((int)c, HEX);
                Serial.print("]");
            }
            
            byteCount++;
        }
        
        // Stats every 2 seconds
        if (millis() - lastPrint > 2000) {
            Serial.print("\\n[");
            Serial.print(byteCount);
            Serial.println(" bytes received]");
            lastPrint = millis();
            
            // Exit after timeout with no data
            if (byteCount == 0) {
                Serial.println("No data - exiting monitor");
                break;
            }
            byteCount = 0;
        }
        
        delay(10);
    }
}
'''

VOLTAGE_DIVIDER = '''/*
 * Voltage Divider Calculator & Tester
 * Calculates and tests voltage divider circuits
 * 
 * Schematic:
 *   Vin ----[R1]----+----[R2]---- GND
 *                   |
 *                  Vout (to ADC)
 * 
 * Formula: Vout = Vin * (R2 / (R1 + R2))
 * 
 * Connect Vout to: {adc_pin}
 */

const int ADC_PIN = {adc_pin};
const float VREF = {vref};        // ADC reference voltage
const int ADC_MAX = 1023;         // 10-bit ADC

// Resistor values (ohms) - adjust to match your circuit
float R1 = {r1};  // Top resistor (Vin side)
float R2 = {r2};  // Bottom resistor (GND side)

// Calculated divider ratio
float dividerRatio;

void setup() {{
    Serial.begin(115200);
    while (!Serial) delay(10);
    
    Serial.println();
    Serial.println("========================================");
    Serial.println("   Voltage Divider Calculator v1.0     ");
    Serial.println("========================================");
    Serial.println();
    
    // Calculate ratio
    dividerRatio = R2 / (R1 + R2);
    float maxVin = VREF / dividerRatio;
    
    Serial.println("Configuration:");
    Serial.print("  R1 (top): ");
    Serial.print(R1 / 1000, 1);
    Serial.println(" kΩ");
    Serial.print("  R2 (bottom): ");
    Serial.print(R2 / 1000, 1);
    Serial.println(" kΩ");
    Serial.print("  Divider ratio: ");
    Serial.println(dividerRatio, 4);
    Serial.print("  ADC reference: ");
    Serial.print(VREF);
    Serial.println("V");
    Serial.print("  Max input voltage: ");
    Serial.print(maxVin, 2);
    Serial.println("V");
    Serial.println();
    Serial.println("Commands:");
    Serial.println("  r - Read voltage");
    Serial.println("  c - Continuous reading");
    Serial.println("  1/2 - Adjust R1/R2 values");
    Serial.println();
}}

void loop() {{
    if (Serial.available()) {{
        char cmd = Serial.read();
        while (Serial.available()) Serial.read();
        
        switch (cmd) {{
            case 'r':
            case 'R':
                readVoltage();
                break;
            case 'c':
            case 'C':
                continuousRead();
                break;
            case '1':
                adjustR1();
                break;
            case '2':
                adjustR2();
                break;
        }}
    }}
}}

void readVoltage() {{
    // Take multiple readings for stability
    long sum = 0;
    for (int i = 0; i < 10; i++) {{
        sum += analogRead(ADC_PIN);
        delay(10);
    }}
    float avgRaw = sum / 10.0;
    
    float vout = (avgRaw * VREF) / ADC_MAX;
    float vin = vout / dividerRatio;
    
    Serial.println("\\n--- Voltage Reading ---");
    Serial.print("ADC raw: ");
    Serial.println(avgRaw, 1);
    Serial.print("Vout (ADC): ");
    Serial.print(vout, 3);
    Serial.println("V");
    Serial.print("Vin (calculated): ");
    Serial.print(vin, 2);
    Serial.println("V");
}}

void continuousRead() {{
    Serial.println("\\nContinuous mode (any key to stop)...");
    
    while (!Serial.available()) {{
        int raw = analogRead(ADC_PIN);
        float vout = (raw * VREF) / ADC_MAX;
        float vin = vout / dividerRatio;
        
        Serial.print("ADC:");
        Serial.print(raw);
        Serial.print(" Vout:");
        Serial.print(vout, 3);
        Serial.print("V Vin:");
        Serial.print(vin, 2);
        Serial.println("V");
        
        delay(500);
    }}
    while (Serial.available()) Serial.read();
}}

void adjustR1() {{
    Serial.println("\\nEnter R1 value in ohms:");
    while (!Serial.available()) delay(10);
    R1 = Serial.parseFloat();
    updateRatio();
}}

void adjustR2() {{
    Serial.println("\\nEnter R2 value in ohms:");
    while (!Serial.available()) delay(10);
    R2 = Serial.parseFloat();
    updateRatio();
}}

void updateRatio() {{
    dividerRatio = R2 / (R1 + R2);
    Serial.print("New ratio: ");
    Serial.println(dividerRatio, 4);
    Serial.print("Max Vin: ");
    Serial.print(VREF / dividerRatio, 2);
    Serial.println("V");
}}
'''


def generate_i2c_scanner() -> str:
    """Generate I2C scanner sketch"""
    return I2C_SCANNER


def generate_gpio_tester(pins: List[int]) -> str:
    """Generate GPIO tester sketch"""
    pins_str = ", ".join(map(str, pins))
    return GPIO_TESTER.format(
        pins=pins_str,
        pins_array=pins_str,
        num_pins=len(pins)
    )


def generate_adc_checker(pins: List[str], vref: float = 5.0) -> str:
    """Generate ADC checker sketch"""
    # Convert pin names to Arduino pin numbers
    pin_nums = []
    for p in pins:
        if p.startswith('A'):
            pin_nums.append(f"A{p[1:]}")
        else:
            pin_nums.append(f"A{p}")
    
    pins_str = ", ".join(pins)
    pins_array = ", ".join(pin_nums)
    
    return ADC_CHECKER.format(
        pins=pins_str,
        pins_array=pins_array,
        num_pins=len(pins),
        vref=vref
    )


def generate_pwm_tester(pins: List[int]) -> str:
    """Generate PWM tester sketch"""
    pins_str = ", ".join(map(str, pins))
    return PWM_TESTER.format(
        pins=pins_str,
        pins_array=pins_str,
        num_pins=len(pins)
    )


def generate_serial_loopback() -> str:
    """Generate serial loopback tester"""
    return SERIAL_LOOPBACK


def generate_voltage_divider(adc_pin: str = "A0", vref: float = 5.0, 
                              r1: float = 30000, r2: float = 7500) -> str:
    """Generate voltage divider calculator sketch"""
    return VOLTAGE_DIVIDER.format(
        adc_pin=adc_pin,
        vref=vref,
        r1=r1,
        r2=r2
    )


def interactive_mode():
    """Interactive sketch generator"""
    print("=" * 60)
    print("Debug Sketch Generator - Interactive Mode")
    print("=" * 60)
    print()
    print("Available sketches:")
    print("  1. I2C Bus Scanner")
    print("  2. GPIO Pin Tester")
    print("  3. ADC/Analog Checker")
    print("  4. PWM Output Tester")
    print("  5. Serial Loopback Test")
    print("  6. Voltage Divider Tester")
    print("  7. Generate All")
    print()
    
    choice = input("Select sketch (1-7): ").strip()
    
    sketch = ""
    filename = "debug_sketch.ino"
    
    if choice == "1":
        sketch = generate_i2c_scanner()
        filename = "i2c_scanner.ino"
        
    elif choice == "2":
        pins_input = input("Enter GPIO pins (comma-separated) [2,3,4,5]: ").strip()
        pins = [int(p.strip()) for p in (pins_input or "2,3,4,5").split(",")]
        sketch = generate_gpio_tester(pins)
        filename = "gpio_tester.ino"
        
    elif choice == "3":
        pins_input = input("Enter ADC pins (comma-separated) [A0,A1,A2]: ").strip()
        pins = [p.strip() for p in (pins_input or "A0,A1,A2").split(",")]
        vref = float(input("Reference voltage [5.0]: ").strip() or "5.0")
        sketch = generate_adc_checker(pins, vref)
        filename = "adc_checker.ino"
        
    elif choice == "4":
        pins_input = input("Enter PWM pins (comma-separated) [3,5,6,9]: ").strip()
        pins = [int(p.strip()) for p in (pins_input or "3,5,6,9").split(",")]
        sketch = generate_pwm_tester(pins)
        filename = "pwm_tester.ino"
        
    elif choice == "5":
        sketch = generate_serial_loopback()
        filename = "serial_loopback.ino"
        
    elif choice == "6":
        adc = input("ADC pin [A0]: ").strip() or "A0"
        vref = float(input("Reference voltage [5.0]: ").strip() or "5.0")
        r1 = float(input("R1 (ohms) [30000]: ").strip() or "30000")
        r2 = float(input("R2 (ohms) [7500]: ").strip() or "7500")
        sketch = generate_voltage_divider(adc, vref, r1, r2)
        filename = "voltage_divider.ino"
        
    elif choice == "7":
        # Generate all into one file
        sketches = [
            "// ===== I2C SCANNER =====",
            generate_i2c_scanner(),
            "\n// ===== GPIO TESTER =====",
            generate_gpio_tester([2, 3, 4, 5]),
            "\n// ===== ADC CHECKER =====",
            generate_adc_checker(["A0", "A1", "A2"]),
        ]
        sketch = "\n\n".join(sketches)
        filename = "debug_suite.ino"
        print("\nNote: Multiple sketches generated. Copy desired section to use.")
    
    else:
        print("Invalid choice")
        return
    
    # Save
    custom_name = input(f"\nOutput filename [{filename}]: ").strip()
    if custom_name:
        filename = custom_name if custom_name.endswith(".ino") else custom_name + ".ino"
    
    with open(filename, 'w') as f:
        f.write(sketch)
    
    print(f"\n✓ Generated: {filename}")
    print(f"  Upload to Arduino and open Serial Monitor at 115200 baud")


def main():
    parser = argparse.ArgumentParser(description="Debug Sketch Generator")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--i2c", action="store_true", help="Generate I2C scanner")
    parser.add_argument("--gpio", action="store_true", help="Generate GPIO tester")
    parser.add_argument("--adc", action="store_true", help="Generate ADC checker")
    parser.add_argument("--pwm", action="store_true", help="Generate PWM tester")
    parser.add_argument("--serial", action="store_true", help="Generate serial loopback")
    parser.add_argument("--voltage", action="store_true", help="Generate voltage divider")
    parser.add_argument("--pins", type=str, help="Comma-separated pin list")
    parser.add_argument("--vref", type=float, default=5.0, help="Reference voltage")
    parser.add_argument("--output", "-o", type=str, help="Output filename")
    parser.add_argument("--all", action="store_true", help="Generate all sketches")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    sketch = ""
    filename = args.output or "debug_sketch.ino"
    
    if args.i2c:
        sketch = generate_i2c_scanner()
        filename = args.output or "i2c_scanner.ino"
    elif args.gpio:
        pins = [int(p) for p in (args.pins or "2,3,4,5").split(",")]
        sketch = generate_gpio_tester(pins)
        filename = args.output or "gpio_tester.ino"
    elif args.adc:
        pins = (args.pins or "A0,A1,A2").split(",")
        sketch = generate_adc_checker(pins, args.vref)
        filename = args.output or "adc_checker.ino"
    elif args.pwm:
        pins = [int(p) for p in (args.pins or "3,5,6,9").split(",")]
        sketch = generate_pwm_tester(pins)
        filename = args.output or "pwm_tester.ino"
    elif args.serial:
        sketch = generate_serial_loopback()
        filename = args.output or "serial_loopback.ino"
    elif args.voltage:
        sketch = generate_voltage_divider("A0", args.vref)
        filename = args.output or "voltage_divider.ino"
    elif args.all:
        sketches = [
            generate_i2c_scanner(),
            generate_gpio_tester([2, 3, 4, 5]),
            generate_adc_checker(["A0", "A1", "A2"]),
            generate_pwm_tester([3, 5, 6, 9]),
            generate_serial_loopback()
        ]
        # Save each separately
        names = ["i2c_scanner.ino", "gpio_tester.ino", "adc_checker.ino", 
                 "pwm_tester.ino", "serial_loopback.ino"]
        for s, n in zip(sketches, names):
            with open(n, 'w') as f:
                f.write(s)
            print(f"Generated: {n}")
        return
    else:
        parser.print_help()
        return
    
    with open(filename, 'w') as f:
        f.write(sketch)
    print(f"Generated: {filename}")


if __name__ == "__main__":
    main()
