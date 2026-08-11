# v1.6.0 Loop Evaluation Research

Checked: 2026-08-11 Asia/Hong_Kong

## Online sources

- [Agent Skills specification](https://agentskills.io/specification) - the
  current specification requires lowercase hyphenated `name`, a non-empty
  `description` describing what the skill does and when to use it, and limits
  the fields to the published frontmatter contract. The repository validator
  keeps those constraints deterministic.
- [Claude Code skills documentation](https://docs.anthropic.com/en/docs/claude-code/skills)
  - the current guidance describes `SKILL.md` as the required entrypoint,
  recommends trigger-focused descriptions, and recommends progressive
  disclosure by keeping detailed references out of the main skill body.
- [Matt Pocock skills](https://github.com/mattpocock/skills) - describes small,
  adaptable, composable skills for real engineering workflows.
- [obra/superpowers](https://github.com/obra/superpowers) - documents skills as
  mandatory composable development workflows and includes skill-authoring
  testing guidance.
- [Addy Osmani agent-skills](https://github.com/addyosmani/agent-skills) - uses
  a lifecycle of define, plan, build, verify, review, and ship.
- [LoopX](https://github.com/huangruiteng/loopx) - describes a local-first
  state kernel for long-running, reviewable loop engineering.

The four repository URLs returned HTTP 200 during this research pass. The
official documentation pages were fetched directly; dynamic page rendering
means this file records stable conclusions rather than copying page markup.

## Applied decisions

1. Keep `embedded-project-loop/SKILL.md` concise and trigger-focused, with
   references and evidence artifacts loaded on demand.
2. Recommend it first only for physical, recovery, measurement, or
   multi-session work. Focused board-independent questions can still use the
   narrow specialist directly.
3. Evaluate the durable contract with a deterministic positive fixture and a
   negative fixture. The negative fixture must fail closed when state or ledger
   fields are missing.
4. Keep model-level semantic triggering and physical target success explicitly
   unverified. The fresh-context reviewer limitation from the prior loop is
   carried forward rather than hidden.

## Local sources used

- `/Users/wed/.agents/skills/loop-engine/SKILL.md`
- `/Users/wed/.agents/skills/long-run-harness-execution/SKILL.md`
- `docs/arduino-skill-contract.md`
- `skills/embedded-project-loop/SKILL.md`
- `skills/arduino-workflow-router/SKILL.md`
