#!/usr/bin/env python3
"""Validate the cross-skill Arduino workflow contract."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
ROUTER = SKILLS_DIR / "arduino-workflow-router" / "SKILL.md"
CONTRACT = ROOT / "docs" / "arduino-skill-contract.md"
BOARD_PROFILE = ROOT / "docs" / "board-support" / "board-profile-template.md"
RECOVERY = SKILLS_DIR / "arduino-workflow-router" / "references" / "failure-recovery.md"
SECURITY = SKILLS_DIR / "arduino-workflow-router" / "references" / "connected-device-security.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def require_file(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")
        return ""
    return read(path)


def require_terms(label: str, content: str, terms: tuple[str, ...], errors: list[str]) -> None:
    missing = [term for term in terms if term.lower() not in content.lower()]
    if missing:
        errors.append(f"{label} missing: {', '.join(missing)}")


def main() -> int:
    errors: list[str] = []
    router = require_file(ROUTER, errors)
    contract = require_file(CONTRACT, errors)
    board_profile = require_file(BOARD_PROFILE, errors)
    recovery = require_file(RECOVERY, errors)
    security = require_file(SECURITY, errors)

    themes = {
        "universal toolchains": (
            router,
            ("Arduino IDE", "Arduino CLI", "PlatformIO", "vendor-specific"),
        ),
        "board and hardware intake": (
            board_profile,
            ("pins", "memory", "peripherals", "voltage", "current", "protocols"),
        ),
        "combined workflow routing": (
            router,
            ("load first", "combined workflow", "can be used together"),
        ),
        "lifecycle proof separation": (
            contract,
            ("build proof", "upload proof", "hardware proof", "system proof", "deployment proof"),
        ),
        "recovery guidance": (
            recovery,
            ("failed upload", "boot failure", "power fault", "corrupted firmware"),
        ),
        "security and maintenance": (
            security,
            ("secrets", "signed", "rollback", "dependency", "decommission"),
        ),
        "standard output": (
            contract,
            ("Assumptions", "Required tools", "Implementation steps", "Tests and evidence", "Known limitations"),
        ),
        "progressive disclosure": (
            router,
            ("references/", "under 500 lines", "load on demand"),
        ),
    }

    for label, (content, terms) in themes.items():
        require_terms(label, content, terms, errors)

    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        errors.append("no active skills found")
    for path in skill_files:
        content = read(path)
        if "arduino-skill-contract.md" not in content:
            errors.append(f"{path.relative_to(ROOT)} does not link arduino-skill-contract.md")
        if len(content.splitlines()) > 500:
            errors.append(f"{path.relative_to(ROOT)} exceeds 500 lines")

    if router and not all(
        (ROUTER.parent / reference).is_file()
        for reference in (
            "references/board-intake.md",
            "references/toolchain-selection.md",
            "references/failure-recovery.md",
            "references/connected-device-security.md",
        )
    ):
        errors.append("router references do not all resolve one level deep")

    passed = len(themes) - sum(
        1 for label, (content, terms) in themes.items()
        if any(term.lower() not in content.lower() for term in terms)
    )
    print(f"Review themes: {passed}/{len(themes)} passing")
    print(f"Active skills checked: {len(skill_files)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Contract validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("Contract validation complete: 8/8 themes passing, 0 errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
