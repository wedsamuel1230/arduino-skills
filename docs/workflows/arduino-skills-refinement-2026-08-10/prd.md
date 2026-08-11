# Arduino Skills Refinement PRD

## Problem

The repository has a useful set of focused Arduino skills, but they are not yet
connected by a universal intake and lifecycle contract. Most guidance assumes a
small set of boards or a particular tool, and users can mistake a clean compile
for proof that upload, electrical behavior, or the integrated system works.

## Goal

Make the skill family reusable across Arduino IDE, Arduino CLI, PlatformIO, and
vendor tools while preserving focused specialist skills. Add a concise router
for combined workflows, a shared board/toolchain/output contract, recovery and
security guidance, and deterministic checks that keep the improvements from
drifting.

## Requirements

1. Add a router that identifies the board, framework, toolchain, constraints,
   and evidence stage before selecting skills.
2. Define a board profile covering pins, memory, peripherals, voltage, current,
   communication protocols, boot/recovery path, and software versions.
3. Support combined firmware, electronics, networking, power, calibration,
   enclosure, deployment, and maintenance workflows with explicit load order.
4. Separate build, upload, hardware, system, and deployment evidence.
5. Provide recovery paths for failed uploads, boot failures, power faults, and
   corrupted firmware.
6. Include connected-device security, secret handling, dependency pinning,
   maintainability, update, rollback, and decommissioning guidance.
7. Standardize each skill's response around assumptions, tools/versions,
   actions, tests/evidence, limitations, and recovery notes.
8. Keep detailed variants in references and keep active SKILL.md files concise.

## Out Of Scope

- Claiming support or testing for boards not present in the user's evidence.
- Rewriting existing generators, sketches, or examples.
- Adding live hardware tests without hardware access.
- Overwriting the existing global `skill-creator` installation.

## Definition Of Done

- `arduino-workflow-router` exists and routes representative combined workflows.
- Shared contract and board profile docs are linked from the root documentation.
- Every active skill points at the shared output contract.
- The repository contract validator reports 8/8 review themes and exits 0.
- The existing Agent Skills validator still exits 0 and no skill exceeds 500
  lines.
- Research sources and unverified runtime behavior are recorded.
