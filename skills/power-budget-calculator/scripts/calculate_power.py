#!/usr/bin/env python3
"""
Power Budget Calculator for Embedded Systems

Calculates total power consumption, duty cycle impact, and battery runtime
for Arduino/ESP32/RP2040 projects.

Usage:
    uv run calculate_power.py --interactive
    uv run calculate_power.py --json input.json
    uv run calculate_power.py --component ESP32 --mode active --duty 10

Output: JSON report with power analysis and battery recommendations
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional
from pathlib import Path

# =============================================================================
# Component Database - Current draw in mA at typical voltages
# =============================================================================

COMPONENT_DATABASE = {
    # Microcontrollers
    "ESP32": {
        "voltage": 3.3,
        "modes": {
            "active_wifi_tx": 260,
            "active_wifi_rx": 95,
            "active_bt": 130,
            "active_cpu": 80,
            "modem_sleep": 20,
            "light_sleep": 0.8,
            "deep_sleep": 0.01,
            "hibernation": 0.005
        },
        "typical_mode": "active_wifi_tx"
    },
    "ESP8266": {
        "voltage": 3.3,
        "modes": {
            "active_wifi_tx": 170,
            "active_wifi_rx": 56,
            "modem_sleep": 15,
            "light_sleep": 0.5,
            "deep_sleep": 0.02
        },
        "typical_mode": "active_wifi_tx"
    },
    "Arduino_Uno": {
        "voltage": 5.0,
        "modes": {
            "active": 45,
            "idle": 35,
            "power_down": 0.1
        },
        "typical_mode": "active"
    },
    "Arduino_Nano": {
        "voltage": 5.0,
        "modes": {
            "active": 20,
            "idle": 15,
            "power_down": 0.006
        },
        "typical_mode": "active"
    },
    "RP2040": {
        "voltage": 3.3,
        "modes": {
            "active_full": 93,
            "active_normal": 24,
            "dormant": 0.18,
            "sleep": 1.3
        },
        "typical_mode": "active_normal"
    },
    "ATtiny85": {
        "voltage": 3.3,
        "modes": {
            "active_8mhz": 5,
            "active_1mhz": 1.5,
            "idle": 0.5,
            "power_down": 0.0001
        },
        "typical_mode": "active_1mhz"
    },
    
    # Sensors
    "BME280": {
        "voltage": 3.3,
        "modes": {
            "measuring": 0.714,
            "sleep": 0.0001
        },
        "typical_mode": "measuring"
    },
    "DHT22": {
        "voltage": 3.3,
        "modes": {
            "measuring": 1.5,
            "standby": 0.05
        },
        "typical_mode": "measuring"
    },
    "MPU6050": {
        "voltage": 3.3,
        "modes": {
            "gyro_accel": 3.8,
            "accel_only": 0.5,
            "sleep": 0.005
        },
        "typical_mode": "gyro_accel"
    },
    "BMP180": {
        "voltage": 3.3,
        "modes": {
            "measuring": 0.65,
            "standby": 0.003
        },
        "typical_mode": "measuring"
    },
    "HC_SR04": {
        "voltage": 5.0,
        "modes": {
            "active": 15,
            "standby": 2
        },
        "typical_mode": "active"
    },
    "VL53L0X": {
        "voltage": 3.3,
        "modes": {
            "ranging": 19,
            "standby": 0.005
        },
        "typical_mode": "ranging"
    },
    
    # Displays
    "OLED_128x64": {
        "voltage": 3.3,
        "modes": {
            "full_on": 20,
            "half_pixels": 10,
            "off": 0.01
        },
        "typical_mode": "half_pixels"
    },
    "LCD_16x2_I2C": {
        "voltage": 5.0,
        "modes": {
            "backlight_on": 25,
            "backlight_off": 2
        },
        "typical_mode": "backlight_on"
    },
    "TFT_1_8": {
        "voltage": 3.3,
        "modes": {
            "active": 40,
            "sleep": 0.5
        },
        "typical_mode": "active"
    },
    "E_Paper_2_9": {
        "voltage": 3.3,
        "modes": {
            "refresh": 40,
            "static": 0.001
        },
        "typical_mode": "static"
    },
    
    # Communication
    "NRF24L01": {
        "voltage": 3.3,
        "modes": {
            "tx": 11.3,
            "rx": 13.5,
            "standby": 0.022,
            "power_down": 0.0009
        },
        "typical_mode": "rx"
    },
    "LoRa_SX1276": {
        "voltage": 3.3,
        "modes": {
            "tx_20dbm": 120,
            "tx_17dbm": 90,
            "rx": 12,
            "sleep": 0.0002
        },
        "typical_mode": "rx"
    },
    "GPS_NEO6M": {
        "voltage": 3.3,
        "modes": {
            "acquisition": 45,
            "tracking": 35,
            "power_save": 11
        },
        "typical_mode": "tracking"
    },
    
    # Actuators
    "Servo_SG90": {
        "voltage": 5.0,
        "modes": {
            "moving": 250,
            "holding": 10,
            "idle": 5
        },
        "typical_mode": "holding"
    },
    "DC_Motor_Small": {
        "voltage": 5.0,
        "modes": {
            "full_load": 500,
            "no_load": 100,
            "stall": 1000
        },
        "typical_mode": "no_load"
    },
    "Relay_5V": {
        "voltage": 5.0,
        "modes": {
            "energized": 80,
            "off": 0
        },
        "typical_mode": "energized"
    },
    "LED": {
        "voltage": 3.3,
        "modes": {
            "on_20ma": 20,
            "on_5ma": 5,
            "off": 0
        },
        "typical_mode": "on_5ma"
    },
    "WS2812B_LED": {
        "voltage": 5.0,
        "modes": {
            "white_full": 60,
            "color_avg": 20,
            "off": 1
        },
        "typical_mode": "color_avg"
    }
}

# Battery capacities in mAh
BATTERY_DATABASE = {
    "CR2032": {"capacity": 220, "voltage": 3.0, "chemistry": "Lithium", "rechargeable": False},
    "AA_Alkaline": {"capacity": 2500, "voltage": 1.5, "chemistry": "Alkaline", "rechargeable": False},
    "AA_NiMH": {"capacity": 2000, "voltage": 1.2, "chemistry": "NiMH", "rechargeable": True},
    "AAA_Alkaline": {"capacity": 1000, "voltage": 1.5, "chemistry": "Alkaline", "rechargeable": False},
    "18650_LiPo": {"capacity": 3000, "voltage": 3.7, "chemistry": "Li-ion", "rechargeable": True},
    "LiPo_1000": {"capacity": 1000, "voltage": 3.7, "chemistry": "LiPo", "rechargeable": True},
    "LiPo_2000": {"capacity": 2000, "voltage": 3.7, "chemistry": "LiPo", "rechargeable": True},
    "LiPo_5000": {"capacity": 5000, "voltage": 3.7, "chemistry": "LiPo", "rechargeable": True},
    "9V_Alkaline": {"capacity": 550, "voltage": 9.0, "chemistry": "Alkaline", "rechargeable": False},
    "LiFePO4_1500": {"capacity": 1500, "voltage": 3.2, "chemistry": "LiFePO4", "rechargeable": True}
}


@dataclass
class ComponentEntry:
    """Single component in the power budget"""
    name: str
    mode: str
    current_ma: float
    voltage: float
    duty_cycle_percent: float = 100.0
    quantity: int = 1
    notes: str = ""
    
    @property
    def effective_current_ma(self) -> float:
        """Current adjusted for duty cycle"""
        return self.current_ma * (self.duty_cycle_percent / 100.0) * self.quantity
    
    @property
    def power_mw(self) -> float:
        """Power in milliwatts"""
        return self.effective_current_ma * self.voltage


@dataclass
class PowerBudget:
    """Complete power budget analysis"""
    project_name: str = "Untitled Project"
    system_voltage: float = 3.3
    components: list = field(default_factory=list)
    safety_margin_percent: float = 20.0
    
    @property
    def total_current_ma(self) -> float:
        """Total current draw in mA"""
        return sum(c.effective_current_ma for c in self.components)
    
    @property
    def total_current_with_margin_ma(self) -> float:
        """Total current with safety margin"""
        return self.total_current_ma * (1 + self.safety_margin_percent / 100.0)
    
    @property
    def total_power_mw(self) -> float:
        """Total power in milliwatts"""
        return sum(c.power_mw for c in self.components)
    
    def calculate_battery_life(self, battery_name: str) -> dict:
        """Calculate runtime for a specific battery"""
        if battery_name not in BATTERY_DATABASE:
            return {"error": f"Unknown battery: {battery_name}"}
        
        battery = BATTERY_DATABASE[battery_name]
        capacity = battery["capacity"]
        
        # Peukert effect approximation (capacity reduces at higher currents)
        current = self.total_current_with_margin_ma
        if current > capacity * 0.2:  # High drain
            effective_capacity = capacity * 0.7
        elif current > capacity * 0.1:  # Medium drain
            effective_capacity = capacity * 0.85
        else:  # Low drain
            effective_capacity = capacity * 0.95
        
        hours = effective_capacity / current if current > 0 else float('inf')
        
        return {
            "battery": battery_name,
            "capacity_mah": capacity,
            "effective_capacity_mah": round(effective_capacity, 1),
            "runtime_hours": round(hours, 2),
            "runtime_days": round(hours / 24, 2),
            "suitable": hours > 1,  # At least 1 hour runtime
            "peukert_note": "High drain reduces effective capacity" if current > capacity * 0.1 else None
        }
    
    def recommend_batteries(self, min_hours: float = 24) -> list:
        """Recommend batteries that meet minimum runtime"""
        recommendations = []
        for battery_name in BATTERY_DATABASE:
            result = self.calculate_battery_life(battery_name)
            if result.get("runtime_hours", 0) >= min_hours:
                recommendations.append(result)
        
        # Sort by runtime descending
        recommendations.sort(key=lambda x: x["runtime_hours"], reverse=True)
        return recommendations
    
    def to_dict(self) -> dict:
        """Export to dictionary"""
        return {
            "project_name": self.project_name,
            "system_voltage": self.system_voltage,
            "safety_margin_percent": self.safety_margin_percent,
            "components": [
                {
                    "name": c.name,
                    "mode": c.mode,
                    "current_ma": c.current_ma,
                    "voltage": c.voltage,
                    "duty_cycle_percent": c.duty_cycle_percent,
                    "quantity": c.quantity,
                    "effective_current_ma": round(c.effective_current_ma, 3),
                    "power_mw": round(c.power_mw, 3),
                    "notes": c.notes
                }
                for c in self.components
            ],
            "totals": {
                "total_current_ma": round(self.total_current_ma, 3),
                "total_current_with_margin_ma": round(self.total_current_with_margin_ma, 3),
                "total_power_mw": round(self.total_power_mw, 3)
            }
        }
    
    def to_json(self) -> str:
        """Export to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def to_markdown_report(self) -> str:
        """Generate markdown report"""
        lines = [
            f"# Power Budget Report: {self.project_name}",
            "",
            "## System Configuration",
            f"- **System Voltage:** {self.system_voltage}V",
            f"- **Safety Margin:** {self.safety_margin_percent}%",
            "",
            "## Component Breakdown",
            "",
            "| Component | Mode | Current (mA) | Duty % | Eff. Current (mA) | Power (mW) |",
            "|-----------|------|--------------|--------|-------------------|------------|"
        ]
        
        for c in self.components:
            lines.append(
                f"| {c.name} | {c.mode} | {c.current_ma:.2f} | {c.duty_cycle_percent:.1f} | "
                f"{c.effective_current_ma:.3f} | {c.power_mw:.3f} |"
            )
        
        lines.extend([
            "",
            "## Totals",
            f"- **Total Current:** {self.total_current_ma:.2f} mA",
            f"- **With Safety Margin:** {self.total_current_with_margin_ma:.2f} mA",
            f"- **Total Power:** {self.total_power_mw:.2f} mW",
            "",
            "## Battery Life Estimates",
            "",
            "| Battery | Capacity (mAh) | Runtime (hours) | Runtime (days) |",
            "|---------|----------------|-----------------|----------------|"
        ])
        
        for battery_name in BATTERY_DATABASE:
            result = self.calculate_battery_life(battery_name)
            lines.append(
                f"| {battery_name} | {result['capacity_mah']} | "
                f"{result['runtime_hours']:.1f} | {result['runtime_days']:.2f} |"
            )
        
        return "\n".join(lines)


