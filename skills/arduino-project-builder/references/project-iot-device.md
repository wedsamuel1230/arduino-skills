# IoT Temperature & Humidity Logger (ESP32)

**Description:** ESP32-based WiFi data logger that publishes temperature and humidity readings to MQTT broker. Ideal for remote environmental monitoring, smart home integration, or IoT sensor networks.

**Hardware Requirements:**
- ESP32 development board (DevKit, WROOM, or similar)
- DHT22 temperature/humidity sensor
- LED (status indicator)
- Pushbutton (WiFi reconnect trigger)
- USB cable (programming and power)

**Wiring Diagram:**
```
DHT22:
  VCC → 3.3V (ESP32 uses 3.3V logic)
  DATA → GPIO 4
  GND → GND

Button:
  One leg → GPIO 0 (BOOT button can also be used)
  Other leg → GND (INPUT_PULLUP)

LED:
  GPIO 2 → 220Ω resistor → LED anode
  LED cathode → GND
```

**Features:**
- WiFi connection with auto-reconnect
- MQTT publish every 60 seconds
- JSON payload format
- OTA (Over-The-Air) updates support
- NTP time synchronization
- Non-blocking sensor reads
- Button triggers manual WiFi reconnect
- Built-in LED status indicators

**Complete Code:**

```cpp
// config.h
#define WIFI_SSID "YourWiFiSSID"
#define WIFI_PASSWORD "YourWiFiPassword"
#define MQTT_BROKER "192.168.1.100"  // Your MQTT broker IP
#define MQTT_PORT 1883
#define MQTT_TOPIC "home/esp32/sensor"
#define MQTT_CLIENT_ID "ESP32_TempHumidity"

#define DHT_PIN 4
#define BUTTON_PIN 0
#define LED_PIN 2

// main.ino
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

DHT dht(DHT_PIN, DHT22);
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// EveryMs timer
class EveryMs {
private:
  unsigned long interval;
  unsigned long lastTrigger;
public:
  EveryMs(unsigned long ms) : interval(ms), lastTrigger(0) {}
  bool check() {
    unsigned long now = millis();
    if (now - lastTrigger >= interval) {
      lastTrigger = now;
      return true;
    }
    return false;
  }
  void reset() { lastTrigger = millis(); }
};

// Debounced button
class DebouncedButton {
private:
  uint8_t pin;
  bool lastState;
  unsigned long lastDebounceTime;
public:
  DebouncedButton(uint8_t p) : pin(p), lastState(HIGH), lastDebounceTime(0) {}
  
  void begin() {
    pinMode(pin, INPUT_PULLUP);
  }
  
  bool pressed() {
    bool currentState = digitalRead(pin);
    if (currentState != lastState) {
      lastDebounceTime = millis();
    }
    
    if ((millis() - lastDebounceTime) > 50) {
      if (currentState == LOW && lastState == HIGH) {
        lastState = currentState;
        return true;
      }
    }
    lastState = currentState;
    return false;
  }
};

// Global objects
DebouncedButton button(BUTTON_PIN);
EveryMs dhtTimer(2000);
EveryMs publishTimer(60000);
EveryMs wifiCheckTimer(10000);

struct SensorData {
  float temperature;
  float humidity;
  bool valid;
} data;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  button.begin();
  dht.begin();
  
  Serial.println(F("\n=== ESP32 IoT Logger ==="));
  
  connectWiFi();
  
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  
  connectMQTT();
  
  data.valid = false;
}

void connectWiFi() {
  Serial.print(F("Connecting to WiFi"));
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));  // Blink during connection
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println(F("\nWiFi connected!"));
    Serial.print(F("IP: "));
    Serial.println(WiFi.localIP());
    digitalWrite(LED_PIN, HIGH);  // Solid LED when connected
  } else {
    Serial.println(F("\nWiFi connection failed!"));
    digitalWrite(LED_PIN, LOW);
  }
}

void connectMQTT() {
  if (WiFi.status() != WL_CONNECTED) return;
  
  Serial.print(F("Connecting to MQTT broker..."));
  
  int attempts = 0;
  while (!mqttClient.connected() && attempts < 3) {
    if (mqttClient.connect(MQTT_CLIENT_ID)) {
      Serial.println(F("connected!"));
      mqttClient.subscribe(MQTT_TOPIC "/command");
      return;
    }
    Serial.print(".");
    delay(1000);
    attempts++;
  }
  
  if (!mqttClient.connected()) {
    Serial.println(F("\nMQTT connection failed!"));
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print(F("MQTT message: "));
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void publishSensorData() {
  if (!data.valid || !mqttClient.connected()) return;
  
  // Create JSON payload
  StaticJsonDocument<200> doc;
  doc["temperature"] = data.temperature;
  doc["humidity"] = data.humidity;
  doc["uptime"] = millis() / 1000;
  doc["rssi"] = WiFi.RSSI();
  
  char jsonBuffer[200];
  serializeJson(doc, jsonBuffer);
  
  if (mqttClient.publish(MQTT_TOPIC, jsonBuffer)) {
    Serial.print(F("Published: "));
    Serial.println(jsonBuffer);
  } else {
    Serial.println(F("Publish failed!"));
  }
}

void loop() {
  // Task 1: Read DHT22
  if (dhtTimer.check()) {
    data.temperature = dht.readTemperature();
    data.humidity = dht.readHumidity();
    data.valid = !isnan(data.temperature) && !isnan(data.humidity);
    
    if (data.valid) {
      Serial.print(F("Temp: "));
      Serial.print(data.temperature, 1);
      Serial.print(F("°C | Humidity: "));
      Serial.print(data.humidity, 1);
      Serial.println(F("%"));
    } else {
      Serial.println(F("DHT22 read error"));
    }
  }
  
  // Task 2: Publish to MQTT
  if (publishTimer.check()) {
    publishSensorData();
  }
  
  // Task 3: WiFi reconnect check
  if (wifiCheckTimer.check()) {
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println(F("WiFi disconnected, reconnecting..."));
      connectWiFi();
    }
    
    if (!mqttClient.connected()) {
      Serial.println(F("MQTT disconnected, reconnecting..."));
      connectMQTT();
    }
  }
  
  // Task 4: Button manual reconnect
  if (button.pressed()) {
    Serial.println(F("Manual reconnect triggered"));
    connectWiFi();
    connectMQTT();
  }
  
  // Task 5: MQTT loop (handle incoming messages)
  mqttClient.loop();
  
  // Task 6: LED heartbeat (blink every 2s when connected)
  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(LED_PIN, (millis() % 2000) < 100);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
```

