#!/usr/bin/env python3
"""
Battery Selector - Compare battery chemistries and find optimal choice

Analyzes project requirements and recommends suitable batteries based on:
- Capacity and runtime
- Size/weight constraints
- Temperature range
- Rechargeability requirements
- Cost optimization

Usage:
    uv run compare_batteries.py --interactive
    uv run compare_batteries.py --current 50 --hours 24 --rechargeable
    uv run compare_batteries.py --project weather_station
"""

import argparse
import json
from dataclasses import dataclass
from typing import List, Optional

# =============================================================================
# Battery Database
# =============================================================================

BATTERY_DATABASE = {
    # Alkaline Primary Cells
    "AA_Alkaline": {
        "chemistry": "Alkaline",
        "voltage_nominal": 1.5,
        "voltage_cutoff": 0.9,
        "capacity_mah": 2500,
        "energy_wh": 3.75,
        "weight_g": 23,
        "dimensions_mm": {"diameter": 14.5, "length": 50.5},
        "temp_range_c": (-20, 55),
        "rechargeable": False,
        "cycle_life": 1,
        "self_discharge_monthly_pct": 2,
        "cost_usd": 0.50,
        "pros": ["Widely available", "Long shelf life", "Low cost"],
        "cons": ["Not rechargeable", "Voltage drops under load", "Poor at cold temps"]
    },
    "AAA_Alkaline": {
        "chemistry": "Alkaline",
        "voltage_nominal": 1.5,
        "voltage_cutoff": 0.9,
        "capacity_mah": 1000,
        "energy_wh": 1.5,
        "weight_g": 11.5,
        "dimensions_mm": {"diameter": 10.5, "length": 44.5},
        "temp_range_c": (-20, 55),
        "rechargeable": False,
        "cycle_life": 1,
        "self_discharge_monthly_pct": 2,
        "cost_usd": 0.40,
        "pros": ["Compact", "Cheap"],
        "cons": ["Limited capacity", "Not rechargeable"]
    },
    "9V_Alkaline": {
        "chemistry": "Alkaline",
        "voltage_nominal": 9.0,
        "voltage_cutoff": 6.0,
        "capacity_mah": 550,
        "energy_wh": 4.95,
        "weight_g": 46,
        "dimensions_mm": {"width": 26.5, "height": 48.5, "depth": 17.5},
        "temp_range_c": (-20, 55),
        "rechargeable": False,
        "cycle_life": 1,
        "self_discharge_monthly_pct": 2,
        "cost_usd": 3.00,
        "pros": ["High voltage, simple power design"],
        "cons": ["Very low capacity", "Expensive per Wh"]
    },
    "CR2032": {
        "chemistry": "Lithium Primary",
        "voltage_nominal": 3.0,
        "voltage_cutoff": 2.0,
        "capacity_mah": 220,
        "energy_wh": 0.66,
        "weight_g": 3,
        "dimensions_mm": {"diameter": 20, "height": 3.2},
        "temp_range_c": (-30, 60),
        "rechargeable": False,
        "cycle_life": 1,
        "self_discharge_monthly_pct": 1,
        "cost_usd": 0.30,
        "pros": ["Very compact", "Long shelf life", "Wide temp range"],
        "cons": ["Very low capacity", "Max ~3mA continuous"]
    },
    
    # NiMH Rechargeable
    "AA_NiMH_2000": {
        "chemistry": "NiMH",
        "voltage_nominal": 1.2,
        "voltage_cutoff": 1.0,
        "capacity_mah": 2000,
        "energy_wh": 2.4,
        "weight_g": 28,
        "dimensions_mm": {"diameter": 14.5, "length": 50.5},
        "temp_range_c": (0, 40),
        "rechargeable": True,
        "cycle_life": 500,
        "self_discharge_monthly_pct": 20,
        "cost_usd": 3.00,
        "pros": ["Rechargeable", "High discharge rate", "No memory effect"],
        "cons": ["High self-discharge", "Lower voltage than alkaline"]
    },
    "AA_NiMH_Eneloop": {
        "chemistry": "NiMH Low Self-Discharge",
        "voltage_nominal": 1.2,
        "voltage_cutoff": 1.0,
        "capacity_mah": 1900,
        "energy_wh": 2.28,
        "weight_g": 27,
        "dimensions_mm": {"diameter": 14.5, "length": 50.5},
        "temp_range_c": (-20, 50),
        "rechargeable": True,
        "cycle_life": 2100,
        "self_discharge_monthly_pct": 1,
        "cost_usd": 4.00,
        "pros": ["Low self-discharge", "Long cycle life", "Good cold performance"],
        "cons": ["Premium price", "Slightly lower capacity"]
    },
    
    # Lithium-ion / LiPo
    "18650_3000": {
        "chemistry": "Li-ion",
        "voltage_nominal": 3.7,
        "voltage_cutoff": 3.0,
        "capacity_mah": 3000,
        "energy_wh": 11.1,
        "weight_g": 48,
        "dimensions_mm": {"diameter": 18.6, "length": 65.2},
        "temp_range_c": (-20, 60),
        "rechargeable": True,
        "cycle_life": 500,
        "self_discharge_monthly_pct": 3,
        "cost_usd": 5.00,
        "pros": ["High energy density", "High discharge rate", "Common"],
        "cons": ["Requires protection circuit", "Needs proper charger"]
    },
    "18650_3500": {
        "chemistry": "Li-ion",
        "voltage_nominal": 3.7,
        "voltage_cutoff": 3.0,
        "capacity_mah": 3500,
        "energy_wh": 12.95,
        "weight_g": 50,
        "dimensions_mm": {"diameter": 18.6, "length": 65.2},
        "temp_range_c": (-20, 60),
        "rechargeable": True,
        "cycle_life": 500,
        "self_discharge_monthly_pct": 3,
        "cost_usd": 8.00,
        "pros": ["Highest capacity 18650", "High energy density"],
        "cons": ["Lower max discharge than 3000mAh", "More expensive"]
    },
    "LiPo_500": {
        "chemistry": "LiPo",
        "voltage_nominal": 3.7,
        "voltage_cutoff": 3.2,
        "capacity_mah": 500,
        "energy_wh": 1.85,
        "weight_g": 12,
        "dimensions_mm": {"width": 30, "height": 40, "thickness": 4},
        "temp_range_c": (0, 45),
        "rechargeable": True,
        "cycle_life": 300,
        "self_discharge_monthly_pct": 3,
        "cost_usd": 4.00,
        "pros": ["Very thin", "Flexible form factor", "Light"],
        "cons": ["Fragile", "Fire risk if punctured", "Puff with age"]
    },
    "LiPo_1000": {
        "chemistry": "LiPo",
        "voltage_nominal": 3.7,
        "voltage_cutoff": 3.2,
        "capacity_mah": 1000,
        "energy_wh": 3.7,
        "weight_g": 22,
        "dimensions_mm": {"width": 34, "height": 50, "thickness": 5},
        "temp_range_c": (0, 45),
        "rechargeable": True,
        "cycle_life": 300,
        "self_discharge_monthly_pct": 3,
        "cost_usd": 6.00,
        "pros": ["Good balance of capacity and size"],
        "cons": ["Requires careful handling"]
    },
    "LiPo_2000": {
        "chemistry": "LiPo",
        "voltage_nominal": 3.7,
        "voltage_cutoff": 3.2,
        "capacity_mah": 2000,
        "energy_wh": 7.4,
        "weight_g": 40,
        "dimensions_mm": {"width": 40, "height": 60, "thickness": 7},
        "temp_range_c": (0, 45),
        "rechargeable": True,
        "cycle_life": 300,
        "self_discharge_monthly_pct": 3,
        "cost_usd": 10.00,
        "pros": ["Good capacity for wearables/portables"],
        "cons": ["More expensive"]
    },
    
    # LiFePO4
    "LiFePO4_1500": {
        "chemistry": "LiFePO4",
        "voltage_nominal": 3.2,
        "voltage_cutoff": 2.5,
        "capacity_mah": 1500,
        "energy_wh": 4.8,
        "weight_g": 42,
        "dimensions_mm": {"diameter": 18.5, "length": 65},
        "temp_range_c": (-20, 60),
        "rechargeable": True,
        "cycle_life": 2000,
        "self_discharge_monthly_pct": 2,
        "cost_usd": 8.00,
        "pros": ["Very long cycle life", "Safer than Li-ion", "Wide temp range"],
        "cons": ["Lower energy density", "3.2V may need boost converter"]
    },
    "LiFePO4_3000": {
        "chemistry": "LiFePO4",
        "voltage_nominal": 3.2,
        "voltage_cutoff": 2.5,
        "capacity_mah": 3000,
        "energy_wh": 9.6,
        "weight_g": 80,
        "dimensions_mm": {"diameter": 26, "length": 65},
        "temp_range_c": (-20, 60),
        "rechargeable": True,
        "cycle_life": 2000,
        "self_discharge_monthly_pct": 2,
        "cost_usd": 12.00,
        "pros": ["High capacity + long life", "Safe chemistry"],
        "cons": ["Larger form factor"]
    }
}


