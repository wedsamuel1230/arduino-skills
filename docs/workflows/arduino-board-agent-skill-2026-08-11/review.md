# Board-Support Review

Checked: 2026-08-11

## Acceptance/spec verdict

**Conditional pass.** The requested board-support Agent Skill boundary is
implemented. The board index, nine profiles, exact lookup assertions, routing,
unsupported/ambiguous handling, pin handoff, and evidence boundaries are
covered. All deterministic acceptance gates pass.

## Quality/regression verdict

**Conditional pass.** The new skill is 121 lines, uses Agent Skills frontmatter,
loads detailed references progressively, and does not duplicate provider skill
content. The existing five protected board profiles and raw pin fixture hashes
are unchanged. `board-selection` and the router have distinct ownership rules.

## Independent reviewer status

One delayed fresh-context reviewer returned a read-only report after the first
dispatch. It found five actionable gaps: variant-incomplete aliases,
eval-only normalization, a missing pin-assignment prerequisite, no model
activation evidence, and unsupported standalone copies of shared-reference
skills. The follow-on candidate addresses those findings. The retry batch still
failed with three upstream `503` responses and one bounded timeout, so there is
no fresh post-repair semantic verdict artifact. Static and deterministic checks
are not presented as a replacement for that missing model-level review.

## Residual risks

- Trigger quality and model selection behavior are not proven by the keyword
- contract harness. The 20-query trigger corpus is dataset-ready but has not
  been run through a host agent.
- Compact index tags could drift from Markdown profiles unless future profile
  changes update both surfaces; the validator enforces identity-contract shape
  and source fields, not semantic equivalence of every capability tag.
- Board-support and related routing skills require the complete repository or
  plugin because their references are intentionally shared.
- No target compilation, upload, wiring, power measurement, runtime, system,
  or deployment evidence exists.
- GIGA R1 WiFi and ESP32-C6 remain deferred pending separate profile research.
