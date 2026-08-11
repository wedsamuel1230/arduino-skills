#!/usr/bin/env python3
"""Validate the discoverable, source-backed Arduino board reference set."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
BOARD_DIR = ROOT / "references" / "boards"
INDEX = BOARD_DIR / "index.json"
URL_RE = re.compile(r"https://[^) \t\r\n>]+")
REQUIRED_HEADINGS = ("## Sources", "## Fact-to-source map")
REQUIRED_TERMS = ("Logic", "PWM", "ADC", "Memory", "current", "Default")
OFFICIAL_HOSTS = (
    "docs.arduino.cc",
    "microchip.com",
    "ww1.microchip.com",
    "espressif.com",
    "docs.espressif.com",
    "github.com",
    "raspberrypi.com",
    "datasheets.raspberrypi.com",
)
OFFICIAL_GITHUB_PREFIXES = (
    "/arduino/",
    "/espressif/",
    "/earlephilhower/",
)


def official_url(url: str) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc.lower().split(":", 1)[0]
    if host == "github.com":
        return parsed.scheme == "https" and parsed.path.startswith(OFFICIAL_GITHUB_PREFIXES)
    return parsed.scheme == "https" and any(
        host == allowed or host.endswith("." + allowed) for allowed in OFFICIAL_HOSTS
    )


def collect_errors(root: Path = ROOT) -> tuple[list[str], int]:
    board_dir = root / "references" / "boards"
    index_path = board_dir / "index.json"
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return ["missing board index: references/boards/index.json"], 0
    except json.JSONDecodeError as exc:
        return [f"invalid board index JSON: {exc}"], 0
    if not isinstance(index, dict):
        return ["board index must be a JSON object"], 0

    profiles = index.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        return ["board index profiles must be a non-empty list"], 0

    errors: list[str] = []
    ids: set[str] = set()
    paths: set[str] = set()
    names: set[str] = set()
    ledger = board_dir / "source-ledger.md"
    ledger_text = ledger.read_text(encoding="utf-8") if ledger.is_file() else ""

    for entry in profiles:
        if not isinstance(entry, dict):
            errors.append("every board index profile must be an object")
            continue
        for field in ("id", "name", "path", "ledger_label", "status", "frameworks", "sources"):
            if field not in entry or not entry[field]:
                errors.append(f"board index entry missing {field}")
        profile_id = entry.get("id")
        name = entry.get("name")
        relative_path = entry.get("path")
        if isinstance(profile_id, str):
            if profile_id in ids:
                errors.append(f"duplicate board profile id: {profile_id}")
            ids.add(profile_id)
        if isinstance(name, str):
            if name in names:
                errors.append(f"duplicate board profile name: {name}")
            names.add(name)
        if not isinstance(relative_path, str):
            continue
        if relative_path in paths:
            errors.append(f"duplicate board profile path: {relative_path}")
        paths.add(relative_path)
        profile_path = (board_dir / relative_path).resolve()
        if profile_path.parent != board_dir.resolve():
            errors.append(f"board profile escapes references/boards: {relative_path}")
            continue
        if not profile_path.is_file():
            errors.append(f"missing board profile: references/boards/{relative_path}")
            continue
        content = profile_path.read_text(encoding="utf-8")
        if not re.search(r"^## .*\bprofile\b", content, re.IGNORECASE | re.MULTILINE):
            errors.append(f"{relative_path}: missing a profile heading")
        for heading in REQUIRED_HEADINGS:
            if heading not in content:
                errors.append(f"{relative_path}: missing {heading}")
        for term in REQUIRED_TERMS:
            if term.lower() not in content.lower():
                errors.append(f"{relative_path}: missing required fact field {term}")
        if "Source status:" not in content:
            errors.append(f"{relative_path}: missing Source status")
        if not re.search(r"\|\s*Fact group\s*\|", content):
            errors.append(f"{relative_path}: missing fact-to-source table")
        if not re.search(r"\b(gap|unknown|verify|unverified)\b", content, re.IGNORECASE):
            errors.append(f"{relative_path}: missing explicit source or hardware gap")

        urls = sorted(set(URL_RE.findall(content)))
        if len(urls) < 2:
            errors.append(f"{relative_path}: fewer than two source URLs")
        for url in urls:
            if not official_url(url):
                errors.append(f"{relative_path}: non-primary or unsupported source host: {url}")
        indexed_sources = entry.get("sources")
        if isinstance(indexed_sources, list):
            for url in indexed_sources:
                if not isinstance(url, str) or url not in content:
                    errors.append(f"{relative_path}: indexed source missing from profile: {url}")
                elif not official_url(url):
                    errors.append(f"{relative_path}: indexed source is not official: {url}")
        else:
            errors.append(f"{relative_path}: sources must be a list")
        if entry.get("status") != "source-backed":
            errors.append(f"{relative_path}: status must be source-backed for this index")
        frameworks = entry.get("frameworks")
        if not isinstance(frameworks, list) or not all(isinstance(item, str) for item in frameworks):
            errors.append(f"{relative_path}: frameworks must be a list of strings")
        label = entry.get("ledger_label")
        if isinstance(label, str) and label not in ledger_text:
            errors.append(f"source ledger missing profile row: {label}")

    discovered = sorted(
        path.name
        for path in board_dir.glob("*.md")
        if path.name not in {"README.md", "source-ledger.md"}
    )
    indexed = sorted(paths)
    if discovered != indexed:
        errors.append(
            "board index does not cover every profile file: "
            f"discovered={discovered}, indexed={indexed}"
        )
    return errors, len(profiles)


def main() -> int:
    errors, profile_count = collect_errors()
    result = {
        "profiles_checked": profile_count,
        "errors": errors,
        "passed": not errors,
    }
    print(json.dumps(result, indent=2))
    if errors:
        print(f"Board reference validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Board reference validation passed: {profile_count} profiles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
