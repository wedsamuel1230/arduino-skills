#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Arduino Project Scaffolding Tool

Generate complete Arduino project structures with config.h, main.ino,
platformio.ini, and README.md from project templates.

Usage:
    uv run scaffold_project.py --type environmental --board esp32 --name "WeatherStation"
    uv run scaffold_project.py --type robot --board uno --output ./my-robot
    uv run scaffold_project.py --interactive
    uv run scaffold_project.py --list
"""

import argparse
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# =============================================================================
# Project Templates
# =============================================================================

PROJECT_TYPES = {
    "environmental": {
        "name": "Environmental Monitor",
        "description": "Multi-sensor data logger (temperature, humidity, light)",
        "sensors": ["DHT22", "Photoresistor"],
        "features": ["CSV logging", "SD card (optional)", "Button control", "LED status"],
        "patterns": ["config", "filtering", "scheduler", "csv", "data-logging"],
        "libraries": ["DHT sensor library"],
    },
    "robot": {
        "name": "Robot Controller",
        "description": "Motor control with obstacle avoidance and state machine",
        "sensors": ["Ultrasonic HC-SR04", "Line sensor (optional)"],
        "actuators": ["DC motors (L298N)", "Servo"],
        "features": ["State machine", "Button control", "Obstacle avoidance"],
        "patterns": ["config", "buttons", "state-machine", "scheduler"],
        "libraries": ["Servo"],
    },
    "iot": {
        "name": "IoT Data Logger",
        "description": "WiFi-connected sensor with MQTT/HTTP data transmission",
        "sensors": ["BME280", "DHT22 (alternative)"],
        "features": ["WiFi connectivity", "MQTT publishing", "JSON formatting", "Deep sleep"],
        "patterns": ["config", "hardware-detection", "scheduler", "filtering"],
        "libraries": ["WiFi", "PubSubClient", "ArduinoJson"],
        "board_requirement": "esp32",
    },
}

BOARD_CONFIGS = {
    "uno": {
        "name": "Arduino UNO",
        "platform": "atmelavr",
        "board": "uno",
        "framework": "arduino",
        "f_cpu": "16000000L",
        "baud": 9600,
        "sram": 2048,
        "defines": ["ARDUINO_AVR_UNO"],
    },
    "esp32": {
        "name": "ESP32 DevKit",
        "platform": "espressif32",
        "board": "esp32dev",
        "framework": "arduino",
        "f_cpu": "240000000L",
        "baud": 115200,
        "sram": 520000,
        "defines": ["ESP32"],
    },
    "rp2040": {
        "name": "Raspberry Pi Pico",
        "platform": "raspberrypi",
        "board": "pico",
        "framework": "arduino",
        "f_cpu": "133000000L",
        "baud": 115200,
        "sram": 264000,
        "defines": ["ARDUINO_ARCH_RP2040"],
    },
}

# =============================================================================
# Template Generators
# =============================================================================


def generate_config_h(project_type: str, board: str, project_name: str) -> str:
    """Generate config.h with board-specific settings."""
    proj = PROJECT_TYPES[project_type]
    
    config = f'''// config.h - Hardware configuration for {project_name}
// Project: {proj["name"]}
// Generated: {datetime.now().strftime("%Y-%m-%d")}

#ifndef CONFIG_H
#define CONFIG_H

// === Board Detection ===
#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_NANO)
  #define BOARD_NAME "Arduino UNO"
  #define LED_PIN 13
  #define BUTTON_PIN 2
  #define I2C_SDA A4
  #define I2C_SCL A5
  #define SRAM_SIZE 2048
  #define SERIAL_BAUD 9600
  #define USE_F_MACRO 1  // Use F() for string constants

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
  #error "Unsupported board! Add configuration."
#endif

'''

    # Project-specific pins
    if project_type == "environmental":
        config += '''// === Environmental Monitor Pins ===
#define DHT_PIN 2
#define LIGHT_PIN A0
#define SD_CS_PIN 10

// Timing intervals (ms)
#define DHT_INTERVAL 2000      // DHT22 needs 2s between reads
#define LIGHT_INTERVAL 1000
#define LOG_INTERVAL 60000
#define HEARTBEAT_INTERVAL 2000

'''
    elif project_type == "robot":
        config += '''// === Robot Controller Pins ===
#define MOTOR_L_EN 5
#define MOTOR_L_IN1 6
#define MOTOR_L_IN2 7
#define MOTOR_R_EN 9
#define MOTOR_R_IN1 10
#define MOTOR_R_IN2 11

#define ULTRASONIC_TRIG 12
#define ULTRASONIC_ECHO 3
#define SERVO_PIN 8

// Robot parameters
#define OBSTACLE_DISTANCE_CM 20
#define MOTOR_SPEED_DEFAULT 200
#define TURN_DURATION_MS 500

'''
    elif project_type == "iot":
        config += '''// === IoT Device Configuration ===
#define DHT_PIN 4
#define STATUS_LED 2

// WiFi credentials (change these!)
#define WIFI_SSID "your-wifi-ssid"
#define WIFI_PASSWORD "your-wifi-password"

// MQTT settings
#define MQTT_SERVER "mqtt.example.com"
#define MQTT_PORT 1883
#define MQTT_TOPIC "sensors/environmental"

// Timing intervals (ms)
#define SENSOR_INTERVAL 30000    // Read sensors every 30s
#define PUBLISH_INTERVAL 60000   // Publish every 60s
#define WIFI_TIMEOUT 30000       // WiFi connection timeout

'''

    config += '''// === Common Settings ===
#define DEBOUNCE_MS 50
#define FILTER_SIZE 10

#endif // CONFIG_H
'''
    return config


def generate_main_ino(project_type: str, board: str, project_name: str) -> str:
    """Generate main.ino for the project type."""
    proj = PROJECT_TYPES[project_type]
    
    if project_type == "environmental":
        return f'''// {project_name} - Environmental Monitor
// {proj["description"]}
// Generated: {datetime.now().strftime("%Y-%m-%d")}

#include "config.h"
#include <DHT.h>

// === Timer Class ===
class EveryMs {{
private:
  unsigned long interval;
  unsigned long lastTrigger;
public:
  EveryMs(unsigned long ms) : interval(ms), lastTrigger(0) {{}}
  bool check() {{
    unsigned long now = millis();
    if (now - lastTrigger >= interval) {{
      lastTrigger = now;
      return true;
    }}
    return false;
  }}
}};

// === Moving Average Filter ===
class MovingAverageFilter {{
private:
  static const uint8_t SIZE = FILTER_SIZE;
  int values[SIZE];
  uint8_t index = 0;
  uint8_t count = 0;
public:
  int filter(int newValue) {{
    values[index] = newValue;
    index = (index + 1) % SIZE;
    if (count < SIZE) count++;
    long sum = 0;
    for (uint8_t i = 0; i < count; i++) sum += values[i];
    return sum / count;
  }}
}};

// === Debounced Button ===
class DebouncedButton {{
private:
  uint8_t pin;
  bool lastState = HIGH;
  unsigned long lastDebounce = 0;
public:
  DebouncedButton(uint8_t p) : pin(p) {{}}
  void begin() {{ pinMode(pin, INPUT_PULLUP); }}
  bool pressed() {{
    bool state = digitalRead(pin);
    if (state != lastState && (millis() - lastDebounce) > DEBOUNCE_MS) {{
      lastDebounce = millis();
      lastState = state;
      return state == LOW;
    }}
    return false;
  }}
}};

// === Global Objects ===
DHT dht(DHT_PIN, DHT22);
MovingAverageFilter lightFilter;
DebouncedButton button(BUTTON_PIN);

EveryMs dhtTimer(DHT_INTERVAL);
EveryMs lightTimer(LIGHT_INTERVAL);
EveryMs logTimer(LOG_INTERVAL);
EveryMs heartbeatTimer(HEARTBEAT_INTERVAL);

struct SensorData {{
  float temperature = NAN;
  float humidity = NAN;
  int lightLevel = 0;
}} data;

bool loggingEnabled = true;
bool ledState = false;

void setup() {{
  Serial.begin(SERIAL_BAUD);
  pinMode(LED_PIN, OUTPUT);
  button.begin();
  dht.begin();
  
  Serial.println(F("=== {project_name} ==="));
  Serial.print(F("Board: "));
  Serial.println(F(BOARD_NAME));
  Serial.println(F("time_ms,temp_c,humidity_%,light"));
}}

void loop() {{
  // Heartbeat LED
  if (heartbeatTimer.check()) {{
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState);
  }}
  
  // Toggle logging with button
  if (button.pressed()) {{
    loggingEnabled = !loggingEnabled;
    Serial.print(F("Logging: "));
    Serial.println(loggingEnabled ? F("ON") : F("OFF"));
  }}
  
  // Read DHT22
  if (dhtTimer.check()) {{
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t)) data.temperature = t;
    if (!isnan(h)) data.humidity = h;
  }}
  
  // Read light sensor
  if (lightTimer.check()) {{
    data.lightLevel = lightFilter.filter(analogRead(LIGHT_PIN));
  }}
  
  // Log data
  if (loggingEnabled && logTimer.check()) {{
    Serial.print(millis());
    Serial.print(',');
    Serial.print(data.temperature, 1);
    Serial.print(',');
    Serial.print(data.humidity, 1);
    Serial.print(',');
    Serial.println(data.lightLevel);
  }}
}}
'''

    elif project_type == "robot":
        return f'''// {project_name} - Robot Controller
// {proj["description"]}
// Generated: {datetime.now().strftime("%Y-%m-%d")}

#include "config.h"
#include <Servo.h>

// === State Machine ===
enum class RobotState {{
  IDLE,
  FORWARD,
  TURNING_LEFT,
  TURNING_RIGHT,
  REVERSE,
  SCANNING
}};

const char* stateNames[] = {{"IDLE", "FORWARD", "LEFT", "RIGHT", "REVERSE", "SCAN"}};

// === Timer Class ===
class EveryMs {{
private:
  unsigned long interval;
  unsigned long lastTrigger;
public:
  EveryMs(unsigned long ms) : interval(ms), lastTrigger(0) {{}}
  bool check() {{
    unsigned long now = millis();
    if (now - lastTrigger >= interval) {{
      lastTrigger = now;
      return true;
    }}
    return false;
  }}
  void reset() {{ lastTrigger = millis(); }}
}};

// === Debounced Button ===
class DebouncedButton {{
private:
  uint8_t pin;
  bool lastState = HIGH;
  unsigned long lastDebounce = 0;
public:
  DebouncedButton(uint8_t p) : pin(p) {{}}
  void begin() {{ pinMode(pin, INPUT_PULLUP); }}
  bool pressed() {{
    bool state = digitalRead(pin);
    if (state != lastState && (millis() - lastDebounce) > DEBOUNCE_MS) {{
      lastDebounce = millis();
      lastState = state;
      return state == LOW;
    }}
    return false;
  }}
}};

// === Global Objects ===
Servo servo;
DebouncedButton startButton(BUTTON_PIN);

RobotState currentState = RobotState::IDLE;
unsigned long stateStartTime = 0;

EveryMs sensorTimer(50);   // Check sensors every 50ms
EveryMs statusTimer(1000); // Print status every 1s

// === Motor Control ===
void setMotors(int leftSpeed, int rightSpeed) {{
  // Left motor
  if (leftSpeed >= 0) {{
    digitalWrite(MOTOR_L_IN1, HIGH);
    digitalWrite(MOTOR_L_IN2, LOW);
  }} else {{
    digitalWrite(MOTOR_L_IN1, LOW);
    digitalWrite(MOTOR_L_IN2, HIGH);
    leftSpeed = -leftSpeed;
  }}
  analogWrite(MOTOR_L_EN, constrain(leftSpeed, 0, 255));
  
  // Right motor
  if (rightSpeed >= 0) {{
    digitalWrite(MOTOR_R_IN1, HIGH);
    digitalWrite(MOTOR_R_IN2, LOW);
  }} else {{
    digitalWrite(MOTOR_R_IN1, LOW);
    digitalWrite(MOTOR_R_IN2, HIGH);
    rightSpeed = -rightSpeed;
  }}
  analogWrite(MOTOR_R_EN, constrain(rightSpeed, 0, 255));
}}

void stopMotors() {{
  setMotors(0, 0);
}}

// === Ultrasonic Sensor ===
long readDistanceCm() {{
  digitalWrite(ULTRASONIC_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(ULTRASONIC_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRASONIC_TRIG, LOW);
  
  long duration = pulseIn(ULTRASONIC_ECHO, HIGH, 30000);
  return duration * 0.034 / 2;  // Convert to cm
}}

// === State Machine ===
void transitionTo(RobotState newState) {{
  if (newState != currentState) {{
    currentState = newState;
    stateStartTime = millis();
    Serial.print(F("State: "));
    Serial.println(stateNames[static_cast<int>(currentState)]);
  }}
}}

void updateStateMachine() {{
  long distance = readDistanceCm();
  unsigned long elapsed = millis() - stateStartTime;
  
  switch (currentState) {{
    case RobotState::IDLE:
      stopMotors();
      break;
      
    case RobotState::FORWARD:
      setMotors(MOTOR_SPEED_DEFAULT, MOTOR_SPEED_DEFAULT);
      if (distance > 0 && distance < OBSTACLE_DISTANCE_CM) {{
        transitionTo(RobotState::REVERSE);
      }}
      break;
      
    case RobotState::REVERSE:
      setMotors(-MOTOR_SPEED_DEFAULT/2, -MOTOR_SPEED_DEFAULT/2);
      if (elapsed > 500) {{
        transitionTo(RobotState::SCANNING);
      }}
      break;
      
    case RobotState::SCANNING:
      stopMotors();
      // Scan left and right, pick clearest direction
      servo.write(45);
      delay(200);
      long leftDist = readDistanceCm();
      servo.write(135);
      delay(200);
      long rightDist = readDistanceCm();
      servo.write(90);
      
      if (leftDist > rightDist) {{
        transitionTo(RobotState::TURNING_LEFT);
      }} else {{
        transitionTo(RobotState::TURNING_RIGHT);
      }}
      break;
      
    case RobotState::TURNING_LEFT:
      setMotors(-MOTOR_SPEED_DEFAULT, MOTOR_SPEED_DEFAULT);
      if (elapsed > TURN_DURATION_MS) {{
        transitionTo(RobotState::FORWARD);
      }}
      break;
      
    case RobotState::TURNING_RIGHT:
      setMotors(MOTOR_SPEED_DEFAULT, -MOTOR_SPEED_DEFAULT);
      if (elapsed > TURN_DURATION_MS) {{
        transitionTo(RobotState::FORWARD);
      }}
      break;
  }}
}}

void setup() {{
  Serial.begin(SERIAL_BAUD);
  
  // Motor pins
  pinMode(MOTOR_L_EN, OUTPUT);
  pinMode(MOTOR_L_IN1, OUTPUT);
  pinMode(MOTOR_L_IN2, OUTPUT);
  pinMode(MOTOR_R_EN, OUTPUT);
  pinMode(MOTOR_R_IN1, OUTPUT);
  pinMode(MOTOR_R_IN2, OUTPUT);
  
  // Ultrasonic pins
  pinMode(ULTRASONIC_TRIG, OUTPUT);
  pinMode(ULTRASONIC_ECHO, INPUT);
  
  // Servo
  servo.attach(SERVO_PIN);
  servo.write(90);
  
  // Button
  startButton.begin();
  pinMode(LED_PIN, OUTPUT);
  
  Serial.println(F("=== {project_name} ==="));
  Serial.println(F("Press button to start/stop"));
}}

void loop() {{
  // Start/stop with button
  if (startButton.pressed()) {{
    if (currentState == RobotState::IDLE) {{
      transitionTo(RobotState::FORWARD);
    }} else {{
      transitionTo(RobotState::IDLE);
    }}
  }}
  
  // Update state machine
  if (sensorTimer.check()) {{
    updateStateMachine();
  }}
  
  // Status LED
  digitalWrite(LED_PIN, currentState != RobotState::IDLE);
  
  // Print status
  if (statusTimer.check()) {{
    Serial.print(F("Distance: "));
    Serial.print(readDistanceCm());
    Serial.println(F(" cm"));
  }}
}}
'''

    elif project_type == "iot":
        return f'''// {project_name} - IoT Data Logger
// {proj["description"]}
// Generated: {datetime.now().strftime("%Y-%m-%d")}
// Requires: ESP32

#include "config.h"

#ifdef HAS_WIFI
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// === Timer Class ===
class EveryMs {{
private:
  unsigned long interval;
  unsigned long lastTrigger;
public:
  EveryMs(unsigned long ms) : interval(ms), lastTrigger(0) {{}}
  bool check() {{
    unsigned long now = millis();
    if (now - lastTrigger >= interval) {{
      lastTrigger = now;
      return true;
    }}
    return false;
  }}
}};

// === Global Objects ===
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
DHT dht(DHT_PIN, DHT22);

EveryMs sensorTimer(SENSOR_INTERVAL);
EveryMs publishTimer(PUBLISH_INTERVAL);
EveryMs statusTimer(5000);

struct SensorData {{
  float temperature = NAN;
  float humidity = NAN;
}} data;

// === WiFi Management ===
bool connectWiFi() {{
  if (WiFi.status() == WL_CONNECTED) return true;
  
  Serial.print(F("Connecting to WiFi"));
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {{
    if (millis() - start > WIFI_TIMEOUT) {{
      Serial.println(F(" FAILED"));
      return false;
    }}
    delay(500);
    Serial.print('.');
  }}
  
  Serial.println(F(" OK"));
  Serial.print(F("IP: "));
  Serial.println(WiFi.localIP());
  return true;
}}

// === MQTT Management ===
bool connectMQTT() {{
  if (mqtt.connected()) return true;
  if (!connectWiFi()) return false;
  
  Serial.print(F("Connecting to MQTT..."));
  
  String clientId = "ESP32-";
  clientId += String(random(0xffff), HEX);
  
  if (mqtt.connect(clientId.c_str())) {{
    Serial.println(F(" OK"));
    return true;
  }}
  
  Serial.print(F(" FAILED, rc="));
  Serial.println(mqtt.state());
  return false;
}}

// === JSON Publishing ===
void publishData() {{
  if (!connectMQTT()) return;
  
  char json[128];
  snprintf(json, sizeof(json),
    "{{\\"temp\\":%.1f,\\"humidity\\":%.1f,\\"uptime\\":%lu}}",
    data.temperature, data.humidity, millis() / 1000);
  
  if (mqtt.publish(MQTT_TOPIC, json)) {{
    Serial.print(F("Published: "));
    Serial.println(json);
  }} else {{
    Serial.println(F("Publish failed"));
  }}
}}

void setup() {{
  Serial.begin(SERIAL_BAUD);
  pinMode(STATUS_LED, OUTPUT);
  dht.begin();
  
  mqtt.setServer(MQTT_SERVER, MQTT_PORT);
  
  Serial.println(F("=== {project_name} ==="));
  Serial.println(F("IoT Environmental Logger"));
  
  connectWiFi();
}}

void loop() {{
  mqtt.loop();
  
  // Status LED (blink when connected)
  static bool ledState = false;
  if (WiFi.status() == WL_CONNECTED) {{
    ledState = !ledState;
    digitalWrite(STATUS_LED, ledState);
  }} else {{
    digitalWrite(STATUS_LED, LOW);
  }}
  
  // Read sensors
  if (sensorTimer.check()) {{
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t)) data.temperature = t;
    if (!isnan(h)) data.humidity = h;
  }}
  
  // Publish data
  if (publishTimer.check()) {{
    publishData();
  }}
  
  // Status output
  if (statusTimer.check()) {{
    Serial.print(F("Temp: "));
    Serial.print(data.temperature, 1);
    Serial.print(F("C, Humidity: "));
    Serial.print(data.humidity, 1);
    Serial.print(F("%, WiFi: "));
    Serial.println(WiFi.status() == WL_CONNECTED ? F("OK") : F("DISCONNECTED"));
  }}
  
  delay(100);
}}

#else
void setup() {{
  Serial.begin(115200);
  Serial.println(F("ERROR: IoT project requires ESP32 with WiFi"));
  Serial.println(F("Please use --board esp32"));
}}
void loop() {{}}
#endif
'''

    return f"// {project_name} - Generated {datetime.now()}\n// TODO: Implement project type '{project_type}'"


def generate_platformio_ini(board: str, project_name: str, libraries: List[str]) -> str:
    """Generate platformio.ini configuration."""
    cfg = BOARD_CONFIGS[board]
    
    lib_deps = "\n".join(f"    {lib}" for lib in libraries) if libraries else "    ; No external libraries"
    
    return f'''; PlatformIO Project Configuration
; {project_name}
; Generated: {datetime.now().strftime("%Y-%m-%d")}

[env:{cfg["board"]}]
platform = {cfg["platform"]}
board = {cfg["board"]}
framework = {cfg["framework"]}

; Serial monitor
monitor_speed = {cfg["baud"]}

; Build flags
build_flags = 
    -D {cfg["defines"][0]}

; Library dependencies
lib_deps =
{lib_deps}

; Upload settings
upload_speed = 921600
'''


def generate_readme(project_name: str, project_type: str, board: str) -> str:
    """Generate README.md for the project."""
    proj = PROJECT_TYPES[project_type]
    cfg = BOARD_CONFIGS[board]
    
    sensors = "\n".join(f"- {s}" for s in proj.get("sensors", []))
    features = "\n".join(f"- {f}" for f in proj["features"])
    
    return f'''# {project_name}

> {proj["description"]}

## Features

{features}

## Hardware Required

**Board:** {cfg["name"]}

**Sensors:**
{sensors}

## Installation

### PlatformIO (Recommended)

```bash
# Clone/download this project
cd {project_name.lower().replace(" ", "-")}

# Build and upload
pio run -t upload

# Open serial monitor
pio device monitor
```

### Arduino IDE

1. Open `src/main.ino`
2. Select board: **{cfg["name"]}**
3. Install required libraries from Library Manager
4. Upload

## Configuration

Edit `src/config.h` to customize:
- Pin assignments
- Timing intervals
- WiFi credentials (if applicable)

## Usage

1. Connect hardware according to pin definitions
2. Upload firmware
3. Open Serial Monitor at {cfg["baud"]} baud
4. Press button to start/stop (if applicable)

## Troubleshooting

- **No serial output:** Check baud rate ({cfg["baud"]})
- **Sensor not detected:** Verify wiring and I2C address
- **WiFi connection fails:** Check credentials in config.h

## License

MIT License - feel free to use and modify!

---
Generated by Arduino Project Builder
'''


# =============================================================================
# Project Scaffolding
# =============================================================================


def scaffold_project(
    project_name: str,
    project_type: str,
    board: str,
    output_dir: Optional[str] = None
) -> str:
    """Create complete project directory structure."""
    
    # Validate inputs
    if project_type not in PROJECT_TYPES:
        return f"Error: Unknown project type '{project_type}'"
    if board not in BOARD_CONFIGS:
        return f"Error: Unknown board '{board}'"
    
    # Check board requirement
    proj = PROJECT_TYPES[project_type]
    if "board_requirement" in proj and board != proj["board_requirement"]:
        return f"Error: {proj['name']} requires {proj['board_requirement']} board"
    
    # Create output directory
    safe_name = project_name.lower().replace(" ", "-")
    if output_dir:
        base_path = Path(output_dir)
    else:
        base_path = Path(safe_name)
    
    src_path = base_path / "src"
    
    try:
        base_path.mkdir(parents=True, exist_ok=True)
        src_path.mkdir(exist_ok=True)
        
        # Generate files
        files_created = []
        
        # config.h
        config_content = generate_config_h(project_type, board, project_name)
        (src_path / "config.h").write_text(config_content)
        files_created.append("src/config.h")
        
        # main.ino
        main_content = generate_main_ino(project_type, board, project_name)
        (src_path / "main.ino").write_text(main_content)
        files_created.append("src/main.ino")
        
        # platformio.ini
        libraries = proj.get("libraries", [])
        pio_content = generate_platformio_ini(board, project_name, libraries)
        (base_path / "platformio.ini").write_text(pio_content)
        files_created.append("platformio.ini")
        
        # README.md
        readme_content = generate_readme(project_name, project_type, board)
        (base_path / "README.md").write_text(readme_content)
        files_created.append("README.md")
        
        # .gitignore
        gitignore = '''.pio/
.vscode/
*.o
*.elf
*.hex
'''
        (base_path / ".gitignore").write_text(gitignore)
        files_created.append(".gitignore")
        
        result = f"✓ Created project: {project_name}\n"
        result += f"  Location: {base_path.absolute()}\n"
        result += f"  Type: {proj['name']}\n"
        result += f"  Board: {BOARD_CONFIGS[board]['name']}\n"
        result += f"  Files created:\n"
        for f in files_created:
            result += f"    - {f}\n"
        result += f"\nNext steps:\n"
        result += f"  cd {base_path}\n"
        result += f"  pio run -t upload\n"
        
        return result
        
    except Exception as e:
        return f"Error creating project: {e}"


def list_project_types():
    """List available project types."""
    print("\n=== Available Project Types ===\n")
    for key, proj in PROJECT_TYPES.items():
        req = f" (requires {proj['board_requirement']})" if "board_requirement" in proj else ""
        print(f"  {key:15} - {proj['name']}{req}")
        print(f"                   {proj['description']}")
        print()
    
    print("=== Supported Boards ===\n")
    for key, cfg in BOARD_CONFIGS.items():
        print(f"  {key:10} - {cfg['name']} ({cfg['sram']} bytes SRAM)")
    print()


def interactive_mode():
    """Interactive project creation wizard."""
    print("\n🔧 Arduino Project Builder - Interactive Mode\n")
    
    # Get project name
    project_name = input("Project name: ").strip()
    if not project_name:
        project_name = "MyArduinoProject"
    
    # Select project type
    print("\nAvailable project types:")
    types_list = list(PROJECT_TYPES.keys())
    for i, t in enumerate(types_list, 1):
        proj = PROJECT_TYPES[t]
        print(f"  {i}. {t} - {proj['name']}")
    
    while True:
        try:
            choice = input("\nSelect type (1-3): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(types_list):
                project_type = types_list[idx]
                break
        except ValueError:
            pass
        print("Invalid choice, try again.")
    
    # Select board
    print("\nAvailable boards:")
    boards_list = list(BOARD_CONFIGS.keys())
    for i, b in enumerate(boards_list, 1):
        cfg = BOARD_CONFIGS[b]
        print(f"  {i}. {b} - {cfg['name']}")
    
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
    
    # Output directory
    output_dir = input(f"\nOutput directory (default: ./{project_name.lower().replace(' ', '-')}): ").strip()
    if not output_dir:
        output_dir = None
    
    # Create project
    print("\n" + "=" * 60)
    result = scaffold_project(project_name, project_type, board, output_dir)
    print(result)


# =============================================================================
# Main
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold complete Arduino projects from templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scaffold_project.py --list
  uv run scaffold_project.py --type environmental --board esp32 --name "WeatherStation"
  uv run scaffold_project.py --type robot --board uno --output ./my-robot
  uv run scaffold_project.py --interactive
        """,
    )
    
    parser.add_argument("--type", "-t", help="Project type (see --list)")
    parser.add_argument("--board", "-b", default="uno", help="Target board: uno, esp32, rp2040")
    parser.add_argument("--name", "-n", default="MyProject", help="Project name")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--list", "-l", action="store_true", help="List project types")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive wizard")
    
    args = parser.parse_args()
    
    if args.list:
        list_project_types()
        return
    
    if args.interactive:
        interactive_mode()
        return
    
    if not args.type:
        parser.print_help()
        print("\nError: --type is required (or use --list / --interactive)")
        sys.exit(1)
    
    result = scaffold_project(args.name, args.type, args.board, args.output)
    print(result)


if __name__ == "__main__":
    main()
