#!/usr/bin/env python3
"""
Error Message Parser - Analyzes Arduino/PlatformIO error messages

Parses compiler errors and provides:
- Plain English explanation
- Likely causes
- Fix suggestions
- Code examples

Usage:
    uv run parse_errors.py --file error_log.txt
    uv run parse_errors.py --message "error: 'LED' was not declared"
    uv run parse_errors.py --interactive
    cat error.txt | uv run parse_errors.py --stdin
"""

import argparse
import re
import json
from dataclasses import dataclass
from typing import List, Optional, Tuple

# =============================================================================
# Error Pattern Database
# =============================================================================

ERROR_PATTERNS = {
    # Declaration/Scope Errors
    r"'(\w+)' was not declared in this scope": {
        "type": "undeclared_identifier",
        "explanation": "The compiler doesn't recognize '{0}'. This happens when you try to use a variable, function, or constant that hasn't been defined yet.",
        "causes": [
            "Typo in variable or function name",
            "Forgot to declare the variable",
            "Missing #include for a library",
            "Variable declared inside a function but used outside",
            "Case sensitivity issue (Arduino is case-sensitive)"
        ],
        "fixes": [
            "Check spelling - Arduino is case-sensitive (LED vs led)",
            "Declare the variable before using it: int {0};",
            "Add the required #include at top of file",
            "If it's a constant, add: #define {0} value",
            "If it's a pin, use: const int {0} = pin_number;"
        ]
    },
    
    r"'(\w+)' does not name a type": {
        "type": "unknown_type",
        "explanation": "The compiler doesn't recognize '{0}' as a valid type. Types define what kind of data a variable can hold.",
        "causes": [
            "Missing #include for a library that defines this type",
            "Typo in the type name",
            "Using a class/struct before it's defined",
            "Library not installed"
        ],
        "fixes": [
            "Add #include <LibraryName.h> at top of sketch",
            "Check the library documentation for correct type name",
            "Install the library: Sketch → Include Library → Manage Libraries",
            "Common types: int, float, char, byte, String, bool"
        ]
    },
    
    # Missing Semicolon/Syntax
    r"expected ('.*?'|';'|'\)'|'\}'|',' |declaration) before": {
        "type": "syntax_error",
        "explanation": "The compiler expected {0} but found something else. This usually means there's a missing punctuation mark on a previous line.",
        "causes": [
            "Missing semicolon ; at end of previous line",
            "Missing closing brace } or parenthesis )",
            "Missing comma in function call or array",
            "Unclosed string (missing quote)"
        ],
        "fixes": [
            "Add semicolon to the END of the previous line",
            "Count your braces - every { needs a matching }",
            "Count parentheses - every ( needs a matching )",
            "Check the line ABOVE the error, not the error line"
        ]
    },
    
    r"expected '\)' before '(\w+)'": {
        "type": "missing_parenthesis",
        "explanation": "Missing closing parenthesis. The function call or expression isn't properly closed.",
        "causes": [
            "Forgot closing ) in function call",
            "Mismatched parentheses in complex expression",
            "Missing comma between function arguments"
        ],
        "fixes": [
            "Add ) to close the function call",
            "Check for matching pairs of parentheses",
            "Use editor highlighting to match brackets"
        ]
    },
    
    # Type Mismatches
    r"invalid conversion from '(\w+\*?)' to '(\w+\*?)'": {
        "type": "type_mismatch",
        "explanation": "You're trying to use a {0} where a {1} is expected. These types aren't compatible.",
        "causes": [
            "Passing wrong type to function",
            "Assigning incompatible values",
            "Mixing pointers with non-pointers",
            "String vs char array confusion"
        ],
        "fixes": [
            "Check function documentation for expected parameter types",
            "Use proper type conversion: (int)value or String(value)",
            "For strings: use .c_str() to convert String to char*",
            "Make sure variable types match what function expects"
        ]
    },
    
    # Function Errors
    r"too few arguments to function '(\w+)'": {
        "type": "missing_arguments",
        "explanation": "Function '{0}' requires more arguments than you provided.",
        "causes": [
            "Forgot to include required parameters",
            "Using wrong function overload",
            "Misread documentation"
        ],
        "fixes": [
            "Check function documentation for required parameters",
            "Look at function definition to see all parameters",
            "Add missing arguments in correct order"
        ]
    },
    
    r"too many arguments to function '(\w+)'": {
        "type": "extra_arguments",
        "explanation": "Function '{0}' received more arguments than it accepts.",
        "causes": [
            "Added extra parameters by mistake",
            "Using wrong function overload",
            "Comma inside a string being interpreted as separator"
        ],
        "fixes": [
            "Remove extra arguments",
            "Check function documentation for correct usage",
            "Verify you're calling the right function"
        ]
    },
    
    r"'class (\w+)' has no member named '(\w+)'": {
        "type": "no_member",
        "explanation": "The '{0}' library/class doesn't have a function or variable called '{1}'.",
        "causes": [
            "Typo in method name",
            "Using method from wrong library version",
            "Method doesn't exist in this library",
            "Object type is wrong"
        ],
        "fixes": [
            "Check library documentation for correct method names",
            "Verify library version matches examples",
            "Look for similar method names (case-sensitive)",
            "Make sure object is correct type"
        ]
    },
    
    # Memory Errors
    r"section.*will not fit in region": {
        "type": "memory_overflow",
        "explanation": "Your code is too large to fit in the microcontroller's memory.",
        "causes": [
            "Using too many libraries",
            "Large arrays or strings",
            "Debug/print statements taking space",
            "Using wrong board selection"
        ],
        "fixes": [
            "Use F() macro for strings: Serial.println(F(\"text\"))",
            "Use PROGMEM for constant arrays",
            "Remove unused libraries and code",
            "Use smaller data types (byte vs int)",
            "Verify correct board is selected in Tools menu"
        ]
    },
    
    r"data.*will not fit|RAM.*overflow": {
        "type": "ram_overflow",
        "explanation": "Your program uses more RAM than available. Variables and runtime data exceed memory limits.",
        "causes": [
            "Large arrays or buffers",
            "Many String objects",
            "Recursive functions",
            "Large local variables"
        ],
        "fixes": [
            "Use PROGMEM for constant data",
            "Use smaller buffers",
            "Avoid String class, use char arrays",
            "Make large arrays global instead of local",
            "Use byte instead of int where possible"
        ]
    },
    
    # Library Errors
    r"No such file or directory.*#include.*<(\w+)": {
        "type": "missing_library",
        "explanation": "The library '{0}' is not installed.",
        "causes": [
            "Library not installed",
            "Typo in library name",
            "Wrong include path",
            "Library in wrong folder"
        ],
        "fixes": [
            "Install library: Sketch → Include Library → Manage Libraries",
            "Search for '{0}' in Library Manager",
            "Check for correct library name (case-sensitive)",
            "Manually install: download .zip, Sketch → Include Library → Add .ZIP"
        ]
    },
    
    r"multiple definition of `(\w+)'": {
        "type": "multiple_definition",
        "explanation": "'{0}' is defined more than once in your code.",
        "causes": [
            "Same variable/function in multiple files",
            "Header file included multiple times without guards",
            "Copy-paste error creating duplicates"
        ],
        "fixes": [
            "Remove duplicate definitions",
            "Use 'extern' keyword for variables shared between files",
            "Add include guards to header files",
            "Search your code for duplicate names"
        ]
    },
    
    # Board/Upload Errors
    r"avrdude.*programmer.*not responding": {
        "type": "upload_fail",
        "explanation": "Cannot communicate with the Arduino board.",
        "causes": [
            "Wrong COM port selected",
            "USB cable is data-only (no data lines)",
            "Driver not installed",
            "Board not connected",
            "Another program using the port"
        ],
        "fixes": [
            "Select correct port: Tools → Port",
            "Try a different USB cable (use data cable, not charge-only)",
            "Unplug and replug the Arduino",
            "Close Serial Monitor and any other serial programs",
            "Try a different USB port",
            "Install/reinstall Arduino drivers"
        ]
    },
    
    r"ser_open\(\).*can't open device": {
        "type": "port_error",
        "explanation": "Cannot open the serial port. The port may be in use or disconnected.",
        "causes": [
            "Port used by another program",
            "Arduino disconnected",
            "Wrong port selected",
            "Permission denied (Linux/Mac)"
        ],
        "fixes": [
            "Close other programs using serial port",
            "Check Arduino is plugged in",
            "Select correct port in Tools → Port",
            "On Linux: add user to dialout group"
        ]
    },
    
    # ESP32/ESP8266 Specific
    r"Brownout detector was triggered": {
        "type": "brownout",
        "explanation": "The ESP32 detected insufficient power and reset to protect itself.",
        "causes": [
            "USB port cannot supply enough current",
            "Power-hungry peripherals",
            "WiFi transmission spikes",
            "Bad USB cable with high resistance"
        ],
        "fixes": [
            "Use powered USB hub",
            "Add external power supply (5V 1A minimum)",
            "Use shorter/better quality USB cable",
            "Add large capacitor (100-470µF) near ESP32 power pins",
            "Reduce WiFi transmit power in code"
        ]
    },
    
    r"rst:0x1.*POWERON_RESET.*rst:0x10.*RTCWDT_RTC_RESET": {
        "type": "watchdog_reset",
        "explanation": "ESP32 watchdog timer reset - code is stuck in a loop or blocking for too long.",
        "causes": [
            "Infinite loop without yield()",
            "Blocking code in callbacks",
            "WiFi.begin() without connection timeout"
        ],
        "fixes": [
            "Add yield() or delay(1) in long loops",
            "Don't block in interrupt handlers",
            "Add timeouts to network operations",
            "Use async/non-blocking patterns"
        ]
    }
}

