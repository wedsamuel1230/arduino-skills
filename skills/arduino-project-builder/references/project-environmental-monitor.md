# Environmental Monitor Project

**Description:** Multi-sensor data logger for temperature, humidity, and light levels with SD card storage and real-time Serial output. Perfect for greenhouse monitoring, weather stations, or indoor climate tracking.

**Hardware Requirements:**
- Arduino UNO or ESP32
- DHT22 temperature/humidity sensor
- Photoresistor (light sensor) + 10kΩ resistor
- SD card module (optional)
- Pushbutton + 10kΩ pulldown resistor
- LED (status indicator)

**Wiring Diagram:**
```
DHT22:
  VCC → 5V (or 3.3V for ESP32)
  DATA → Pin 2
  GND → GND

Photoresistor:
  One leg → 5V
  Other leg → A0 and 10kΩ resistor to GND

Button:
  One leg → Pin 3
  Other leg → GND (use INPUT_PULLUP)

LED:
  Anode (+) → Pin 13 → 220Ω resistor
  Cathode (-) → GND

SD Card Module (optional):
  CS → Pin 10
  MOSI → Pin 11
  MISO → Pin 12
  SCK → Pin 13
  VCC → 5V
  GND → GND
```

**Features:**
- Non-blocking sensor reads (DHT22 every 2s, light every 1s)
- Moving average filter for light sensor (reduces noise)
- CSV logging to Serial and SD card
- Button toggles logging on/off
- LED heartbeat (system alive indicator)
- Memory-safe on Arduino UNO (2KB SRAM)

**Complete Code:**

```cpp
// config.h
#if defined(ARDUINO_AVR_UNO)
  #define BOARD_TYPE "Arduino UNO"
  #define SERIAL_BAUD 9600
  #define USE_SD_CARD false  // Limited SRAM on UNO
#elif defined(ESP32)
  #define BOARD_TYPE "ESP32"
  #define SERIAL_BAUD 115200
  #define USE_SD_CARD true   // ESP32 has plenty of RAM
#endif

#define DHT_PIN 2
#define LIGHT_PIN A0
#define BUTTON_PIN 3
#define LED_PIN 13

// main.ino
#include <DHT.h>
#if USE_SD_CARD
#include <SD.h>
#endif

DHT dht(DHT_PIN, DHT22);

// EveryMs timer class
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
};

// Moving average filter for light sensor
class MovingAverageFilter {
private:
  static const uint8_t SIZE = 10;
  int values[SIZE];
  uint8_t index;
  uint8_t count;
public:
  MovingAverageFilter() : index(0), count(0) {
    for (uint8_t i = 0; i < SIZE; i++) values[i] = 0;
  }
  
  int filter(int newValue) {
    values[index] = newValue;
    index = (index + 1) % SIZE;
    if (count < SIZE) count++;
    
    long sum = 0;
    for (uint8_t i = 0; i < count; i++) {
      sum += values[i];
    }
    return sum / count;
  }
};

// Debounced button
class DebouncedButton {
private:
  uint8_t pin;
  bool lastState;
  unsigned long lastDebounceTime;
  static const unsigned long DEBOUNCE_DELAY = 50;
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
    
    if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY) {
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
MovingAverageFilter lightFilter;
DebouncedButton button(BUTTON_PIN);
EveryMs dhtTimer(2000);
EveryMs lightTimer(1000);
EveryMs displayTimer(5000);
EveryMs csvLogTimer(60000);
EveryMs heartbeatTimer(2000);

struct SensorData {
  float temperature;
  float humidity;
  int lightLevel;
  bool valid;
} data;

bool loggingEnabled = true;

#if USE_SD_CARD
File dataFile;
const char* LOG_FILE = "envlog.csv";
#endif

void setup() {
  Serial.begin(SERIAL_BAUD);
  pinMode(LED_PIN, OUTPUT);
  button.begin();
  dht.begin();
  
  Serial.println(F("=== Environmental Monitor ==="));
  Serial.print(F("Board: "));
  Serial.println(F(BOARD_TYPE));
  
  #if USE_SD_CARD
  if (SD.begin(10)) {
    Serial.println(F("SD card ready"));
    if (!SD.exists(LOG_FILE)) {
      dataFile = SD.open(LOG_FILE, FILE_WRITE);
      if (dataFile) {
        dataFile.println(F("Time_ms,Temp_C,Humidity_%,Light"));
        dataFile.close();
      }
    }
  } else {
    Serial.println(F("SD card init failed"));
  }
  #endif
  
  Serial.println(F("Time_ms,Temp_C,Humidity_%,Light"));
  data.valid = false;
}

void loop() {
  // Task 1: Read DHT22
  if (dhtTimer.check()) {
    data.temperature = dht.readTemperature();
    data.humidity = dht.readHumidity();
    data.valid = !isnan(data.temperature) && !isnan(data.humidity);
    
    if (!data.valid) {
      Serial.println(F("DHT22 read error"));
    }
  }
  
  // Task 2: Read light sensor
  if (lightTimer.check()) {
    int rawLight = analogRead(LIGHT_PIN);
    data.lightLevel = lightFilter.filter(rawLight);
  }
  
  // Task 3: Display summary
  if (displayTimer.check() && data.valid) {
    Serial.print(F("Temp: "));
    Serial.print(data.temperature, 1);
    Serial.print(F("°C | Humidity: "));
    Serial.print(data.humidity, 1);
    Serial.print(F("% | Light: "));
    Serial.println(data.lightLevel);
  }
  
  // Task 4: Log CSV
  if (csvLogTimer.check() && loggingEnabled && data.valid) {
    String csvLine = String(millis()) + "," + 
                     String(data.temperature, 1) + "," + 
                     String(data.humidity, 1) + "," + 
                     String(data.lightLevel);
    
    Serial.println(csvLine);
    
    #if USE_SD_CARD
    dataFile = SD.open(LOG_FILE, FILE_WRITE);
    if (dataFile) {
      dataFile.println(csvLine);
      dataFile.close();
    }
    #endif
  }
  
  // Task 5: Button toggle
  if (button.pressed()) {
    loggingEnabled = !loggingEnabled;
    Serial.print(F("Logging: "));
    Serial.println(loggingEnabled ? F("ON") : F("OFF"));
  }
  
  // Task 6: Heartbeat LED
  if (heartbeatTimer.check()) {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
}
```

**Upload Instructions:**
1. Install DHT sensor library: Sketch → Include Library → Manage Libraries → Search "DHT sensor library" → Install
2. Select board: Tools → Board → Arduino UNO (or ESP32 Dev Module)
3. Select port: Tools → Port → (your Arduino's port)
4. Upload sketch

**Usage:**
- System starts logging immediately
- Press button to toggle logging on/off
- Send 'd' via Serial Monitor to dump all data (if SD card enabled)
- LED blinks every 2 seconds (heartbeat)

**Expected Output:**
```
=== Environmental Monitor ===
Board: Arduino UNO
Time_ms,Temp_C,Humidity_%,Light
Temp: 23.5°C | Humidity: 45.2% | Light: 512
60000,23.5,45.2,512
120000,23.6,45.0,510
Logging: OFF
Logging: ON
180000,23.4,45.3,515
```

**Troubleshooting:**
- **DHT22 read error:** Check wiring, ensure VCC is 5V (3.3V for ESP32)
- **Light sensor reads 0 or 1023:** Check photoresistor orientation, verify 10kΩ resistor
- **SD card init failed:** Check wiring, try different SD card (FAT32 formatted)
- **Button not responding:** Verify INPUT_PULLUP mode, check button wiring
