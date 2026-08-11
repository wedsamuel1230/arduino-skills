---
name: embedded-project-loop
description: Use first when Arduino or embedded hardware work spans sessions, parts delivery, wiring, soldering, flashing, measurements, field tests, recovery, or a durable next-todo is needed. Maintain explicit evidence and concrete physical-world user gates instead of assuming completion.
metadata:
  triggers: "hardware loop, next todo, long-running embedded project, physical gate, evidence log, resume hardware work"
  recommended: "first for long-running or physical work"
  attribution: "Adapted from the local loop-engine and long-run-harness-execution contracts; physical evidence remains user-owned."
---

# Embedded Project Loop

Use a small durable loop for work that crosses the boundary between files and
physical hardware. The agent may prepare and verify host-side artifacts, but it
must not invent soldering, flashing, measurement, or field evidence.

## Recommended entry point

Load this skill before `arduino-workflow-router` whenever the request includes
physical hardware, more than one session, a pending measurement, a field test,
or recovery work. It owns the durable goal, next todo, evidence boundary,
rollback path, and physical gate. The router then selects board, wiring, code,
toolchain, test, and deployment specialists without closing this loop on its
behalf.

## State

Use `.arduino/` in the project, or a user-selected external evidence directory:

```text
.arduino/goal.md
.arduino/next-todo.md
.arduino/board-profile.md
.arduino/evidence/{build,upload,hardware,system,deployment}/
.arduino/experiment-log.jsonl
.arduino/resume-token.md
```

Keep secrets, tokens, private network credentials, and unredacted personal data
out of these artifacts. `goal.md` records the exact target, success criteria,
non-goals, safety constraints, stop conditions, and rollback path. The next-todo
file contains one action, owner, prerequisites, expected evidence, gate, and
status.

## Bounded iteration

1. Read the goal, next todo, board profile, and last ledger entry.
2. Select one causal firmware, wiring, power, measurement, or diagnostic change.
3. Run the narrowest safe host/build check available.
4. Stop at a physical gate if the next action requires the user.
5. Compare the supplied observation with the expected result and independent
   safety gate.
6. Append the action, evidence path, decision, rollback, and next todo.
7. Keep only a verified candidate; otherwise record a blocker or restore the
   current experiment surface.

One iteration must not combine several wiring changes, firmware images, power
sources, or measurements. One change keeps failures attributable.

## Physical gate

Use a specific question and wait for the observation:

```text
Physical gate: On <exact board/revision>, perform <one action> with power
<state>. Capture <measurement/log/photo> at <location>. Expected:
<observable result>. Reply with the observation or `blocked: <reason>`; do not
reply with an unverified yes.
```

For a failed upload, request the exact port/device identity, image/hash, and
redacted uploader log. For a power question, request the meter location, units,
and minimum/maximum observed value. For wiring, request a continuity/polarity
check or labeled photo before enabling loads.

## Evidence boundary

- Build evidence proves source/configuration and dependency compilation only.
- Upload evidence proves an image was accepted by a named target path only.
- Hardware evidence requires target identity plus measurements, serial output,
  continuity, scope data, or a contextualized photo.
- System evidence requires the integrated scenario and representative load.
- Deployment evidence requires health check, staged update, rollback, recovery,
  and maintenance records.

If evidence is absent, say `unverified` or `blocked` and keep the next todo open.
Read the router recovery reference before erase, bootloader repair, or reflash.

## Anti-rationalization

| Shortcut | Response |
|---|---|
| "The checkbox is done." | Require the artifact and proof stage. |
| "The compile passed." | Do not promote it to upload, hardware, or system proof. |
| "The user probably wired it." | Ask the concrete gate question and wait. |
| "Try three fixes together." | Split them into one-change iterations. |
| "Erase first." | Confirm target, last-known-good image, recovery path, and data-loss impact. |
| "No new output means success." | Record a no-op observation; it does not close the goal. |

## Verification

- State files exist and the next todo names one deterministic action.
- Every completed physical step links to evidence with a proof-stage label.
- The ledger records decision, rollback, and next candidate append-only.
- Stop conditions and repair caps are explicit.
- In this repository, run `python3 scripts/run_arduino_evals.py`; the
  `loop-engine-evidence-contract` case checks valid and invalid durable loop
  artifacts and fails closed when required state or ledger fields are missing.

## Shared output contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
