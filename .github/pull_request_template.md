## Description

<!-- Describe what this PR accomplishes -->

## Type of Change

- [ ] 🎓 New Skill 
- [ ] 🐛 Bug fix
- [ ] 📝 Documentation improvement
- [ ] 🔧 Infrastructure/tooling
- [ ] 🚀 Performance improvement

## For New Skills Only

**Skill Name:** 
**Category:** `arduino` | `maker` | `project-builder`
**Platforms:** Arduino UNO | ESP32 | RP2040

### Pre-Submission Checklist

#### Code Quality
- [ ] Code compiles without warnings (Arduino IDE or PlatformIO)
- [ ] Uses `unsigned long` for millis() timing
- [ ] Bounds checking on all arrays
- [ ] F() macro for string constants on UNO
- [ ] No hardcoded pins (uses config.h pattern)
- [ ] Memory-safe (no buffer overflows)

#### Documentation
- [ ] SKILL.md has complete YAML frontmatter
- [ ] All required sections present (Overview, Core Principles, Implementation, Verification, etc.)
- [ ] Code examples include explanatory comments
- [ ] Verification steps show ✅ and ❌ examples
- [ ] At least 2 advanced patterns documented
- [ ] References to related skills included

#### Testing
- [ ] Tested on Arduino UNO (or limitation documented)
- [ ] Tested on ESP32 (or limitation documented)
- [ ] Tested on RP2040 (or limitation documented)
- [ ] Platform support clearly marked in SKILL.md

#### Scripts (if applicable)
- [ ] Uses PEP 723 inline dependencies (no requirements.txt)
- [ ] Runs with `uv run script.py` or `python script.py`
- [ ] Has `--help` output
- [ ] Generated code compiles successfully

### Design Review

**Problem Solved:**
<!-- What problem does this skill address? -->

**Implementation Approach:**
<!-- Why did you choose this design? What trade-offs exist? -->

**Verification Approach:**
<!-- How should users verify this skill works? -->

## For Non-Skill Changes

- [ ] Changes follow existing patterns
- [ ] Documentation updated (if applicable)
- [ ] No breaking changes introduced
- [ ] Changelog entry added (if applicable)

## Testing

<!-- Describe testing performed -->
- [ ] Tested locally
- [ ] No regressions observed
- [ ] Existing skills still work

## Additional Context

<!-- Add any other context (diagrams, references, related issues) -->

---

**Thank you for contributing to Arduino Skills!** 🚀
