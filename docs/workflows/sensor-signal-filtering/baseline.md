# Baseline Evidence

- Date: 2026-08-17 Asia/Hong_Kong
- Commit: `d06ea78b96a07d67905f290451ffb38f522ec14b`.
- Worktree: clean on `main` before the skill skeleton was initialized.

Commands and results before the candidate:

- `python3 scripts/validate_agent_skills.py` -> 29 skills, 0 warnings, 0 errors.
- `python3 scripts/validate_arduino_skill_contract.py` -> 8/8 themes, 0 errors.
- `python3 scripts/validate_arduino_plugin.py` -> 29 skills, 0 errors.
- `python3 scripts/run_arduino_evals.py --output /tmp/arduino-skills-baseline-eval-results.json` -> 18/18 cases passed.
- `git diff --check` -> no output and exit 0.

The generated empty `skills/sensor-signal-filtering/` skeleton is the planned
candidate surface; no behavior or repository routing was changed at baseline.
The commit value is fixed from the inspected checkout and should be refreshed
if the baseline is recreated.
