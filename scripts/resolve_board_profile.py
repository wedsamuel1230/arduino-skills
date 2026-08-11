#!/usr/bin/env python3
"""Resolve an indexed board name without fuzzy matching or family guessing."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "references" / "boards" / "index.json"
EXIT_CODES = {
    "resolved": 0,
    "needs-disambiguation": 2,
    "unsupported": 3,
    "invalid-input": 4,
}


def normalize_query(value: str) -> str:
    """Normalize names for exact lookup; intentionally do not perform fuzzy matching."""
    return "-".join(re.findall(r"[a-z0-9]+", value.lower()))


def _identity_from_query(query: str, contract: dict[str, Any]) -> set[str]:
    normalized_query = normalize_query(query)
    confirmed: set[str] = set()
    for variant in contract.get("variants", []):
        if normalize_query(str(variant)) in normalized_query.split("-"):
            confirmed.add("variant")
    if any(
        normalize_query(str(variant)) in normalized_query
        for variant in contract.get("variants", [])
    ):
        confirmed.add("variant")
    if re.search(r"wroom-(?:02u?|1|2)", normalized_query):
        confirmed.add("module_suffix")
    return confirmed


def _identity_from_args(values: list[str]) -> set[str]:
    confirmed: set[str] = set()
    for value in values:
        key, separator, content = value.partition("=")
        if separator and key.strip() and content.strip():
            confirmed.add(key.strip())
    return confirmed


def resolve_profile(
    index: dict[str, Any],
    query: str,
    *,
    purpose: str = "lookup",
    identity: list[str] | None = None,
) -> dict[str, Any]:
    normalized_query = normalize_query(query)
    matches: list[dict[str, Any]] = []
    for profile in index.get("profiles", []):
        candidates = [profile.get("id", ""), profile.get("name", ""), *profile.get("aliases", [])]
        matched_alias = next(
            (candidate for candidate in candidates if normalize_query(str(candidate)) == normalized_query),
            None,
        )
        if matched_alias is not None:
            matches.append(
                {
                    "id": profile.get("id"),
                    "name": profile.get("name"),
                    "path": profile.get("path"),
                    "matched_alias": matched_alias,
                    "identity_contract": profile.get("identity_contract", {}),
                    "evidence": profile.get("evidence", {}),
                }
            )

    if not matches:
        return {
            "status": "unsupported",
            "reason": "no-exact-indexed-match",
            "query": query,
            "normalized_query": normalized_query,
            "matches": [],
        }
    if len(matches) > 1:
        return {
            "status": "needs-disambiguation",
            "reason": "multiple-exact-indexed-matches",
            "query": query,
            "normalized_query": normalized_query,
            "matches": matches,
            "required_disambiguators": ["board identity"],
        }

    match = matches[0]
    contract = match["identity_contract"]
    required_key = {
        "pin": "required_for_pin_advice",
        "electrical": "required_for_electrical_advice",
    }.get(purpose)
    required = list(contract.get(required_key, [])) if required_key else []
    confirmed = _identity_from_query(query, contract)
    confirmed.update(_identity_from_args(identity or []))
    missing = [field for field in required if field not in confirmed]
    result: dict[str, Any] = {
        "status": "resolved" if not missing else "needs-disambiguation",
        "reason": "identity-complete" if not missing else "missing-identity-fields",
        "query": query,
        "normalized_query": normalized_query,
        "matches": matches,
        "required_disambiguators": missing,
        "purpose": purpose,
    }
    return result


def load_index(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("profiles"), list):
        raise ValueError("board index must be an object with a profiles list")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve an exact indexed Arduino board profile")
    parser.add_argument("--query", required=True, help="Exact board id, name, or alias")
    parser.add_argument("--purpose", choices=("lookup", "pin", "electrical"), default="lookup")
    parser.add_argument("--identity", action="append", default=[], metavar="FIELD=VALUE")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    args = parser.parse_args()
    try:
        result = resolve_profile(load_index(args.index), args.query, purpose=args.purpose, identity=args.identity)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "invalid-input", "error": str(exc)}, indent=2))
        return EXIT_CODES["invalid-input"]
    print(json.dumps(result, indent=2))
    return EXIT_CODES[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
