# Research Notes: Sensor Signal Filtering

Date: 2026-08-17

## Local codebase findings

- `skills/arduino-code-generator/references/patterns-filtering.md` and its
  example already provide moving-average, median, and EMA snippets. They are
  code-pattern ownership, not a signal-chain diagnosis or hardware design
  workflow.
- `sensor-calibration-workbench` explicitly starts after detection and signal
  operation are proven. Filtering must therefore keep calibration separate
  from sensor bring-up and electrical diagnosis.
- `circuit-debugger` and `wiring-safety-check` own electrical fault isolation,
  voltage/current/level boundaries, and measurements. The new skill composes
  with them and adds the filter-specific questions: bandwidth, aliasing, ADC
  drive/settling, cutoff, latency, startup, and raw/fault observability.
- `hardware-tdd` and `embedded-project-loop` already define host/simulation/
  build/target/system stages and physical gates. The new skill reuses those
  boundaries rather than inventing a second acceptance ladder.
- The package validators require `metadata.triggers`, a shared contract link,
  valid relative references, and a main `SKILL.md` below 500 lines. Forward
  evals are declarative and can assert terms and route existence.

## Software best-practice notes

| Fact or recommendation | Evidence tier | Application |
|---|---|---|
| Aliasing occurs before digital filtering; sampling must be designed against signal bandwidth and Nyquist | high-confidence engineering fact | Capture raw timestamps and choose a sample rate/analog attenuation before selecting an algorithm |
| Median filters are useful for isolated impulsive samples but are non-linear | engineering fact | Use an odd window and test real step/event preservation |
| Moving averages have bounded history and latency; EMA trades alpha against smoothing and response | engineering fact | State window/alpha, warm-up, group delay, RAM/CPU cost, and threshold impact |
| EMA startup should use the first valid sample rather than an artificial zero | implementation invariant | Host test prevents a false startup transient |
| Kalman/model-based filters require a model and noise assumptions | engineering inference grounded in control practice | Do not present default gains as universal tuning |
| Raw samples, filtered samples, saturation, and quality/fault flags should remain observable | repository evidence and safety inference | Prevent a filter from hiding a disconnected/clipped sensor |

## Hardware best-practice notes

| Fact or recommendation | Evidence tier | Application |
|---|---|---|
| A first-order RC corner is `f_c = 1 / (2 * pi * R * C)` | established circuit relation | Use it as a starting calculation, then verify tolerance and loading |
| ADC sample-and-hold behavior makes source impedance and acquisition time material | MCU-dependent fact | Require the exact MCU datasheet before choosing R or claiming settling |
| A single RC pole gives limited stopband attenuation | established filter behavior | Check anti-alias attenuation; add poles/buffer only with stability/headroom review |
| Capacitors, cables, grounds, references, and supply returns can change the measured signal | hardware-dependent fact | Measure ADC pin, sensor output, rail, and ground under the real load |
| A shared ground does not make a 5 V signal safe for a 3.3 V ADC | repository wiring contract | Route voltage/level questions through `wiring-safety-check` |
| Software smoothing cannot repair clipping, wrong reference, missing ground, or aliasing | engineering fact | Keep hardware gates explicit and retain raw data |

## Sources

Primary/official starting points consulted or linked:

- [Agent Skills quickstart](https://agentskills.io/skill-creation/quickstart)
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)
- [Agent Skills optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Agent Skills evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)
- [Agent Skills using scripts](https://agentskills.io/skill-creation/using-scripts)
- [Microchip AVR121](https://ww1.microchip.com/downloads/en/Appnotes/Atmel-2559-Enhancing-ADC-Resolution-by-Oversampling-and-Averaging-ApplicationNote_AVR121.pdf)
- [ST AN2834](https://www.st.com/resource/en/application_note/an2834-how-to-get-the-best-adc-accuracy-in-stm32-microcontrollers-stmicroelectronics.pdf)
- [Arduino analogRead](https://docs.arduino.cc/language-reference/en/functions/analog-io/analogRead/)
- [Espressif ADC calibration](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc/adc_calibration.html)

The Agent Skills pages were reachable over HTTPS during discovery. Their
rendered site response is documentation HTML rather than a stable local data
file, so the repository's own validators and tests remain the reproducible
acceptance surface. The external electronics links are reference starting
points; exact board, sensor, and MCU claims remain conditional on identity and
datasheet verification.
