# Board Expansion Run Manifest

- objective: Add at least four mainstream, source-backed board profiles while
  preserving the existing Arduino skill package and custom pin convention.
- constraints:
  - Preserve all five existing board profile files and existing fixture output.
  - Use official primary sources and pinned core variants where available.
  - Keep compile, upload, hardware, system, and deployment evidence separate.
  - Do not claim physical success without user-provided evidence.
- acceptance_criteria:
  - Nine board profiles are indexed and pass the board-reference validator.
  - Existing structural, plugin, contract, forward-eval, and hash gates pass.
  - New profiles include required fields, source maps, current caveats, and gaps.
  - README, source ledger, changelog, and loop evidence describe the additions.
- stop_conditions:
  - A protected profile hash changes.
  - A candidate lacks two official sources for its required facts.
  - A repair weakens a validator or invents hardware evidence.
  - Three bounded repair cycles are exhausted.
- budget_limits:
  - Three candidate/repair cycles maximum.
  - One additive merge slice followed by targeted and full deterministic gates.
  - Fresh reviewer attempt is bounded and read-only.
