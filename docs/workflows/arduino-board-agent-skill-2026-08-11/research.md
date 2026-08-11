# Board-Support Agent Skill Research

Checked: 2026-08-11

## Evidence status

Four parallel research agents were dispatched with disjoint read-only scopes;
the service initially returned upstream `503 Service Unavailable` responses.
One delayed fresh reviewer later returned a read-only acceptance report with
actionable findings. A second four-agent retry reproduced three `503` failures
and one bounded wait with no report; all errored or pending threads were closed.
No delegated agent modified the repository.

The implementation decision below therefore uses direct repository inspection
and accessible canonical/primary sources. The missing delegated reports and
fresh semantic verdict are recorded as residual evaluation risk, not silently
treated as passes.

## Direct source checks

- [Agent Skills specification](https://agentskills.io/specification), fetched
  2026-08-11: `SKILL.md` requires `name` and `description`, recommends specific
  trigger keywords, progressive disclosure, on-demand `references/`, and a
  focused main file under 500 lines.
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices.md)
  and [trigger evaluation guidance](https://agentskills.io/skill-creation/optimizing-descriptions.md),
  fetched 2026-08-11: keep descriptions intent- and trigger-focused, bundle
  repeated deterministic work as scripts, and evaluate activation with held-out
  positive/negative queries and repeated runs.
- [Arduino hardware documentation](https://docs.arduino.cc/hardware/), checked
  as the vendor board-documentation root on 2026-08-11. Existing profile facts
  remain the source-backed board records; this loop adds no new board claims.
- [Espressif ESP32-C3 GPIO documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/gpio.html),
  fetched 2026-08-11: confirms the need to treat GPIO2/GPIO8/GPIO9 as
  strapping pins and GPIO18/GPIO19 as USB-JTAG-sensitive on C3.
- [Arduino-ESP32 LEDC documentation](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html),
  fetched 2026-08-11: confirms PWM capability and API behavior are SoC/core
  dependent and must not be presented as a universal board pin guarantee.
- [Raspberry Pi Pico documentation](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html),
  checked 2026-08-11 as the primary board-documentation root. The existing Pico
  profile remains bounded to RP2040 and Arduino-Pico.

## Gaps found

The previous package had detailed Markdown profiles and a profile index, but the
index did not provide query aliases, MCU/architecture identity, logic level,
capability tags, pin-risk tags, identity scope, toolchain families, or explicit
physical evidence status. `board-selection` also combined fact lookup with the
separate decision of choosing a board. That made named-board retrieval and
trigger ownership less precise for an AI agent.

## Decision

Add `skills/board-support/` as the authoritative named-board lookup skill.
Keep `board-selection` as the owner for choosing, replacing, or comparing boards
against requirements. Keep `arduino-workflow-router` as the owner for combined
workflows, with `board-support` loaded when a named target must be resolved.

The machine-readable index now carries a compact retrieval summary for every
existing profile. Detailed facts remain in the Markdown profiles and their
fact-to-source maps. The validator enforces the summary contract and keeps
`physical_status: unverified` fail-closed.

## Follow-on AI reference hardening

The delayed reviewer identified four gaps in the first implementation: a unique
alias could still represent a multi-variant physical family; lookup
normalization existed only inside the eval harness; direct `pin-assignment`
activation did not require an exact board-support handoff; and standalone
per-skill installation could omit shared references. A fifth gap was the lack
of host-level activation evidence.

The follow-on candidate addresses these without duplicating board facts:

- schema version 3 adds an `identity_contract` to every index record;
- `board-support` emits a stable resolution envelope and blocks
  variant-sensitive advice with `needs-disambiguation`;
- `scripts/resolve_board_profile.py` is the single exact-match implementation
  consumed by the eval harness and board validator;
- the router documents conditional board-selection versus board-support order,
  and `pin-assignment` requires a resolved handoff;
- a 20-query train/validation trigger corpus is checked structurally and marked
  model-run pending; no static check is presented as activation proof;
- plugin distribution now documents board-support as a package-context skill.

## Rejected alternatives

- Upgrade `board-selection` only: rejected because it would make board-choice
  and named-board lookup share a broad trigger and blur the downstream owner.
- Put every pin and bus fact in JSON: rejected because it would duplicate the
  Markdown fact-to-source maps and create a second drift-prone source of truth.
- Add more board profiles in this loop: rejected because the requested change is
  the AI reference contract; GIGA R1 WiFi and ESP32-C6 still need separate
  source/core-variant reviews.

## Acceptance impact

The new deterministic surface covers exact lookup, compact index/evidence
fields, variant identity boundaries, resolver behavior, ambiguous clone
handling, unsupported boards, pin handoff, toolchain boundaries, composed router
order, and all pre-existing behavior. It does not prove model trigger selection,
physical wiring, compilation, upload, runtime, system, or deployment behavior.