@dataclass
class ProjectRequirements:
    """Project power requirements"""
    average_current_ma: float
    peak_current_ma: Optional[float] = None
    target_runtime_hours: float = 24
    min_voltage: float = 3.0
    max_voltage: float = 5.0
    rechargeable_required: bool = False
    max_weight_g: Optional[float] = None
    max_volume_cc: Optional[float] = None
    min_temp_c: float = 0
    max_temp_c: float = 40
    max_cost_usd: Optional[float] = None
    cycle_count_target: int = 1


def calculate_runtime(battery: dict, current_ma: float) -> float:
    """Calculate runtime in hours, accounting for Peukert effect"""
    capacity = battery["capacity_mah"]
    
    # Simple Peukert approximation
    c_rate = current_ma / capacity
    if c_rate > 1.0:
        effective_capacity = capacity * 0.6  # High drain penalty
    elif c_rate > 0.5:
        effective_capacity = capacity * 0.8
    elif c_rate > 0.2:
        effective_capacity = capacity * 0.9
    else:
        effective_capacity = capacity * 0.95
    
    return effective_capacity / current_ma if current_ma > 0 else float('inf')


def calculate_volume(dims: dict) -> float:
    """Calculate volume in cc from dimensions"""
    if "diameter" in dims:
        # Cylindrical
        r = dims["diameter"] / 2 / 10  # mm to cm
        h = dims.get("length", dims.get("height", 0)) / 10
        return 3.14159 * r * r * h
    else:
        # Rectangular
        w = dims.get("width", 0) / 10
        h = dims.get("height", 0) / 10
        d = dims.get("depth", dims.get("thickness", 0)) / 10
        return w * h * d


