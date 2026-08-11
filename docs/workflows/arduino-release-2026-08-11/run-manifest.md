# v1.6.0 Release Run Manifest

- objective: Publish a verified v1.6.0 Arduino skills release with a
  loop-engine eval and an explicit embedded-project-loop recommendation.
- constraints:
  - Preserve the v1.5.0 baseline and existing board/pin conventions.
  - Keep `skills/` as the only skill-content source of truth.
  - Do not claim physical or semantic model-level success.
  - Do not force-push or rewrite existing tags.
- acceptance_criteria:
  - The new loop-engine case passes with positive and negative fixtures.
  - All existing structural and regression gates pass.
  - Public docs and release notes consistently identify v1.6.0.
  - The v1.6.0 commit and annotated tag are pushed to `origin`.
- stop_conditions:
  - Any failed gate, metadata mismatch, or unverified secret in the staged diff.
  - GitHub push or release creation fails after bounded retry.
- budget_limits:
  - One implementation slice and up to three scoped repair cycles.
  - One final verification pass before commit, tag, and push.
