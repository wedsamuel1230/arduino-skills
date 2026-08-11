# Run Manifest

```yaml
objective: "Upgrade the Arduino skill family into a mainstream-ready, toolchain-neutral plugin with independent eval gates."
constraints:
  - "Keep skills/ as the only skill-content source of truth."
  - "Preserve raw ordered constexpr int pin declarations and C/C++ embedded-first guidance."
  - "Separate compile, upload, hardware, system, and deployment evidence."
  - "Do not claim physical success without user-provided measurements, logs, or photos."
  - "Do not overwrite the existing global skill-creator installation."
acceptance_criteria:
  - "All active SKILL.md files pass frontmatter and reference validation."
  - "The plugin validator passes for the root, Codex, Claude, Cursor, and Agent Skills CLI adapters."
  - "The contract validator reports 8/8 review themes and the forward suite passes all declared cases."
  - "Five board profiles have fact-to-source maps and explicit source gaps."
  - "A fresh-context reviewer reports the post-repair verdict in evals/fresh-review-post-repair.md."
stop_conditions:
  - "A required evaluator remains unavailable after the configured bounded retries."
  - "A repair would weaken or modify an evaluator to make a candidate pass."
  - "A physical or live-device claim cannot be supported by evidence."
  - "Rollback verification fails."
budget_limits:
  - "At most three repair cycles for a failed evaluation."
  - "One cohesive patch per repair cycle, followed by targeted and full validation."
  - "No broad deletion, force push, deployment, or secret-touching action."
owner: "coordinator"
created_at: "2026-08-10"
updated_at: "2026-08-10"
```

The repository is intentionally left uncommitted. Existing user changes are
part of the working baseline and are preserved for the final handoff.
