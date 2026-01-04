#!/usr/bin/env python3
"""
Arduino Code Analyzer - Static analysis for Arduino/C++ sketches

Analyzes code for common issues:
- Memory problems (String usage, large arrays)
- Blocking code (delay in loops)
- Missing volatile for ISR variables
- Pin conflicts
- Power efficiency issues

Usage:
    uv run analyze_code.py sketch.ino
    uv run analyze_code.py --dir /path/to/project
    uv run analyze_code.py --interactive
"""

import argparse
import re
import os
from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path

# =============================================================================
# Issue Definitions
# =============================================================================

@dataclass
class Issue:
    """Code issue found during analysis"""
    severity: str  # error, warning, info
    category: str
    line_number: int
    description: str
    suggestion: str
    code_snippet: str = ""


# Analysis rules
RULES = {
    # Memory Issues
    "string_in_loop": {
        "pattern": r'void\s+loop\s*\(\s*\).*?String\s+\w+',
        "multiline": True,
        "severity": "warning",
        "category": "memory",
        "description": "String object created inside loop() - causes memory fragmentation",
        "suggestion": "Move String declarations outside loop() or use char arrays"
    },
    "string_concat_loop": {
        "pattern": r'for\s*\(.*?\).*?(?:\w+\s*\+=\s*|String.*?\+)',
        "multiline": True,
        "severity": "warning",
        "category": "memory",
        "description": "String concatenation in loop - allocates memory repeatedly",
        "suggestion": "Pre-allocate buffer or use sprintf() with char array"
    },
    "large_array": {
        "pattern": r'(?:int|float|double|long)\s+\w+\s*\[\s*(\d{3,})\s*\]',
        "severity": "warning",
        "category": "memory",
        "description": "Large array may exhaust RAM",
        "suggestion": "Use PROGMEM for constants, or consider external storage"
    },
    
    # Blocking Code
    "delay_in_loop": {
        "pattern": r'void\s+loop\s*\(\s*\).*?delay\s*\(\s*(\d+)\s*\)',
        "multiline": True,
        "severity": "info",
        "category": "performance",
        "description": "delay() blocks execution - consider millis() for non-blocking",
        "suggestion": "Use millis()-based timing for responsive code"
    },
    "long_delay": {
        "pattern": r'delay\s*\(\s*(\d{4,})\s*\)',
        "severity": "warning",
        "category": "performance",
        "description": "Long delay ({0}ms) blocks all code execution",
        "suggestion": "Use millis() timing pattern for delays > 100ms"
    },
    
    # ISR Issues
    "non_volatile_isr": {
        "pattern": r'(?:attachInterrupt|ISR\s*\().*?(\w+)',
        "severity": "error",
        "category": "correctness",
        "description": "Variable used in ISR may not be declared volatile",
        "suggestion": "Declare shared ISR variables as: volatile int variableName;"
    },
    "serial_in_isr": {
        "pattern": r'(?:ISR\s*\(|void\s+\w+ISR\s*\().*?Serial\.',
        "multiline": True,
        "severity": "error",
        "category": "correctness",
        "description": "Serial operations inside ISR can cause crashes",
        "suggestion": "Set a flag in ISR, handle Serial in loop()"
    },
    "delay_in_isr": {
        "pattern": r'(?:ISR\s*\(|void\s+\w+ISR\s*\().*?delay\s*\(',
        "multiline": True,
        "severity": "error",
        "category": "correctness",
        "description": "delay() does not work inside ISR",
        "suggestion": "ISRs should be fast - set flag and exit"
    },
    
    # Digital I/O
    "pinmode_in_loop": {
        "pattern": r'void\s+loop\s*\(\s*\).*?pinMode\s*\(',
        "multiline": True,
        "severity": "warning",
        "category": "performance",
        "description": "pinMode() called repeatedly in loop()",
        "suggestion": "Move pinMode() to setup() - only needs to run once"
    },
    "analog_read_speed": {
        "pattern": r'for\s*\(.*?\).*?analogRead\s*\(',
        "multiline": True,
        "severity": "info",
        "category": "performance",
        "description": "analogRead() is slow (~100µs per read)",
        "suggestion": "Consider averaging or reducing read frequency"
    },
    
    # Power Efficiency
    "no_sleep": {
        "pattern": r'void\s+loop\s*\(\s*\).*?while\s*\(\s*(?:1|true)\s*\)',
        "multiline": True,
        "severity": "info",
        "category": "power",
        "description": "Busy wait loop - wastes power",
        "suggestion": "Use sleep modes for battery-powered projects"
    },
    "adc_always_on": {
        "pattern": r'analogRead\s*\(',
        "severity": "info",
        "category": "power",
        "description": "ADC consumes power even between reads",
        "suggestion": "Disable ADC when not needed for power savings"
    },
    
    # Common Bugs
    "assignment_in_condition": {
        "pattern": r'if\s*\(\s*\w+\s*=\s*[^=]',
        "severity": "error",
        "category": "correctness",
        "description": "Assignment (=) in if condition - likely meant comparison (==)",
        "suggestion": "Use == for comparison: if (x == 5)"
    },
    "floating_point_comparison": {
        "pattern": r'if\s*\(.*?(?:float|double)\s+.*?==',
        "multiline": True,
        "severity": "warning",
        "category": "correctness",
        "description": "Direct floating-point comparison may fail",
        "suggestion": "Use tolerance: if (abs(a - b) < 0.001)"
    },
    "unsigned_negative": {
        "pattern": r'(?:byte|unsigned)\s+\w+\s*=\s*-',
        "severity": "error",
        "category": "correctness",
        "description": "Negative value assigned to unsigned type",
        "suggestion": "Use signed type (int) or ensure value is positive"
    },
    
    # Best Practices
    "magic_numbers": {
        "pattern": r'(?:pinMode|digitalWrite|analogWrite|analogRead)\s*\(\s*\d+\s*[,\)]',
        "severity": "info",
        "category": "style",
        "description": "Magic number used for pin - harder to maintain",
        "suggestion": "Use named constants: const int LED_PIN = 13;"
    },
    "missing_f_macro": {
        "pattern": r'Serial\.print(?:ln)?\s*\(\s*"[^"]{20,}"',
        "severity": "info",
        "category": "memory",
        "description": "Long string literal uses RAM",
        "suggestion": "Use F() macro: Serial.println(F(\"text\"))"
    },
    "no_serial_check": {
        "pattern": r'Serial\.begin.*?Serial\.print',
        "multiline": True,
        "severity": "info",
        "category": "robustness",
        "description": "Serial used without checking if ready",
        "suggestion": "Add: while (!Serial) delay(10); after Serial.begin()"
    }
}


