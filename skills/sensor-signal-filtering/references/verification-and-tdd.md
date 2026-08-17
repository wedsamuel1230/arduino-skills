# Verification And TDD

## Test in layers

Keep the maker and checker separate. The bundled Python tests are deterministic
behavior evidence; an independent review checks that the skill's advice and
scope match the request.

| Stage | What it can prove | What it cannot prove |
|---|---|---|
| Host unit/vector test | Filter startup, bounds, spike/step behavior, parameter errors | Arduino timing, ADC physics, sensor health |
| Simulation or recorded replay | Candidate response on a known vector and latency tradeoff | New electrical noise, component tolerance, target ADC behavior |
| Exact-board compile | Source/toolchain compatibility for the named FQBN | Upload, wiring, waveform, system behavior |
| Upload/serial observation | Named image reached a named port and emitted the expected log | Correct circuit, filtered signal, or physical safety |
| Target measurement | ADC pin, rail/ground, waveform, saturation, and component response | Generalization beyond the measured setup |
| System test | Sensor behavior under real load/environment and acceptance limits | Deployment or long-term drift unless measured |

## Behavior-first checklist

Before changing the helper or example, add a failing test for the intended
behavior. At minimum cover:

- first-sample initialization without an artificial zero transient
- odd-window median rejection of one isolated spike
- moving-average warm-up and bounded history
- EMA step response, bounds, and alpha validation
- malformed/non-finite input and structured CLI output

The target integration gate separately covers raw sample preservation and
explicit saturation/fault handling. It needs an exact ADC range and sensor
fault contract, so it must be tested on the target rather than guessed in the
board-neutral host helper.

Run:

```text
python3 -m unittest tests/test_sensor_signal_filtering.py
python3 skills/sensor-signal-filtering/scripts/filter_benchmark.py --help
```

## Target test record

Record the exact board/revision, core/tool versions, ADC configuration, sensor,
component values/tolerances, ambient/load state, sample period, raw capture,
filtered capture, and acceptance threshold. Label each result as build,
upload, hardware, system, or deployment proof. A user-provided meter/scope
reading or photo is required before declaring a physical gate passed.

## Recovery and security

Keep a known-good raw-reading sketch and an unfiltered diagnostic path. If a
filter causes a control loop or watchdog regression, restore the last accepted
parameter/code surface and rerun the host gate before another target attempt.
Do not place Wi-Fi credentials, tokens, private captures, or unredacted logs in
examples or reports.