def add_component_from_database(budget: PowerBudget, component_name: str, 
                                mode: Optional[str] = None, 
                                duty_cycle: float = 100.0,
                                quantity: int = 1) -> bool:
    """Add a component from the database to the budget"""
    if component_name not in COMPONENT_DATABASE:
        print(f"Warning: Unknown component '{component_name}'", file=sys.stderr)
        return False
    
    comp_data = COMPONENT_DATABASE[component_name]
    
    # Use specified mode or typical mode
    if mode is None:
        mode = comp_data.get("typical_mode", list(comp_data["modes"].keys())[0])
    
    if mode not in comp_data["modes"]:
        print(f"Warning: Unknown mode '{mode}' for {component_name}", file=sys.stderr)
        return False
    
    current = comp_data["modes"][mode]
    voltage = comp_data["voltage"]
    
    entry = ComponentEntry(
        name=component_name,
        mode=mode,
        current_ma=current,
        voltage=voltage,
        duty_cycle_percent=duty_cycle,
        quantity=quantity
    )
    
    budget.components.append(entry)
    return True


def interactive_mode():
    """Run calculator in interactive mode"""
    print("=" * 60)
    print("Power Budget Calculator - Interactive Mode")
    print("=" * 60)
    print()
    
    project_name = input("Project name [My Project]: ").strip() or "My Project"
    voltage_str = input("System voltage (3.3/5.0) [3.3]: ").strip() or "3.3"
    
    try:
        voltage = float(voltage_str)
    except ValueError:
        voltage = 3.3
    
    budget = PowerBudget(project_name=project_name, system_voltage=voltage)
    
    print("\nAvailable components:")
    for i, name in enumerate(COMPONENT_DATABASE.keys(), 1):
        print(f"  {i:2}. {name}")
    
    print("\nEnter components (empty line to finish):")
    
    while True:
        comp_input = input("\nComponent name (or number): ").strip()
        if not comp_input:
            break
        
        # Handle numeric input
        if comp_input.isdigit():
            idx = int(comp_input) - 1
            names = list(COMPONENT_DATABASE.keys())
            if 0 <= idx < len(names):
                comp_input = names[idx]
            else:
                print("Invalid number")
                continue
        
        if comp_input not in COMPONENT_DATABASE:
            print(f"Unknown component: {comp_input}")
            continue
        
        # Show available modes
        modes = COMPONENT_DATABASE[comp_input]["modes"]
        typical = COMPONENT_DATABASE[comp_input].get("typical_mode", list(modes.keys())[0])
        print(f"  Available modes: {', '.join(modes.keys())}")
        
        mode = input(f"  Mode [{typical}]: ").strip() or typical
        duty_str = input("  Duty cycle % [100]: ").strip() or "100"
        qty_str = input("  Quantity [1]: ").strip() or "1"
        
        try:
            duty = float(duty_str)
            qty = int(qty_str)
        except ValueError:
            duty = 100.0
            qty = 1
        
        add_component_from_database(budget, comp_input, mode, duty, qty)
        print(f"  Added: {comp_input} ({mode}) @ {duty}% duty x{qty}")
    
    # Generate report
    print("\n" + "=" * 60)
    print(budget.to_markdown_report())
    
    # Save option
    save = input("\nSave report to file? (y/n) [n]: ").strip().lower()
    if save == 'y':
        filename = f"{project_name.replace(' ', '_')}_power_budget.md"
        with open(filename, 'w') as f:
            f.write(budget.to_markdown_report())
        print(f"Saved to: {filename}")
        
        # Also save JSON
        json_filename = f"{project_name.replace(' ', '_')}_power_budget.json"
        with open(json_filename, 'w') as f:
            f.write(budget.to_json())
        print(f"Saved to: {json_filename}")


