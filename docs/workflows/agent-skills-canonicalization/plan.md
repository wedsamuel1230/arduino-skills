# Agent Skills Canonicalization Plan

**Goal:** Normalize this repository to the current Agent Skills model and remove
schema, path, and progressive-disclosure drift.

**Scope:** Documentation and skill-structure refinement only. Do not change the
behavior of bundled Arduino or Python tooling unless required for path
correctness.

## Task Group 1: Artifact chain and validator

### Task 1.1

- Target files: `prd.md`, `plan.md`, `tests-map.md`
- Action: create repo-local lifecycle artifacts for the refinement work
- Verification: confirm files exist and cover contract, plan, and verification

### Task 1.2

- Target files: `scripts/validate_agent_skills.py`
- Action: add a repo-local validator for required frontmatter fields, allowed
  top-level keys, directory-name alignment, and line-count guidance
- Verification:
  - `python3 scripts/validate_agent_skills.py`

## Task Group 2: Root documentation normalization

### Task 2.1

- Target files: `README.md`
- Action:
  - replace ACP wording with Agent Skills wording
  - document progressive disclosure explicitly
  - fix root command examples to use `skills/...`
  - align architecture notes with the actual repo layout
- Verification:
  - `rg -n "ACP|Agent Context Protocol" README.md`
  - `rg -n "uv run (arduino|power|bom|datasheet)" README.md`

### Task 2.2

- Target files: `CONTRIBUTING.md`, `DEVELOPMENT.md`, `arduino-skills.md`
- Action:
  - replace legacy authoring templates with `name`/`description`
  - describe body sections as recommended structure, not legacy schema
  - add progressive-disclosure guidance
  - fix repo-root command examples
- Verification:
  - `rg -n "^id: |^title: |^whenToUse: |^category:" CONTRIBUTING.md DEVELOPMENT.md arduino-skills.md`
  - `rg -n "uv run (arduino|power|bom|datasheet)|python (arduino|power|bom|datasheet)" CONTRIBUTING.md DEVELOPMENT.md arduino-skills.md`

## Task Group 3: Skill frontmatter normalization

### Task 3.1

- Target files: all `skills/*/SKILL.md`
- Action:
  - remove unsupported top-level keys from active skill frontmatter
  - align `name` with each skill directory
  - add spec-aligned descriptions where missing
- Verification:
  - `python3 scripts/validate_agent_skills.py`

### Task 3.2

- Target files:
  - `skills/arduino-cli-skill/SKILL.md`
  - `skills/arduino-serial-monitor/SKILL.md`
  - `skills/freertos-patterns/SKILL.md`
  - `skills/mermaid-diagram-generator/SKILL.md`
- Action: fix the currently non-canonical or mixed frontmatter in the outlier
  skills
- Verification:
  - `python3 scripts/validate_agent_skills.py`

## Task Group 4: Progressive-disclosure refactors

### Task 4.1

- Target files:
  - `skills/freertos-patterns/SKILL.md`
  - existing files under `skills/freertos-patterns/references/`
- Action: rewrite the main skill into a compact activation guide that points to
  existing references by task type
- Verification:
  - `wc -l skills/freertos-patterns/SKILL.md`
  - `python3 scripts/validate_agent_skills.py`

### Task 4.2

- Target files:
  - `skills/mermaid-diagram-generator/SKILL.md`
  - `skills/mermaid-diagram-generator/references/code-patterns.md`
  - `skills/mermaid-diagram-generator/references/validation-checklist.md`
- Action: move bulk extraction and validation detail into focused references
- Verification:
  - `wc -l skills/mermaid-diagram-generator/SKILL.md`
  - `python3 scripts/validate_agent_skills.py`

### Task 4.3

- Target files:
  - `skills/enclosure-designer/SKILL.md`
  - `skills/enclosure-designer/references/design-workflow.md`
  - `skills/enclosure-designer/references/dimensions.md`
  - `skills/enclosure-designer/references/print-and-protection.md`
- Action: split enclosure workflow detail into references and keep the main
  skill focused on activation and navigation
- Verification:
  - `wc -l skills/enclosure-designer/SKILL.md`
  - `python3 scripts/validate_agent_skills.py`

## Task Group 5: Final verification

### Task 5.1

- Target files: all touched files
- Action: run the validator and targeted grep checks, then capture residual risk
- Verification:
  - `python3 scripts/validate_agent_skills.py`
  - `rg -n "^id: |^title: |^whenToUse: |^category: |^version: |^tags:" skills/*/SKILL.md`
  - `for f in skills/*/SKILL.md; do wc -l "$f"; done | sort -nr`

## Execution Order

1. Create artifacts and validator
2. Normalize root docs and templates
3. Normalize skill frontmatter
4. Refactor oversized skills into progressive-disclosure form
5. Run final validation

## Stop Conditions

- Stop if any skill needs a directory rename to become valid
- Stop if command-path fixes imply broken scripts rather than broken docs
- Stop if progressive-disclosure cuts would remove unique guidance with no place
  to relocate it
