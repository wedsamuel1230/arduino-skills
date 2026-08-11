# Board Expansion Backlog

- task_id: source-research
  title: Select four candidates with complete primary-source coverage
  priority: high
  dependencies: [baseline]
  acceptance_criteria:
    - Four candidates have official board/MCU/core sources and explicit deferred alternatives.
- task_id: profile-merge
  title: Add board profiles and discoverable index
  priority: high
  dependencies: [source-research]
  acceptance_criteria:
    - Nine profiles are indexed, source-mapped, and gap-labeled.
- task_id: validator-and-docs
  title: Add deterministic board validator and update docs
  priority: high
  dependencies: [profile-merge]
  acceptance_criteria:
    - Board validator discovers every profile and plugin validator consumes it.
- task_id: full-gates
  title: Run independent structural and regression gates
  priority: high
  dependencies: [validator-and-docs]
  acceptance_criteria:
    - All local gates pass and protected profile hashes remain unchanged.
