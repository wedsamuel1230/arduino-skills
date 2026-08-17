# Analog Front End

Use exact sensor and MCU datasheets before choosing values. The values below
are design relationships and measurement questions, not board-independent pin
limits.

## Simple RC input network

For a voltage-output sensor, a common first-order low-pass is:

```text
sensor output ---- Rseries ----+---- ADC input
                               |
                               C
                               |
                              AGND
```

Its ideal corner is `f_c = 1 / (2 * pi * Rseries * C)`. Choose the passband,
sample rate, required attenuation near and above Nyquist, sensor loading, and
latency together. A single RC pole is shallow; it may be insufficient for a
strict anti-alias requirement. More poles or an active filter need a verified
buffer, stability, headroom, noise, and power budget.

## ADC drive and settling

The ADC input often charges an internal sampling capacitor during acquisition.
An external resistor and a high-impedance sensor can prevent the input from
settling, especially at higher sample rates or after a large voltage step.
Check the exact MCU ADC acquisition-time and source-impedance guidance. If the
settling error is too large, consider a lower impedance path, a supported
longer acquisition time, or a stable buffer amplifier. Do not copy a resistor
value from another board family.

Also check whether the sensor output is stable with the added capacitive load.
Some modules require a minimum load, a particular cable capacitance, or a
buffer. Verify the sensor's output range against the ADC input and absolute
maximum limits; a shared ground does not make an over-voltage signal safe.

## Noise and protection checklist

- Place sensor and ADC decoupling according to their datasheets; check rail
  noise under the actual radio, motor, display, or relay load.
- Keep high-current and fast digital return paths away from the analog return;
  document the chosen ground topology instead of promising that a star ground
  always solves noise.
- Use short wiring, suitable shielding/twisted pairs, and a defined reference
  for long or exposed sensor leads. Inspect cable pickup before increasing
  software smoothing.
- Add series impedance, clamps, or a qualified level shifter only after checking
  leakage, clamp current, input absolute maximum, startup state, and failure
  energy. Follow `wiring-safety-check` for 5 V/3.3 V boundaries.
- Preserve the raw ADC range and detect saturation. A capacitor cannot repair a
  clipped input, missing ground, wrong reference, or disconnected sensor.

## Measurement sequence

1. With the sensor disconnected, verify board ground, ADC reference/configured
   range, and the legal input voltage using an appropriate instrument.
2. Apply a known safe DC level or a calibrated source and record raw counts at
   the intended sample rate.
3. Connect the sensor and repeat with quiet and worst-case loads. Compare ADC
   pin, sensor output, supply, and ground observations.
4. For a filter candidate, inject a bounded step or frequency sweep and record
   the raw and filtered response, settling time, cutoff estimate, and any
   clipping or oscillation.
5. Change one component, routing choice, or software parameter per iteration;
   record the result and the rollback point.

No host calculation or successful compile substitutes for these target-side
measurements. If no meter or scope is available, report the hardware gate as
blocked and give one concrete measurement request.

## Source starting points

- [Microchip AVR121: Enhancing ADC Resolution by Oversampling](https://ww1.microchip.com/downloads/en/Appnotes/Atmel-2559-Enhancing-ADC-Resolution-by-Oversampling-and-Averaging-ApplicationNote_AVR121.pdf)
- [ST AN2834: How to get the best ADC accuracy in STM32 microcontrollers](https://www.st.com/resource/en/application_note/an2834-how-to-get-the-best-adc-accuracy-in-stm32-microcontrollers-stmicroelectronics.pdf)
- [Arduino analogRead reference](https://docs.arduino.cc/language-reference/en/functions/analog-io/analogRead/)
- [Espressif ADC calibration API](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc/adc_calibration.html)
