# Agent Skills Canonicalization PRD

## Problem Statement

The repository's skills and contributor docs no longer agree on what a valid skill
looks like. The repo currently mixes multiple frontmatter schemas, several docs
teach legacy fields, some command examples point at paths that do not exist from
the repo root, and three skills exceed the recommended size for progressive
disclosure. This makes the repository harder to maintain and lowers confidence
that contributors will add skills in the format current Agent Skills-compatible
clients expect.

## Solution

Standardize the repository on the current Agent Skills model:

- use `name` and `description` as the canonical frontmatter contract
- remove legacy top-level keys from active skills and authoring templates
- treat `SKILL.md` as a focused entrypoint and move heavy detail into
  `references/`, `scripts/`, and `assets/`
- align README and contributor docs with the current repository layout and
  command paths
- add a lightweight local validator so conformance can be checked directly from
  the repo

## AI Translation Layer

- Mission: Canonicalize this repo to the current Agent Skills spec and make the
  structure self-validating.
- Core behavior contract: Every active skill uses one frontmatter schema, docs
  teach that schema, and oversized skills are slim enough to support progressive
  disclosure.
- Constraints: Keep changes surgical, preserve existing skill intent, do not
  redesign unrelated content, and prefer local validation over manual drift.
- Definition of done: All skills pass local schema validation, root docs match
  the actual repo layout and command paths, and previously oversized skills are
  reduced below the progressive-disclosure guideline.

## User Stories

1. As a contributor, I want one canonical SKILL.md schema, so that I do not have
   to guess which frontmatter fields are valid.
2. As a maintainer, I want legacy schema drift removed from active docs, so that
   future contributions do not reintroduce old formats.
3. As an agent consuming this repo, I want concise top-level skill files, so
   that I can activate skills without loading unnecessary context.
4. As a contributor, I want detailed reference material separated from the main
   instructions, so that I can extend skills without bloating discovery-time
   content.
5. As a maintainer, I want a repo-local validator, so that schema checks do not
   depend on memory or manual review.
6. As a user following README examples, I want commands that run from the repo
   root, so that the documented workflows work as written.
7. As a maintainer, I want the architecture section to describe the actual repo,
   so that readers are not sent to directories that do not exist.
8. As an agent using `freertos-patterns`, I want a compact entrypoint and
   targeted reference loading, so that I only read queue, mutex, or advanced
   guidance when the task needs it.
9. As an agent using `mermaid-diagram-generator`, I want compact core
   instructions and separate extraction/validation references, so that diagram
   tasks stay focused.
10. As an agent using `enclosure-designer`, I want the design workflow, board
    dimensions, and print guidance split into separate references, so that I can
    load only the relevant material.
11. As a reviewer, I want the repo to encode progressive-disclosure guidance in
    both docs and skill structure, so that conformance stays visible.
12. As a future contributor, I want local artifacts describing the change
    objective, implementation plan, and verification map, so that follow-on
    work can continue without rediscovery.

## Execution Phases

### Phase 1: Canonical schema and documentation contract

- Goal: Normalize frontmatter and authoring docs to the current Agent Skills
  model.
- Acceptance criteria:
  - all skills use `name` and `description`
  - legacy top-level keys are removed from active skills
  - README, CONTRIBUTING, DEVELOPMENT, and design guidance teach the same schema
  - root command examples reference valid repo paths
- Dependencies: repo audit and current external spec review
- Exit condition: the validator can enforce the frontmatter contract and the
  docs no longer contradict it

### Phase 2: Progressive-disclosure refactors

- Goal: Reduce oversized skills by keeping only core activation instructions in
  `SKILL.md` and moving bulk detail to references.
- Acceptance criteria:
  - `freertos-patterns`, `mermaid-diagram-generator`, and `enclosure-designer`
    are each under 500 lines
  - main skill files explicitly tell the agent when to open each reference
  - moved material remains discoverable through relative references
- Dependencies: Phase 1 schema contract
- Exit condition: the three oversized skills validate structurally and fit the
  progressive-disclosure guideline

### Phase 3: Verification and maintenance support

- Goal: Add a repeatable conformance check and record the resulting workflow in
  repo-local artifacts.
- Acceptance criteria:
  - a local validator reports clean results
  - artifact files document the implementation and verification expectations
  - residual gaps are listed explicitly if any remain
- Dependencies: completed structural and content edits
- Exit condition: fresh validation evidence exists and remaining risk is named

## Writing Plan Handoff

