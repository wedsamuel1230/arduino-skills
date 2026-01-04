# Sensor Filtering & ADC Patterns

## Moving Average Filter

```cpp
class MovingAverageFilter {
private:
  float* buffer;
  uint8_t size;
  uint8_t index;
  float sum;
  
public:
  MovingAverageFilter(uint8_t windowSize) : size(windowSize), index(0), sum(0) {
    buffer = new float[size];
    for (uint8_t i = 0; i < size; i++) buffer[i] = 0;
  }
  
  ~MovingAverageFilter() { delete[] buffer; }
  
  float filter(float newValue) {
    sum -= buffer[index];
    buffer[index] = newValue;
    sum += newValue;
    index = (index + 1) % size;
    return sum / size;
  }
};

// Usage
MovingAverageFilter tempFilter(10);

void loop() {
  float raw = analogRead(A0);
  float filtered = tempFilter.filter(raw);
  Serial.println(filtered);
  delay(100);
}
```

## Median Filter (Noise Spike Removal)

```cpp
class MedianFilter {
private:
  float* buffer;
  uint8_t size;
  uint8_t index;
  
public:
  MedianFilter(uint8_t windowSize) : size(windowSize), index(0) {
    buffer = new float[size];
  }
  
  float filter(float newValue) {
    buffer[index++] = newValue;
    if (index >= size) index = 0;
    
    float sorted[size];
    memcpy(sorted, buffer, size * sizeof(float));
    
    // Bubble sort
    for (uint8_t i = 0; i < size - 1; i++) {
      for (uint8_t j = 0; j < size - i - 1; j++) {
        if (sorted[j] > sorted[j + 1]) {
          float temp = sorted[j];
          sorted[j] = sorted[j + 1];
          sorted[j + 1] = temp;
        }
      }
    }
    
    return sorted[size / 2];
  }
};
```

## DHT22 Non-Blocking Reader

```cpp
#include <DHT.h>
#include "config.h"

#define DHT_PIN 2
#define DHT_TYPE DHT22

DHT dht(DHT_PIN, DHT_TYPE);
MovingAverageFilter tempFilter(5);

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  static unsigned long lastRead = 0;
  
  if (millis() - lastRead >= 2000) {  // DHT22 needs 2s between reads
    float temp = dht.readTemperature();
    
    if (!isnan(temp)) {
      float filtered = tempFilter.filter(temp);
      Serial.print(F("Temp: "));
      Serial.print(filtered, 1);
      Serial.println(F(" °C"));
    }
    
    lastRead = millis();
  }
}
```

## Calibration Pattern

```cpp
struct SensorCalibration {
  float offset;
  float gain;
};

float applyCalibration(float rawValue, SensorCalibration cal) {
  return (rawValue * cal.gain) + cal.offset;
}

// Example usage
SensorCalibration tempCal = {-0.5, 1.02};  // -0.5°C offset, 2% gain correction
float calibrated = applyCalibration(rawTemp, tempCal);
```

## Validation Pattern

```cpp
bool validateSensorReading(float value, float min, float max) {
  if (isnan(value) || isinf(value)) {
    Serial.println(F("❌ Invalid reading (NaN/Inf)"));
    return false;
  }
  
  if (value < min || value > max) {
    Serial.print(F("⚠️  Out of range: "));
    Serial.println(value);
    return false;
  }
  
  return true;
}

// Usage
float temp = dht.readTemperature();
if (validateSensorReading(temp, -40, 80)) {
  // Use validated temperature
}
```

## Key Points
- Always use filters for ADC readings (analog sensors are noisy)
- Moving average: smooth readings, good for slow-changing sensors
- Median filter: remove spikes, good for sensors with occasional glitches
- DHT22 requires 2000ms between reads (hardware limitation)
- Always validate readings (check for NaN, range limits)
- Calibration: measure known values, calculate offset and gain