# Common Arduino keywords that might be typos
COMMON_TYPOS = {
    "Led": "LED",
    "led": "LED",
    "HIGH": "HIGH",
    "high": "HIGH",
    "Low": "LOW",
    "low": "LOW",
    "input": "INPUT",
    "output": "OUTPUT",
    "serial": "Serial",
    "SERIAL": "Serial",
    "String": "String",
    "string": "String",
    "Delay": "delay",
    "DELAY": "delay",
    "pinmode": "pinMode",
    "PinMode": "pinMode",
    "digitalwrite": "digitalWrite",
    "DigitalWrite": "digitalWrite",
    "digitalread": "digitalRead",
    "DigitalRead": "digitalRead",
    "analogwrite": "analogWrite",
    "AnalogWrite": "analogWrite",
    "analogread": "analogRead",
    "AnalogRead": "analogRead"
}


@dataclass
class ParsedError:
    """Parsed error information"""
    original: str
    error_type: str
    explanation: str
    causes: List[str]
    fixes: List[str]
    line_number: Optional[int] = None
    file_name: Optional[str] = None
    identifier: Optional[str] = None


def extract_location(error_line: str) -> Tuple[Optional[str], Optional[int]]:
    """Extract file name and line number from error"""
    # Pattern: /path/to/file.ino:123:45: error:
    match = re.search(r'([^/\\:]+\.(?:ino|cpp|c|h)):(\d+):', error_line)
    if match:
        return match.group(1), int(match.group(2))
    return None, None


