# Code-to-Diagram Patterns

Use this reference when you need to map code structure to a Mermaid diagram
type.

## State Machines

Prefer a state diagram when the source contains:

- `enum` or named state constants
- `switch` statements over a current state
- explicit transitions such as `currentState = NEXT_STATE`

Extraction checklist:

1. List the stable state names first.
2. Map only real transitions, not temporary local flags.
3. Keep guard conditions short.
4. Collapse repeated self-transitions unless they matter to the user.

## Flowcharts

Prefer a flowchart when the request is about control flow instead of named
states.

Good inputs:

- initialization sequences
- validation gates
- error-handling branches
- one-shot workflows

Avoid flowcharts when the code is really an event-driven state machine.

## Timing Diagrams

Use timing diagrams when the question depends on order and edges:

- I2C, SPI, UART, or custom signaling
- sensor sample cadence
- ISR to task signaling order
- debounce windows or timeout behavior

Capture:

- signal names
- ordering
- repeated cadence if it matters
- notable waits, setup, hold, or timeout windows

## FreeRTOS or Multicore Architecture

Use a flowchart or graph when the request is about task relationships rather
than temporal protocol edges.

Show:

- task or core ownership
- queues or notifications
- shared resources
- watchdog or timer interactions

Do not encode every line of code. Show the communication boundaries.
