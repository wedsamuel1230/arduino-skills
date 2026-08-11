# Arduino Board-Support Agent Skill Loop

Status: CONDITIONALLY COMPLETE. The local package and deterministic gates pass;
the follow-on identity and resolver contract is implemented. Host-level trigger
activation and physical evidence remain unrun.

## Baseline and best state

- Baseline: v1.6.0 package with 28 skills, 9 source-backed board profiles,
  8/8 shared contract themes, and 11/11 forward cases.
- Best local state: 29 skills, the new `board-support` skill, schema version 3
  board summaries and identity contracts for all 9 profiles, the deterministic
  resolver, and 18/18 forward cases.
- Protected invariants: five legacy board profile hashes and the raw ordered
  `constexpr int` pin fixture remain unchanged.

## Accepted changes

- Exact-board lookup is owned by `board-support`.
- Board choice/replacement remains owned by `board-selection`.
- Combined workflows route through `arduino-workflow-router`, then
  `board-support` when a named target must be resolved.
- The index exposes aliases, MCU/architecture, logic level, capability/risk
  tags, identity contracts, toolchain families, and source/physical evidence
  status. The resolver and resolution envelope fail closed on identity gaps.
- The Markdown profiles remain the detailed fact-to-source records.
- The board validator and eval harness fail closed on missing AI fields or a
  physical status other than `unverified`.
- `pin-assignment` requires a resolved `board-support` handoff, and the router
  documents the board-selection versus board-support order.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| Agent Skills structural validator | PASS | 29 skills, 0 warnings/errors |
| Plugin/regression validator | PASS | 29 skills, baseline/new inventories preserved |
| Board reference validator | PASS | 9 profiles, schema v3 and identity fields present |
| Shared skill contract | PASS | 8/8 themes |
| Forward behavior | PASS | 18/18 cases |
| Protected hashes | PASS | five profiles and pin fixture |
| Python syntax and diff check | PASS | `py_compile`, `git diff --check` |
| Official plugin validator | PASS | local package schema check |
| Host trigger activation | UNRUN | 20-query train/validation corpus is dataset-ready |
| Fresh semantic review | CONDITIONAL | one delayed finding report; no post-repair verdict artifact |

## Sources and evidence boundary

Agent Skills specification, Arduino documentation, Espressif GPIO/LEDC
documentation, and Raspberry Pi Pico documentation were checked on 2026-08-11.
Existing board facts remain tied to the profile source ledger. No physical
board was wired, flashed, compiled for target hardware, powered, measured,
tested at system level, or deployed in this loop.

## Stop reason

The primary retrieval metric reached the original target and the follow-on
identity/resolver gates passed with all deterministic correctness gates. The
loop stops conditionally because host-level trigger activation and physical
evidence are not available; those limits are recorded in `review.md` and the
append-only experiment ledger.
