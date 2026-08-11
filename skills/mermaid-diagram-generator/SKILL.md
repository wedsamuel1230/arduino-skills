---
name: mermaid-diagram-generator
description: Use when users need Mermaid diagrams for Arduino code structure, state machines, timing diagrams, task architecture, or workflow documentation.
metadata: {triggers: "Mermaid diagram, state machine diagram, timing diagram, workflow"}
---

# Mermaid Diagram Generator

Generate Mermaid diagrams from Arduino and embedded-system concepts without
loading unnecessary detail up front.

## Resources

- `scripts/generate_diagram.py` - CLI generator for diagram output
- `references/diagram-templates.md` - Mermaid templates by diagram type
- `references/code-patterns.md` - code-to-diagram extraction heuristics
- `references/validation-checklist.md` - rendering and syntax checks

## When to Use

Use this skill when the request asks to:

- visualize a state machine
- turn code into a flowchart
- document timing or protocol sequences
- show FreeRTOS task relationships
- add a diagram to project documentation

Do not use it for tiny code snippets where a diagram adds no clarity.

## Workflow

1. Identify the diagram type:
   - state flow -> open `references/code-patterns.md`
   - timing or protocol sequence -> open `references/diagram-templates.md`
   - task architecture -> open both `code-patterns.md` and
     `diagram-templates.md`
2. Prefer the simplest diagram that explains the behavior.
3. Use `scripts/generate_diagram.py` when the input is structured enough for
   automation.
4. Run through `references/validation-checklist.md` before presenting the final
   Mermaid output.

## Verification

- Mermaid syntax parses without errors.
- The diagram uses the correct abstraction level for the request.
- State names, transitions, or signals match the source material exactly.
- The output is readable without reverse-engineering the code.

## Integration

- Pair with `freertos-patterns` for task and synchronization diagrams.
- Pair with `arduino-code-generator` when a generated sketch also needs visual
  documentation.
- Pair with `readme-generator` when the diagram should ship in repository docs.

## Shared Output Contract

Use [the shared Arduino skill contract](../../docs/arduino-skill-contract.md):
state assumptions, required tools and versions, implementation steps,
tests/evidence by proof stage, known limitations, and recovery/security notes.
