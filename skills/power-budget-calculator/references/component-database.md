# Component Current Draw Database

Comprehensive reference for common embedded system components.
Data sourced from manufacturer datasheets - always verify with actual datasheet for your specific component.

## Table of Contents
- [Microcontrollers](#microcontrollers)
- [Sensors](#sensors)
- [Displays](#displays)
- [Communication Modules](#communication-modules)
- [Actuators](#actuators)
- [Power Regulators](#power-regulators)

---

## Microcontrollers

### ESP32 (3.3V)
| Mode | Current (mA) | Notes |
|------|--------------|-------|
| Active (WiFi TX) | 260 | Max during transmission |
| Active (WiFi RX) | 95 | Receiving data |
| Active (BT) | 130 | Bluetooth active |
| Active (CPU only) | 80 | 240MHz, no radio |
| Modem Sleep | 20 | CPU active, modem off |
| Light Sleep | 0.8 | RTC + ULP running |
| Deep Sleep | 0.01 | RTC timer only |
| Hibernation | 0.005 | RTC off |

**Datasheet Reference:** ESP32 Technical Reference Manual, Section 8

### ESP8266 (3.3V)
| Mode | Current (mA) | Notes |
|------|--------------|-------|
| Active (TX 802.11b) | 170 | Peak during TX |
| Active (RX) | 56 | Receiving |
| Modem Sleep | 15 | CPU active |
| Light Sleep | 0.5 | |
| Deep Sleep | 0.02 | |

### Arduino Uno (ATmega328P @ 5V)
| Mode | Current (mA) | Notes |
|------|--------------|-------|
| Active | 45 | Including regulator |
| Idle | 35 | CPU halted |
| Power Down | 0.1 | External interrupt wake |

**Note:** Raw ATmega328P @ 3.3V/8MHz uses ~5mA active

### Arduino Nano (5V)
| Mode | Current (mA) | Notes |
|------|--------------|-------|
| Active | 20 | With CH340 USB chip |
| Idle | 15 | |
| Power Down | 0.006 | CH340 draws power when USB connected |

### Raspberry Pi Pico (RP2040 @ 3.3V)
| Mode | Current (mA) | Notes |
|------|--------------|-------|
| Active (Full) | 93 | Both cores @ 133MHz |
| Active (Normal) | 24 | Single core, lower clock |
| Sleep | 1.3 | |
| Dormant | 0.18 | |

### ATtiny85 (3.3V)
| Mode | Current (mA) | Notes |
|------|--------------|-------|
| Active @ 8MHz | 5 | |
| Active @ 1MHz | 1.5 | |
| Idle | 0.5 | |
| Power Down | 0.0001 | WDT disabled |

---

## Sensors

### Temperature/Humidity

| Sensor | Voltage | Measuring (mA) | Sleep (µA) | Notes |
|--------|---------|----------------|------------|-------|
| BME280 | 3.3 | 0.714 | 0.1 | Temp/Hum/Pressure |
| BME680 | 3.3 | 3.1 | 0.15 | + Gas sensor |
| DHT22 | 3.3-5 | 1.5 | 50 | 2s between reads |
| DHT11 | 3.3-5 | 0.5 | 60 | Less accurate |
| SHT31 | 3.3 | 0.8 | 0.2 | High precision |
| DS18B20 | 3.3-5 | 1.5 | 750 (nA) | 1-Wire |

### Motion/Position

| Sensor | Voltage | Active (mA) | Sleep (µA) | Notes |
|--------|---------|-------------|------------|-------|
| MPU6050 | 3.3 | 3.8 | 5 | 6-axis IMU |
| MPU9250 | 3.3 | 3.7 | 8 | 9-axis IMU |
| ADXL345 | 3.3 | 0.14 | 0.1 | 3-axis accel |
| BNO055 | 3.3 | 12.3 | 40 | 9-axis + fusion |

### Distance

| Sensor | Voltage | Active (mA) | Standby (mA) | Notes |
|--------|---------|-------------|--------------|-------|
| HC-SR04 | 5 | 15 | 2 | Ultrasonic 2-400cm |
| VL53L0X | 3.3 | 19 | 0.005 | ToF laser 2m |
| VL53L1X | 3.3 | 20 | 0.005 | ToF laser 4m |

### Light

| Sensor | Voltage | Active (mA) | Sleep (µA) | Notes |
|--------|---------|-------------|------------|-------|
| BH1750 | 3.3 | 0.12 | 0.01 | Lux meter |
| TSL2591 | 3.3 | 0.4 | 0.5 | High dynamic range |
| VEML7700 | 3.3 | 0.045 | 0.5 | Ambient light |

### Pressure/Altitude

| Sensor | Voltage | Active (mA) | Sleep (µA) | Notes |
|--------|---------|-------------|------------|-------|
| BMP180 | 3.3 | 0.65 | 3 | Basic pressure |
| BMP280 | 3.3 | 0.71 | 0.1 | Weather-grade |
| MS5611 | 3.3 | 1.4 | 0.14 | High resolution |

---

## Displays

| Display | Voltage | Active (mA) | Sleep (mA) | Notes |
|---------|---------|-------------|------------|-------|
| OLED 0.96" 128x64 | 3.3 | 10-20 | 0.01 | Depends on pixels lit |
| OLED 1.3" 128x64 | 3.3 | 15-30 | 0.01 | |
| LCD 16x2 (I2C) | 5 | 25 (backlight on) | 2 | |
| LCD 20x4 (I2C) | 5 | 30 | 3 | |
| TFT 1.8" ST7735 | 3.3 | 40 | 0.5 | With backlight |
| TFT 2.4" ILI9341 | 3.3 | 80 | 1 | Touch adds 5mA |
| E-Paper 2.9" | 3.3 | 40 (refresh) | 0.001 | Static display |

**E-Paper Note:** Only draws power during refresh (~2 seconds). Static display essentially zero power.

---

## Communication Modules

### Wireless

| Module | Voltage | TX (mA) | RX (mA) | Sleep (µA) | Notes |
|--------|---------|---------|---------|------------|-------|
| NRF24L01 | 3.3 | 11.3 | 13.5 | 0.9 | 2.4GHz |
| NRF24L01+PA+LNA | 3.3 | 115 | 45 | 0.9 | Long range |
| LoRa SX1276 | 3.3 | 90-120 | 12 | 0.2 | 433/868/915MHz |
| HC-05 | 3.3 | 40 | 8 | - | Bluetooth Classic |
| HM-10 | 3.3 | 8.5 | 8.5 | 0.4 | BLE |
| RFM69 | 3.3 | 45 | 16 | 0.1 | 433/868/915MHz |

### GPS

| Module | Voltage | Acquisition (mA) | Tracking (mA) | Sleep (mA) | Notes |
|--------|---------|------------------|---------------|------------|-------|
| NEO-6M | 3.3-5 | 45 | 35 | 11 | u-blox |
| NEO-7M | 3.3 | 40 | 30 | 7 | |
| NEO-M8N | 3.3 | 35 | 25 | 5 | |
| BN-220 | 3.3-5 | 50 | 25 | - | GPS + GLONASS |

### Wired

| Interface | Typical Current | Notes |
|-----------|-----------------|-------|
| MAX485 (RS485) | 0.5mA idle, 1.2mA TX | |
| MCP2515 (CAN) | 5mA | |
| W5500 (Ethernet) | 132mA | |

---

## Actuators

### Servos

| Servo | Voltage | Moving (mA) | Holding (mA) | Idle (mA) |
|-------|---------|-------------|--------------|-----------|
| SG90 (micro) | 5 | 250-500 | 10 | 5 |
| MG996R | 5 | 500-900 | 50 | 10 |
| MG90S | 5 | 350-650 | 20 | 5 |

### Motors

| Type | Typical Range | Notes |
|------|---------------|-------|
| Small DC motor | 100-500mA | No load to load |
| 28BYJ-48 stepper | 240mA | Per phase |
| NEMA17 stepper | 400-1700mA | Per phase |

### Other

| Actuator | Current | Notes |
|----------|---------|-------|
| 5V Relay | 70-90mA | Coil energized |
| Piezo buzzer | 5-30mA | Depends on frequency |
| LED (standard) | 5-20mA | Per LED |
| WS2812B LED | 60mA max | Full white, per LED |

---

## Power Regulators

Regulator quiescent current (overhead):

| Regulator | Quiescent Current | Notes |
|-----------|-------------------|-------|
| AMS1117-3.3 | 5mA | Linear, common |
| HT7333 | 4µA | Ultra-low dropout |
| MCP1700 | 1.6µA | Low power |
| RT9013 | 25µA | Low dropout |
| AP2112 | 55µA | |

**Note:** Linear regulators waste power as heat: P_waste = (V_in - V_out) × I_load

---

## Measurement Tips

1. **Always measure actual current** - Datasheet values are typical, your component may vary
2. **Consider startup current** - Many devices draw 2-10x more during initialization
3. **Decoupling capacitors** - Add 100µF near power-hungry modules
4. **Separate power rails** - Keep noisy loads (motors) separate from sensitive circuits
5. **Use a current meter** - USB power meters or inline multimeters
