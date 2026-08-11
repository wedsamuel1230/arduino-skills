---
name: library-selection
description: Use when selecting, replacing, pinning, or auditing an Arduino, ESP32, RP2040, C++, or vendor-framework library. Compare architecture support, framework and version compatibility, API behavior, footprint, maintenance, provenance, security, and hardware assumptions before installation.
metadata:
  triggers: "choose library, Arduino library, dependency, compatible library, library version, package audit"
  attribution: "Adapted from Agent Skills verification guidance and the shared Arduino toolchain contract."
---

# Library Selection

Treat a library as part of the firmware and hardware contract. A popular
package that compiles for one architecture may still use incompatible pins,
timers, memory, bus assumptions, or APIs on another.

## Intake

Record exact board/module, architecture, Arduino core or vendor SDK, compiler,
toolchain, required API, bus/pin constraints, memory budget, license boundary,
update policy, and whether the device is connected or field-updatable.

## Process

1. Find the upstream source, release/tag, license, supported architectures, and
   framework instructions. Prefer primary repositories and current release notes.
2. Compare candidate API fit, board variants, transitive dependencies, flash/
   SRAM/heap impact, blocking behavior, concurrency, bus/pull-up assumptions,
   and error/recovery behavior.
3. Check open issues and maintenance signals without treating stars or install
   count as compatibility proof.
4. Select a pinned version, record provenance and rationale, and document
   unsupported board/framework branches.
5. Run a minimal compile fixture, then a simulated or target behavior check.

## Anti-rationalization

| Shortcut | Response |
|---|---|
| "It has many installs." | Verify architecture, core version, API, and hardware contract. |
| "The newest version is best." | Read release notes, compatibility, footprint, and regression history. |
| "The I2C scanner found it." | Test library initialization, register reads, timing, and error paths. |
| "It worked on AVR." | Recheck ESP32/S3/Pico architecture, pins, timers, and memory. |
| "The dependency is only a helper." | Include transitive code and license/security review. |

## Verification

- Candidate comparison contains source, version, architecture, and license.
- Minimal compile output names the exact FQBN/environment and dependency
  resolution.
- Memory delta and one runtime/simulation behavior result are recorded.
- Connected devices have a dependency update and secret-handling plan.

## Shared output contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