def evaluate_battery(battery_name: str, battery: dict, req: ProjectRequirements) -> dict:
    """Evaluate a battery against requirements"""
    result = {
        "name": battery_name,
        "chemistry": battery["chemistry"],
        "voltage": battery["voltage_nominal"],
        "capacity_mah": battery["capacity_mah"],
        "energy_wh": battery["energy_wh"],
        "score": 100,
        "issues": [],
        "suitable": True
    }
    
    # Voltage check
    if battery["voltage_nominal"] < req.min_voltage:
        result["issues"].append(f"Voltage too low ({battery['voltage_nominal']}V < {req.min_voltage}V)")
        result["score"] -= 50
    if battery["voltage_nominal"] > req.max_voltage:
        result["issues"].append(f"Voltage too high ({battery['voltage_nominal']}V > {req.max_voltage}V)")
        result["score"] -= 30
    
    # Runtime check
    runtime = calculate_runtime(battery, req.average_current_ma)
    result["runtime_hours"] = round(runtime, 2)
    
    if runtime < req.target_runtime_hours:
        deficit_pct = (1 - runtime / req.target_runtime_hours) * 100
        result["issues"].append(f"Runtime {runtime:.1f}h < target {req.target_runtime_hours}h ({deficit_pct:.0f}% short)")
        result["score"] -= min(50, deficit_pct / 2)
    else:
        bonus = min(20, (runtime / req.target_runtime_hours - 1) * 10)
        result["score"] += bonus
    
    # Rechargeable check
    if req.rechargeable_required and not battery["rechargeable"]:
        result["issues"].append("Not rechargeable (required)")
        result["score"] -= 100
        result["suitable"] = False
    
    # Cycle life check
    if battery["cycle_life"] < req.cycle_count_target:
        result["issues"].append(f"Cycle life {battery['cycle_life']} < required {req.cycle_count_target}")
        result["score"] -= 30
    
    # Weight check
    if req.max_weight_g and battery["weight_g"] > req.max_weight_g:
        result["issues"].append(f"Too heavy ({battery['weight_g']}g > {req.max_weight_g}g)")
        result["score"] -= 20
    
    # Volume check
    volume = calculate_volume(battery["dimensions_mm"])
    result["volume_cc"] = round(volume, 2)
    if req.max_volume_cc and volume > req.max_volume_cc:
        result["issues"].append(f"Too large ({volume:.1f}cc > {req.max_volume_cc}cc)")
        result["score"] -= 20
    
    # Temperature check
    temp_range = battery["temp_range_c"]
    if req.min_temp_c < temp_range[0]:
        result["issues"].append(f"Cold temp limit {temp_range[0]}°C > required {req.min_temp_c}°C")
        result["score"] -= 20
    if req.max_temp_c > temp_range[1]:
        result["issues"].append(f"Hot temp limit {temp_range[1]}°C < required {req.max_temp_c}°C")
        result["score"] -= 20
    
    # Cost check
    if req.max_cost_usd and battery["cost_usd"] > req.max_cost_usd:
        result["issues"].append(f"Cost ${battery['cost_usd']:.2f} > budget ${req.max_cost_usd:.2f}")
        result["score"] -= 15
    
    # Peak current check (LiPo/Li-ion can handle high peaks, coin cells cannot)
    if req.peak_current_ma:
        if battery["chemistry"] == "Lithium Primary" and req.peak_current_ma > 5:
            result["issues"].append(f"Coin cell can't handle {req.peak_current_ma}mA peaks")
            result["score"] -= 40
    
    result["cost_per_wh"] = round(battery["cost_usd"] / battery["energy_wh"], 3)
    result["wh_per_g"] = round(battery["energy_wh"] / battery["weight_g"], 4)
    
    if result["score"] < 0:
        result["suitable"] = False
    
    return result


