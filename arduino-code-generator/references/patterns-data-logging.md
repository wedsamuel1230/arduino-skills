# Data Logging & Persistence Patterns

## EEPROM Logging with CRC Validation

```cpp
#include <EEPROM.h>

struct LogEntry {
  uint32_t timestamp;
  float temperature;
  float humidity;
  uint16_t crc;
};

class EEPROMLogger {
private:
  uint16_t currentAddress;
  const uint16_t maxAddress;
  
  uint16_t calculateCRC(const LogEntry& entry) {
    uint16_t crc = 0xFFFF;
    const uint8_t* data = (const uint8_t*)&entry;
    for (size_t i = 0; i < sizeof(entry) - sizeof(entry.crc); i++) {
      crc ^= data[i];
      for (uint8_t j = 0; j < 8; j++) {
        if (crc & 0x0001) {
          crc = (crc >> 1) ^ 0xA001;
        } else {
          crc = crc >> 1;
        }
      }
    }
    return crc;
  }
  
public:
  EEPROMLogger(uint16_t maxAddr = 1024) 
    : currentAddress(0), maxAddress(maxAddr) {}
  
  void writeEntry(uint32_t timestamp, float temp, float humid) {
    if (currentAddress + sizeof(LogEntry) > maxAddress) {
      Serial.println(F("EEPROM full"));
      return;
    }
    
    LogEntry entry;
    entry.timestamp = timestamp;
    entry.temperature = temp;
    entry.humidity = humid;
    entry.crc = calculateCRC(entry);
    
    EEPROM.put(currentAddress, entry);
    currentAddress += sizeof(LogEntry);
    
    Serial.print(F("Logged to EEPROM at "));
    Serial.println(currentAddress - sizeof(LogEntry));
  }
  
  bool readEntry(uint16_t index, LogEntry& entry) {
    uint16_t addr = index * sizeof(LogEntry);
    if (addr >= currentAddress) return false;
    
    EEPROM.get(addr, entry);
    
    uint16_t calculatedCRC = calculateCRC(entry);
    if (calculatedCRC != entry.crc) {
      Serial.println(F("CRC mismatch - corrupted data"));
      return false;
    }
    
    return true;
  }
  
  void dumpAll() {
    Serial.println(F("=== EEPROM Dump ==="));
    uint16_t entryCount = currentAddress / sizeof(LogEntry);
    
    for (uint16_t i = 0; i < entryCount; i++) {
      LogEntry entry;
      if (readEntry(i, entry)) {
        Serial.print(entry.timestamp);
        Serial.print(F(","));
        Serial.print(entry.temperature, 2);
        Serial.print(F(","));
        Serial.println(entry.humidity, 2);
      }
    }
  }
  
  void clear() {
    currentAddress = 0;
    Serial.println(F("EEPROM cleared"));
  }
};

EEPROMLogger logger;

void setup() {
  Serial.begin(115200);
}

void loop() {
  static EveryMs logTimer(60000);  // Log every 60 seconds
  
  if (logTimer.check()) {
    float temp = readTemperature();
    float humid = readHumidity();
    logger.writeEntry(millis(), temp, humid);
  }
  
  if (Serial.available() && Serial.read() == 'd') {
    logger.dumpAll();
  }
}
```

## SD Card Buffered Logger

```cpp
#include <SD.h>

class SDBufferedLogger {
private:
  static const uint8_t BUFFER_SIZE = 10;
  String buffer[BUFFER_SIZE];
  uint8_t bufferIndex;
  const char* filename;
  bool sdReady;
  
public:
  SDBufferedLogger(const char* file) 
    : bufferIndex(0), filename(file), sdReady(false) {}
  
  bool begin(uint8_t csPin = 10) {
    sdReady = SD.begin(csPin);
    if (!sdReady) {
      Serial.println(F("SD card init failed"));
      return false;
    }
    
    // Write CSV header if file doesn't exist
    if (!SD.exists(filename)) {
      File dataFile = SD.open(filename, FILE_WRITE);
      if (dataFile) {
        dataFile.println(F("Timestamp,Temperature,Humidity,Light"));
        dataFile.close();
      }
    }
    
    Serial.println(F("SD card ready"));
    return true;
  }
  
  void logData(uint32_t timestamp, float temp, float humid, int light) {
    // Build CSV line
    String line = String(timestamp) + "," + 
                  String(temp, 2) + "," + 
                  String(humid, 2) + "," + 
                  String(light);
    
    buffer[bufferIndex++] = line;
    
    // Flush buffer when full
    if (bufferIndex >= BUFFER_SIZE) {
      flush();
    }
  }
  
  void flush() {
    if (!sdReady || bufferIndex == 0) return;
    
    File dataFile = SD.open(filename, FILE_WRITE);
    if (dataFile) {
      for (uint8_t i = 0; i < bufferIndex; i++) {
        dataFile.println(buffer[i]);
      }
      dataFile.close();
      Serial.print(F("Flushed "));
      Serial.print(bufferIndex);
      Serial.println(F(" entries to SD"));
      bufferIndex = 0;
    } else {
      Serial.println(F("Failed to open SD file"));
    }
  }
  
  void dumpFile() {
    if (!sdReady) return;
    
    File dataFile = SD.open(filename, FILE_READ);
    if (dataFile) {
      Serial.println(F("=== SD Card Contents ==="));
      while (dataFile.available()) {
        Serial.write(dataFile.read());
      }
      dataFile.close();
    }
  }
};

SDBufferedLogger sdLogger("datalog.csv");

void setup() {
  Serial.begin(115200);
  sdLogger.begin(10);  // CS pin 10
}

void loop() {
  static EveryMs logTimer(5000);  // Log every 5 seconds
  
  if (logTimer.check()) {
    float temp = readTemperature();
    float humid = readHumidity();
    int light = analogRead(A0);
    sdLogger.logData(millis(), temp, humid, light);
  }
  
  // Manual flush command
  if (Serial.available() && Serial.read() == 'f') {
    sdLogger.flush();
  }
}
```

