# PRD: Sensor Signal Filtering Skill

## Problem

Arduino users regularly add a moving average or capacitor after observing
unstable ADC values, without first separating sensor dynamics, aliasing, ADC
acquisition limits, wiring/power noise, calibration, and software policy. The
repository already has a code-only filtering pattern, but it lacks a focused
skill that designs and verifies the complete analog-to-filtered-value path.

## Goal

Add `sensor-signal-filtering`, a composable skill for selecting, implementing,
and testing filters for analog and sampled sensor data while giving bounded,
board-aware analog front-end advice.

## Users and use cases

- A maker has noisy `analogRead()` values and needs a diagnostic sequence before
  choosing EMA, median, moving-average, or another filter.
- An embedded developer needs a fixed-rate ADC pipeline with explicit latency,
  startup, saturation, outlier, and fault behavior.
- A hardware designer needs an RC or active anti-alias/input network checked
  against sensor output drive, ADC acquisition time, voltage limits, noise,
  protection, grounding, and measurement evidence.
- A reviewer needs host-side deterministic tests plus a target-board gate that
  does not confuse compilation with physical validation.

## Scope

In scope: intake and diagnosis, sampling/aliasing, analog RC/input conditioning,
software filter selection, calibration order, bounded Arduino examples,
host-side simulation/TDD, measurement checklists, and evidence separation.

Out of scope: choosing a board without `board-support`, replacing the existing
code-generator pattern library, claims about a particular board's ADC without
its exact profile/datasheet, automatic component procurement, and physical
acceptance without user-provided measurements.

## Acceptance criteria

1. The skill has valid frontmatter, a trigger-rich description, shared-contract
   link, one-level progressive-disclosure references, a runnable example, and a
   deterministic non-interactive script with `--help`.
2. Guidance covers both software and hardware filtering, including aliasing,
   sample rate, RC cutoff, source impedance/ADC settling, rail/ground/wiring,
   filter latency, saturation, calibration, and fault handling.
3. Host tests prove filter startup, spike behavior, step response, invalid
   configuration rejection, and structured CLI output.
4. Router, README, changelog, and forward evals expose the skill without
   duplicating ownership of `arduino-code-generator`, `circuit-debugger`,
   `wiring-safety-check`, or `sensor-calibration-workbench`.
5. CI runs the host tests, package/contract/plugin validators, forward evals,
   and whitespace checks on relevant changes.
6. Independent review records specification compliance and quality/regression
   findings; no hardware behavior is reported as verified.

## Evidence boundary

Host tests and CI establish script, documentation, and repository-contract
evidence only. Arduino compilation, upload, ADC waveform quality, rail noise,
filter cutoff, sensor stability, and end-to-end system behavior remain separate
target/hardware gates.
