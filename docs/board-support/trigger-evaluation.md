# Board-Support Trigger Evaluation

`evals/board-support-trigger-queries.json` is a held-out corpus for model-level
activation testing. It follows the Agent Skills guidance to mix positive,
negative, casual, exact, and near-miss prompts rather than treating keyword
presence as trigger proof.

## Run contract

Run each query three times in a clean agent context with the repository plugin
available. Record whether `skills/board-support/SKILL.md` was loaded, then
calculate the trigger rate per query. A positive query passes when the rate is
at least 0.5; a negative query passes when it is below 0.5. Keep the validation
split untouched while revising the description.

The repository's deterministic eval runner validates the board contract and the
trigger corpus shape, but it cannot observe a host agent's skill activation. A
model run must therefore be reported separately from `18/18`-style static
contract results. No model activation run is claimed in this checkout because
the delegated evaluation service was unavailable during this loop.

## Review boundaries

- Keep the essential trigger boundary in frontmatter `description`; metadata
  trigger hints are supplemental and nonstandard.
- Treat `board-selection`, `pin-assignment`, and `wiring-safety-check` as
  near-miss owners when the user does not need a named-board reference.
- If a pin request names a board, `board-support` may still be required as a
  prerequisite even when `pin-assignment` owns the declaration format.
- Do not claim a trigger pass from a static string search or from a successful
  board-profile lookup.
