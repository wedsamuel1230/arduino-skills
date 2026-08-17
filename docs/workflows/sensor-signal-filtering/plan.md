# Implementation Plan: Sensor Signal Filtering

## Phase 1: Define

- [x] Inventory existing filtering, calibration, circuit, wiring, board, and
  hardware-test ownership.
- [x] Record baseline validator/eval results and current commit.
- [x] Capture primary external/local authoring and electronics references.
- [x] Define four independent gate families: structural, behavioral,
  regression, and review/evidence.

## Phase 2: Build with TDD

1. Add failing `unittest` cases for the deterministic filter benchmark script:
   startup without zero bias, median spike rejection, moving-average window,
   EMA step behavior, invalid parameters, and JSON CLI output.
2. Run the focused test file and preserve the expected red failure.
3. Implement the standard-library-only script with non-interactive argparse,
   closed filter choices, JSON/CSV output, and useful errors.
4. Run the focused tests to reach green.
5. Add the compact skill, one Arduino example, and three directly linked
   references for selection, analog conditioning, and verification.

## Phase 3: Integrate

- Add a filter-specific route to `arduino-workflow-router` after board intake
  and before calibration; keep code generation as an implementation helper.
- Add forward-contract cases and include the skill in the plugin validator's
  explicit new-skill inventory.
- Update README and changelog; do not add per-skill README or provider-body
  duplicates.
- Add a GitHub Actions workflow that runs deterministic host and repository
  gates without claiming a physical-board test.

## Phase 4: Verify and review

- Run the focused unit tests and script smoke commands.
- Run the local quick validator through isolated PyYAML tooling if available.
- Run all repository validators, forward evals, and `git diff --check`.
- Inspect links, frontmatter, line counts, diff scope, and generated JSON.
- Obtain independent acceptance/spec and quality/regression review from a
  fresh subagent; repair only scoped findings and re-run all gates.

## Stop conditions

Stop when all four gate families pass and no critical review finding remains;
stop earlier for missing evaluator evidence, unsafe hardware advice, repeated
service failure, three repair cycles, or no meaningful progress. Preserve the
best verified state and record unverified physical work.

## Phase 5: Ship

- [x] Record the final deterministic gate run as E5 in the append-only ledger.
- [x] Write the final report with baseline, best state, evidence, risks, and
  stop reason.
- [x] Mark model activation and target hardware validation as unverified.
- [ ] Run model activation and exact-board physical gates when the required
  model harness, board, sensor, and instruments are available.