def main():
    parser = argparse.ArgumentParser(description="Power Budget Calculator for Embedded Systems")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--json", "-j", type=str, help="Load configuration from JSON file")
    parser.add_argument("--component", "-c", type=str, help="Single component to calculate")
    parser.add_argument("--mode", "-m", type=str, help="Operating mode for component")
    parser.add_argument("--duty", "-d", type=float, default=100.0, help="Duty cycle percentage")
    parser.add_argument("--list", "-l", action="store_true", help="List all components")
    parser.add_argument("--output", "-o", type=str, help="Output file (json or md)")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available Components:")
        print("-" * 60)
        for name, data in COMPONENT_DATABASE.items():
            modes = ", ".join(data["modes"].keys())
            print(f"{name} ({data['voltage']}V): {modes}")
        print("\nAvailable Batteries:")
        print("-" * 60)
        for name, data in BATTERY_DATABASE.items():
            print(f"{name}: {data['capacity']}mAh @ {data['voltage']}V ({data['chemistry']})")
        return
    
    if args.interactive:
        interactive_mode()
        return
    
    if args.json:
        # Load from JSON
        with open(args.json, 'r') as f:
            config = json.load(f)
        
        budget = PowerBudget(
            project_name=config.get("project_name", "Loaded Project"),
            system_voltage=config.get("system_voltage", 3.3),
            safety_margin_percent=config.get("safety_margin_percent", 20.0)
        )
        
        for comp in config.get("components", []):
            if comp.get("name") in COMPONENT_DATABASE:
                add_component_from_database(
                    budget, 
                    comp["name"], 
                    comp.get("mode"),
                    comp.get("duty_cycle_percent", 100.0),
                    comp.get("quantity", 1)
                )
            else:
                # Custom component
                entry = ComponentEntry(
                    name=comp["name"],
                    mode=comp.get("mode", "custom"),
                    current_ma=comp.get("current_ma", 0),
                    voltage=comp.get("voltage", budget.system_voltage),
                    duty_cycle_percent=comp.get("duty_cycle_percent", 100.0),
                    quantity=comp.get("quantity", 1)
                )
                budget.components.append(entry)
        
        if args.output:
            if args.output.endswith('.json'):
                with open(args.output, 'w') as f:
                    f.write(budget.to_json())
            else:
                with open(args.output, 'w') as f:
                    f.write(budget.to_markdown_report())
            print(f"Output saved to: {args.output}")
        else:
            print(budget.to_markdown_report())
        return
    
    if args.component:
        budget = PowerBudget(project_name="Quick Calculation")
        add_component_from_database(budget, args.component, args.mode, args.duty)
        print(budget.to_json())
        return
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
