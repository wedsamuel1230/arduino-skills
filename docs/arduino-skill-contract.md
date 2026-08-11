# Shared Arduino Skill Contract

This contract applies to every skill in this repository. It keeps the skill
family useful across boards, frameworks, and host environments without making
each specialist skill repeat a complete embedded handbook.

## Intake Before Advice

Capture or clearly mark unknowns before choosing pins, libraries, commands, or
recovery actions:

- board family, exact model/revision, MCU, bootloader, and target voltage
- pin map and reserved pins, memory/flash/RAM limits, peripherals, and buses
- expected voltage/current for each powered load and the supply path
- communication protocols, network role, security requirements, and update path
- Arduino IDE, Arduino CLI, PlatformIO, or vendor-specific toolchain
- host OS, tool versions, board package/framework versions, library versions,
  and the exact reproduction or existing project files

Use [the board profile template](board-support/board-profile-template.md) when
the task is more than a small, board-independent explanation.

## Toolchain And Compatibility

Treat the toolchain as a variable, not as an implicit Arduino IDE assumption.
Identify the source of truth for dependency versions and report compatibility
checks before implementation:

- Arduino IDE: board package, library manager versions, selected board and port
- Arduino CLI: CLI version, core index, FQBN, port, and library resolution
- PlatformIO: platform/framework version, environment, board ID, and lockfile
- Vendor-specific tools: SDK/tool version, flash layout, bootloader utility,
  debug probe, signing, and recovery requirements

If a command or library is only verified for one toolchain, label it as such.
Do not silently translate a CLI, PlatformIO, or vendor command into an IDE
workflow.

## Evidence Stages

Report evidence by stage. A passing earlier stage does not prove a later one:

1. **Build proof**: source/configuration parses and compiles for the exact
   target and dependency versions.
2. **Upload proof**: the intended device accepts the image through the named
   transport and the image identity is recorded.
3. **Hardware proof**: power, reset, pins, buses, peripherals, and runtime
   observations match the design on the target hardware.
4. **System proof**: the integrated behavior meets the requirement under
   representative load, network, timing, and failure conditions.
5. **Deployment proof**: update, rollback, recovery, observability, and
   maintenance procedures work for the intended field environment.

Use `unverified` when a stage was not run. Compilation success is never a
substitute for hardware or system success.

## Pin declaration convention

When the user requests pin declarations, preserve the repository convention:
raw `constexpr int` declarations, fixed numeric order starting at the user's
required logical ID (for example `101, 102, 103, ...`), and no extra syntax or
explanation in declarations-only output. Treat those logical IDs separately
from physical GPIO numbers. Physical assignments still require exact-board
direction, boot, flash/PSRAM, USB, bus, voltage, pull, and current checks.

## Physical-world gate

If the next action requires wiring, soldering, flashing, powering, measuring, or
taking a photo, stop and ask one concrete question that names the board, action,
power state, expected observation, and evidence path. Accept the user's
measurement, log, photo, or explicit `blocked: <reason>` response. Never infer a
physical result from a plan, heartbeat, compile log, or an unqualified yes.
An unverified yes is not evidence.

## Loop-engine contract

When `embedded-project-loop` is the recommended entry point, maintain a durable
state object with a goal, one primary metric, correctness gates, hard
constraints, editable and protected surfaces, baseline, best-known state,
evaluation method, acceptance rule, rollback method, plateau rule, stop
conditions, experiment history, and open uncertainties. The baseline and
best-known state must name commands, results, and evidence paths.

The experiment ledger is append-only JSONL. Each row records the hypothesis,
changed files, command, result, metric, gate results, acceptance decision,
revert evidence, lesson, and next candidate. Change one causal variable per
iteration. A heartbeat or todo update without an artifact or independent
observation is not progress.

Run the repository loop evaluation with:

```bash
python3 scripts/run_arduino_evals.py --output evals/eval-results.json
```

The `loop-engine-evidence-contract` case checks both a complete fixture and an
incomplete fixture. A passing build or heartbeat does not close a hardware,
system, or deployment gate.

## Required Output

Every skill response should contain these sections, even when a section is
short:

1. **Assumptions**: confirmed facts, inferred facts, and missing inputs.
2. **Required tools and versions**: host tools, board package/framework, and
   library or dependency versions.
3. **Implementation steps**: ordered actions, with board/toolchain branches
   called out instead of hidden.
4. **Tests and evidence**: commands or measurements, labeled by proof stage.
5. **Known limitations**: unsupported boards, unverified behavior, and scope
   boundaries.
6. **Recovery and security notes**: relevant rollback, secret-handling, and
   connected-device maintenance actions.

Specialist skills may use a richer domain-specific format, but these facts must
remain findable. Do not print secrets or copy credentials into logs, examples,
or generated configuration.

## Lifecycle Boundary

Route a complete request through requirements, design, implementation, build,
upload, hardware validation, system validation, deployment, and maintenance.
Use a focused specialist directly when the user has already supplied the
inputs and only one stage is in scope.