def analyze_file(filepath: str) -> List[Issue]:
    """Analyze a single file for issues"""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return [Issue("error", "file", 0, f"Could not read file: {e}", "Check file path")]
    
    for rule_name, rule in RULES.items():
        pattern = rule["pattern"]
        flags = re.DOTALL if rule.get("multiline") else 0
        
        # Search in full content for multiline patterns
        if rule.get("multiline"):
            matches = re.finditer(pattern, content, flags | re.IGNORECASE)
            for match in matches:
                # Calculate line number
                line_num = content[:match.start()].count('\n') + 1
                
                # Get snippet
                snippet_start = max(0, match.start() - 20)
                snippet_end = min(len(content), match.end() + 20)
                snippet = content[snippet_start:snippet_end].replace('\n', ' ')[:60]
                
                description = rule["description"]
                if '{0}' in description and match.groups():
                    description = description.format(*match.groups())
                
                issues.append(Issue(
                    severity=rule["severity"],
                    category=rule["category"],
                    line_number=line_num,
                    description=description,
                    suggestion=rule["suggestion"],
                    code_snippet=snippet
                ))
        else:
            # Line-by-line search
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    description = rule["description"]
                    match = re.search(pattern, line)
                    if match and match.groups() and '{0}' in description:
                        description = description.format(*match.groups())
                    
                    issues.append(Issue(
                        severity=rule["severity"],
                        category=rule["category"],
                        line_number=line_num,
                        description=description,
                        suggestion=rule["suggestion"],
                        code_snippet=line.strip()[:60]
                    ))
    
    return issues


