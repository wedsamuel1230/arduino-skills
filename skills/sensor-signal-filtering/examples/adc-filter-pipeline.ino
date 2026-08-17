/*
 * Board-neutral ADC signal pipeline example.
 *
 * Replace SENSOR_PIN and any ADC reference/resolution assumptions after exact
 * board intake. This example reports counts, not volts, so it does not invent
 * a board-specific full-scale value.
 */

constexpr int SENSOR_PIN = A0;
constexpr uint32_t SAMPLE_PERIOD_US = 10000UL;
constexpr float FILTER_ALPHA = 0.20f;

class EmaFilter {
 public:
  float update(float sample) {
    if (!initialized_) {
      value_ = sample;
      initialized_ = true;
    } else {
      value_ = FILTER_ALPHA * sample + (1.0f - FILTER_ALPHA) * value_;
    }
    return value_;
  }

 private:
  float value_ = 0.0f;
  bool initialized_ = false;
};

EmaFilter filter;
uint32_t last_sample_us = 0;

void setup() {
  Serial.begin(115200);
  pinMode(SENSOR_PIN, INPUT);
  Serial.println(F("raw_counts,ema_counts"));
}

void loop() {
  const uint32_t now_us = static_cast<uint32_t>(micros());
  if (static_cast<uint32_t>(now_us - last_sample_us) < SAMPLE_PERIOD_US) {
    return;
  }
  last_sample_us = now_us;

  const int raw_counts = analogRead(SENSOR_PIN);
  const float filtered_counts = filter.update(static_cast<float>(raw_counts));

  Serial.print(raw_counts);
  Serial.print(F(","));
  Serial.println(filtered_counts, 3);
}
