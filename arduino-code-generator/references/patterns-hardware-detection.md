# Hardware Detection & Adaptive Configuration

## Board Detection Pattern

```cpp
// config.h - Auto-detect board and set defaults

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_NANO)
  #define BOARD_TYPE "Arduino UNO/Nano"
  #define MAX_SRAM 2048
  #define HAS_WIFI false
  #define SERIAL_BAUD 9600
  
#elif defined(ARDUINO_ESP32_DEV) || defined(ESP32)
  #define BOARD_TYPE "ESP32"
  #define MAX_SRAM 327680
  #define HAS_WIFI true
  #define SERIAL_BAUD 115200
  
#elif defined(ARDUINO_ARCH_RP2040)
  #define BOARD_TYPE "Raspberry Pi Pico"
  #define MAX_SRAM 262144
  #define HAS_WIFI false
  #define SERIAL_BAUD 115200
  
#else
  #define BOARD_TYPE "Unknown Board"
  #define MAX_SRAM 2048
  #define HAS_WIFI false
  #define SERIAL_BAUD 9600
#endif

// Runtime board info
struct BoardInfo {
  static const char* getBoardType() { return BOARD_TYPE; }
  static uint32_t getMaxSRAM() { return MAX_SRAM; }
  static bool hasWiFi() { return HAS_WIFI; }
  static uint32_t getSerialBaud() { return SERIAL_BAUD; }
};

void printBoardInfo() {
  Serial.println(F("=== Board Information ==="));
  Serial.print(F("Board: "));
  Serial.println(BoardInfo::getBoardType());
  Serial.print(F("Max SRAM: "));
  Serial.print(BoardInfo::getMaxSRAM());
  Serial.println(F(" bytes"));
  Serial.print(F("WiFi: "));
  Serial.println(BoardInfo::hasWiFi() ? F("Yes") : F("No"));
}
```

## Memory Monitoring

```cpp
#ifdef __AVR__
#include <AvailableMemory.h>

int getFreeMemory() {
  extern int __heap_start, *__brkval;
  int v;
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}
#endif

class MemoryMonitor {
private:
  int minFreeMemory;
  unsigned long checkInterval;
  unsigned long lastCheck;
  
public:
  MemoryMonitor(unsigned long intervalMs = 1000)
    : minFreeMemory(999999), checkInterval(intervalMs), lastCheck(0) {}
  
  void update() {
    unsigned long now = millis();
    if (now - lastCheck >= checkInterval) {
      #ifdef __AVR__
      int freeMem = getFreeMemory();
      if (freeMem < minFreeMemory) {
        minFreeMemory = freeMem;
      }
      
      if (freeMem < 200) {
        Serial.println(F("WARNING: Low memory!"));
      }
      #endif
      lastCheck = now;
    }
  }
  
  void printStats() {
    #ifdef __AVR__
    Serial.print(F("Free SRAM: "));
    Serial.print(getFreeMemory());
    Serial.print(F(" bytes (min: "));
    Serial.print(minFreeMemory);
    Serial.println(F(")"));
    #else
    Serial.println(F("Memory monitoring not available"));
    #endif
  }
};

MemoryMonitor memMonitor;

void setup() {
  Serial.begin(SERIAL_BAUD);
  printBoardInfo();
}

void loop() {
  memMonitor.update();
  
  // Your code here
  
  if (Serial.available() && Serial.read() == 'm') {
    memMonitor.printStats();
  }
}
```

## Adaptive Buffer Sizing

```cpp
// Adjust buffer size based on available SRAM
#if defined(ARDUINO_AVR_UNO)
  #define BUFFER_SIZE 64        // UNO has limited RAM
  #define MAX_SAMPLES 50
#elif defined(ESP32)
  #define BUFFER_SIZE 1024      // ESP32 has plenty of RAM
  #define MAX_SAMPLES 1000
#elif defined(ARDUINO_ARCH_RP2040)
  #define BUFFER_SIZE 512
  #define MAX_SAMPLES 500
#else
  #define BUFFER_SIZE 64        // Safe default for unknown boards
  #define MAX_SAMPLES 50
#endif

class AdaptiveLogger {
private:
  float samples[MAX_SAMPLES];
  uint16_t sampleCount;
  
public:
  AdaptiveLogger() : sampleCount(0) {}
  
  void addSample(float value) {
    if (sampleCount < MAX_SAMPLES) {
      samples[sampleCount++] = value;
    } else {
      Serial.println(F("Buffer full"));
    }
  }
  
  float getAverage() const {
    if (sampleCount == 0) return 0.0;
    float sum = 0.0;
    for (uint16_t i = 0; i < sampleCount; i++) {
      sum += samples[i];
    }
    return sum / sampleCount;
  }
  
  uint16_t getMaxCapacity() const { return MAX_SAMPLES; }
  uint16_t getCurrentCount() const { return sampleCount; }
};
```

## Feature Detection

```cpp
class FeatureDetection {
public:
  static bool hasSPIFFS() {
    #ifdef ESP32
    return true;
    #else
    return false;
    #endif
  }
  
  static bool hasEEPROM() {
    #if defined(ARDUINO_AVR_UNO) || defined(ESP32)
    return true;
    #else
    return false;
    #endif
  }
  
  static bool hasAnalogRead() {
    // All Arduino boards have ADC
    return true;
  }
  
  static bool hasDAC() {
    #ifdef ESP32
    return true;  // ESP32 has 2 DAC channels
    #else
    return false;
    #endif
  }
  
  static uint8_t getAnalogResolution() {
    #ifdef ESP32
    return 12;  // 12-bit ADC
    #elif defined(ARDUINO_ARCH_RP2040)
    return 12;  // 12-bit ADC
    #else
    return 10;  // 10-bit ADC (UNO, Nano)
    #endif
  }
};

void setup() {
  Serial.begin(SERIAL_BAUD);
  
  Serial.println(F("=== Feature Detection ==="));
  Serial.print(F("SPIFFS: "));
  Serial.println(FeatureDetection::hasSPIFFS() ? F("Yes") : F("No"));
  Serial.print(F("EEPROM: "));
  Serial.println(FeatureDetection::hasEEPROM() ? F("Yes") : F("No"));
  Serial.print(F("DAC: "));
  Serial.println(FeatureDetection::hasDAC() ? F("Yes") : F("No"));
  Serial.print(F("ADC Resolution: "));
  Serial.print(FeatureDetection::getAnalogResolution());
  Serial.println(F(" bits"));
}
```

## Key Points
- Use preprocessor directives (#if defined) for compile-time detection
- Create BoardInfo static class for runtime queries
- Monitor SRAM on AVR boards (UNO has only 2KB)
- Adaptive buffer sizing prevents out-of-memory crashes
- Feature detection allows graceful degradation
- Print board info in setup() for debugging
- Use F() macro to store strings in flash (saves SRAM)
