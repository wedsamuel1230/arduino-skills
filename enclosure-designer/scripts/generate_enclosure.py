#!/usr/bin/env python3
"""
Enclosure Generator - Parametric OpenSCAD enclosure generator

Generates customizable enclosure designs for electronics projects.
Supports various form factors, mounting patterns, and features.

Usage:
    uv run generate_enclosure.py --interactive
    uv run generate_enclosure.py --width 100 --depth 60 --height 30 --output my_case.scad
    uv run generate_enclosure.py --pcb "Arduino Uno" --output arduino_case.scad
"""

import argparse
import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# =============================================================================
# PCB Database - Common board dimensions
# =============================================================================

PCB_DATABASE = {
    "Arduino Uno": {
        "width": 68.6,
        "depth": 53.4,
        "height": 15,  # Component height
        "mounting_holes": [
            (14.0, 2.5),
            (15.2, 50.8),
            (66.0, 7.6),
            (66.0, 35.6)
        ],
        "hole_diameter": 3.2,
        "usb_position": "left",
        "usb_offset_y": 31.75,
        "power_jack": True
    },
    "Arduino Nano": {
        "width": 43.2,
        "depth": 18.5,
        "height": 8,
        "mounting_holes": [],
        "hole_diameter": 0,
        "usb_position": "left",
        "usb_offset_y": 9.25
    },
    "Arduino Mega": {
        "width": 101.6,
        "depth": 53.4,
        "height": 15,
        "mounting_holes": [
            (14.0, 2.5),
            (15.2, 50.8),
            (90.2, 2.5),
            (96.5, 35.6)
        ],
        "hole_diameter": 3.2,
        "usb_position": "left",
        "usb_offset_y": 31.75,
        "power_jack": True
    },
    "ESP32 DevKit": {
        "width": 51.5,
        "depth": 28.0,
        "height": 10,
        "mounting_holes": [
            (2.5, 2.5),
            (2.5, 25.5),
            (49.0, 2.5),
            (49.0, 25.5)
        ],
        "hole_diameter": 2.5,
        "usb_position": "left"
    },
    "ESP8266 NodeMCU": {
        "width": 57.0,
        "depth": 31.0,
        "height": 8,
        "mounting_holes": [
            (2.5, 2.5),
            (2.5, 28.5),
            (54.5, 2.5),
            (54.5, 28.5)
        ],
        "hole_diameter": 3.0,
        "usb_position": "left"
    },
    "Raspberry Pi Pico": {
        "width": 51.0,
        "depth": 21.0,
        "height": 4,
        "mounting_holes": [
            (2.0, 11.4),
            (49.0, 11.4)
        ],
        "hole_diameter": 2.1,
        "usb_position": "left"
    },
    "Raspberry Pi Zero": {
        "width": 65.0,
        "depth": 30.0,
        "height": 5,
        "mounting_holes": [
            (3.5, 3.5),
            (3.5, 26.5),
            (61.5, 3.5),
            (61.5, 26.5)
        ],
        "hole_diameter": 2.75,
        "usb_position": "right",
        "micro_usb": True,
        "mini_hdmi": True
    },
    "Custom": {
        "width": 100,
        "depth": 60,
        "height": 25,
        "mounting_holes": [],
        "hole_diameter": 3.0
    }
}


@dataclass
class EnclosureConfig:
    """Enclosure configuration parameters"""
    # Interior dimensions
    inner_width: float = 100
    inner_depth: float = 60
    inner_height: float = 30
    
    # Wall parameters
    wall_thickness: float = 2.5
    bottom_thickness: float = 2.5
    top_thickness: float = 2.0
    
    # Corner parameters
    corner_radius: float = 3.0
    
    # Lid style
    lid_style: str = "snap"  # snap, screw, slide
    lid_tolerance: float = 0.3
    
    # Ventilation
    ventilation: bool = True
    vent_slot_width: float = 2.0
    vent_slot_length: float = 15.0
    vent_count: int = 4
    
    # Mounting options
    pcb_standoff_height: float = 5.0
    pcb_standoff_diameter: float = 6.0
    pcb_hole_diameter: float = 3.0
    mounting_holes: List[tuple] = field(default_factory=list)
    
    # Features
    cable_hole: bool = True
    cable_hole_diameter: float = 8.0
    cable_hole_position: str = "back"
    
    # Display cutout (optional)
    display_cutout: bool = False
    display_width: float = 50
    display_height: float = 20
    
    # Button holes (optional)
    button_holes: List[dict] = field(default_factory=list)
    
    # Output
    quality: int = 50  # $fn value