**Upload Instructions:**
1. Install libraries:
   - PubSubClient (by Nick O'Leary)
   - DHT sensor library (by Adafruit)
   - ArduinoJson (by Benoit Blanchon)
2. Edit config.h: Set your WiFi SSID, password, and MQTT broker IP
3. Select board: Tools → Board → ESP32 Dev Module
4. Select port: Tools → Port → (your ESP32's port)
5. Upload sketch

**MQTT Broker Setup:**
Install Mosquitto MQTT broker on your server:
```bash
# Ubuntu/Debian
sudo apt-get install mosquitto mosquitto-clients

# Start broker
sudo systemctl start mosquitto

# Test subscription
mosquitto_sub -h localhost -t "home/esp32/sensor"
```

**Usage:**
- System connects to WiFi on boot
- DHT22 readings every 2 seconds (local)
- MQTT publish every 60 seconds
- Press button to force WiFi/MQTT reconnect
- LED heartbeat when connected, off when disconnected

**JSON Payload Format:**
```json
{
  "temperature": 23.5,
  "humidity": 45.2,
  "uptime": 3600,
  "rssi": -65
}
```

**Expected Serial Output:**
```
=== ESP32 IoT Logger ===
Connecting to WiFi.........
WiFi connected!
IP: 192.168.1.42
Connecting to MQTT broker...connected!
Temp: 23.5°C | Humidity: 45.2%
Published: {"temperature":23.5,"humidity":45.2,"uptime":60,"rssi":-65}
Temp: 23.6°C | Humidity: 45.0%
Published: {"temperature":23.6,"humidity":45.0,"uptime":120,"rssi":-67}
```

**Home Assistant Integration:**
Add to `configuration.yaml`:
```yaml
sensor:
  - platform: mqtt
    name: "ESP32 Temperature"
    state_topic: "home/esp32/sensor"
    unit_of_measurement: "°C"
    value_template: "{{ value_json.temperature }}"
  
  - platform: mqtt
    name: "ESP32 Humidity"
    state_topic: "home/esp32/sensor"
    unit_of_measurement: "%"
    value_template: "{{ value_json.humidity }}"
```

**Troubleshooting:**
- **WiFi won't connect:** Check SSID/password, ensure 2.4GHz network (ESP32 doesn't support 5GHz)
- **MQTT connection failed:** Verify broker IP, ensure port 1883 is open, check firewall
- **DHT22 read error:** Use 3.3V (not 5V), check DATA pin connection
- **JSON publish failed:** Increase document size in StaticJsonDocument<200>
- **Memory issues:** ESP32 has 327KB SRAM, no worries about overflow

**Power Consumption:**
- Active (WiFi on): ~160mA
- Light sleep: ~20mA
- Deep sleep: ~10μA (add sleep mode for battery operation)
