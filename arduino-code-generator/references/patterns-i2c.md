# I2C Communication Patterns

## I2C Scanner

```cpp
#include <Wire.h>

void scanI2C() {
  Serial.println(F("\n=== I2C Scanner ==="));
  uint8_t found = 0;
  
  for (uint8_t addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    uint8_t error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.print(F("Device found at 0x"));
      if (addr < 16) Serial.print(F("0"));
      Serial.println(addr, HEX);
      found++;
    }
  }
  
  Serial.print(F("Total devices: "));
  Serial.println(found);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  scanI2C();
}
```

## Read Register Pattern

```cpp
uint8_t readRegister(uint8_t addr, uint8_t reg) {
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(addr, (uint8_t)1);
  return Wire.read();
}

// Usage
uint8_t chipID = readRegister(0x76, 0xD0);  // BME280 chip ID
```

## Write Register Pattern

```cpp
void writeRegister(uint8_t addr, uint8_t reg, uint8_t value) {
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.write(value);
  Wire.endTransmission();
}
```

## Device Detection

```cpp
bool checkI2CDevice(uint8_t addr) {
  Wire.beginTransmission(addr);
  return (Wire.endTransmission() == 0);
}

// Usage
if (checkI2CDevice(0x76)) {
  Serial.println(F("BME280 detected!"));
}
```
