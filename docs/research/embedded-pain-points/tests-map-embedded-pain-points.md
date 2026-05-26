# Embedded Pain-Point Skills Tests Map

## Behavior 1: first-wave skills solve distinct problem classes

- Intent: prevent overlap and generic catch-all design
- Future checks:
  - each candidate has a one-sentence mission
  - each candidate lists existing-skill overlap explicitly
  - no candidate collapses into "general debugging"

## Behavior 2: discovery evidence is traceable to real external pain

- Intent: ensure new skills are backed by recurring user pain, not guesswork
- Future checks:
  - each skill proposal cites at least one external ecosystem signal
  - dates and source URLs are recorded

## Behavior 3: future skill implementations follow the current Agent Skills contract

- Intent: ensure any new skill folders fit the canonical repo structure
- Future checks:
  - `python3 scripts/validate_agent_skills.py`

## Behavior 4: helper scripts are runnable

- Intent: keep any new automation assets practical
- Future checks:
  - `python3 skills/<skill-name>/scripts/<script>.py --help`

## Behavior 5: workflow references are actionable

- Intent: each future skill should drive the user through a deterministic
  decision path
- Future checks:
  - branch conditions are explicit
  - next actions are concrete
  - expected evidence is named at each high-risk branch
