---
name: freertos-patterns
description: Use when users need ESP32 FreeRTOS or RP2040 multicore patterns for task creation, queues, synchronization, memory checks, task notifications, or cross-core coordination.
metadata: {triggers: "FreeRTOS, multicore, task, queue, mutex, cross-core"}
---

# FreeRTOS Patterns for ESP32 and RP2040

Use this skill for real concurrency problems on ESP32 or RP2040. Keep the main
flow focused and load the detailed reference that matches the user's exact
problem.

## Resources

- `references/patterns-task-creation.md` - task lifecycle, priorities, stack
  sizing, and task startup
- `references/patterns-queues.md` - inter-task communication with queues
- `references/patterns-synchronization.md` - mutexes, semaphores, critical
  sections, and ISR coordination
- `references/patterns-memory.md` - stack sizing, heap checks, and monitoring
- `references/patterns-advanced.md` - watchdogs, notifications, event groups,
  timers, and affinity
- `assets/workflow.mmd` - architecture overview

## When to Use

Use this skill when the request includes:

- multiple concurrent jobs on ESP32
- task priorities or preemption
- queue, semaphore, mutex, or notification design
- RP2040 `setup1` and `loop1` multicore coordination
- watchdog-safe long-running behavior
- debugging race conditions, stack overflows, or deadlocks

Do not use this skill when:

- the target is UNO or another single-core board
- a simple `millis()` scheduler solves the problem
- the request is only about one blocking loop with no concurrency requirement

## Workflow

1. Confirm the target platform first:
   - ESP32 -> FreeRTOS task model
   - RP2040 -> dual-core coordination model
2. Identify the dominant problem:
   - task startup -> open `patterns-task-creation.md`
   - communication -> open `patterns-queues.md`
   - shared data or ISR signaling -> open `patterns-synchronization.md`
   - stack or heap risk -> open `patterns-memory.md`
   - watchdogs, notifications, timers, or affinity -> open
     `patterns-advanced.md`
3. Solve one synchronization boundary at a time. Avoid mixing queue, mutex, and
   notification advice unless the design truly needs all of them.
4. Keep board-specific details explicit. ESP32 FreeRTOS guidance and RP2040
   multicore guidance are not interchangeable.

## Core Rules

- Prefer the smallest concurrency primitive that solves the problem.
- Protect shared state explicitly. "Probably safe" is not safe.
- Use `vTaskDelay()` or event-driven blocking on ESP32, never `delay()` inside
  a task.
- Budget stack size deliberately and verify it with runtime evidence.
- For RP2040, define core ownership clearly before sharing data.

## Verification

- Confirm each task or core has a single clear responsibility.
- Check queue depth, notification flow, or mutex coverage against the concrete
  data path.
- For ESP32, inspect stack headroom with
  `uxTaskGetStackHighWaterMark()` where the task size is uncertain.
- Verify the sketch can keep making progress without deadlock or busy waiting.
- If an ISR is involved, verify the synchronization primitive is ISR-safe for
  that platform.

## Common Failure Modes

- undersized task stack
- `delay()` used inside a FreeRTOS task
- unprotected shared data
- deadlock from inconsistent lock order
- RP2040 core startup assumptions without mutex or ownership discipline

## Integration

- Combine with `arduino-code-generator` when the user needs a full sketch rather
  than design guidance.
- Combine with `circuit-debugger` only after the concurrency design looks sound
  and a hardware timing issue still remains.
- Combine with `mermaid-diagram-generator` when the concurrency design needs a
  task, queue, or event-flow diagram.

## Shared Output Contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
