# v1.6.0 Release Backlog

- task_id: release-v1.6.0-loop-eval
  title: Release v1.6.0 loop evaluation and recommendation
  priority: high
  dependencies: [baseline-v1.5.0]
  acceptance_criteria:
    - embedded-project-loop is documented as the first skill for physical or multi-session work
    - 11 forward-contract cases pass, including valid and invalid loop artifacts
    - all package and board gates pass
    - v1.6.0 commit and annotated tag are pushed to origin
  proof_plan:
    - evals/eval-results.json
    - docs/workflows/arduino-release-2026-08-11/final-report.md
    - git show v1.6.0
  status: ready_to_publish
