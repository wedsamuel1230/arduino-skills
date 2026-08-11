# Board Expansion Sprint Contract

- sprint_id: board-profile-index-and-gates
- included_tasks: [source-research, profile-merge, validator-and-docs, full-gates]
- excluded_tasks:
  - Physical board wiring, flashing, upload, power, measurement, system tests,
    deployment, and release publishing.
  - GIGA R1 WiFi and ESP32-C6 profile creation.
- done_criteria:
  - Four new profiles are source-backed and discoverable.
  - Existing five profile files and pin fixture are unchanged.
  - Documentation and changelog describe accepted and deferred work.
- verification_criteria:
  - Run board, structural, plugin, contract, forward-eval, Python syntax, JSON,
    diff, and protected-hash checks.
  - Compare all acceptance criteria with fresh command output before completion.
