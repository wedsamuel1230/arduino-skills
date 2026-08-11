# v1.6.0 Release Loop Plan

## Define

Primary metric: number of declared forward-contract cases that pass, with a
target of 11/11 after adding the loop-engine artifact case. The independent
correctness gates are skill structure, plugin contract, shared Arduino
contract, board references, behavioral cases, official host manifest, Python
syntax, JSON parsing, diff cleanliness, and release metadata consistency.

## Build

1. Create the local Wayfinder map and one claimed release task.
2. Add the positive/negative loop-engine fixtures and evaluator assertion.
3. Make `embedded-project-loop` the documented recommended first entry for
   physical and multi-session work.
4. Update public docs, changelog, research, release notes, and durable state.

## Verify

Run the deterministic suite before staging:

```bash
python3 scripts/validate_agent_skills.py
python3 scripts/validate_arduino_skill_contract.py
python3 scripts/validate_board_references.py
python3 scripts/validate_arduino_plugin.py
python3 scripts/run_arduino_evals.py --output evals/eval-results.json
UV_CACHE_DIR=/private/tmp/arduino-skills-uv-cache uv run --no-project --with pyyaml \
  /Users/wed/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 -m py_compile scripts/*.py
python3 -m json.tool evals/evals.json >/dev/null
git diff --check
```

Then compare the release metadata with `v1.5.0`, inspect the staged diff, and
only then create and push the annotated `v1.6.0` tag.

## Stop conditions

- Any failed evaluator or protected customization regression.
- A release metadata mismatch or dirty staged diff containing secrets.
- A required GitHub credential or network operation fails.
- Physical or semantic model-level evidence is requested but unavailable.
