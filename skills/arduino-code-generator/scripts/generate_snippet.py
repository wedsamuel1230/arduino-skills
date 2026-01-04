#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Arduino Code Snippet Generator

Generate production-ready Arduino code snippets from pattern templates.
Supports UNO, ESP32, and RP2040 boards with proper pin configurations.

Usage:
    uv run generate_snippet.py --pattern config --board esp32
    uv run generate_snippet.py --pattern buttons --board uno --pin 3
    uv run generate_snippet.py --pattern i2c --board rp2040 --output scanner.ino
    uv run generate_snippet.py --interactive
    uv run generate_snippet.py --list
"""

import argparse
import sys
from dataclasses import dataclass
from typing import Optional

# =============================================================================
# Board Configurations
# =============================================================================

BOARD_CONFIGS = {
    "uno": {
        "name": "Arduino UNO",
        "define": "ARDUINO_AVR_UNO",
        "led": 13,
        "button": 2,
        "sda": "A4",
        "scl": "A5",
        "sram": 2048,
        "baud": 9600,
        "adc_bits": 10,
        "has_wifi": False,
    },
    "esp32": {
        "name": "ESP32",
        "define": "ESP32",
        "led": 2,
        "button": 4,
        "sda": 21,
        "scl": 22,
        "sram": 520000,
        "baud": 115200,
        "adc_bits": 12,
        "has_wifi": True,
    },
    "rp2040": {
        "name": "RP2040",
        "define": "ARDUINO_ARCH_RP2040",
        "led": 25,
        "button": 14,
        "sda": 4,
        "scl": 5,
        "sram": 264000,
        "baud": 115200,
        "adc_bits": 12,
        "has_wifi": False,
    },
}

# =============================================================================
# Pattern Templates
# =============================================================================

PATTERNS = {
    "config": {
        "name": "Config.h Hardware Abstraction",
        "description": "Multi-board configuration with conditional compilation",
        "template": '''// config.h - Hardware abstraction layer
#ifndef CONFIG_H
#define CONFIG_H

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_NANO)
  #define BOARD_NAME "Arduino UNO"
  #define LED_PIN 13
  #define BUTTON_PIN 2
  #define I2C_SDA A4
  #define I2C_SCL A5
  #define SRAM_SIZE 2048
  #define SERIAL_BAUD 9600

#elif defined(ESP32)
  #define BOARD_NAME "ESP32"
  #define LED_PIN 2
  #define BUTTON_PIN 4
  #define I2C_SDA 21
  #define I2C_SCL 22
  #define SRAM_SIZE 520000
  #define SERIAL_BAUD 115200
  #define HAS_WIFI 1
  #define HAS_BLE 1

#elif defined(ARDUINO_ARCH_RP2040)
  #define BOARD_NAME "RP2040"
  #define LED_PIN 25
  #define BUTTON_PIN 14
  #define I2C_SDA 4
  #define I2C_SCL 5
  #define SRAM_SIZE 264000
  #define SERIAL_BAUD 115200

#else
  #error "Unsupported board! Add configuration for your board."
#endif

// === Common Settings ===
#define DEBOUNCE_MS 50
#define SENSOR_INTERVAL_MS 1000
#define LOG_INTERVAL_MS 60000

#endif // CONFIG_H
''',
    },
    "buttons": {
        "name": "Button Debouncing",
        "description": "Debounced button with press/release/long-press detection",
        "template": '''// DebouncedButton - Software debouncing with event detection
// Pin: {button_pin} (configured for INPUT_PULLUP)

class DebouncedButton {{
public:
  enum Event {{ NONE, PRESSED, RELEASED, LONG_PRESS }};
  
private:
  uint8_t pin;
  bool lastStableState;
  bool lastReading;
  unsigned long lastDebounceTime;
  unsigned long pressStartTime;
  bool longPressTriggered;
  
  static const unsigned long DEBOUNCE_MS = 50;
  static const unsigned long LONG_PRESS_MS = 1000;
  
public:
  DebouncedButton(uint8_t p) : pin(p), lastStableState(HIGH), lastReading(HIGH),
    lastDebounceTime(0), pressStartTime(0), longPressTriggered(false) {{}}
  
  void begin() {{
    pinMode(pin, INPUT_PULLUP);
  }}
  
  Event update() {{
    bool reading = digitalRead(pin);
    unsigned long now = millis();
    
    // Reset debounce timer on state change
    if (reading != lastReading) {{
      lastDebounceTime = now;
    }}
    lastReading = reading;
    
    // Wait for stable state
    if ((now - lastDebounceTime) < DEBOUNCE_MS) {{
      return NONE;
    }}
    
    // State changed
    if (reading != lastStableState) {{
      lastStableState = reading;
      
      if (reading == LOW) {{
        // Button pressed
        pressStartTime = now;
        longPressTriggered = false;
        return PRESSED;
      }} else {{
        // Button released
        return longPressTriggered ? NONE : RELEASED;
      }}
    }}
    
    // Check for long press (while held)
    if (lastStableState == LOW && !longPressTriggered) {{
      if ((now - pressStartTime) >= LONG_PRESS_MS) {{
        longPressTriggered = true;
        return LONG_PRESS;
      }}
    }}
    
    return NONE;
  }}
  
  bool isPressed() const {{ return lastStableState == LOW; }}
}};

// === Usage Example ===
DebouncedButton button({button_pin});

void setup() {{
  Serial.begin({baud});
  button.begin();
  Serial.println(F("Button ready - press, release, or hold for 1s"));
}}

void loop() {{
  DebouncedButton::Event event = button.update();
  
  switch (event) {{
    case DebouncedButton::PRESSED:
      Serial.println(F("PRESSED"));
      break;
    case DebouncedButton::RELEASED:
      Serial.println(F("RELEASED (short press)"));
      break;
    case DebouncedButton::LONG_PRESS:
      Serial.println(F("LONG PRESS detected!"));
      break;
    default:
      break;
  }}
}}
''',
    },
    "i2c": {
        "name": "I2C Scanner & Diagnostics",
        "description": "Scan I2C bus and identify connected devices",
        "template": '''// I2C Scanner - Detect devices on the I2C bus
// SDA: Pin {sda}, SCL: Pin {scl}

#include <Wire.h>

// Known I2C device addresses
struct I2CDevice {{
  uint8_t address;
  const char* name;
}};

const I2CDevice KNOWN_DEVICES[] = {{
  {{0x3C, "SSD1306 OLED"}},
  {{0x3D, "SSD1306 OLED (alt)"}},
  {{0x27, "LCD I2C (PCF8574)"}},
  {{0x3F, "LCD I2C (PCF8574A)"}},
  {{0x76, "BME280/BMP280"}},
  {{0x77, "BME280/BMP280 (alt)"}},
  {{0x68, "MPU6050/DS3231 RTC"}},
  {{0x57, "AT24C32 EEPROM"}},
  {{0x50, "AT24C256 EEPROM"}},
  {{0x48, "ADS1115 ADC"}},
  {{0x40, "INA219 Current Sensor"}},
  {{0x29, "VL53L0X ToF Sensor"}},
  {{0x39, "APDS9960 Gesture"}},
  {{0x5A, "MLX90614 IR Temp"}},
}};
const uint8_t KNOWN_COUNT = sizeof(KNOWN_DEVICES) / sizeof(KNOWN_DEVICES[0]);

const char* identifyDevice(uint8_t address) {{
  for (uint8_t i = 0; i < KNOWN_COUNT; i++) {{
    if (KNOWN_DEVICES[i].address == address) {{
      return KNOWN_DEVICES[i].name;
    }}
  }}
  return "Unknown";
}}

void scanI2C() {{
  Serial.println(F("\\n=== I2C Scanner ==="));
  Serial.println(F("Scanning...\\n"));
  
  uint8_t found = 0;
  
  for (uint8_t addr = 1; addr < 127; addr++) {{
    Wire.beginTransmission(addr);
    uint8_t error = Wire.endTransmission();
    
    if (error == 0) {{
      found++;
      Serial.print(F("Found: 0x"));
      if (addr < 16) Serial.print('0');
      Serial.print(addr, HEX);
      Serial.print(F(" - "));
      Serial.println(identifyDevice(addr));
    }} else if (error == 4) {{
      Serial.print(F("Error at 0x"));
      if (addr < 16) Serial.print('0');
      Serial.println(addr, HEX);
    }}
  }}
  
  Serial.print(F("\\nDevices found: "));
  Serial.println(found);
  
  if (found == 0) {{
    Serial.println(F("\\nTroubleshooting:"));
    Serial.println(F("- Check wiring (SDA/SCL swapped?)"));
    Serial.println(F("- Verify power to I2C devices"));
    Serial.println(F("- Add 4.7kΩ pull-up resistors"));
    Serial.println(F("- Check I2C address on device"));
  }}
}}

void setup() {{
  Serial.begin({baud});
  while (!Serial) {{ ; }}  // Wait for Serial (Leonardo/Pro Micro)
  
  Wire.begin({sda}, {scl});
  Serial.println(F("I2C Scanner Ready"));
  Serial.print(F("SDA: Pin {sda}, SCL: Pin {scl}"));
  
  scanI2C();
}}

void loop() {{
  // Rescan every 5 seconds
  delay(5000);
  scanI2C();
}}
''',
    },
    "scheduler": {
        "name": "Non-blocking Scheduler",
        "description": "millis()-based timer for multi-tasking without delay()",
        "template": '''// EveryMs - Non-blocking timer class
// Replaces delay() with proper millis() timing

class EveryMs {{
private:
  unsigned long interval;
  unsigned long lastTrigger;
  
public:
  EveryMs(unsigned long ms) : interval(ms), lastTrigger(0) {{}}
  
  bool check() {{
    unsigned long now = millis();
    // Handles millis() overflow correctly (unsigned subtraction)
    if (now - lastTrigger >= interval) {{
      lastTrigger = now;
      return true;
    }}
    return false;
  }}
  
  void reset() {{
    lastTrigger = millis();
  }}
  
  void setInterval(unsigned long ms) {{
    interval = ms;
  }}
  
  unsigned long elapsed() const {{
    return millis() - lastTrigger;
  }}
}};

// === Multi-Task Example ===
EveryMs ledTimer(500);      // Blink LED every 500ms
EveryMs sensorTimer(2000);  // Read sensor every 2s
EveryMs logTimer(10000);    // Log data every 10s

bool ledState = false;

void setup() {{
  Serial.begin({baud});
  pinMode({led_pin}, OUTPUT);
  Serial.println(F("Non-blocking scheduler ready"));
}}

void loop() {{
  // Task 1: Blink LED (500ms)
  if (ledTimer.check()) {{
    ledState = !ledState;
    digitalWrite({led_pin}, ledState);
  }}
  
  // Task 2: Read sensor (2s)
  if (sensorTimer.check()) {{
    int value = analogRead(A0);
    Serial.print(F("Sensor: "));
    Serial.println(value);
  }}
  
  // Task 3: Log data (10s)
  if (logTimer.check()) {{
    Serial.print(F("Uptime: "));
    Serial.print(millis() / 1000);
    Serial.println(F(" seconds"));
  }}
  
  // Other non-blocking code can run here
}}
''',
    },
    "csv": {
        "name": "CSV Data Logger",
        "description": "Structured CSV output for data logging and analysis",
        "template": '''// CSV Logger - Structured data output for Serial/SD
// Format: timestamp,sensor1,sensor2,...

class CSVLogger {{
private:
  bool headerPrinted;
  unsigned long startTime;
  
public:
  CSVLogger() : headerPrinted(false), startTime(0) {{}}
  
  void begin() {{
    startTime = millis();
  }}
  
  void printHeader(const char* fields[], uint8_t count) {{
    if (!headerPrinted) {{
      Serial.print(F("time_ms"));
      for (uint8_t i = 0; i < count; i++) {{
        Serial.print(',');
        Serial.print(fields[i]);
      }}
      Serial.println();
      headerPrinted = true;
    }}
  }}
  
  void startRow() {{
    Serial.print(millis() - startTime);
  }}
  
  void addInt(int value) {{
    Serial.print(',');
    Serial.print(value);
  }}
  
  void addFloat(float value, uint8_t decimals = 2) {{
    Serial.print(',');
    Serial.print(value, decimals);
  }}
  
  void addString(const char* value) {{
    Serial.print(',');
    Serial.print(value);
  }}
  
  void endRow() {{
    Serial.println();
  }}
}};

// === Usage Example ===
CSVLogger logger;
const char* FIELDS[] = {{"temp_c", "humidity", "light"}};
const uint8_t FIELD_COUNT = 3;

EveryMs logTimer(5000);  // Log every 5 seconds

void setup() {{
  Serial.begin({baud});
  logger.begin();
  logger.printHeader(FIELDS, FIELD_COUNT);
}}

void loop() {{
  if (logTimer.check()) {{
    // Simulate sensor readings
    float temp = 22.5 + (random(-20, 20) / 10.0);
    float humidity = 45.0 + (random(-50, 50) / 10.0);
    int light = analogRead(A0);
    
    logger.startRow();
    logger.addFloat(temp);
    logger.addFloat(humidity);
    logger.addInt(light);
    logger.endRow();
  }}
}}

// Output format (copy to Excel/Python):
// time_ms,temp_c,humidity,light
// 5000,22.7,44.2,512
// 10000,22.3,45.8,498
// 15000,23.1,44.9,521
''',
    },
    "filtering": {
        "name": "ADC Filtering",
        "description": "Moving average and median filters for noisy sensors",
        "template": '''// Sensor Filters - Reduce noise from analog readings

// === Moving Average Filter ===
template<uint8_t SIZE>
class MovingAverageFilter {{
private:
  int values[SIZE];
  uint8_t index;
  uint8_t count;
  long sum;
  
public:
  MovingAverageFilter() : index(0), count(0), sum(0) {{
    for (uint8_t i = 0; i < SIZE; i++) values[i] = 0;
  }}
  
  int filter(int newValue) {{
    sum -= values[index];
    values[index] = newValue;
    sum += newValue;
    index = (index + 1) % SIZE;
    if (count < SIZE) count++;
    return sum / count;
  }}
  
  void reset() {{
    index = 0;
    count = 0;
    sum = 0;
    for (uint8_t i = 0; i < SIZE; i++) values[i] = 0;
  }}
}};

// === Median Filter (3 samples) ===
class MedianFilter3 {{
private:
  int v0, v1, v2;
  
public:
  MedianFilter3() : v0(0), v1(0), v2(0) {{}}
  
  int filter(int newValue) {{
    v0 = v1;
    v1 = v2;
    v2 = newValue;
    
    // Sort and return middle value
    if (v0 <= v1) {{
      if (v1 <= v2) return v1;        // v0 <= v1 <= v2
      if (v0 <= v2) return v2;        // v0 <= v2 < v1
      return v0;                       // v2 < v0 <= v1
    }} else {{
      if (v0 <= v2) return v0;        // v1 < v0 <= v2
      if (v1 <= v2) return v2;        // v1 <= v2 < v0
      return v1;                       // v2 < v1 < v0
    }}
  }}
}};

// === Usage Example ===
MovingAverageFilter<10> avgFilter;  // 10-sample average
MedianFilter3 medFilter;            // 3-sample median

EveryMs readTimer(100);  // Read every 100ms
EveryMs printTimer(1000); // Print every 1s

int rawValue, avgValue, medValue;

void setup() {{
  Serial.begin({baud});
  Serial.println(F("Raw,Average,Median"));
}}

void loop() {{
  if (readTimer.check()) {{
    rawValue = analogRead(A0);
    avgValue = avgFilter.filter(rawValue);
    medValue = medFilter.filter(rawValue);
  }}
  
  if (printTimer.check()) {{
    Serial.print(rawValue);
    Serial.print(',');
    Serial.print(avgValue);
    Serial.print(',');
    Serial.println(medValue);
  }}
}}
''',
    },
    "state-machine": {
        "name": "State Machine",
        "description": "Enum-based FSM for complex behavior control",
        "template": '''// State Machine - Enum-based finite state machine
// Example: Traffic light controller

enum class State {{
  RED,
  RED_YELLOW,
  GREEN,
  YELLOW
}};

const char* stateNames[] = {{"RED", "RED_YELLOW", "GREEN", "YELLOW"}};

class TrafficLight {{
private:
  State currentState;
  unsigned long stateStartTime;
  
  // State durations in milliseconds
  static const unsigned long RED_DURATION = 5000;
  static const unsigned long RED_YELLOW_DURATION = 1000;
  static const unsigned long GREEN_DURATION = 4000;
  static const unsigned long YELLOW_DURATION = 2000;
  
public:
  TrafficLight() : currentState(State::RED), stateStartTime(0) {{}}
  
  void begin() {{
    stateStartTime = millis();
    updateOutputs();
    printState();
  }}
  
  void update() {{
    unsigned long elapsed = millis() - stateStartTime;
    State nextState = currentState;
    
    switch (currentState) {{
      case State::RED:
        if (elapsed >= RED_DURATION) nextState = State::RED_YELLOW;
        break;
      case State::RED_YELLOW:
        if (elapsed >= RED_YELLOW_DURATION) nextState = State::GREEN;
        break;
      case State::GREEN:
        if (elapsed >= GREEN_DURATION) nextState = State::YELLOW;
        break;
      case State::YELLOW:
        if (elapsed >= YELLOW_DURATION) nextState = State::RED;
        break;
    }}
    
    if (nextState != currentState) {{
      transition(nextState);
    }}
  }}
  
private:
  void transition(State newState) {{
    currentState = newState;
    stateStartTime = millis();
    updateOutputs();
    printState();
  }}
  
  void updateOutputs() {{
    // Set LED outputs based on state
    bool red = false, yellow = false, green = false;
    
    switch (currentState) {{
      case State::RED:        red = true; break;
      case State::RED_YELLOW: red = true; yellow = true; break;
      case State::GREEN:      green = true; break;
      case State::YELLOW:     yellow = true; break;
    }}
    
    // digitalWrite(RED_LED, red);
    // digitalWrite(YELLOW_LED, yellow);
    // digitalWrite(GREEN_LED, green);
  }}
  
  void printState() {{
    Serial.print(F("State: "));
    Serial.println(stateNames[static_cast<int>(currentState)]);
  }}
}};

// === Usage ===
TrafficLight traffic;

void setup() {{
  Serial.begin({baud});
  traffic.begin();
}}

void loop() {{
  traffic.update();
}}
''',
    },
    "hardware-detection": {
        "name": "Hardware Detection",
        "description": "Auto-detect board type and connected sensors",
        "template": '''// Hardware Detection - Identify board and peripherals at runtime

#include <Wire.h>

struct BoardInfo {{
  const char* name;
  uint32_t sramSize;
  uint32_t flashSize;
  bool hasWifi;
  bool hasBle;
}};

BoardInfo detectBoard() {{
  BoardInfo info;
  
  #if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_NANO)
    info.name = "Arduino UNO/Nano";
    info.sramSize = 2048;
    info.flashSize = 32768;
    info.hasWifi = false;
    info.hasBle = false;
  #elif defined(ESP32)
    info.name = "ESP32";
    info.sramSize = 520000;
    info.flashSize = 4194304;
    info.hasWifi = true;
    info.hasBle = true;
  #elif defined(ARDUINO_ARCH_RP2040)
    info.name = "RP2040";
    info.sramSize = 264000;
    info.flashSize = 2097152;
    info.hasWifi = false;  // Unless Pico W
    info.hasBle = false;
  #else
    info.name = "Unknown";
    info.sramSize = 0;
    info.flashSize = 0;
    info.hasWifi = false;
    info.hasBle = false;
  #endif
  
  return info;
}}

uint32_t getFreeSram() {{
  #if defined(ESP32)
    return ESP.getFreeHeap();
  #elif defined(ARDUINO_ARCH_RP2040)
    return rp2040.getFreeHeap();
  #else
    // AVR: estimate free RAM
    extern int __heap_start, *__brkval;
    int v;
    return (int)&v - (__brkval == 0 ? (int)&__heap_start : (int)__brkval);
  #endif
}}

bool scanI2CDevice(uint8_t address) {{
  Wire.beginTransmission(address);
  return Wire.endTransmission() == 0;
}}

void detectSensors() {{
  Serial.println(F("\\n=== Sensor Detection ==="));
  
  // BME280/BMP280
  if (scanI2CDevice(0x76) || scanI2CDevice(0x77)) {{
    Serial.println(F("✓ BME280/BMP280 found"));
  }}
  
  // SSD1306 OLED
  if (scanI2CDevice(0x3C) || scanI2CDevice(0x3D)) {{
    Serial.println(F("✓ SSD1306 OLED found"));
  }}
  
  // MPU6050
  if (scanI2CDevice(0x68)) {{
    Serial.println(F("✓ MPU6050 IMU found (or DS3231 RTC)"));
  }}
  
  // LCD I2C
  if (scanI2CDevice(0x27) || scanI2CDevice(0x3F)) {{
    Serial.println(F("✓ LCD I2C found"));
  }}
}}

void setup() {{
  Serial.begin({baud});
  while (!Serial) {{ ; }}
  
  BoardInfo board = detectBoard();
  
  Serial.println(F("\\n=== Board Information ==="));
  Serial.print(F("Board: "));
  Serial.println(board.name);
  Serial.print(F("SRAM: "));
  Serial.print(board.sramSize);
  Serial.println(F(" bytes"));
  Serial.print(F("Flash: "));
  Serial.print(board.flashSize);
  Serial.println(F(" bytes"));
  Serial.print(F("WiFi: "));
  Serial.println(board.hasWifi ? "Yes" : "No");
  Serial.print(F("BLE: "));
  Serial.println(board.hasBle ? "Yes" : "No");
  
  Serial.print(F("\\nFree SRAM: "));
  Serial.print(getFreeSram());
  Serial.println(F(" bytes"));
  
  Wire.begin();
  detectSensors();
}}

void loop() {{
  // Periodically check memory
  static EveryMs memCheck(5000);
  if (memCheck.check()) {{
    Serial.print(F("Free SRAM: "));
    Serial.println(getFreeSram());
  }}
}}
''',
    },
    "data-logging": {
        "name": "Data Logging (EEPROM/SD)",
        "description": "Persistent storage with EEPROM and SD card",
        "template": '''// Data Logging - EEPROM settings + SD card logging

#include <EEPROM.h>
#if defined(ESP32)
  #include <SD.h>
#else
  #include <SD.h>
#endif

// === CRC8 for data validation ===
uint8_t crc8(const uint8_t* data, size_t len) {{
  uint8_t crc = 0xFF;
  while (len--) {{
    crc ^= *data++;
    for (uint8_t i = 0; i < 8; i++) {{
      crc = (crc & 0x80) ? (crc << 1) ^ 0x31 : crc << 1;
    }}
  }}
  return crc;
}}

// === EEPROM Settings Manager ===
struct Settings {{
  uint8_t version;
  uint16_t logInterval;
  uint8_t sensorCount;
  char deviceName[16];
  uint8_t crc;
}};

class SettingsManager {{
private:
  static const uint8_t CURRENT_VERSION = 1;
  static const uint16_t EEPROM_ADDR = 0;
  
public:
  Settings settings;
  
  void loadDefaults() {{
    settings.version = CURRENT_VERSION;
    settings.logInterval = 5000;
    settings.sensorCount = 3;
    strncpy(settings.deviceName, "DataLogger", 15);
    settings.deviceName[15] = '\\0';
  }}
  
  bool load() {{
    #if defined(ESP32)
    EEPROM.begin(sizeof(Settings));
    #endif
    
    EEPROM.get(EEPROM_ADDR, settings);
    
    uint8_t stored_crc = settings.crc;
    settings.crc = 0;
    uint8_t calc_crc = crc8((uint8_t*)&settings, sizeof(Settings) - 1);
    
    if (stored_crc != calc_crc || settings.version != CURRENT_VERSION) {{
      Serial.println(F("EEPROM: Invalid or old data, loading defaults"));
      loadDefaults();
      return false;
    }}
    
    settings.crc = stored_crc;
    Serial.println(F("EEPROM: Settings loaded"));
    return true;
  }}
  
  void save() {{
    settings.crc = 0;
    settings.crc = crc8((uint8_t*)&settings, sizeof(Settings) - 1);
    
    EEPROM.put(EEPROM_ADDR, settings);
    
    #if defined(ESP32)
    EEPROM.commit();
    #endif
    
    Serial.println(F("EEPROM: Settings saved"));
  }}
  
  void print() {{
    Serial.println(F("=== Current Settings ==="));
    Serial.print(F("Device: "));
    Serial.println(settings.deviceName);
    Serial.print(F("Log Interval: "));
    Serial.print(settings.logInterval);
    Serial.println(F(" ms"));
    Serial.print(F("Sensor Count: "));
    Serial.println(settings.sensorCount);
  }}
}};

// === SD Card Logger ===
class SDLogger {{
private:
  const char* filename;
  bool sdReady;
  
public:
  SDLogger(const char* fname) : filename(fname), sdReady(false) {{}}
  
  bool begin(uint8_t csPin = 10) {{
    if (SD.begin(csPin)) {{
      sdReady = true;
      Serial.println(F("SD card ready"));
      
      // Create header if new file
      if (!SD.exists(filename)) {{
        File f = SD.open(filename, FILE_WRITE);
        if (f) {{
          f.println(F("timestamp_ms,temp_c,humidity,light"));
          f.close();
        }}
      }}
      return true;
    }}
    Serial.println(F("SD card failed"));
    return false;
  }}
  
  bool log(unsigned long timestamp, float temp, float humidity, int light) {{
    if (!sdReady) return false;
    
    File f = SD.open(filename, FILE_WRITE);
    if (f) {{
      f.print(timestamp);
      f.print(',');
      f.print(temp, 2);
      f.print(',');
      f.print(humidity, 2);
      f.print(',');
      f.println(light);
      f.close();
      return true;
    }}
    return false;
  }}
}};

// === Usage Example ===
SettingsManager settings;
SDLogger sdLog("datalog.csv");

void setup() {{
  Serial.begin({baud});
  
  settings.load();
  settings.print();
  
  sdLog.begin();
}}

void loop() {{
  // Log data every interval
  static EveryMs logTimer(settings.settings.logInterval);
  
  if (logTimer.check()) {{
    // Simulate sensor data
    float temp = 22.5;
    float humidity = 45.0;
    int light = analogRead(A0);
    
    sdLog.log(millis(), temp, humidity, light);
    Serial.println(F("Data logged"));
  }}
  
  // Check for settings update command
  if (Serial.available()) {{
    char cmd = Serial.read();
    if (cmd == 's') {{
      settings.save();
    }} else if (cmd == 'p') {{
      settings.print();
    }}
  }}
}}
''',
    },
}

# =============================================================================
# Code Generation Functions
# =============================================================================


def generate_snippet(pattern: str, board: str, **kwargs) -> str:
    """Generate code snippet for specified pattern and board."""
    if pattern not in PATTERNS:
        return f"Error: Unknown pattern '{pattern}'. Use --list to see available patterns."

    if board not in BOARD_CONFIGS:
        return f"Error: Unknown board '{board}'. Supported: uno, esp32, rp2040"

    template = PATTERNS[pattern]["template"]
    config = BOARD_CONFIGS[board]

    # Merge board config with user overrides
    params = {
        "baud": config["baud"],
        "led_pin": kwargs.get("led_pin", config["led"]),
        "button_pin": kwargs.get("button_pin", config["button"]),
        "sda": kwargs.get("sda", config["sda"]),
        "scl": kwargs.get("scl", config["scl"]),
        "board_name": config["name"],
    }

    try:
        return template.format(**params)
    except KeyError as e:
        return f"Error: Missing parameter {e}"


def list_patterns():
    """List all available patterns."""
    print("\n=== Available Patterns ===\n")
    for key, info in PATTERNS.items():
        print(f"  {key:20} - {info['description']}")
    print("\n=== Supported Boards ===\n")
    for key, info in BOARD_CONFIGS.items():
        wifi = "WiFi" if info["has_wifi"] else ""
        print(f"  {key:10} - {info['name']:15} ({info['sram']} bytes SRAM) {wifi}")
    print()


def interactive_mode():
    """Run interactive wizard for code generation."""
    print("\n🔧 Arduino Code Snippet Generator - Interactive Mode\n")

    # Select pattern
    print("Available patterns:")
    patterns_list = list(PATTERNS.keys())
    for i, p in enumerate(patterns_list, 1):
        print(f"  {i}. {p} - {PATTERNS[p]['description']}")

    while True:
        try:
            choice = input("\nSelect pattern (1-9): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(patterns_list):
                pattern = patterns_list[idx]
                break
        except ValueError:
            pass
        print("Invalid choice, try again.")

    # Select board
    print("\nAvailable boards:")
    boards_list = list(BOARD_CONFIGS.keys())
    for i, b in enumerate(boards_list, 1):
        wifi = " (WiFi)" if BOARD_CONFIGS[b]["has_wifi"] else ""
        print(f"  {i}. {b} - {BOARD_CONFIGS[b]['name']}{wifi}")

    while True:
        try:
            choice = input("\nSelect board (1-3): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(boards_list):
                board = boards_list[idx]
                break
        except ValueError:
            pass
        print("Invalid choice, try again.")

    # Generate
    print(f"\n{'='*60}")
    print(f"Generating: {PATTERNS[pattern]['name']} for {BOARD_CONFIGS[board]['name']}")
    print(f"{'='*60}\n")

    code = generate_snippet(pattern, board)
    print(code)

    # Save option
    save = input("\nSave to file? (y/n): ").strip().lower()
    if save == "y":
        filename = input("Filename (e.g., sketch.ino): ").strip()
        if filename:
            with open(filename, "w") as f:
                f.write(code)
            print(f"✓ Saved to {filename}")


# =============================================================================
# Main
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Generate Arduino code snippets from pattern templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run generate_snippet.py --list
  uv run generate_snippet.py --pattern config --board esp32
  uv run generate_snippet.py --pattern buttons --board uno --output button.ino
  uv run generate_snippet.py --interactive
        """,
    )

    parser.add_argument("--pattern", "-p", help="Pattern to generate (see --list)")
    parser.add_argument(
        "--board", "-b", default="uno", help="Target board: uno, esp32, rp2040"
    )
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument(
        "--list", "-l", action="store_true", help="List available patterns"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive wizard mode"
    )
    parser.add_argument("--button-pin", type=int, help="Override button pin")
    parser.add_argument("--led-pin", type=int, help="Override LED pin")

    args = parser.parse_args()

    if args.list:
        list_patterns()
        return

    if args.interactive:
        interactive_mode()
        return

    if not args.pattern:
        parser.print_help()
        print("\nError: --pattern is required (or use --list / --interactive)")
        sys.exit(1)

    # Generate code
    kwargs = {}
    if args.button_pin:
        kwargs["button_pin"] = args.button_pin
    if args.led_pin:
        kwargs["led_pin"] = args.led_pin

    code = generate_snippet(args.pattern, args.board, **kwargs)

    if args.output:
        with open(args.output, "w") as f:
            f.write(code)
        print(f"✓ Generated {args.output}")
    else:
        print(code)


if __name__ == "__main__":
    main()