def generate_base_box(config: EnclosureConfig) -> str:
    """Generate the base enclosure module"""
    
    outer_w = config.inner_width + 2 * config.wall_thickness
    outer_d = config.inner_depth + 2 * config.wall_thickness
    outer_h = config.inner_height + config.bottom_thickness
    
    return f'''
// Base box with rounded corners
module base_box() {{
    difference() {{
        // Outer shell
        minkowski() {{
            cube([{outer_w - 2*config.corner_radius}, 
                  {outer_d - 2*config.corner_radius}, 
                  {outer_h/2}]);
            cylinder(r={config.corner_radius}, h={outer_h/2}, $fn={config.quality});
        }}
        
        // Interior cutout
        translate([{config.wall_thickness}, {config.wall_thickness}, {config.bottom_thickness}])
            cube([{config.inner_width}, {config.inner_depth}, {config.inner_height + 1}]);
        
        // Lid lip cutout
        translate([{config.wall_thickness - config.lid_tolerance}, 
                   {config.wall_thickness - config.lid_tolerance}, 
                   {outer_h - 3}])
            cube([{config.inner_width + 2*config.lid_tolerance}, 
                  {config.inner_depth + 2*config.lid_tolerance}, 
                  5]);
    }}
}}
'''


def generate_lid(config: EnclosureConfig) -> str:
    """Generate the lid module"""
    
    outer_w = config.inner_width + 2 * config.wall_thickness
    outer_d = config.inner_depth + 2 * config.wall_thickness
    lip_w = config.inner_width + config.lid_tolerance * 2
    lip_d = config.inner_depth + config.lid_tolerance * 2
    
    return f'''
// Lid with lip
module lid() {{
    union() {{
        // Top plate
        minkowski() {{
            cube([{outer_w - 2*config.corner_radius}, 
                  {outer_d - 2*config.corner_radius}, 
                  {config.top_thickness/2}]);
            cylinder(r={config.corner_radius}, h={config.top_thickness/2}, $fn={config.quality});
        }}
        
        // Inner lip
        translate([{config.wall_thickness - config.lid_tolerance/2}, 
                   {config.wall_thickness - config.lid_tolerance/2}, 
                   -{2.5}])
            difference() {{
                cube([{lip_w}, {lip_d}, 2.5]);
                translate([1.5, 1.5, -0.1])
                    cube([{lip_w - 3}, {lip_d - 3}, 3]);
            }}
    }}
}}
'''


def generate_standoffs(config: EnclosureConfig) -> str:
    """Generate PCB standoff modules"""
    
    if not config.mounting_holes:
        return "// No mounting holes defined"
    
    standoffs = []
    for i, (x, y) in enumerate(config.mounting_holes):
        standoffs.append(f'''
    // Standoff {i+1}
    translate([{config.wall_thickness + x}, {config.wall_thickness + y}, {config.bottom_thickness}])
        difference() {{
            cylinder(d={config.pcb_standoff_diameter}, h={config.pcb_standoff_height}, $fn={config.quality});
            translate([0, 0, -0.1])
                cylinder(d={config.pcb_hole_diameter}, h={config.pcb_standoff_height + 1}, $fn={config.quality});
        }}''')
    
    return f'''
// PCB Standoffs
module standoffs() {{
{"".join(standoffs)}
}}
'''


def generate_ventilation(config: EnclosureConfig) -> str:
    """Generate ventilation slots"""
    
    if not config.ventilation:
        return "// Ventilation disabled"
    
    outer_w = config.inner_width + 2 * config.wall_thickness
    
    return f'''
// Ventilation slots
module vent_slots() {{
    slot_spacing = {config.vent_slot_length + 5};
    start_y = ({config.inner_depth} - ({config.vent_count} - 1) * slot_spacing) / 2;
    
    for (i = [0:{config.vent_count - 1}]) {{
        // Left side vents
        translate([-1, {config.wall_thickness} + start_y + i * slot_spacing, {config.bottom_thickness + 5}])
            rotate([0, 90, 0])
                hull() {{
                    cylinder(d={config.vent_slot_width}, h={config.wall_thickness + 2}, $fn=20);
                    translate([0, {config.vent_slot_length}, 0])
                        cylinder(d={config.vent_slot_width}, h={config.wall_thickness + 2}, $fn=20);
                }}
        
        // Right side vents
        translate([{outer_w - config.wall_thickness - 1}, {config.wall_thickness} + start_y + i * slot_spacing, {config.bottom_thickness + 5}])
            rotate([0, 90, 0])
                hull() {{
                    cylinder(d={config.vent_slot_width}, h={config.wall_thickness + 2}, $fn=20);
                    translate([0, {config.vent_slot_length}, 0])
                        cylinder(d={config.vent_slot_width}, h={config.wall_thickness + 2}, $fn=20);
                }}
    }}
}}
'''