def parse_error(error_text: str) -> List[ParsedError]:
    """Parse error message and return explanation"""
    results = []
    
    # Split into lines and process
    lines = error_text.strip().split('\n')
    
    for line in lines:
        # Skip non-error lines
        if 'error:' not in line.lower() and 'warning:' not in line.lower():
            continue
        
        file_name, line_num = extract_location(line)
        
        # Try to match against known patterns
        for pattern, info in ERROR_PATTERNS.items():
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                # Extract captured groups for formatting
                groups = match.groups()
                
                explanation = info["explanation"]
                if groups:
                    try:
                        explanation = explanation.format(*groups)
                    except (IndexError, KeyError):
                        pass
                
                fixes = []
                for fix in info["fixes"]:
                    if groups:
                        try:
                            fix = fix.format(*groups)
                        except (IndexError, KeyError):
                            pass
                    fixes.append(fix)
                
                results.append(ParsedError(
                    original=line,
                    error_type=info["type"],
                    explanation=explanation,
                    causes=info["causes"],
                    fixes=fixes,
                    line_number=line_num,
                    file_name=file_name,
                    identifier=groups[0] if groups else None
                ))
                break
        else:
            # No pattern matched - generic error
            results.append(ParsedError(
                original=line,
                error_type="unknown",
                explanation="Error not in database. See original message.",
                causes=["Check the exact error message"],
                fixes=["Search online for this specific error"],
                line_number=line_num,
                file_name=file_name
            ))
    
    return results


