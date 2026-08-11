# Make Board Resolution Variant-Safe For AI Consumers

- Type: `wayfinder:research`
- Status: `resolved`
- Assignee: `coordinator`
- Parent map: [Wayfinder Map: Authoritative Board-Support Agent Skill](../wayfinder-map.md)

## Question

What is still missing for `board-support` to behave as a reusable AI reference
and safe handoff rather than a prose-only board lookup?

## Evidence

- The Agent Skills specification recommends focused descriptions, progressive
  disclosure, reusable scripts, and model-level trigger evaluation.
- A delayed fresh reviewer found that one exact alias can still identify a
  profile covering multiple physical variants, that normalization existed only
  in the eval harness, that direct pin assignment did not require a board-support
  gate, and that standalone per-skill installation can omit shared references.
- The repository's existing board profiles already document the relevant
  variant boundaries; no new board fact is required for this decision.

## Resolution

Add schema version 3 `identity_contract` records with explicit profile type,
variants, and advice-specific required identity fields. Add the shared
`resolution_status` envelope and a deterministic `resolve_board_profile.py`
helper. Require a resolved board-support handoff before pin selection, make the
router's board-selection versus board-support order conditional, and add a
20-query held-out trigger corpus. Document that board-support is a
package-context skill requiring the complete repository/plugin.

The deterministic gates pass: 29 skills, 9 profiles, 8/8 shared contract
themes, 18/18 forward cases, plugin validation, protected hashes, Python syntax,
and diff checks. Model activation rates and physical behavior remain unrun.
