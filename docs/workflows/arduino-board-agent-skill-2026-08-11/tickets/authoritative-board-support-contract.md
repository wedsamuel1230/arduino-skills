# Choose the authoritative board-support Agent Skill contract

- Type: `wayfinder:research`
- Status: `resolved`
- Assignee: `coordinator`
- Parent map: [Wayfinder Map: Authoritative Board-Support Agent Skill](../wayfinder-map.md)

## Question

Should this repository add a new `board-support` Agent Skill or upgrade
`board-selection` as the single authoritative AI-facing board reference entry
point? Define the minimum retrieval-oriented profile contract, evidence/source
model, exact-board and framework/toolchain identity rules, downstream pin
handoff, unsupported-board behavior, and deterministic evals needed to prove
the contract without weakening existing conventions.

## Constraints

- Existing `references/boards/index.json` and Markdown profiles are the current
  source-backed inventory and must remain discoverable.
- Existing `board-selection` ownership and routing must not become ambiguous.
- Raw ordered `constexpr int` declarations remain unchanged.
- A compile or document check is not hardware proof.
- Recommendations must be grounded in current Agent Skills guidance and primary
  board documentation patterns, with URLs and checked dates.

## Required resolution evidence

- Four independent research reports covering Agent Skills design, skill boundary,
  board capability gaps, and eval design.
- A decision with rejected alternatives and reasons.
- A proposed field-level contract with required versus optional fields.
- A bounded implementation and verification scope, or an explicit decision to
  defer implementation pending a missing dependency.

## Resolution

Add `skills/board-support/SKILL.md` as the exact-board lookup owner. Keep
`board-selection` for board choice/replacement and `arduino-workflow-router` for
combined workflows. Extend `references/boards/index.json` with the compact
AI-reference fields defined in
`references/boards/ai-reference-schema.md`; retain Markdown profiles as the
detailed source-backed records. Require exact identity and one normalized match,
fail closed on ambiguous/unsupported boards, and hand profile constraints to
`pin-assignment` before any declarations.

The implementation adds five board-support scenarios and two deterministic
assertion types. Structural, board, plugin, contract, forward, protected-hash,
diff, syntax, and official plugin gates pass. The delegated research agents and
fresh semantic reviewers were unavailable, so semantic trigger quality remains
an explicit residual risk.

Resolution evidence: [research report](../research.md), [baseline and loop
state](../assets/loop-state.json), and [18-case eval result](../../../../evals/eval-results.json).