- Recommended plan objective: canonicalize the repo to the current Agent Skills
  model and remove documentation/structure drift
- Major task groups:
  - add lifecycle artifacts and local validator
  - normalize docs and command paths
  - normalize skill frontmatter
  - refactor oversized skills into progressive-disclosure form
  - run local validation and record evidence
- Dependencies that must stay ordered:
  - validator contract before final verification
  - schema/doc normalization before progressive-disclosure rewrites
  - verification only after all touched skills and docs are updated
- Expected artifacts:
  - `prd.md`
  - `plan.md`
  - `tests-map.md`
  - `scripts/validate_agent_skills.py`
- Plan-level verification expectations:
  - validator clean across all skills
  - no legacy frontmatter keys in active skills
  - oversized skills reduced below 500 lines

## Executing Plan Handoff

- Recommended execution mode: one sequential batch for artifacts and schema
  normalization, then one batch for progressive-disclosure skill rewrites, then
  a final verification batch
- Expected batch or slice order:
  1. add repo-local artifacts and validator
  2. update root docs and templates
  3. normalize skill frontmatter
  4. refactor oversized skills and add support references
  5. run validator and targeted spot checks
- Checkpoints that require review or proof:
  - validator output after structural edits
  - line-count evidence for previously oversized skills
  - root doc path checks
- Likely blocked states:
  - docs that reference generated packaging surfaces no longer present
  - line-count reductions that remove too much operational guidance
  - hidden script path assumptions in examples
- Verification gates before completion:
  - clean validator run
  - no active skill above 500 lines
  - documentation examples reference real paths

## Implementation Decisions

- Keep the repo on the current Agent Skills spec and remove mixed legacy
  frontmatter from active skills.
- Use only spec-aligned top-level keys in active skills unless an optional spec
  field is genuinely required.
- Treat `SKILL.md` as a narrow activation surface and shift detail into support
  files when the main file gets too large.
- Preserve the repository's existing skill directory names and align each
  skill's `name` to the directory name.
- Add a small repo-local validator instead of depending solely on an external
  validation tool.
- Update root documentation to reflect the actual workspace layout and command
  invocation paths from the repo root.
- Keep marketplace-related metadata subordinate to `SKILL.md`; it is auxiliary
  packaging, not the canonical authoring source.

## Testing Decisions

- Good tests here verify external contract, not prose aesthetics.
- The main contract is structural:
  - required frontmatter fields are present
  - invalid top-level legacy keys are absent
  - `name` matches the parent directory
  - the progressive-disclosure size ceiling is respected
- Modules to test:
  - the repo-local validator
  - all active `skills/*/SKILL.md` files through that validator
  - root docs by targeted path and content checks
- Prior art in the repo is limited for this exact workflow, so verification will
  rely on deterministic validation commands and targeted grep-based checks.

## TDD Slice Seeds

### Phase 1

- Behavior under test: a skill with legacy frontmatter fails validation
- Expected red evidence: validator reports disallowed top-level keys
- Minimum green target: all active skills pass required-key and allowed-key
  checks
- Likely refactor boundary: reusable frontmatter validation helpers

- Behavior under test: root docs teach current paths and schema
- Expected red evidence: grep finds legacy `id:`/`title:` authoring examples or
  root commands missing the `skills/` prefix
- Minimum green target: docs point to the canonical schema and runnable paths
- Likely refactor boundary: shared wording across README, CONTRIBUTING, and
  DEVELOPMENT

### Phase 2

- Behavior under test: oversized skills stay within progressive-disclosure bounds
- Expected red evidence: validator reports line-count warnings/errors for the
  three large skills
- Minimum green target: each touched skill is below 500 lines and points to
  support references by need
- Likely refactor boundary: new reference files grouped by workflow stage

### Phase 3

- Behavior under test: the repo provides repeatable conformance evidence
- Expected red evidence: validator or grep checks fail after edits
- Minimum green target: validation commands succeed with no structural errors
- Likely refactor boundary: clearer validator output formatting

## Out of Scope

- Rewriting every skill body for style consistency when no spec issue exists
- Changing the underlying Arduino examples or Python automation logic
- Reworking marketplace metadata formats beyond documentation positioning
- Adding CI workflows or external publishing automation
- Renaming skill directories

## Further Notes

- External guidance used for this PRD:
  - https://agentskills.io/specification
  - https://agentskills.io/skill-creation/best-practices
  - https://agentskills.io/skill-creation/optimizing-descriptions
  - https://code.claude.com/docs/en/sub-agents