def check_typo(identifier: str) -> Optional[str]:
    """Check if identifier might be a typo of common Arduino keyword"""
    if identifier in COMMON_TYPOS:
        return COMMON_TYPOS[identifier]
    
    # Case-insensitive check
    lower = identifier.lower()
    for typo, correct in COMMON_TYPOS.items():
        if typo.lower() == lower:
            return correct
    
    return None


def format_report(errors: List[ParsedError], verbose: bool = True) -> str:
    """Format error analysis as readable report"""
    if not errors:
        return "No errors found in input."
    
    lines = [
        "=" * 60,
        "          ERROR ANALYSIS REPORT",
        "=" * 60,
        ""
    ]
    
    for i, err in enumerate(errors, 1):
        lines.append(f"Error #{i}: {err.error_type.upper()}")
        lines.append("-" * 40)
        
        if err.file_name:
            loc = f"{err.file_name}"
            if err.line_number:
                loc += f", line {err.line_number}"
            lines.append(f"Location: {loc}")
        
        lines.append("")
        lines.append(f"🔍 What happened:")
        lines.append(f"   {err.explanation}")
        
        # Check for typo suggestion
        if err.identifier:
            suggestion = check_typo(err.identifier)
            if suggestion:
                lines.append(f"   💡 Did you mean: {suggestion}")
        
        if verbose:
            lines.append("")
            lines.append("📋 Possible causes:")
            for cause in err.causes[:3]:
                lines.append(f"   • {cause}")
            
            lines.append("")
            lines.append("🔧 How to fix:")
            for fix in err.fixes[:3]:
                lines.append(f"   • {fix}")
        
        lines.append("")
        lines.append(f"Original: {err.original[:80]}...")
        lines.append("")
    
    return "\n".join(lines)


def interactive_mode():
    """Interactive error analysis"""
    print("=" * 60)
    print("Error Message Explainer - Interactive Mode")
    print("=" * 60)
    print()
    print("Paste your error message (press Enter twice when done):")
    print()
    
    lines = []
    while True:
        line = input()
        if not line and lines and not lines[-1]:
            break
        lines.append(line)
    
    error_text = "\n".join(lines)
    
    if not error_text.strip():
        print("No error message provided.")
        return
    
    errors = parse_error(error_text)
    report = format_report(errors)
    print(report)


def main():
    parser = argparse.ArgumentParser(description="Arduino Error Message Parser")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--file", "-f", type=str, help="Read errors from file")
    parser.add_argument("--message", "-m", type=str, help="Single error message")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--brief", "-b", action="store_true", help="Brief output")
    
    args = parser.parse_args()
    
    error_text = ""
    
    if args.interactive:
        interactive_mode()
        return
    
    if args.file:
        with open(args.file, 'r') as f:
            error_text = f.read()
    elif args.message:
        error_text = args.message
    elif args.stdin:
        import sys
        error_text = sys.stdin.read()
    else:
        parser.print_help()
        return
    
    errors = parse_error(error_text)
    
    if args.json:
        import dataclasses
        output = [dataclasses.asdict(e) for e in errors]
        print(json.dumps(output, indent=2))
    else:
        print(format_report(errors, verbose=not args.brief))


if __name__ == "__main__":
    main()
