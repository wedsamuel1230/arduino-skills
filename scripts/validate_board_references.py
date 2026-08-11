#!/usr/bin/env python3
"""Validate the discoverable, source-backed Arduino board reference set."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from resolve_board_profile import normalize_query


ROOT = Path(__file__).resolve().parents[1]
BOARD_DIR = ROOT / "references" / "boards"
INDEX = BOARD_DIR / "index.json"
URL_RE = re.compile(r"https://[^) \t\r\n>]+")
REQUIRED_HEADINGS = ("## Sources", "## Fact-to-source map")
REQUIRED_TERMS = ("Logic", "PWM", "ADC", "Memory", "current", "Default")
REQUIRED_INDEX_FIELDS = (
    "aliases",
    "mcu",
    "architecture",
    "logic_level",
    "capability_tags",
    "risk_tags",
    "identity_scope",
    "identity_contract",
    "toolchains",
    "evidence",
)
REQUIRED_EVIDENCE_FIELDS = ("source_confidence", "checked", "physical_status")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
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
    if index.get("schema_version") != 3:
        errors.append("board index schema_version must be 3")
    query_contract = index.get("ai_query_contract")
    if query_contract != "ai-reference-schema.md":
        errors.append("board index must point to ai-reference-schema.md")
    elif not (board_dir / query_contract).is_file():
        errors.append("missing AI board reference schema: references/boards/ai-reference-schema.md")
    ids: set[str] = set()
    paths: set[str] = set()
    names: set[str] = set()
    lookup_keys: dict[str, str] = {}
    ledger = board_dir / "source-ledger.md"
    ledger_text = ledger.read_text(encoding="utf-8") if ledger.is_file() else ""

    for entry in profiles:
        if not isinstance(entry, dict):
            errors.append("every board index profile must be an object")
            continue
        for field in ("id", "name", "path", "ledger_label", "status", "frameworks", "sources"):
            if field not in entry or not entry[field]:
                errors.append(f"board index entry missing {field}")
        for field in REQUIRED_INDEX_FIELDS:
            if field not in entry or entry[field] in (None, "", []):
                errors.append(f"board index entry missing AI field {field}")
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
        lookup_values = [value for value in (profile_id, name) if isinstance(value, str)]
        aliases = entry.get("aliases")
        if isinstance(aliases, list):
            lookup_values.extend(value for value in aliases if isinstance(value, str))
        for value in lookup_values:
            lookup_key = normalize_query(value)
            if not lookup_key:
                continue
            previous = lookup_keys.get(lookup_key)
            if previous and previous != profile_id:
                errors.append(
                    f"ambiguous board lookup key {value!r}: profiles {previous} and {profile_id}"
                )
            else:
                lookup_keys[lookup_key] = str(profile_id)
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
        aliases = entry.get("aliases")
        if not isinstance(aliases, list) or not aliases or not all(isinstance(item, str) and item.strip() for item in aliases):
            errors.append(f"{relative_path}: aliases must be a non-empty list of strings")
        for field in ("mcu", "architecture", "logic_level", "identity_scope"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{relative_path}: {field} must be a non-empty string")
        identity_contract = entry.get("identity_contract")
        if not isinstance(identity_contract, dict):
            errors.append(f"{relative_path}: identity_contract must be an object")
        else:
            profile_type = identity_contract.get("profile_type")
            if profile_type not in {"exact-board", "bounded-variant-family"}:
                errors.append(f"{relative_path}: identity_contract profile_type is invalid")
            for field in ("variants", "required_for_pin_advice", "required_for_electrical_advice"):
                values = identity_contract.get(field)
                if not isinstance(values, list) or not all(isinstance(item, str) and item.strip() for item in values):
                    errors.append(f"{relative_path}: identity_contract {field} must be a list of strings")
            if profile_type == "bounded-variant-family" and not identity_contract.get("variants"):
                errors.append(f"{relative_path}: bounded variant family must list variants")
            if profile_type == "exact-board" and identity_contract.get("variants"):
                errors.append(f"{relative_path}: exact board must not list variants")
        for field in ("capability_tags", "risk_tags", "toolchains"):
            values = entry.get(field)
            if not isinstance(values, list) or not values or not all(isinstance(item, str) and item.strip() for item in values):
                errors.append(f"{relative_path}: {field} must be a non-empty list of strings")
        evidence = entry.get("evidence")
        if not isinstance(evidence, dict):
            errors.append(f"{relative_path}: evidence must be an object")
        else:
            for field in REQUIRED_EVIDENCE_FIELDS:
                if not isinstance(evidence.get(field), str) or not evidence[field].strip():
                    errors.append(f"{relative_path}: evidence missing {field}")
            if not str(evidence.get("source_confidence", "")).startswith("primary-source-backed"):
                errors.append(f"{relative_path}: evidence source_confidence must name primary-source backing")
            if not DATE_RE.fullmatch(str(evidence.get("checked", ""))):
                errors.append(f"{relative_path}: evidence checked must be YYYY-MM-DD")
            if evidence.get("physical_status") != "unverified":
                errors.append(f"{relative_path}: physical_status must remain unverified")
        label = entry.get("ledger_label")
        if isinstance(label, str) and label not in ledger_text:
            errors.append(f"source ledger missing profile row: {label}")

    discovered = sorted(
        path.name
        for path in board_dir.glob("*.md")
        if path.name not in {"README.md", "source-ledger.md", "ai-reference-schema.md"}
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
