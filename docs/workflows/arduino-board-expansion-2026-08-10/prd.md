# Arduino Board Expansion PRD

## Goal

Add a bounded set of mainstream board profiles to the Arduino skill package so
board selection and pin/wiring guidance can cover more exact targets without
turning board-family assumptions into hardware claims.

## Baseline

- Five existing profiles: Uno R3, Uno R4 Minima/WiFi, classic ESP32 DevKit/WROOM,
  ESP32-S3 DevKit, and Pico/Pico W.
- Existing validators pass with 28 active skills and 8/8 contract themes.
- Existing board profiles are protected from content changes in this loop.

## Candidate pool

Research will compare Arduino Mega 2560 Rev3, Arduino Nano Every, Arduino Nano
ESP32, Arduino GIGA R1 WiFi, ESP32-C3 DevKitC-02, and ESP32-C6-DevKitC-1.
Only candidates with at least two authoritative sources and complete required
profile fields will be kept.

## Definition of done

- Four or more new board profiles are added, bringing the total to at least
  nine.
- Each profile has voltage/logic, pins/PWM, ADC, buses, memory, current
  caveats, pitfalls, sources, a fact-to-source map, and explicit gaps.
- Board index, source ledger, and validator discover all profiles without
  duplicating host-specific skill content.
- Existing validators, forward evals, link checks, and regression hashes pass.
- No physical board, upload, power, or deployment success is claimed.
