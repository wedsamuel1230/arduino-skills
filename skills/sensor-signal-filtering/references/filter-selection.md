# Filter Selection

## Sampling first

Define `T_s` as the actual sample period and `f_s = 1/T_s`. The Nyquist
frequency is `f_s / 2`; energy above it can alias into the signal band before a
digital filter runs. Start with a sample rate several times higher than the
highest signal frequency of interest, then verify the chosen sensor bandwidth,
latency, and anti-alias attenuation rather than treating a 5x or 10x ratio as a
guarantee.

Capture raw data with timestamps. A stable input that moves by one or two ADC
counts is a different problem from periodic interference, one-sample spikes,
or a slow sensor that is being sampled too quickly for the required response.

## Selection table

| Observation or requirement | First candidate | Cost and risk to state |
|---|---|---|
| Isolated impulsive spikes | Odd-window median | Non-linear; can flatten narrow real events |
| Bounded noise, known short window | Moving average | Uses RAM/CPU and adds about `(N-1)/2` sample periods of group delay |
| Low-cost smoothing with adjustable response | EMA/IIR | Alpha controls noise versus latency; startup must initialize from the first valid sample |
| Known passband/stopband requirement | Designed FIR/IIR | Requires coefficient, numeric-range, timing, and response verification |
| A physical/state model and noise statistics exist | Kalman or observer | Do not use default gains; wrong model can look plausible while being wrong |

For thresholded outputs, keep filtering separate from hysteresis/debounce. A
threshold policy can reduce chatter but does not remove analog noise or aliasing.
Do not stack filters until the latency and cutoff of the combined response are
written down.

## EMA reference

For a sample `x[n]`, use:

`y[n] = alpha * x[n] + (1 - alpha) * y[n-1]`, where `0 < alpha <= 1`.

Initialize `y[0]` from the first valid sample. For a desired first-order time
constant, a useful starting relation is `alpha = 1 - exp(-T_s / tau)`; verify
the measured step response at the real sample period. Smaller alpha means more
smoothing and more delay. Keep the raw value so a stuck, saturated, or
out-of-range sensor is still visible.

## Calibration and fault order

1. Validate the raw count is in the ADC's legal range and flag saturation,
   disconnect, impossible jumps, and missing samples.
2. Remove electrical spikes with the selected bounded filter while retaining
   the raw sample and a quality flag.
3. Apply a linear scale/offset or filter in the equivalent linear domain. For a
   non-linear sensor conversion, filter counts/voltage before the non-linear
   mapping unless the model explicitly requires another order.
4. Apply calibrated units, range checks, and threshold/hysteresis policy.

The exact order depends on the sensor model. Record it rather than silently
assuming that calibration fixes noise or that filtering fixes a bad reference.

## Host-side vector check

Use the bundled helper for deterministic design vectors:

```text
python3 scripts/filter_benchmark.py \
  --samples "100,101,100,300,102" \
  --filter median --window 3 --format json
```

The helper tests algorithm shape and startup behavior. It does not prove the
Arduino scheduler's sample period, ADC settling, component tolerance, or
physical cutoff.
