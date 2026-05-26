#!/usr/bin/env python3
"""Validate repo skills against the current Agent Skills contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
ALLOWED_TOP_LEVEL_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
WARNING_LINE_LIMIT = 500
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_frontmatter(path: Path) -> tuple[list[str], list[tuple[str, str]], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []

    if len(lines) < 3 or lines[0].strip() != "---":
        return lines, [], ["missing opening frontmatter delimiter"]

    try:
        closing_index = lines[1:].index("---") + 1
    except ValueError:
        return lines, [], ["missing closing frontmatter delimiter"]

    frontmatter_lines = lines[1:closing_index]
    entries: list[tuple[str, str]] = []

    for raw_line in frontmatter_lines:
        if not raw_line.strip() or raw_line.startswith(" ") or raw_line.startswith("\t"):
            continue
        if ":" not in raw_line:
            errors.append(f"invalid frontmatter line: {raw_line}")
            continue
        key, value = raw_line.split(":", 1)
        entries.append((key.strip(), value.strip()))

    return lines, entries, errors


def validate_skill(path: Path) -> tuple[list[str], list[str]]:
    lines, entries, errors = load_frontmatter(path)
    warnings: list[str] = []
    entry_map: dict[str, str] = {}

    for key, value in entries:
        if key in entry_map:
            errors.append(f"duplicate top-level key: {key}")
        entry_map[key] = value

    for key in entry_map:
        if key not in ALLOWED_TOP_LEVEL_KEYS:
            errors.append(f"disallowed top-level key: {key}")

    name = entry_map.get("name", "").strip().strip('"').strip("'")
    description = entry_map.get("description", "").strip()

    if not name:
        errors.append("missing required key: name")
    else:
        if not NAME_PATTERN.fullmatch(name):
            errors.append("invalid name format")
        if name != path.parent.name:
            errors.append(
                f"name does not match directory: expected {path.parent.name}, found {name}"
            )
        if len(name) > 64:
            errors.append("name exceeds 64 characters")

    if not description:
        errors.append("missing required key: description")
    elif len(description) > 1024:
        errors.append("description exceeds 1024 characters")

    if len(lines) > WARNING_LINE_LIMIT:
        warnings.append(
            f"SKILL.md exceeds recommended {WARNING_LINE_LIMIT} lines: {len(lines)}"
        )

    return errors, warnings


def main() -> int:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print("No skill files found.", file=sys.stderr)
        return 1

    total_errors = 0
    total_warnings = 0

    for path in skill_files:
        rel_path = path.relative_to(ROOT)
        errors, warnings = validate_skill(path)
        if not errors and not warnings:
            print(f"OK      {rel_path}")
            continue
        for message in errors:
            total_errors += 1
            print(f"ERROR   {rel_path}: {message}")
        for message in warnings:
            total_warnings += 1
            print(f"WARNING {rel_path}: {message}")

    if total_errors == 0:
        print(
            f"Validation complete: {len(skill_files)} skills checked, "
            f"{total_warnings} warnings, 0 errors."
        )
        return 0

    print(
        f"Validation failed: {len(skill_files)} skills checked, "
        f"{total_warnings} warnings, {total_errors} errors.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
