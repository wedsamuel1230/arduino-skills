# Release v1.6.0 loop evaluation and recommendation

labels: `wayfinder:task`
status: ready_to_publish
owner: coordinator
blocked_by: none

## Question

What repository changes and independent checks are required to make
`embedded-project-loop` the recommended first skill for long-running Arduino
hardware work, verify its loop-engine artifact contract, update all public
release guidance, and publish `v1.6.0` from `v1.5.0`?

## Acceptance criteria

- The recommendation is explicit in the loop skill, router, shared contract,
  README, contributor/development docs, and plugin distribution docs.
- The eval suite validates a complete loop state and append-only JSONL ledger and
  rejects incomplete artifacts.
- Research sources and the decision boundary are recorded locally.
- The release metadata and notes identify `v1.6.0` and retain the `v1.5.0`
  baseline.
- All structural, contract, board, behavioral, host-manifest, syntax, and diff
  gates pass before commit, tag, and push.

## Resolution

The recommendation is now explicit in the skill, router, host wrappers, shared
contract, README, contributor/development guides, plugin distribution notes,
and release notes. The forward suite passes 11/11 cases, including the
positive/negative loop-engine fixture evaluation; 28 skills, 9 board profiles,
8/8 contract themes, the official plugin validator, JSON/Python syntax, and
diff checks also pass. Physical and model-level semantic evidence remains
unverified. GitHub publication is the remaining authorized release operation.
