# v1.6.0 Release Heartbeat

- current_sprint: release-pre-publish
- completed_sprints:
  - wayfinder-map
  - loop-engine-evaluator
  - recommendation-and-docs
  - final-gates
- blockers:
  - Physical, upload, system, and deployment proof is intentionally unavailable.
  - Fresh-context semantic review from the prior loop did not persist its artifact.
- next_action: Inspect the staged diff, then commit, tag, and push v1.6.0 if the release surface contains no secrets or unrelated changes.
- tool_tier_escalations:
  - tool: curl
    tier: 1
    criterion_or_risk: Current Agent Skills and loop-engine research.
    lower_tier_insufficient: Local files cannot establish current online guidance.
    reason: User requested online research for the release update.
    proof_ref: docs/workflows/arduino-release-2026-08-11/research.md
  - tool: Python validators
    tier: 2
    criterion_or_risk: Cross-file eval, board, and plugin invariants.
    lower_tier_insufficient: Static reading cannot prove parser and fixture behavior.
    reason: The new loop case must be executable and fail closed.
    proof_ref: evals/eval-results.json