def generate_cable_hole(config: EnclosureConfig) -> str:
    """Generate cable hole cutout"""
    
    if not config.cable_hole:
        return "// Cable hole disabled"
    
    outer_w = config.inner_width + 2 * config.wall_thickness
    outer_d = config.inner_depth + 2 * config.wall_thickness
    outer_h = config.inner_height + config.bottom_thickness
    
    positions = {
        "back": f"translate([{outer_w/2}, {outer_d + 1}, {outer_h/2}]) rotate([90, 0, 0])",
        "front": f"translate([{outer_w/2}, -1, {outer_h/2}]) rotate([90, 0, 0])",
        "left": f"translate([-1, {outer_d/2}, {outer_h/2}]) rotate([0, 90, 0])",
        "right": f"translate([{outer_w + 1}, {outer_d/2}, {outer_h/2}]) rotate([0, 90, 0])"
    }
    
    pos = positions.get(config.cable_hole_position, positions["back"])
    
    return f'''
// Cable hole
module cable_hole() {{
    {pos}
        cylinder(d={config.cable_hole_diameter}, h={config.wall_thickness + 2}, $fn={config.quality});
}}
'''


def generate_display_cutout(config: EnclosureConfig) -> str:
    """Generate display cutout for lid"""
    
    if not config.display_cutout:
        return "// Display cutout disabled"
    
    outer_w = config.inner_width + 2 * config.wall_thickness
    outer_d = config.inner_depth + 2 * config.wall_thickness
    
    return f'''
// Display cutout
module display_cutout() {{
    translate([{(outer_w - config.display_width)/2}, 
               {(outer_d - config.display_height)/2}, 
               -1])
        cube([{config.display_width}, {config.display_height}, {config.top_thickness + 2}]);
}}
'''


def generate_full_scad(config: EnclosureConfig, pcb_name: Optional[str] = None) -> str:
    """Generate complete OpenSCAD file"""
    
    header = f'''/*
 * Parametric Electronics Enclosure
 * Generated by enclosure-designer skill
 * 
 * PCB: {pcb_name or "Custom"}
 * Interior: {config.inner_width} x {config.inner_depth} x {config.inner_height} mm
 * Wall: {config.wall_thickness} mm
 */

// Quality setting (higher = smoother curves, slower render)
$fn = {config.quality};

'''

    modules = [
        header,
        generate_base_box(config),
        generate_lid(config),
        generate_standoffs(config),
        generate_ventilation(config),
        generate_cable_hole(config),
        generate_display_cutout(config)
    ]
    
    # Assembly
    assembly = f'''
// === ASSEMBLY ===
// Uncomment the parts you want to render/export

// Base with standoffs and cutouts
difference() {{
    union() {{
        base_box();
        standoffs();
    }}
    vent_slots();
    cable_hole();
}}

// Lid - move aside for printing
translate([{config.inner_width + 2 * config.wall_thickness + 10}, 0, 0]) {{
    difference() {{
        lid();
        display_cutout();
    }}
}}

// For STL export, render parts separately:
// !base_box();
// !lid();
'''

    return "\n".join(modules) + assembly


def config_from_pcb(pcb_name: str, clearance: float = 5.0) -> EnclosureConfig:
    """Create enclosure config from PCB database entry"""
    
    if pcb_name not in PCB_DATABASE:
        raise ValueError(f"Unknown PCB: {pcb_name}. Available: {', '.join(PCB_DATABASE.keys())}")
    
    pcb = PCB_DATABASE[pcb_name]
    
    return EnclosureConfig(
        inner_width=pcb["width"] + clearance * 2,
        inner_depth=pcb["depth"] + clearance * 2,
        inner_height=pcb["height"] + clearance,
        mounting_holes=[(x + clearance, y + clearance) for x, y in pcb.get("mounting_holes", [])],
        pcb_hole_diameter=pcb.get("hole_diameter", 3.0),
        cable_hole=True,
        cable_hole_position="left" if pcb.get("usb_position") == "left" else "right"
    )


