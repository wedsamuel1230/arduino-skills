# Board Expansion Resume Token

- last_accepted_sprint: full-deterministic-gates
- unresolved_defects:
  - Independent fresh-review artifact is unavailable; coordinator review is
    conditional and must not be represented as an independent PASS.
  - No physical board or deployment evidence exists.
- active_constraints:
  - Preserve five existing board profile files and raw ordered constexpr int output.
  - Keep source-backed claims and board-level current gaps explicit.
  - Do not broaden the candidate set beyond the four selected boards.
- deterministic_next_step: Read `fresh-review.md` if present; otherwise record the
  bounded reviewer-service result, then run `select_best.py`, `detect_plateau.py`,
  and the final local gate suite.