def find_best_batteries(req: ProjectRequirements, top_n: int = 5) -> List[dict]:
    """Find the best batteries for the requirements"""
    results = []
    
    for name, battery in BATTERY_DATABASE.items():
        result = evaluate_battery(name, battery, req)
        results.append(result)
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results[:top_n]


def generate_comparison_table(results: List[dict]) -> str:
    """Generate markdown comparison table"""
    lines = [
        "| Battery | Chemistry | Voltage | Runtime (h) | Score | Issues |",
        "|---------|-----------|---------|-------------|-------|--------|"
    ]
    
    for r in results:
        issues = "; ".join(r["issues"][:2]) if r["issues"] else "✓ Meets requirements"
        status = "✓" if r["suitable"] else "✗"
        lines.append(
            f"| {r['name']} | {r['chemistry']} | {r['voltage']}V | "
            f"{r['runtime_hours']:.1f} | {r['score']:.0f} {status} | {issues} |"
        )
    
    return "\n".join(lines)


def generate_report(req: ProjectRequirements, results: List[dict]) -> str:
    """Generate full battery selection report"""
    lines = [
        "# Battery Selection Report",
        "",
        "## Requirements",
        f"- Average Current: {req.average_current_ma} mA",
        f"- Target Runtime: {req.target_runtime_hours} hours",
        f"- Voltage Range: {req.min_voltage}V - {req.max_voltage}V",
        f"- Rechargeable: {'Required' if req.rechargeable_required else 'Optional'}",
        f"- Temperature Range: {req.min_temp_c}°C to {req.max_temp_c}°C",
        "",
        "## Top Recommendations",
        "",
        generate_comparison_table(results),
        ""
    ]
    
    # Detailed analysis of top choice
    if results and results[0]["suitable"]:
        top = results[0]
        battery = BATTERY_DATABASE[top["name"]]
        lines.extend([
            f"## Recommended: {top['name']}",
            "",
            f"**Chemistry:** {top['chemistry']}",
            f"**Nominal Voltage:** {top['voltage']}V",
            f"**Capacity:** {top['capacity_mah']} mAh ({battery['energy_wh']} Wh)",
            f"**Expected Runtime:** {top['runtime_hours']:.1f} hours",
            f"**Weight:** {battery['weight_g']}g",
            f"**Cost:** ${battery['cost_usd']:.2f}",
            "",
            "**Pros:**",
        ])
        for pro in battery.get("pros", []):
            lines.append(f"- {pro}")
        
        lines.append("")
        lines.append("**Cons:**")
        for con in battery.get("cons", []):
            lines.append(f"- {con}")
    
    return "\n".join(lines)


