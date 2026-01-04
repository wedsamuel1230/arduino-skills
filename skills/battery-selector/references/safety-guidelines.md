# Battery Safety Guidelines for Makers

## Chemistry-Specific Safety

### Lithium Polymer (LiPo)
**Risk Level: HIGH - Handle with care**

1. **Never** puncture, crush, or deform the pouch
2. **Never** charge above 4.2V per cell
3. **Never** discharge below 3.0V per cell (3.2V recommended)
4. **Never** charge unattended or overnight
5. **Always** use a proper balance charger
6. **Store** at ~3.8V (storage voltage) if not using for weeks
7. **Dispose** of puffy/swollen batteries immediately (fire hazard)

**Charging Requirements:**
- CC/CV (Constant Current / Constant Voltage) charger required
- Charge rate: 0.5C to 1C maximum (1C = capacity in mAh as current)
- Example: 1000mAh battery → max 1A charge current
- Recommended ICs: TP4056, MCP73831, BQ24072

### Lithium-Ion (18650, etc.)
**Risk Level: MEDIUM-HIGH**

1. Use cells with built-in protection circuit (PCB/BMS)
2. Never short-circuit terminals
3. Respect temperature limits during charging (0-45°C typical)
4. Use battery holder with proper polarity protection
5. Protected cells are ~2-3mm longer than unprotected

**Charging Requirements:**
- Similar to LiPo: CC/CV at 4.2V cutoff
- Charge rate: 0.5C standard, 1C fast charge
- Same charger ICs work: TP4056, MCP73831

### LiFePO4 (Lithium Iron Phosphate)
**Risk Level: LOW-MEDIUM - Safest lithium chemistry**

1. Different voltage: 3.2V nominal, 3.6V max, 2.5V cutoff
2. More tolerant of abuse than Li-ion/LiPo
3. No thermal runaway risk
4. Requires LiFePO4-specific charger (NOT Li-ion charger!)
5. Excellent cycle life (2000+ cycles)

**Charging Requirements:**
- CC/CV at 3.6V cutoff (not 4.2V!)
- Dedicated IC: CN3058E or similar LiFePO4 charger
- Can use TP5000 with proper configuration

### NiMH (Nickel Metal Hydride)
**Risk Level: LOW**

1. Can handle overcharge better than lithium
2. Use -ΔV detection chargers for fast charge
3. Trickle charge at C/10 to C/20
4. Self-discharge varies by type (Eneloop = low, standard = high)
5. No fire/explosion risk

**Charging Requirements:**
- Delta-V detection for fast charge
- Timer backup recommended
- Simple trickle charge at C/10 acceptable
- Can parallel cells directly

### Alkaline (Non-rechargeable)
**Risk Level: VERY LOW**

1. Do NOT attempt to recharge (can leak/burst)
2. Remove from device if not using for extended period
3. Check for leaks before handling old batteries
4. Dispose properly - some recycling programs accept

## Protection Circuit Design

### Essential Components for Lithium:

```
Battery Protection PCB Functions:
├── Overcharge Protection (OVP)
│   └── Disconnect at 4.25V-4.35V
├── Overdischarge Protection (UVP)
│   └── Disconnect at 2.4V-3.0V
├── Overcurrent Protection (OCP)
│   └── Disconnect at defined current limit
├── Short Circuit Protection (SCP)
│   └── Immediate disconnect
└── Temperature Protection (OTP)
    └── Optional but recommended
```

### Recommended Protection ICs:

| IC | Features | Cost |
|----|----------|------|
| DW01A | OVP, UVP, OCP, SCP | $0.05 |
| FS312F-G | Same + better UVP threshold | $0.08 |
| S8261 | Higher current capability | $0.10 |
| BQ2970 | Integrated with balancing | $0.50 |

### Schematic Pattern:

```
[Battery +] ─── [Protection IC] ─── [MOSFET] ─── [Output +]
                      │
[Battery -] ─────────┴──────────────────────── [Output -]
```

## Charging System Design

### Single Cell LiPo/Li-ion (TP4056):

```
USB 5V ──► TP4056 Module ──► LiPo Battery
               │                  │
           [CHRG LED]        [Protection]
           [DONE LED]
```

**TP4056 Module Pinout:**
- IN+, IN-: 5V input
- BAT+, BAT-: Battery connection
- OUT+, OUT-: Load output (with protection)

### Solar Charging:

```
Solar Panel ──► CN3065 ──► LiPo ──► Load
    │             │
 [MPPT]       [CC/CV]
```

**Key Parameters:**
- Panel voltage: ~6V for 5V charging
- CN3065 handles MPPT and charging
- Add blocking diode for reverse protection

## Temperature Considerations

### Charging Temperature Limits:
| Chemistry | Min Charge | Max Charge |
|-----------|------------|------------|
| LiPo      | 0°C        | 45°C       |
| Li-ion    | 0°C        | 45°C       |
| LiFePO4   | 0°C        | 45°C       |
| NiMH      | 0°C        | 40°C       |

### Discharge Temperature Limits:
| Chemistry | Min Discharge | Max Discharge |
|-----------|---------------|---------------|
| LiPo      | -20°C         | 60°C          |
| Li-ion    | -20°C         | 60°C          |
| LiFePO4   | -20°C         | 60°C          |
| NiMH      | -20°C         | 50°C          |

**Cold Weather Charging:**
- NEVER charge lithium batteries below 0°C
- Internal damage causes lithium plating
- Pre-warm battery before charging in cold

## Storage Guidelines

### Long-term Storage:

| Chemistry | Storage Voltage | Storage State |
|-----------|-----------------|---------------|
| LiPo/Li-ion | 3.7-3.8V | ~40% charge |
| LiFePO4 | 3.2-3.3V | ~50% charge |
| NiMH | Any | Periodic top-up |
| Alkaline | N/A | Cool, dry place |

### Storage Environment:
- Temperature: 15-25°C ideal
- Humidity: <50% RH
- Away from metal objects
- In fireproof container for LiPo
- Check monthly for swelling/damage

## Emergency Procedures

### LiPo Fire:
1. Do NOT use water
2. Use sand or dry chemical extinguisher (Class D)
3. Ventilate area (toxic fumes)
4. Let battery burn out if safe to do so
5. Cool surrounding area to prevent spread

### Battery Leak (Alkaline/NiMH):
1. Wear gloves - alkaline electrolyte is caustic
2. Neutralize with vinegar (for alkaline)
3. Clean area thoroughly
4. Dispose of battery properly

### Swollen LiPo:
1. Do NOT puncture
2. Place in fireproof container outdoors
3. Discharge to 0V using resistor (if safe)
4. Take to battery recycling center
5. Never dispose in regular trash

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                  BATTERY QUICK REFERENCE                │
├─────────────────────────────────────────────────────────┤
│  LiPo/Li-ion: 3.7V nom, 4.2V max, 3.0V min, CC/CV     │
│  LiFePO4:     3.2V nom, 3.6V max, 2.5V min, CC/CV     │
│  NiMH:        1.2V nom, 1.4V max, 1.0V min, -ΔV       │
│  Alkaline:    1.5V nom, (non-rechargeable)             │
├─────────────────────────────────────────────────────────┤
│  ⚠️  Never charge lithium below 0°C                    │
│  ⚠️  Never leave lithium charging unattended           │
│  ⚠️  Dispose of puffy batteries immediately            │
│  ⚠️  Use protection circuits on all lithium cells      │
└─────────────────────────────────────────────────────────┘
```
