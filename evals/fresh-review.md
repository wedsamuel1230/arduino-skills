# Independent Fresh Review

> Historical pre-repair evidence. The paths and findings below describe the
> repository state before the recorded repair slices; use the current local
> validators, `evals/eval-results.json`, and `docs/workflows/arduino-skills-refinement-2026-08-10/review.md`
> for the current state. This file is retained to show the regression baseline
> and the defects that drove the repairs.

## Role and independence

Evaluator role: independent, fresh-context reviewer of the completed repository
change. The implementation was not edited, the existing `evals/fresh-review.md`
template was not used as a verdict, and the result is based on the current tree,
diff, required eval inputs, validator output, host plugin schema, and board-source
spot checks.

Repair attempt: 0

## Family verdicts

| Family | Verdict | Basis |
|---|---|---|
| Structural | FAIL for the full plugin contract | Repository validators pass, but the Codex marketplace source shape conflicts with the installed host contract. |
| Behavioral | FAIL / unproven | The 10/10 runner checks file terms and fixtures; it does not execute prompts, trigger selection, routing precedence, or output quality. |
| Regression | PASS with documentation/tooling findings | All 20 baseline skills remain; the raw ordered `constexpr int` convention, C/C++ embedded-first orientation, and physical-proof boundary remain. |
| Board-source | PASS for bounded coverage and spot checks; FAIL for reproducible evidence | Five references exist and ESP32, ESP32-S3, and Arduino-Pico variant maps matched; source revisions and two URL fetches remain unresolved. |

## Gate scores

Scores are evaluator gates, not claims of runtime success.

| Gate | Score | Rationale |
|---|---:|---|
| Functionality | 72/100 | Required router, contract, recovery, security, lifecycle, and board surfaces are present, but host packaging and trigger execution are not release-proven. |
| Coverage | 63/100 | 28 active skills and 10 declared cases cover the requested themes; the harness omits a required serial-routing assertion and does not exercise the declared prompts. |
| Regression | 82/100 | Baseline preservation and safety boundaries pass; stale workflow records, a malformed Markdown fence, duplicate metadata, and a release-command typo remain. |
| Evidence | 55/100 | Deterministic checks and source spot checks pass in scope; agent behavior, reproducible source revisions, and all physical stages are absent. |

## Deterministic evidence

- `scripts/validate_agent_skills.py`: 28 skills, 0 warnings, 0 errors.
- `scripts/validate_arduino_skill_contract.py`: 8/8 themes pass.
- `scripts/validate_arduino_plugin.py`: 28 skills, baseline/new sets present,
  0 errors.
- The official manifest validator passes only with `uv run --with pyyaml`.
  Its documented plain `python3` invocation fails with `ModuleNotFoundError:
  yaml`.
- `scripts/run_arduino_evals.py` reports 10/10, but this is static lexical and
  fixture proof, not agent-level behavioral proof.
- `git diff --check` passes. No local broken skill/reference path was found by
  the repository validators.

No board was wired, flashed, uploaded to, measured, or deployed. No physical or
system success is claimed.

## Defects, ordered by severity

1. **High - Codex marketplace packaging is not host-contract compliant.**
   `.agents/plugins/marketplace.json:8-10` uses a string `"source": "./"`.
   The installed Codex creator contract requires an object with `source` and
   `path` (`/Users/wed/.codex/skills/.system/plugin-creator/SKILL.md:138-153`).
   `scripts/validate_arduino_plugin.py:183-205` hard-codes the string form, so
   its green result cannot catch this defect. The install instructions are in
   `docs/plugin-distribution.md:26-41`.

2. **High - The eval result is false-green for behavioral acceptance.**
   `scripts/run_arduino_evals.py:35-39,46-69` searches terms and writes JSON;
   it never runs the prompts or checks selected skills, order, output sections,
   or routing precedence. In addition, `evals/evals.json:49-55` requires serial
   diagnostics in the combined route, while the router check at
   `scripts/run_arduino_evals.py:53-54` does not test
   `arduino-serial-monitor`. The declared pin assertion about declarations-only
   commentary is also not evaluated.

3. **Medium - Durable workflow evidence is stale and misstates the current
   package.** `docs/workflows/arduino-skills-refinement-2026-08-10/progress.md:21-34`,
   `review.md:12-37`, `report.md:3-23`, and
   `assets/loop-state.json:89-97` report 19 or 20 skills, while the current tree
   has 28. The experiment log repeats those obsolete results at lines 1-4.