## Wear Leveling for Flash Storage

```cpp
#ifdef ESP32
#include <Preferences.h>

class WearLeveledStorage {
private:
  Preferences prefs;
  const char* namespaceName;
  uint8_t currentSlot;
  static const uint8_t MAX_SLOTS = 10;
  
public:
  WearLeveledStorage(const char* ns) : namespaceName(ns), currentSlot(0) {}
  
  bool begin() {
    if (!prefs.begin(namespaceName, false)) {
      Serial.println(F("Failed to init Preferences"));
      return false;
    }
    
    // Load last used slot
    currentSlot = prefs.getUChar("slot", 0);
    return true;
  }
  
  void writeValue(const char* key, float value) {
    // Rotate through slots to distribute writes
    String slotKey = String(key) + String(currentSlot);
    prefs.putFloat(slotKey.c_str(), value);
    
    currentSlot = (currentSlot + 1) % MAX_SLOTS;
    prefs.putUChar("slot", currentSlot);
  }
  
  float readValue(const char* key) {
    // Read from current slot
    uint8_t readSlot = (currentSlot == 0) ? MAX_SLOTS - 1 : currentSlot - 1;
    String slotKey = String(key) + String(readSlot);
    return prefs.getFloat(slotKey.c_str(), 0.0);
  }
  
  void clear() {
    prefs.clear();
    currentSlot = 0;
    Serial.println(F("Storage cleared"));
  }
};

WearLeveledStorage storage("myapp");

void setup() {
  Serial.begin(115200);
  storage.begin();
}

void loop() {
  static EveryMs saveTimer(10000);
  
  if (saveTimer.check()) {
    float temp = readTemperature();
    storage.writeValue("temp", temp);
    Serial.print(F("Saved: "));
    Serial.println(temp);
  }
}
#endif
```

## Circular Buffer for In-Memory Logging

```cpp
template <typename T, uint16_t SIZE>
class CircularBuffer {
private:
  T buffer[SIZE];
  uint16_t writeIndex;
  uint16_t count;
  
public:
  CircularBuffer() : writeIndex(0), count(0) {}
  
  void push(const T& value) {
    buffer[writeIndex] = value;
    writeIndex = (writeIndex + 1) % SIZE;
    if (count < SIZE) count++;
  }
  
  T get(uint16_t index) const {
    if (index >= count) return T();
    uint16_t actualIndex = (writeIndex - count + index + SIZE) % SIZE;
    return buffer[actualIndex];
  }
  
  uint16_t size() const { return count; }
  bool isFull() const { return count == SIZE; }
  
  void clear() {
    writeIndex = 0;
    count = 0;
  }
  
  void dump() const {
    for (uint16_t i = 0; i < count; i++) {
      Serial.println(get(i));
    }
  }
};

CircularBuffer<float, 100> tempHistory;

void loop() {
  static EveryMs sampleTimer(1000);
  
  if (sampleTimer.check()) {
    float temp = readTemperature();
    tempHistory.push(temp);
    
    if (tempHistory.isFull()) {
      Serial.println(F("Buffer full - oldest data overwritten"));
    }
  }
  
  if (Serial.available() && Serial.read() == 'h') {
    tempHistory.dump();
  }
}
```

## Key Points
- EEPROM: Use CRC validation to detect corrupted data
- SD Card: Buffer writes to reduce file open/close operations (reduces wear)
- Wear leveling: Rotate write locations to extend flash lifetime
- Circular buffer: In-memory logging with automatic overflow handling
- Always flush buffers before power loss or reset
- EEPROM has limited write cycles (~100,000 writes per byte)
- F() macro stores strings in flash, not RAM
