#!/usr/bin/env python3
"""
README Generator - Creates professional README.md for Arduino/maker projects

Analyzes project structure and generates documentation including:
- Project description
- Hardware requirements
- Wiring diagrams (ASCII)
- Installation instructions
- Usage examples
- License

Usage:
    uv run generate_readme.py --interactive
    uv run generate_readme.py --project "Weather Station" --board "ESP32"
    uv run generate_readme.py --scan /path/to/project
"""

import argparse
import os
import re
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# =============================================================================
# Templates
# =============================================================================

README_TEMPLATE = '''# {project_name}

{badges}

{description}

## 📋 Features

{features}

## 🔧 Hardware Required

{hardware_list}

### Wiring Diagram

{wiring_diagram}

## 📦 Dependencies

{dependencies}

## 🚀 Installation

{installation}

## 📖 Usage

{usage}

## ⚙️ Configuration

{configuration}

## 🐛 Troubleshooting

{troubleshooting}

## 📄 License

{license}

---
{footer}
'''

ASCII_WIRING_TEMPLATES = {
    "i2c": '''```
                    {board}
                 ┌──────────┐
                 │  VIN  5V │─────────────┐
                 │  GND     │───────────┐ │
                 │  SDA {sda} │────────┐ │ │
                 │  SCL {scl} │──────┐ │ │ │
                 └──────────┘      │ │ │ │
                                   │ │ │ │
    {device}                       │ │ │ │
 ┌──────────────┐                  │ │ │ │
 │  VCC         │──────────────────┼─┼─┼─┘
 │  GND         │──────────────────┼─┼─┘
 │  SDA         │──────────────────┼─┘
 │  SCL         │──────────────────┘
 └──────────────┘
```''',

    "spi": '''```
                    {board}
                 ┌──────────┐
                 │  VIN  5V │─────────────┐
                 │  GND     │───────────┐ │
                 │  MOSI {mosi}│────────┐ │ │
                 │  MISO {miso}│──────┐ │ │ │
                 │  SCK  {sck}│────┐ │ │ │ │
                 │  CS   {cs}│──┐ │ │ │ │ │
                 └──────────┘  │ │ │ │ │ │
                               │ │ │ │ │ │
    {device}                   │ │ │ │ │ │
 ┌──────────────┐              │ │ │ │ │ │
 │  VCC         │──────────────┼─┼─┼─┼─┼─┘
 │  GND         │──────────────┼─┼─┼─┼─┘
 │  DIN/MOSI    │──────────────┼─┼─┼─┘
 │  DOUT/MISO   │──────────────┼─┼─┘
 │  CLK/SCK     │──────────────┼─┘
 │  CS/SS       │──────────────┘
 └──────────────┘
```''',

    "simple_led": '''```
    {board}            LED + Resistor
 ┌──────────┐          
 │  Pin {pin} │─────────┬─────[{resistor}Ω]────►├── 
 │  GND     │─────────┴────────────────────────┘
 └──────────┘
```''',

    "servo": '''```
    {board}               Servo
 ┌──────────┐         ┌────────┐
 │  VIN  5V │─────────│ Red    │
 │  GND     │─────────│ Brown  │
 │  Pin {pin} │─────────│ Orange │
 └──────────┘         └────────┘
```''',

    "generic": '''```
Connections:
{connections}
```'''
}

BOARD_PINOUTS = {
    "Arduino Uno": {"sda": "A4", "scl": "A5", "mosi": "11", "miso": "12", "sck": "13"},
    "Arduino Nano": {"sda": "A4", "scl": "A5", "mosi": "11", "miso": "12", "sck": "13"},
    "Arduino Mega": {"sda": "20", "scl": "21", "mosi": "51", "miso": "50", "sck": "52"},
    "ESP32": {"sda": "21", "scl": "22", "mosi": "23", "miso": "19", "sck": "18"},
    "ESP8266": {"sda": "D2", "scl": "D1", "mosi": "D7", "miso": "D6", "sck": "D5"},
    "Raspberry Pi Pico": {"sda": "GP4", "scl": "GP5", "mosi": "GP19", "miso": "GP16", "sck": "GP18"},
}


@dataclass
class ProjectInfo:
    """Project information"""
    name: str = "My Arduino Project"
    description: str = "An Arduino-based project."
    board: str = "Arduino Uno"
    features: List[str] = field(default_factory=list)
    hardware: List[Dict] = field(default_factory=list)
    libraries: List[str] = field(default_factory=list)
    wiring_type: str = "generic"
    connections: List[Dict] = field(default_factory=list)
    license: str = "MIT"
    author: str = ""
    version: str = "1.0.0"


