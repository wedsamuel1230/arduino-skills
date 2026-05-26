# Agent Skills Canonicalization Tests Map

## Behavior 1: Every active skill uses the canonical frontmatter contract

- Intent: catch mixed or legacy top-level fields before they drift further
- Checks:
  - required `name`
  - required `description`
  - allowed top-level keys only
  - `name` matches the skill directory
- Command:

```bash
python3 scripts/validate_agent_skills.py
```

## Behavior 2: Root docs teach runnable repo-root commands

- Intent: prevent documentation from pointing at nonexistent top-level paths
- Checks:
  - repo-root examples use `skills/...`
  - old root-path examples are removed
- Commands:

```bash
rg -n "uv run (arduino|power|bom|datasheet)|python (arduino|power|bom|datasheet)" README.md DEVELOPMENT.md arduino-skills.md
rg -n "uv run skills/|python skills/" README.md DEVELOPMENT.md arduino-skills.md
```

## Behavior 3: Authoring docs teach the current Agent Skills schema

- Intent: keep contributor guidance aligned with the validator and active skills
- Checks:
  - no legacy authoring template keys remain in the touched root docs
  - docs explain progressive disclosure
- Commands:

```bash
rg -n "^id: |^title: |^whenToUse: |^category:" CONTRIBUTING.md DEVELOPMENT.md arduino-skills.md
rg -n "progressive disclosure|Agent Skills" README.md CONTRIBUTING.md DEVELOPMENT.md arduino-skills.md
```

## Behavior 4: Previously oversized skills fit the progressive-disclosure guideline

- Intent: ensure the main activation surface stays concise
- Checks:
  - `freertos-patterns`
  - `mermaid-diagram-generator`
  - `enclosure-designer`
- Command:

```bash
for f in \
  skills/freertos-patterns/SKILL.md \
  skills/mermaid-diagram-generator/SKILL.md \
  skills/enclosure-designer/SKILL.md
do
  wc -l "$f"
done
```

## Behavior 5: Legacy frontmatter no longer exists in active skills

- Intent: guarantee one canonical schema across the active repo surface
- Command:

```bash
rg -n "^id: |^title: |^whenToUse: |^category: |^version: |^tags:" skills/*/SKILL.md
```
