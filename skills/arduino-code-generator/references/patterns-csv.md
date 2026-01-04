# CSV Data Output Pattern

## Basic CSV Logger

```cpp
class CSVLogger {
private:
  bool headerPrinted;
  
public:
  CSVLogger() : headerPrinted(false) {}
  
  void printHeader(const char* header) {
    if (!headerPrinted) {
      Serial.println(header);
      headerPrinted = true;
    }
  }
  
  void logData(float val1, float val2, int val3) {
    Serial.print(val1, 2);
    Serial.print(F(","));
    Serial.print(val2, 2);
    Serial.print(F(","));
    Serial.println(val3);
  }
};

// Usage
CSVLogger logger;

void setup() {
  Serial.begin(115200);
  logger.printHeader("Time_ms,Temp_C,Humidity_%,Light");
}

void loop() {
  static unsigned long lastLog = 0;
  
  if (millis() - lastLog >= 1000) {
    logger.logData(25.5, 60.2, 512);
    lastLog = millis();
  }
}
```

## With Timestamp

```cpp
void logWithTimestamp(float temp, float humid) {
  Serial.print(millis());
  Serial.print(F(","));
  Serial.print(temp, 2);
  Serial.print(F(","));
  Serial.println(humid, 1);
}
```

## Key Points
- Use F() macro for strings on UNO (saves SRAM)
- Print header once at startup
- Use consistent decimal places (temp, 2 = 25.50)
- Excel/Python can import CSV directly
