---
name: sensor-signal-filtering
description: Use when the main problem is a noisy or aliased analog/ADC signal and the task needs signal-chain diagnosis or filter-path selection across sampling, anti-aliasing, RC/input conditioning, ADC source impedance/settling, latency, startup, saturation, or raw/fault observability. Apply it when software filtering and hardware signal conditioning interact, even when the request only says that an analog sensor is unstable. Hand reusable Arduino snippets to arduino-code-generator, board facts to board-support, voltage/pin/rail safety to wiring-safety-check or circuit-debugger, and calibration after detection to sensor-calibration-workbench.
metadata: {triggers: "ADC noise, analog sensor filtering, sensor signal conditioning, RC low-pass, anti-aliasing, EMA, median filter, moving average, source impedance, ADC settling"}
---

# Sensor Signal Filtering

Design the signal chain from sensor output to reported value. Keep raw samples,
filtered values, timing, saturation, and fault flags observable; a filter must
not conceal a broken sensor or unsafe voltage.

## Intake gate

Record or label unknowns before selecting a component or algorithm:

- exact board, MCU, core/framework, ADC channel, resolution, reference, input
  range, acquisition time, and toolchain versions
- sensor part/module, output type and drive impedance, supply, cable length,
  expected signal bandwidth, valid range, warm-up, and failure behavior
- sample period/jitter budget, acceptable latency, step-response requirement,
  threshold policy, calibration model, and available measurement tools

Resolve the board with `board-support` before board-specific ADC advice. For
physical or multi-session work, load `embedded-project-loop` first and keep its
measurement gate open.

## Workflow

1. Capture raw samples at a stated, repeatable rate before filtering. Separate
   sensor dynamics from spikes, aliasing, quantization, ADC settling, rail/
   ground noise, EMI, and calibration error.
2. Set the sampling rate from the signal bandwidth and latency budget. Check
   Nyquist and alias attenuation; do not use a software filter to recover
   information already aliased into the band.
3. Choose one filter with an explicit window/alpha/model and calculate its
   startup behavior, delay, memory, CPU cost, and effect on thresholds.
   Common starting choices are moving-average for bounded windows, median for
   isolated spikes, and EMA/IIR for low-cost smoothing; model-based filters
   require a stated model and noise assumptions.
4. Check the analog path: sensor loading, RC cutoff, ADC acquisition/settling,
   reference and ground, cable/noise coupling, input protection, voltage
   limits, decoupling, and motor/radio current return paths.
5. Implement raw-plus-filtered telemetry and fault/saturation indicators.
   Validate deterministic vectors on the host before target compilation.
6. Change one causal variable per hardware iteration. Measure the ADC pin and
   supply/ground with the same configuration used by the firmware.

## Load on demand

- Read [`references/filter-selection.md`](references/filter-selection.md) for
  sampling math, algorithm tradeoffs, calibration order, and latency choices.
- Read [`references/analog-front-end.md`](references/analog-front-end.md) for
  RC/input networks, ADC drive/settling, wiring, protection, and measurements.
- Read [`references/verification-and-tdd.md`](references/verification-and-tdd.md)
  for host, simulation, build, target, and system gates.
- Use the diagnostic-only [`examples/adc-filter-pipeline.ino`](examples/adc-filter-pipeline.ino)
  as a board-neutral fixed-rate EMA starting point; fill in board-specific ADC
  assumptions before converting counts to volts. Reusable generated filtering
  patterns remain owned by `arduino-code-generator`.
- Run the deterministic helper with `python3
  scripts/filter_benchmark.py --help` or a captured vector. It is a design/TDD
  aid, not a replacement for target timing or electrical measurements.

The existing [`arduino-code-generator` filtering pattern](../arduino-code-generator/references/patterns-filtering.md)
owns reusable code snippets. This skill owns signal-chain diagnosis, filter
selection, hardware interaction, and evidence boundaries. Use
`circuit-debugger` for fault isolation, `wiring-safety-check` for logic and
rail limits, and `sensor-calibration-workbench` only after detection and signal
integrity are established.

## Output contract

Use the [shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence, known limitations, and recovery/security notes.

- **Build proof:** host tests and an exact-board compile, if run.
- **Upload proof:** an uploader result for a named port/image, if run.
- **Hardware proof:** measured ADC pin, rail/ground, waveform, or wiring result.
- **System proof:** observed sensor behavior under the real load/environment.
- **Deployment proof:** field rollout, rollback, and maintenance evidence.

Never promote a passing host test, HTTP response, serial banner, or CI job to
hardware or system proof. If the board, sensor, circuit, or measurement is
unknown, stop at a bounded plan and name the next measurement.
