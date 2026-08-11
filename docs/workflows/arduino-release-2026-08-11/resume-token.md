# v1.6.0 Release Resume Token

- last_accepted_sprint: final-gates
- unresolved_defects:
  - Final deterministic gates and release publication are pending.
  - No physical or semantic model-level proof is available.
  - The prior independent reviewer artifact remains unavailable.
- active_constraints:
  - Preserve v1.5.0 history, raw ordered constexpr declarations, and C/C++ embedded-first guidance.
  - Keep `embedded-project-loop` first only for physical or multi-session work.
  - Do not claim a pushed release until the command succeeds.
- deterministic_next_step: Inspect `git diff --cached`, create the v1.6.0 release commit and annotated tag only if the staged surface is clean, push main and v1.6.0, then verify both remote refs.