def interactive_mode():
    """Run battery selector interactively"""
    print("=" * 60)
    print("Battery Selector - Interactive Mode")
    print("=" * 60)
    print()
    
    current = float(input("Average current draw (mA): "))
    peak = input("Peak current (mA) [optional]: ").strip()
    peak = float(peak) if peak else None
    
    runtime = float(input("Target runtime (hours) [24]: ").strip() or "24")
    
    min_v = float(input("Minimum voltage required (V) [3.0]: ").strip() or "3.0")
    max_v = float(input("Maximum voltage (V) [5.0]: ").strip() or "5.0")
    
    rechargeable = input("Rechargeable required? (y/n) [n]: ").strip().lower() == 'y'
    
    weight = input("Max weight (g) [optional]: ").strip()
    weight = float(weight) if weight else None
    
    min_temp = float(input("Min operating temp (°C) [0]: ").strip() or "0")
    max_temp = float(input("Max operating temp (°C) [40]: ").strip() or "40")
    
    budget = input("Max cost ($) [optional]: ").strip()
    budget = float(budget) if budget else None
    
    req = ProjectRequirements(
        average_current_ma=current,
        peak_current_ma=peak,
        target_runtime_hours=runtime,
        min_voltage=min_v,
        max_voltage=max_v,
        rechargeable_required=rechargeable,
        max_weight_g=weight,
        min_temp_c=min_temp,
        max_temp_c=max_temp,
        max_cost_usd=budget
    )
    
    results = find_best_batteries(req)
    report = generate_report(req, results)
    
    print("\n" + "=" * 60)
    print(report)
    
    # Save option
    save = input("\nSave report? (y/n) [n]: ").strip().lower()
    if save == 'y':
        filename = "battery_selection_report.md"
        with open(filename, 'w') as f:
            f.write(report)
        print(f"Saved to: {filename}")


def main():
    parser = argparse.ArgumentParser(description="Battery Selector for Embedded Projects")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--current", "-c", type=float, help="Average current (mA)")
    parser.add_argument("--hours", "-t", type=float, default=24, help="Target runtime (hours)")
    parser.add_argument("--rechargeable", "-r", action="store_true", help="Require rechargeable")
    parser.add_argument("--min-voltage", type=float, default=3.0, help="Min voltage")
    parser.add_argument("--max-voltage", type=float, default=5.0, help="Max voltage")
    parser.add_argument("--list", "-l", action="store_true", help="List all batteries")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.list:
        print("Battery Database:")
        print("-" * 80)
        for name, b in BATTERY_DATABASE.items():
            print(f"{name:20} {b['chemistry']:15} {b['voltage_nominal']}V "
                  f"{b['capacity_mah']:5}mAh ${b['cost_usd']:.2f}")
        return
    
    if args.interactive:
        interactive_mode()
        return
    
    if args.current:
        req = ProjectRequirements(
            average_current_ma=args.current,
            target_runtime_hours=args.hours,
            min_voltage=args.min_voltage,
            max_voltage=args.max_voltage,
            rechargeable_required=args.rechargeable
        )
        
        results = find_best_batteries(req)
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(generate_report(req, results))
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
