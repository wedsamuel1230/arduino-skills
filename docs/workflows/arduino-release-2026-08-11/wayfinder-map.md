# Wayfinder Map: Arduino Skills v1.6.0 Loop Evaluation

labels: `wayfinder:map`
tracker: local-markdown
status: closed

## Destination

Publish a verified `v1.6.0` release from the `v1.5.0` baseline with
`embedded-project-loop` documented as the recommended first skill for physical
and multi-session work, and with executable loop-engine evidence checks.

## Notes

This is an AFK execution override for the user's explicit implementation and
release request. Keep the Agent Skills source-of-truth rule, the raw ordered
`constexpr int` convention, C/C++ embedded-first guidance, and the boundary
between host proof and physical proof. Consult `loop-engine`, `wayfinder`, and
the shared Arduino contract.

## Decisions so far

- [Release v1.6.0 loop evaluation and recommendation](tickets/release-v1.6.0-loop-eval.md) - 11/11 evals and package gates passed, then commit `9882eb6`, tag `v1.6.0`, the GitHub Release, and remote refs were verified.

## Not yet specified

- A future semantic evaluator that invokes an actual model and scores novel
  trigger selection remains outside this deterministic repository harness.
- Physical board, upload, measurement, system, and deployment evidence remains
  user-owned and is not part of this release acceptance.

## Out of scope

- Adding a new board family in this release slice; the four board profiles from
  the board-expansion loop remain the current additions.
- Replacing the existing global `~/.agents/skills/` installation or changing
  secrets, credentials, or deployment infrastructure.
