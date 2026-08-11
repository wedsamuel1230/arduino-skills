---
name: non-blocking-patterns
description: Use when Arduino or embedded C++ code uses delay(), needs button debouncing, periodic work, cooperative scheduling, watchdog-safe timing, state machines, or latency/jitter control under sensor, network, or motor load.
metadata:
  triggers: "delay, millis, debounce, timing, scheduler, state machine, watchdog, jitter"
  attribution: "Adapted from embedded C++ timing practice and the repository's existing code-generator patterns."
---

# Non-Blocking Patterns

Keep the main loop responsive and make timing behavior testable. Prefer C/C++
patterns that can be compiled for the exact board; use Python only for relevant
test or log analysis tooling.

## Intake

Record board/core version, task periods, deadlines, maximum work duration,
input bounce, serial/network behavior, watchdog policy, interrupt constraints,
and the safety response for missed deadlines.

## Process

1. List each periodic or event-driven task with period, deadline, and worst-case
   work. Identify any blocking library call.
2. Replace long `delay()` calls with unsigned wrap-safe elapsed checks such as
   `if (static_cast<unsigned long>(now - last) >= period)`. Use hardware timers
   or RTOS tasks only when board and framework support is confirmed.
3. Model multi-step work as an explicit state machine with bounded transitions;
   do not hide waits inside a helper.
4. Debounce inputs using a stable-state timer or event filter, not a blocking
   pause. Bound serial parsing, network retries, and sensor conversion waits.
5. Define watchdog feeding, output inhibit, timeout, and recovery behavior.
6. Measure loop latency and task jitter under representative logging, radio,
   storage, and actuator load.

## Anti-rationalization

| Shortcut | Response |
|---|---|
| "A shorter delay is fine." | It is still blocking; show the deadline and replace it. |
| "The loop is fast on USB." | Measure with the actual radio, storage, and actuator load. |
| "The enum makes it a state machine." | Require timed transitions, explicit entry/exit, and timeout behavior. |
| "The watchdog can be fed everywhere." | Define ownership and fail-safe behavior; do not mask a stuck task. |
| "`millis()` never wraps." | Use unsigned subtraction and test the wrap boundary. |

## Verification

- No unbounded blocking call remains in the time-critical path without a
  documented reason and timeout.
- Debounce, wraparound, timeout, and missed-deadline cases have tests.
- Exact-target compile proof and timing/serial evidence are separate.
- Outputs enter a safe state when a task, sensor, or communication path times
  out.

## Shared output contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
