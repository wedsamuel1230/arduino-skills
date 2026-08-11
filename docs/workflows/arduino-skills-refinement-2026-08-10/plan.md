# Arduino Skills Refinement Plan

## Slice 1: Contract And Router

- Add the failing `scripts/validate_arduino_skill_contract.py` contract check.
- Add `skills/arduino-workflow-router/SKILL.md`.
- Add router references for board intake, toolchain selection, failure recovery,
  and connected-device security.
- Add `docs/arduino-skill-contract.md` and
  `docs/board-support/board-profile-template.md`.

Verification: run the new validator and confirm it fails only because existing
skills have not yet been linked to the shared contract.

## Slice 2: Existing Skill Alignment

- Add one concise shared-contract pointer to every existing active skill.
- Add toolchain and evidence-stage boundaries to the builder, CLI, generator,
  serial, error, power/connectivity, and OTA skills where the review directly
  exposes a gap.
- Preserve existing examples, scripts, and specialized references.

Verification: run both validators and check all active skill line counts.

## Slice 3: Root Docs And Research

- Update README, `arduino-skills.md`, CONTRIBUTING, DEVELOPMENT, diagrams, and
  CHANGELOG to expose the router, lifecycle, supported toolchains, and proof
  boundaries.
- Record online Agent Skills and skill-discovery sources, install evidence, and
  residual runtime-evaluation gaps.
- Add prompt-level evaluation cases for future forward tests.

Verification: run link/path checks, inspect the diff, and write the final review
and loop report.

## Stop Conditions

- Stop if an existing skill needs a broad rewrite to satisfy the contract.
- Stop if a reference cannot be linked one level deep from the router.
- Stop if the validator begins judging prose style instead of observable
  structure or explicit coverage.
