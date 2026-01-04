# Example BOM: Weather Station Project

**Generated:** 2026-01-04
**Target Board:** ESP32 DevKit
**Quantity:** 1 unit
**Estimated Total:** $35-55 (per unit)

## Project Description
Battery-powered outdoor weather station with temperature, humidity, pressure sensors. Displays on OLED, logs to SD card, sends data via WiFi every 15 minutes.

---

## Core Components

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| 1 | ESP32 DevKit V1 | ESP32-WROOM-32, 38 pins | $6-12 | [Amazon](https://amazon.com/dp/B07Q576VWZ) / [AliExpress](https://aliexpress.com/item/32959541446.html) |
| 1 | MicroSD Card Module | SPI interface, 3.3V | $1-3 | [Amazon](https://amazon.com/dp/B07BJ2P6X6) |
| 1 | MicroSD Card | 8-32GB, Class 10 | $5-10 | [Amazon](https://amazon.com/dp/B073JWXGNT) |

## Sensors

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| 1 | BME280 | I2C, Temp/Humidity/Pressure, 3.3V | $5-12 | [Amazon](https://amazon.com/dp/B07KR24P6P) / [Adafruit](https://adafruit.com/product/2652) |
| 1 | BH1750 | I2C, Light sensor (lux), 3.3V | $2-5 | [Amazon](https://amazon.com/dp/B07DNYPLWD) |

## Display

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| 1 | SSD1306 OLED | I2C, 128x64, 0.96", White | $4-8 | [Amazon](https://amazon.com/dp/B07D9H83WJ) |

## Power Components

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| 1 | TP4056 Module | USB LiPo charger with protection | $1-3 | [Amazon](https://amazon.com/dp/B098T5N1X9) |
| 1 | 18650 Battery | 3.7V 2600mAh+, protected | $5-10 | [Amazon](https://amazon.com/dp/B07Y8FWKGJ) |
| 1 | 18650 Holder | Single cell, wire leads | $1-2 | [Amazon](https://amazon.com/dp/B07CWGN8SL) |
| 1 | MT3608 Boost | 3.7V → 5V step-up | $1-3 | [Amazon](https://amazon.com/dp/B089JYBF25) |
| 1 | Slide Switch | SPDT, panel mount | $0.50 | [Amazon](https://amazon.com/dp/B07RQ7T2T3) |

## Passive Components

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| 2 | 4.7kΩ Resistor | 1/4W, for I2C pull-ups | $0.10 | From resistor kit |
| 2 | 100nF Capacitor | Ceramic, decoupling | $0.10 | From capacitor kit |
| 1 | 100µF Capacitor | Electrolytic, 16V | $0.20 | From capacitor kit |

## Mechanical & Connectors

| Qty | Component | Specifications | Est. Price | Supplier Links |
|-----|-----------|----------------|------------|----------------|
| 1 | Project Enclosure | Weatherproof, ~100x68x50mm | $5-10 | [Amazon](https://amazon.com/dp/B07TYNYW1S) |
| 1 | Cable Glands | PG7, for wire entry | $2-5 | [Amazon](https://amazon.com/dp/B07JNC64M4) |
| 1 | Breadboard | 400 tie points (prototyping) | $2-4 | [Amazon](https://amazon.com/dp/B01EV6LJ7G) |
| 20 | Jumper Wires | M-M and M-F assortment | $3-6 | [Amazon](https://amazon.com/dp/B01EV70C78) |

---

## Cost Summary

| Category | Low Est. | High Est. |
|----------|----------|-----------|
| Core Components | $12 | $25 |
| Sensors | $7 | $17 |
| Display | $4 | $8 |
| Power | $9 | $18 |
| Passives | $0.50 | $1 |
| Mechanical | $10 | $20 |
| **TOTAL** | **$43** | **$89** |

*Note: Prices vary by supplier and region. AliExpress is cheapest but slowest.*

---

## Compatibility Warnings

⚠️ **Voltage:** All sensors are 3.3V - ESP32 is 3.3V logic ✅ Compatible

⚠️ **I2C Addresses:**
- BME280: 0x76 (default) or 0x77
- BH1750: 0x23 (default) or 0x5C
- SSD1306: 0x3C (default) or 0x3D
- **No conflicts with default addresses** ✅

⚠️ **Current Budget:**
```
Component           Typical Current
─────────────────────────────────────
ESP32 (active)      80-240mA
ESP32 (deep sleep)  10µA
BME280              0.1mA
BH1750              0.2mA
SSD1306 OLED        20mA
SD Card (write)     100mA peak
─────────────────────────────────────
Total Active:       ~400mA max
Deep Sleep:         ~0.2mA
```
18650 @ 2600mAh → 6.5 hours continuous, or months with proper sleep cycles

---

## Substitution Notes

💡 **BME280 → DHT22:** Cheaper ($3-5), but less accurate and no pressure. Wire is simpler (single GPIO).

💡 **SSD1306 → 16x2 LCD:** Cheaper ($3), but needs more pins and I2C adapter. Less info display.

💡 **ESP32 → ESP8266:** Cheaper ($3), fewer GPIO, no Bluetooth. Works for this project.

💡 **18650 → 2x AA:** Simpler, no special charger needed. Shorter battery life, voltage less stable.

---

## Tools Required

If not already owned:
- [ ] Soldering iron + solder (for permanent build)
- [ ] Wire strippers
- [ ] Multimeter (essential for debugging)
- [ ] Hot glue gun (for securing components in enclosure)
- [ ] Drill + bits (for enclosure mounting holes)

---

## Wiring Summary

```
ESP32          Component
──────         ─────────
GPIO21 (SDA) → BME280 SDA, BH1750 SDA, OLED SDA
GPIO22 (SCL) → BME280 SCL, BH1750 SCL, OLED SCL
GPIO5  (CS)  → SD Card CS
GPIO18 (SCK) → SD Card SCK
GPIO19 (MISO)→ SD Card MISO
GPIO23 (MOSI)→ SD Card MOSI
3.3V         → All VCC pins
GND          → All GND pins
```

---

## Order Checklist

```
□ ESP32 DevKit
□ BME280 sensor module
□ BH1750 light sensor
□ SSD1306 OLED display
□ MicroSD card module
□ MicroSD card (8GB+)
□ TP4056 charger module
□ 18650 battery (protected!)
□ 18650 holder
□ MT3608 boost converter
□ Enclosure
□ Cable glands
□ Jumper wires
□ Breadboard (if prototyping)
```