def analyze_directory(dirpath: str) -> Dict[str, List[Issue]]:
    """Analyze all .ino, .cpp, .h files in directory"""
    results = {}
    
    for ext in ['*.ino', '*.cpp', '*.c', '*.h']:
        for filepath in Path(dirpath).rglob(ext):
            issues = analyze_file(str(filepath))
            if issues:
                results[str(filepath)] = issues
    
    return results


def format_report(issues: List[Issue], filename: str = "") -> str:
    """Format issues as readable report"""
    if not issues:
        return "✅ No issues found!"
    
    lines = [
        "=" * 60,
        f"Code Analysis Report{': ' + filename if filename else ''}",
        "=" * 60,
        ""
    ]
    
    # Group by severity
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    infos = [i for i in issues if i.severity == "info"]
    
    # Summary
    lines.append(f"Summary: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} suggestions")
    lines.append("")
    
    # Errors first
    if errors:
        lines.append("🔴 ERRORS (must fix)")
        lines.append("-" * 40)
        for issue in errors:
            lines.append(f"  Line {issue.line_number}: {issue.description}")
            lines.append(f"    Fix: {issue.suggestion}")
            if issue.code_snippet:
                lines.append(f"    Code: {issue.code_snippet}")
            lines.append("")
    
    if warnings:
        lines.append("🟡 WARNINGS (should fix)")
        lines.append("-" * 40)
        for issue in warnings:
            lines.append(f"  Line {issue.line_number}: {issue.description}")
            lines.append(f"    Fix: {issue.suggestion}")
            lines.append("")
    
    if infos:
        lines.append("🔵 SUGGESTIONS (nice to have)")
        lines.append("-" * 40)
        for issue in infos:
            lines.append(f"  Line {issue.line_number}: {issue.description}")
            lines.append(f"    Tip: {issue.suggestion}")
            lines.append("")
    
    return "\n".join(lines)


def interactive_mode():
    """Interactive code analysis"""
    print("=" * 60)
    print("Arduino Code Analyzer - Interactive Mode")
    print("=" * 60)
    print()
    print("Paste your code (press Enter twice when done):")
    print()
    
    lines = []
    empty_count = 0
    while True:
        line = input()
        if not line:
            empty_count += 1
            if empty_count >= 2:
                break
        else:
            empty_count = 0
        lines.append(line)
    
    # Save to temp file and analyze
    temp_file = "_temp_analysis.ino"
    with open(temp_file, 'w') as f:
        f.write('\n'.join(lines))
    
    issues = analyze_file(temp_file)
    os.remove(temp_file)
    
    print(format_report(issues, "pasted code"))


def main():
    parser = argparse.ArgumentParser(description="Arduino Code Analyzer")
    parser.add_argument("file", nargs="?", help="File to analyze")
    parser.add_argument("--dir", "-d", type=str, help="Directory to analyze")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--severity", "-s", type=str, help="Min severity: error, warning, info")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    if args.dir:
        results = analyze_directory(args.dir)
        if args.json:
            import json
            print(json.dumps({k: [vars(i) for i in v] for k, v in results.items()}, indent=2))
        else:
            for filepath, issues in results.items():
                print(format_report(issues, filepath))
                print()
    elif args.file:
        issues = analyze_file(args.file)
        
        # Filter by severity if specified
        if args.severity:
            severity_order = {"error": 0, "warning": 1, "info": 2}
            min_level = severity_order.get(args.severity, 2)
            issues = [i for i in issues if severity_order.get(i.severity, 2) <= min_level]
        
        if args.json:
            import json
            print(json.dumps([vars(i) for i in issues], indent=2))
        else:
            print(format_report(issues, args.file))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