4. **Medium - One modified skill has a malformed output-contract section.**
   `skills/error-message-explainer/SKILL.md:423-438` opens a code fence before
   the `Shared Output Contract` heading and closes it after the section. The
   contract is therefore rendered as code content rather than a Markdown
   instruction section.

5. **Medium - A referenced script is not runnable through its documented clean
   command.** `skills/arduino-serial-monitor/SKILL.md:150-155` lists `pyserial`
   and `colorama` but `scripts/monitor_serial.py:6-15` has no PEP 723 metadata or
   pinned install path. `uv run --no-project ... --help` fails here with
   `ModuleNotFoundError: serial`.

6. **Medium - Board-source evidence is not reproducible enough for release.**
   `references/boards/README.md:16-22` asks for source revisions, but the
   profiles cite mutable `master`/latest URLs, for example
   `references/boards/esp32-devkit.md:41-45`, `esp32-s3-devkit.md:40-44`, and
   `pico-pico-w.md:42-46`, without fact-to-source sections or revisions. Fresh
   fetches returned HTTP 403 for the Microchip URL at
   `arduino-uno-r3.md:29` and the Raspberry Pi documentation URL at
   `pico-pico-w.md:44`; other board URLs returned 200. The profiles' broad
   `source-backed` statements are therefore not fully independently verifiable
   from this run.

7. **Medium - Trigger precedence is underspecified.** The broad router trigger
   (`skills/arduino-workflow-router/SKILL.md:3`) overlaps the complete-application
   trigger in `skills/arduino-project-builder/SKILL.md:3` and the board-choice
   trigger in `skills/board-selection/SKILL.md:3`. No forward harness proves that
   a combined request selects the router first and preserves the documented
   order.

8. **Low - Duplicate provider metadata creates stale discovery surfaces.** There
   are 13 nested `skills/*/.claude-plugin/marketplace.json` files with older
   per-skill versions/descriptions, for example
   `skills/arduino-code-generator/.claude-plugin/marketplace.json:1-18`, while
   `docs/plugin-distribution.md:1-4` declares `skills/` the single content
   source. Remove them or generate and validate them from one source.

9. **Low - Release command typo.** `README.md:418-422` creates tag `v1.6.0` but
   pushes `v1.5.0`.

## Token and progressive-disclosure risks

The 28 active `SKILL.md` files total 4,931 lines and 22,438 words; five are at
least 430 lines and `code-review-facilitator` is exactly 500 lines. The router is
concise and references are on-demand, but a combined route can still load many
large specialists without an explicit token budget or maximum specialist count.
The router says "under 500 lines" (`skills/arduino-workflow-router/SKILL.md:27-29`)
while the validator permits 500 inclusive (`scripts/validate_arduino_skill_contract.py:89`).

## Suggested revisions

- Align the Codex marketplace entry and its validator with the host schema, then
  run an actual marketplace add/load smoke test; document the PyYAML bootstrap.
- Replace lexical evals with a forward prompt harness that consumes every
  `evals/evals.json` assertion, checks route order/precedence, and validates the
  shared output contract.
- Refresh the workflow artifacts for 28 skills and pin board URLs to dated
  releases or commit SHAs with per-fact source mapping.
- Fix the Markdown fence, make serial dependencies self-contained, remove or
  generate nested metadata, and correct the release push command.

## Acceptance checks

1. All repository validators and the official validator pass from a documented
   clean environment; Codex marketplace add/install/load succeeds.
2. The 10 declared prompts execute in a fresh host harness, including the serial
   route and pairwise overlap cases, with expected order and output sections.
3. Current durable state records 28 skills and current validator/eval results.
4. Every referenced script's documented `--help` path runs with declared,
   reproducible dependencies; Markdown/reference checks are clean.
5. All five board profiles have pinned, accessible primary sources and fact-level
   mappings. Physical and deployment gates remain explicitly unverified unless
   user-supplied measurements/logs/photos are added.

## Overall verdict

**CONDITIONAL - not mainstream-ready for release.** The repository content and
safety/regression baseline are substantially present, but the Codex marketplace
contract and behavioral evidence gates must be repaired before claiming a
mainstream-ready plugin.
