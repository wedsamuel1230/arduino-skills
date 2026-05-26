# Mermaid Validation Checklist

Use this reference before returning a Mermaid diagram.

## Syntax Checks

- Validate node labels and edge syntax.
- Keep labels short enough to render cleanly.
- Avoid unsupported Mermaid features unless the target renderer is known.

## Structural Checks

- The selected diagram type matches the problem.
- States, tasks, or signals map directly to the source material.
- Arrows express directionality correctly.
- The diagram does not hide important branching or synchronization points.

## Readability Checks

- Remove decorative detail that does not help the reader.
- Group repeated or equivalent steps when it improves scanability.
- Keep the first read understandable without referring back to the code for
  every edge.

## Final Review

- Re-read the user's question and confirm the diagram answers it.
- If the diagram comes from generated output, spot-check the highest-risk edges
  manually.
- If the diagram is intended for README or docs, prefer stable naming over local
  shorthand.
