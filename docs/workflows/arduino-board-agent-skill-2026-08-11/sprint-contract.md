# Board-Support Agent Skill Sprint Contract

- sprint_id: `arduino-board-agent-skill-2026-08-11`
- primary_metric: `board_support_retrieval_contract_gates`
- baseline: `0` new retrieval-oriented gates beyond the existing board validator
- target: `at least 6` board-support gates, with all existing gates still passing
- budget: `one research decision plus one cohesive implementation patch`

## Included

- Agent Skills and embedded-board workflow research.
- One authoritative board-support skill boundary decision.
- Structured board-reference contract and validator/eval updates if supported.
- Routing, README, contract, changelog, and workflow documentation updates that
  directly describe the accepted surface.
- Independent acceptance and quality/regression review.

## Excluded

- Physical board testing, flashing, wiring, power, system, or deployment proof.
- Unbounded addition of board profiles.
- Provider-specific duplicate skill content.
- Changes to unrelated specialist workflows.

## Acceptance

- The board-support entry point has a unique, specific trigger and no ambiguous
  ownership with `board-selection`.
- Exact-board identity, source/evidence status, framework/toolchain compatibility,
  capability lookup, pin-safety handoff, and unsupported-board behavior are explicit.
- Existing five protected profile hashes, ordered pin declarations, and C/C++
  embedded-first guidance remain intact.
- New deterministic scenarios cover a known board, an ambiguous board/clone, an
  unsupported board, and a pin-allocation handoff.
- Structural, plugin, contract, forward, board-reference, diff, and regression
  checks pass; no physical success is claimed.