def scan_ino_file(filepath: str) -> Dict:
    """Scan .ino file for libraries and pin definitions"""
    info = {
        "libraries": [],
        "pins": [],
        "functions": []
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return info
    
    # Find includes
    includes = re.findall(r'#include\s*[<"]([^>"]+)[>"]', content)
    info["libraries"] = [inc.replace('.h', '') for inc in includes]
    
    # Find pin definitions
    pin_defs = re.findall(r'(?:const\s+int|#define)\s+(\w*(?:PIN|LED|BTN|BUTTON|SERVO|MOTOR)\w*)\s*[=\s]+(\d+)', 
                          content, re.IGNORECASE)
    info["pins"] = [(name, num) for name, num in pin_defs]
    
    # Check for I2C usage
    if 'Wire' in content or 'Wire.h' in str(includes):
        info["uses_i2c"] = True
    
    # Check for SPI usage
    if 'SPI' in content or 'SPI.h' in str(includes):
        info["uses_spi"] = True
    
    return info


def generate_wiring_diagram(project: ProjectInfo) -> str:
    """Generate ASCII wiring diagram"""
    pinout = BOARD_PINOUTS.get(project.board, BOARD_PINOUTS["Arduino Uno"])
    
    if project.wiring_type == "i2c" and project.hardware:
        device = project.hardware[0].get("name", "I2C Device")
        return ASCII_WIRING_TEMPLATES["i2c"].format(
            board=project.board,
            device=device,
            sda=pinout["sda"],
            scl=pinout["scl"]
        )
    
    elif project.wiring_type == "spi" and project.hardware:
        device = project.hardware[0].get("name", "SPI Device")
        return ASCII_WIRING_TEMPLATES["spi"].format(
            board=project.board,
            device=device,
            mosi=pinout["mosi"],
            miso=pinout["miso"],
            sck=pinout["sck"],
            cs="10"
        )
    
    elif project.connections:
        # Generic connection list
        lines = []
        for conn in project.connections:
            lines.append(f"  {project.board} {conn.get('from', '?')} ──── {conn.get('to', '?')} {conn.get('device', '')}")
        return ASCII_WIRING_TEMPLATES["generic"].format(
            connections="\n".join(lines)
        )
    
    return "_Add wiring diagram here_"


def generate_hardware_list(project: ProjectInfo) -> str:
    """Generate hardware requirements list"""
    lines = [f"- 1x {project.board}"]
    
    for hw in project.hardware:
        qty = hw.get("qty", 1)
        name = hw.get("name", "Component")
        note = hw.get("note", "")
        line = f"- {qty}x {name}"
        if note:
            line += f" ({note})"
        lines.append(line)
    
    # Add common items
    lines.extend([
        "- USB cable for programming",
        "- Breadboard and jumper wires"
    ])
    
    return "\n".join(lines)


def generate_dependencies(project: ProjectInfo) -> str:
    """Generate dependencies section"""
    if not project.libraries:
        return "No external libraries required."
    
    lines = ["Install these libraries via Arduino Library Manager:"]
    lines.append("")
    for lib in project.libraries:
        lines.append(f"- `{lib}`")
    
    lines.extend([
        "",
        "**To install:**",
        "1. Open Arduino IDE",
        "2. Go to Sketch → Include Library → Manage Libraries",
        "3. Search for each library and click Install"
    ])
    
    return "\n".join(lines)


def generate_installation(project: ProjectInfo) -> str:
    """Generate installation instructions"""
    return f'''1. **Clone or download** this repository
   ```bash
   git clone https://github.com/yourusername/{project.name.lower().replace(" ", "-")}.git
   ```

2. **Open the project** in Arduino IDE
   - File → Open → Select the `.ino` file

3. **Install required libraries** (see Dependencies section)

4. **Select your board**
   - Tools → Board → {project.board}

5. **Select the port**
   - Tools → Port → (select your Arduino's port)

6. **Upload the sketch**
   - Click the Upload button (→) or press Ctrl+U'''


def generate_usage(project: ProjectInfo) -> str:
    """Generate usage instructions"""
    return f'''1. Connect the hardware according to the wiring diagram
2. Upload the code to your {project.board}
3. Open Serial Monitor at 115200 baud
4. The system will start automatically

### Serial Commands

| Command | Description |
|---------|-------------|
| `status` | Show current status |
| `help` | List available commands |

_Customize this section based on your project's functionality._'''


def generate_readme(project: ProjectInfo) -> str:
    """Generate complete README"""
    
    # Generate badges
    badges = f"![Version](https://img.shields.io/badge/version-{project.version}-blue) "
    badges += f"![Board](https://img.shields.io/badge/board-{project.board.replace(' ', '%20')}-green) "
    badges += f"![License](https://img.shields.io/badge/license-{project.license}-orange)"
    
    # Generate features list
    features = ""
    if project.features:
        features = "\n".join(f"- ✅ {f}" for f in project.features)
    else:
        features = "- ✅ Feature 1\n- ✅ Feature 2\n- ✅ Feature 3"
    
    # Generate sections
    readme = README_TEMPLATE.format(
        project_name=project.name,
        badges=badges,
        description=project.description,
        features=features,
        hardware_list=generate_hardware_list(project),
        wiring_diagram=generate_wiring_diagram(project),
        dependencies=generate_dependencies(project),
        installation=generate_installation(project),
        usage=generate_usage(project),
        configuration="_Add configuration options here_",
        troubleshooting='''| Problem | Solution |
|---------|----------|
| Won't compile | Check library installations |
| No serial output | Verify baud rate is 115200 |
| Device not detected | Check wiring connections |''',
        license=f"This project is licensed under the {project.license} License.",
        footer=f"Made with ❤️ for the maker community • {datetime.now().year}"
    )
    
    return readme


def interactive_mode():
    """Interactive README generator"""
    print("=" * 60)
    print("README Generator - Interactive Mode")
    print("=" * 60)
    print()
    
    project = ProjectInfo()
    
    # Basic info
    project.name = input("Project name [My Arduino Project]: ").strip() or "My Arduino Project"
    project.description = input("Short description: ").strip() or "An Arduino-based project."
    
    # Board selection
    print("\nAvailable boards:")
    boards = list(BOARD_PINOUTS.keys())
    for i, b in enumerate(boards, 1):
        print(f"  {i}. {b}")
    choice = input(f"Select board (1-{len(boards)}) [1]: ").strip() or "1"
    try:
        project.board = boards[int(choice) - 1]
    except:
        project.board = "Arduino Uno"
    
    # Features
    print("\nEnter features (one per line, empty to finish):")
    while True:
        feat = input("  - ").strip()
        if not feat:
            break
        project.features.append(feat)
    
    # Hardware
    print("\nEnter hardware components (empty name to finish):")
    while True:
        name = input("  Component name: ").strip()
        if not name:
            break
        qty = input("  Quantity [1]: ").strip() or "1"
        project.hardware.append({"name": name, "qty": int(qty)})
    
    # Libraries
    print("\nEnter required libraries (empty to finish):")
    while True:
        lib = input("  Library: ").strip()
        if not lib:
            break
        project.libraries.append(lib)
    
    # Wiring type
    print("\nWiring diagram type:")
    print("  1. I2C device")
    print("  2. SPI device")
    print("  3. Generic/Custom")
    wtype = input("Select (1-3) [3]: ").strip() or "3"
    project.wiring_type = {"1": "i2c", "2": "spi", "3": "generic"}.get(wtype, "generic")
    
    # Generate
    readme = generate_readme(project)
    
    # Output
    filename = input("\nOutput filename [README.md]: ").strip() or "README.md"
    with open(filename, 'w') as f:
        f.write(readme)
    
    print(f"\n✓ Generated: {filename}")
    print(f"  Project: {project.name}")
    print(f"  Board: {project.board}")


def main():
    parser = argparse.ArgumentParser(description="README Generator for Arduino Projects")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--project", "-p", type=str, help="Project name")
    parser.add_argument("--board", "-b", type=str, default="Arduino Uno", help="Board type")
    parser.add_argument("--description", "-d", type=str, help="Project description")
    parser.add_argument("--scan", "-s", type=str, help="Scan directory for .ino files")
    parser.add_argument("--output", "-o", type=str, default="README.md", help="Output file")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    project = ProjectInfo(
        name=args.project or "My Arduino Project",
        board=args.board,
        description=args.description or "An Arduino-based project."
    )
    
    # Scan directory if provided
    if args.scan:
        for root, dirs, files in os.walk(args.scan):
            for f in files:
                if f.endswith('.ino'):
                    info = scan_ino_file(os.path.join(root, f))
                    project.libraries.extend(info.get("libraries", []))
                    if info.get("uses_i2c"):
                        project.wiring_type = "i2c"
                    elif info.get("uses_spi"):
                        project.wiring_type = "spi"
        project.libraries = list(set(project.libraries))  # Remove duplicates
    
    readme = generate_readme(project)
    
    with open(args.output, 'w') as f:
        f.write(readme)
    
    print(f"Generated: {args.output}")


if __name__ == "__main__":
    main()
