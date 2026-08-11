# Backlog

## Items

```yaml
items:
  - task_id: audit-baseline
    title: "Record the existing skill inventory and preserved conventions"
    priority: required
    dependencies: []
    acceptance_criteria:
      - "Baseline records 20 repository skills and five global Arduino sibling skills."
      - "Raw ordered constexpr int declarations and C/C++ embedded-first guidance are recorded."
    proof_plan:
      - "docs/workflows/arduino-skills-refinement-2026-08-10/progress.md"
    status: completed
  - task_id: merge-plugin
    title: "Add router, composable skills, board references, lifecycle guidance, and host adapters"
    priority: required
    dependencies:
      - audit-baseline
    acceptance_criteria:
      - "The source of truth contains 28 active skills."
      - "Five board profiles, shared output contract, recovery/security references, and host manifests exist."
    proof_plan:
      - "python3 scripts/validate_arduino_plugin.py"
      - "references/boards/source-ledger.md"
    status: completed
  - task_id: deterministic-gates
    title: "Run structural, contract, forward, syntax, and diff checks"
    priority: required
    dependencies:
      - merge-plugin
    acceptance_criteria:
      - "Structural and contract validators pass."
      - "All ten forward-contract cases pass."
      - "Python compilation and git diff checks pass."
    proof_plan:
      - "evals/eval-results.json"
      - "docs/workflows/arduino-skills-refinement-2026-08-10/assets/experiment-log.jsonl"
    status: completed
  - task_id: post-repair-review
    title: "Obtain an independent fresh-context semantic review"
    priority: required
    dependencies:
      - deterministic-gates
    acceptance_criteria:
      - "Reviewer writes evals/fresh-review-post-repair.md without changing implementation files."
      - "Verdict and unresolved issues are reconciled with local evaluator evidence."
    proof_plan:
      - "evals/fresh-review-post-repair.md"
    status: blocked
  - task_id: physical-validation
    title: "Validate target hardware, upload, power, and deployment behavior"
    priority: deferred
    dependencies:
      - post-repair-review
    acceptance_criteria:
      - "User supplies board identity, tool versions, wiring, and fresh measurements/logs/photos."
      - "Hardware and system evidence is recorded separately from build evidence."
    proof_plan:
      - "User-provided evidence log"
    status: deferred
```
