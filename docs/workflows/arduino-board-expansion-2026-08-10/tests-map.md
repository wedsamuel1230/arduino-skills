# Board Expansion Tests Map

## Structural

- `python3 scripts/validate_board_references.py`
- `python3 scripts/validate_arduino_plugin.py`
- `python3 scripts/validate_agent_skills.py`
- `python3 scripts/validate_arduino_skill_contract.py`

## Regression

- Compare `assets/baseline-hashes.txt` with hashes for the five protected
  existing board profiles.
- Confirm existing board names and links remain present.
- Run `python3 scripts/run_arduino_evals.py --output evals/eval-results.json`.

## Source accuracy

- Every added profile has at least two official source URLs.
- Every requested field maps to one or more source numbers.
- Mutable product pages and board-specific current or clone gaps are explicit.
- `assets/source-status-2026-08-11.txt` records a fresh HTTP 200 check for all
  14 indexed sources belonging to the four added profiles.

## Scope

These tests validate documentation and routing surfaces only. They do not prove
that a physical board compiles, flashes, powers a load, or behaves in a system.
