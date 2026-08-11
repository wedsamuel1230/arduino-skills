# Research Notes

## Primary Agent Skills Guidance

- [Agent Skills specification](https://agentskills.io/specification): the
  discovery-critical fields are `name` and `description`; names match their
  directories; the main `SKILL.md` should stay under 500 lines, with details in
  directly referenced files.
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices):
  write only what the agent needs, match specificity to task fragility, use
  plan-validate-execute loops, keep gotchas visible, and make validation
  observable.
- [Anthropic skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md):
  use realistic prompts, compare an improved skill with a baseline when useful,
  add objective assertions where possible, and iterate from observed results.
- Local Codex skill-creator: `~/.codex/skills/.system/skill-creator/SKILL.md`.
  It reinforces concise entrypoints, progressive disclosure, appropriate
  degrees of freedom, and protection of validation integrity.

## Skill Discovery Evidence

`find-skills` searched [skills.sh](https://skills.sh/) for skill creation,
authoring, prompt engineering, validation, and workflow skills on 2026-08-10.
The strongest direct matches included `anthropics/skills@skill-creator` at
346.7K installs and `openai/skills@skill-creator` at 3.2K installs. Existing
local `skill-creator` ownership made overwriting that name unsafe, so the
distinct official OpenAI companions were installed instead:

```text
npx skills add openai/skills --skill plugin-creator cli-creator -g --copy -y
```

Verified Codex copies:

- `~/.agents/skills/cli-creator/SKILL.md`
- `~/.agents/skills/plugin-creator/SKILL.md`

The installer also reported that PromptScript does not support global skill
installation. That warning does not invalidate the verified Codex copies.

The official Codex plugin validator was also run with an isolated cache and
passed after fetching its PyYAML dependency.

## Adapted And Excluded

- Adapted: progressive disclosure, explicit trigger descriptions, realistic
  evaluations, and validation loops.
- Adapted: the distinction between an agent's output contract and detailed
  domain references.
- Excluded: provider-specific assumptions, hidden chain-of-thought output, and
  claims that a skill is hardware-tested merely because it contains a checklist.
