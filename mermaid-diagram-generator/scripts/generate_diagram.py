#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = ["argparse"]
# ///

"""Generate Mermaid diagrams from Arduino code.

Usage:
    uv run generate_diagram.py --input main.ino --type state-machine
    uv run generate_diagram.py --interactive
"""

import argparse
import re
import sys

def extract_states(code):
    """Extract state definitions from Arduino code."""
    states = []
    
    # Pattern 1: enum StateType { STATE_A, STATE_B, ... }
    enum_pattern = r'enum\s+\w+\s*\{([^}]+)\}'
    enum_match = re.search(enum_pattern, code)
    if enum_match:
        states_str = enum_match.group(1)
        states = [s.strip().split('=')[0].strip() 
                 for s in states_str.split(',') if s.strip()]
    
    # Pattern 2: #define STATE_A 0
    define_pattern = r'#define\s+(STATE_\w+)\s+\d+'
    states += re.findall(define_pattern, code)
    
    return list(set(states))

def extract_transitions(code, states):
    """Extract state transitions from code."""
    transitions = []
    
    for state in states:
        # Pattern: currentState = NEXT_STATE or state = NEXT_STATE
        pattern = rf'\w*[Ss]tate\s*=\s*({"|".join(states)})'
        matches = re.findall(pattern, code)
        
        for next_state in matches:
            if next_state in states and next_state != state:
                transitions.append((state, next_state))
    
    return list(set(transitions))

def generate_state_diagram(states, transitions):
    """Generate Mermaid state diagram."""
    lines = ["```mermaid", "stateDiagram-v2"]
    
    if states:
        lines.append(f"    [*] --> {states[0]}")
    
    for from_state, to_state in transitions:
        lines.append(f"    {from_state} --> {to_state}")
    
    if states and ('DONE' in states[-1] or 'END' in states[-1]):
        lines.append(f"    {states[-1]} --> [*]")
    
    lines.append("```")
    return '\n'.join(lines)

def generate_flowchart(code):
    """Generate basic flowchart from code structure."""
    lines = ["```mermaid", "flowchart TD"]
    lines.append('    A["Start"] --> B{"Check Condition"}')
    lines.append('    B -->|Yes| C["Action A"]')
    lines.append('    B -->|No| D["Action B"]')
    lines.append('    C --> E["End"]')
    lines.append('    D --> E')
    lines.append("```")
    return '\n'.join(lines)

def generate_timing_diagram():
    """Generate I2C timing sequence diagram."""
    lines = ["```mermaid", "sequenceDiagram"]
    lines.append("    participant M as Master")
    lines.append("    participant S as Slave")
    lines.append("    M->>S: START")
    lines.append("    M->>S: ADDRESS + W")
    lines.append("    S->>M: ACK")
    lines.append("    M->>S: DATA")
    lines.append("    S->>M: ACK")
    lines.append("    M->>S: STOP")
    lines.append("```")
    return '\n'.join(lines)

def interactive_mode():
    """Interactive diagram generation."""
    print("\n=== Mermaid Diagram Generator ===")
    print("1. State Machine (from Arduino code)")
    print("2. Flowchart (template)")
    print("3. Timing Diagram (I2C example)")
    
    choice = input("\nSelect type (1-3): ").strip()
    
    if choice == '1':
        file_path = input("Arduino file path: ").strip()
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            states = extract_states(code)
            transitions = extract_transitions(code, states)
            
            print(f"\nFound {len(states)} states")
            print(f"Found {len(transitions)} transitions")
            
            diagram = generate_state_diagram(states, transitions)
            print("\n" + diagram)
            
            output = input("\nSave to file? (path or Enter to skip): ").strip()
            if output:
                with open(output, 'w') as f:
                    f.write(diagram)
                print(f"Saved to {output}")
        
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            return 1
    
    elif choice == '2':
        diagram = generate_flowchart("")
        print("\n" + diagram)
    
    elif choice == '3':
        diagram = generate_timing_diagram()
        print("\n" + diagram)
    
    else:
        print("Invalid choice")
        return 1
    
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Generate Mermaid diagrams from Arduino code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run generate_diagram.py --input main.ino --type state-machine --output docs/fsm.mmd
  uv run generate_diagram.py --interactive
  uv run generate_diagram.py --type timing --output docs/i2c.mmd
        """
    )
    
    parser.add_argument('--input', '-i', help='Arduino input file (.ino)')
    parser.add_argument('--type', '-t', 
                       choices=['state-machine', 'flowchart', 'timing'],
                       default='state-machine',
                       help='Diagram type (default: state-machine)')
    parser.add_argument('--output', '-o', help='Output file (.mmd or .md)')
    parser.add_argument('--interactive', action='store_true',
                       help='Interactive mode')
    
    args = parser.parse_args()
    
    if args.interactive:
        return interactive_mode()
    
    # Non-interactive mode
    if args.type == 'state-machine':
        if not args.input:
            print("Error: --input required for state-machine type")
            return 1
        
        try:
            with open(args.input, 'r') as f:
                code = f.read()
            
            states = extract_states(code)
            transitions = extract_transitions(code, states)
            
            print(f"Extracted {len(states)} states, {len(transitions)} transitions")
            
            diagram = generate_state_diagram(states, transitions)
        
        except FileNotFoundError:
            print(f"Error: File not found: {args.input}")
            return 1
    
    elif args.type == 'flowchart':
        diagram = generate_flowchart("")
    
    elif args.type == 'timing':
        diagram = generate_timing_diagram()
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(diagram)
        print(f"Diagram saved to {args.output}")
    else:
        print(diagram)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