def interactive_mode():
    """Run enclosure generator interactively"""
    print("=" * 60)
    print("Enclosure Generator - Interactive Mode")
    print("=" * 60)
    print()
    
    # PCB selection
    print("Available PCBs:")
    for i, name in enumerate(PCB_DATABASE.keys(), 1):
        pcb = PCB_DATABASE[name]
        print(f"  {i}. {name} ({pcb['width']}x{pcb['depth']}mm)")
    
    print()
    choice = input("Select PCB by number (or 'c' for custom dimensions): ").strip()
    
    if choice.lower() == 'c':
        width = float(input("Interior width (mm) [100]: ").strip() or "100")
        depth = float(input("Interior depth (mm) [60]: ").strip() or "60")
        height = float(input("Interior height (mm) [30]: ").strip() or "30")
        
        config = EnclosureConfig(
            inner_width=width,
            inner_depth=depth,
            inner_height=height
        )
        pcb_name = None
    else:
        try:
            idx = int(choice) - 1
            pcb_name = list(PCB_DATABASE.keys())[idx]
            clearance = float(input("Clearance around PCB (mm) [5]: ").strip() or "5")
            config = config_from_pcb(pcb_name, clearance)
            print(f"\nGenerated enclosure for {pcb_name}")
        except (ValueError, IndexError):
            print("Invalid selection, using custom")
            config = EnclosureConfig()
            pcb_name = None
    
    # Features
    print("\nFeatures:")
    config.wall_thickness = float(input(f"Wall thickness (mm) [{config.wall_thickness}]: ").strip() or config.wall_thickness)
    config.ventilation = input("Add ventilation slots? (y/n) [y]: ").strip().lower() != 'n'
    config.cable_hole = input("Add cable hole? (y/n) [y]: ").strip().lower() != 'n'
    
    if input("Add display cutout? (y/n) [n]: ").strip().lower() == 'y':
        config.display_cutout = True
        config.display_width = float(input("Display width (mm) [50]: ").strip() or "50")
        config.display_height = float(input("Display height (mm) [20]: ").strip() or "20")
    
    # Generate
    scad_code = generate_full_scad(config, pcb_name)
    
    # Output
    filename = input("\nOutput filename [enclosure.scad]: ").strip() or "enclosure.scad"
    with open(filename, 'w') as f:
        f.write(scad_code)
    
    print(f"\n✓ Generated: {filename}")
    print(f"  Interior: {config.inner_width} x {config.inner_depth} x {config.inner_height} mm")
    print(f"  Exterior: {config.inner_width + 2*config.wall_thickness} x "
          f"{config.inner_depth + 2*config.wall_thickness} x "
          f"{config.inner_height + config.bottom_thickness + config.top_thickness} mm")
    print(f"\nOpen in OpenSCAD to preview and export STL")


def main():
    parser = argparse.ArgumentParser(description="Parametric Enclosure Generator")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--pcb", "-p", type=str, help="PCB name from database")
    parser.add_argument("--width", "-W", type=float, help="Interior width (mm)")
    parser.add_argument("--depth", "-D", type=float, help="Interior depth (mm)")
    parser.add_argument("--height", "-H", type=float, help="Interior height (mm)")
    parser.add_argument("--wall", "-w", type=float, default=2.5, help="Wall thickness (mm)")
    parser.add_argument("--clearance", "-c", type=float, default=5.0, help="PCB clearance (mm)")
    parser.add_argument("--output", "-o", type=str, default="enclosure.scad", help="Output file")
    parser.add_argument("--list", "-l", action="store_true", help="List available PCBs")
    parser.add_argument("--json", action="store_true", help="Output config as JSON")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available PCB profiles:")
        print("-" * 60)
        for name, pcb in PCB_DATABASE.items():
            holes = len(pcb.get("mounting_holes", []))
            print(f"  {name:20} {pcb['width']:6.1f} x {pcb['depth']:5.1f} x {pcb['height']:4.1f}mm "
                  f"({holes} mounting holes)")
        return
    
    if args.interactive:
        interactive_mode()
        return
    
    # Generate from parameters
    if args.pcb:
        config = config_from_pcb(args.pcb, args.clearance)
        config.wall_thickness = args.wall
        scad_code = generate_full_scad(config, args.pcb)
    elif args.width and args.depth and args.height:
        config = EnclosureConfig(
            inner_width=args.width,
            inner_depth=args.depth,
            inner_height=args.height,
            wall_thickness=args.wall
        )
        scad_code = generate_full_scad(config)
    else:
        parser.print_help()
        return
    
    if args.json:
        # Output config as JSON
        import dataclasses
        print(json.dumps(dataclasses.asdict(config), indent=2))
    else:
        with open(args.output, 'w') as f:
            f.write(scad_code)
        print(f"Generated: {args.output}")


if __name__ == "__main__":
    main()
