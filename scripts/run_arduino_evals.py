#!/usr/bin/env python3
"""Run the declarative Arduino prompt contract suite.

This is a deterministic forward-contract harness. It consumes every prompt,
route, and assertion in ``evals/evals.json`` and checks the repository's
instructions, fixtures, output contract, and routing precedence. It does not
pretend to be a model invocation; the fresh-context reviewer supplies the
independent semantic evaluation.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from resolve_board_profile import normalize_query, resolve_profile

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "evals.json"
CONTRACT = ROOT / "docs" / "arduino-skill-contract.md"
BOARD_INDEX = ROOT / "references" / "boards" / "index.json"
LOOP_FIXTURE_DIR = ROOT / "evals" / "fixtures" / "loop-engine"
DECLARATION_RE = re.compile(r"^constexpr int [a-zA-Z_][a-zA-Z0-9_]* = (\d+);$")
REQUIRED_CONTRACT_TERMS = (
    "assumptions",
    "required tools and versions",
    "implementation steps",
    "tests and evidence",
    "known limitations",
    "recovery and security notes",
)
LOOP_STATE_KEYS = (
    "goal",
    "primary_metric",
    "correctness_gates",
    "hard_constraints",
    "editable_surface",
    "protected_files",
    "baseline",
    "best_known_state",
    "experiment_budget",
    "per_iteration_budget",
    "evaluation_method",
    "acceptance_rule",
    "rollback_method",
    "plateau_rule",
    "stop_conditions",
    "experiment_history",
    "open_uncertainties",
)
LOOP_STATE_SNAPSHOT_KEYS = ("id", "commands", "results", "evidence_paths")
LOOP_LEDGER_KEYS = (
    "id",
    "timestamp",
    "baseline_id",
    "hypothesis",
    "changed_files",
    "command",
    "result",
    "primary_metric",
    "correctness_gates",
    "acceptance_decision",
    "revert_evidence",
    "lesson",
    "next_candidate",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_path(skill: str) -> Path:
    return ROOT / "skills" / skill / "SKILL.md"


def skill_text(skill: str) -> str:
    return " ".join(skill_path(skill).read_text(encoding="utf-8").lower().split())


def check(name: str, passed: bool, evidence: str) -> dict[str, object]:
    return {"name": name, "passed": passed, "evidence": evidence}


def check_pin_fixture() -> list[dict[str, object]]:
    output_path = ROOT / "evals/fixtures/esp32-buttons-leds.txt"
    hardware_path = ROOT / "evals/fixtures/esp32-buttons-leds.hardware-map.json"
    lines = output_path.read_text(encoding="utf-8").splitlines()
    matches = [DECLARATION_RE.fullmatch(line) for line in lines]
    values = [int(match.group(1)) for match in matches if match]
    hardware = load_json(hardware_path)
    output_pins = list(hardware["outputs"].values())
    reserved_output_pins = set(hardware["reserved_output_pins"])
    return [
        check(
            "raw declarations only",
            len(lines) == 6 and all(matches),
            str(output_path),
        ),
        check(
            "ordered logical IDs",
            values == [101, 102, 103, 104, 105, 106],
            repr(values),
        ),
        check(
            "safe physical output choices",
            not reserved_output_pins.intersection(output_pins),
            repr({"outputs": output_pins, "reserved": sorted(reserved_output_pins)}),
        ),
        check(
            "declarations contain no commentary",
            all(line.startswith("constexpr int ") and line.endswith(";") for line in lines),
            "fixture contains declarations only; no headings, fences, or comments",
        ),
    ]


def check_skill_terms(skill: str, terms: list[str]) -> list[dict[str, object]]:
    path = skill_path(skill)
    text = " ".join(path.read_text(encoding="utf-8").lower().split())
    return [check(term, " ".join(term.lower().split()) in text, str(path)) for term in terms]


def check_board_index_contract() -> list[dict[str, object]]:
    required_fields = (
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
    required_evidence = ("source_confidence", "checked", "physical_status")
    try:
        index = load_json(BOARD_INDEX)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        return [check("board index loads", False, str(exc))]

    profiles = index.get("profiles", []) if isinstance(index, dict) else []
    lookup_keys: dict[str, str] = {}
    collisions: list[str] = []
    for profile in profiles:
        values = [profile.get("id", ""), profile.get("name", ""), *profile.get("aliases", [])]
        for value in values:
            key = normalize_query(value)
            previous = lookup_keys.get(key)
            if previous and previous != profile.get("id"):
                collisions.append(f"{key}:{previous}:{profile.get('id')}")
            else:
                lookup_keys[key] = profile.get("id", "")
    checks: list[dict[str, object]] = [
        check("board index schema", isinstance(index, dict) and index.get("schema_version") == 3, str(BOARD_INDEX)),
        check("AI query contract link", isinstance(index, dict) and index.get("ai_query_contract") == "ai-reference-schema.md", str(BOARD_INDEX)),
        check("all profiles expose retrieval fields", all(all(field in profile for field in required_fields) for profile in profiles), repr(required_fields)),
        check("all profiles expose evidence fields", all(isinstance(profile.get("evidence"), dict) and all(field in profile["evidence"] for field in required_evidence) for profile in profiles), repr(required_evidence)),
        check("physical status stays unverified", all(profile.get("evidence", {}).get("physical_status") == "unverified" for profile in profiles), "board index evidence"),
        check("profile aliases are non-empty", all(isinstance(profile.get("aliases"), list) and profile["aliases"] for profile in profiles), "board index aliases"),
        check("board lookup keys are unique", not collisions, repr(collisions)),
        check("source confidence names primary sources", all(str(profile.get("evidence", {}).get("source_confidence", "")).startswith("primary-source-backed") for profile in profiles), "board index evidence"),
        check(
            "identity contracts are structured",
            all(
                isinstance(profile.get("identity_contract"), dict)
                and profile["identity_contract"].get("profile_type") in {"exact-board", "bounded-variant-family"}
                and isinstance(profile["identity_contract"].get("variants"), list)
                and isinstance(profile["identity_contract"].get("required_for_pin_advice"), list)
                and isinstance(profile["identity_contract"].get("required_for_electrical_advice"), list)
                for profile in profiles
            ),
            "board index identity_contract",
        ),
    ]
    return checks


def check_board_lookup(assertion: dict[str, Any]) -> list[dict[str, object]]:
    query = assertion.get("query", "")
    expected_id = assertion.get("expected_id", "")
    try:
        index = load_json(BOARD_INDEX)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        return [check("board lookup index loads", False, str(exc))]

    result = resolve_profile(index, query, purpose="lookup")
    matches = [profile.get("id") for profile in result.get("matches", [])]
    return [
        check("board query has one exact match", result.get("status") == "resolved" and len(matches) == 1, repr({"query": query, "matches": matches, "status": result.get("status")})),
        check("board query resolves expected profile", matches == [expected_id], repr({"expected": expected_id, "matches": matches})),
    ]


def check_board_identity(assertion: dict[str, Any]) -> list[dict[str, object]]:
    try:
        index = load_json(BOARD_INDEX)
        result = resolve_profile(
            index,
            assertion.get("query", ""),
            purpose=assertion.get("purpose", "lookup"),
            identity=assertion.get("identity", []),
        )
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError) as exc:
        return [check("board identity resolver loads", False, str(exc))]
    expected_status = assertion.get("expected_status")
    expected_missing = assertion.get("expected_missing", [])
    return [
        check("board identity status", result.get("status") == expected_status, repr(result)),
        check("board identity missing fields", result.get("required_disambiguators", []) == expected_missing, repr(result)),
    ]


def check_route(case: dict[str, Any]) -> list[dict[str, object]]:
    route = case.get("route", [])
    checks: list[dict[str, object]] = []
    paths_exist = bool(route) and all(skill_path(skill).is_file() for skill in route)
    checks.append(check("route skills exist", paths_exist, repr(route)))
    if not paths_exist:
        return checks

    router_text = skill_text("arduino-workflow-router")
    names_are_unique = len(route) == len(set(route))
    checks.append(check("route has no duplicate owners", names_are_unique, repr(route)))

    if case["id"] == "wiring-and-pin-composition":
        marker = "default combined order"
        order_section = router_text[router_text.find(marker) :] if marker in router_text else ""
        positions = [order_section.find(f"`{skill}`") for skill in route]
        ordered = bool(order_section) and all(position >= 0 for position in positions)
        ordered = ordered and positions == sorted(positions)
        checks.append(check("combined route order", ordered, repr({"route": route, "positions": positions})))
    return checks


def check_trigger_precedence() -> list[dict[str, object]]:
    path = skill_path("arduino-workflow-router")
    text = path.read_text(encoding="utf-8").lower()
    terms = [
        "## trigger precedence",
        "this router owns",
        "arduino-project-builder",
        "board-selection",
        "combined-workflow order",
    ]
    return [check(term, term in text, str(path)) for term in terms]


def check_shared_output_contract(route: list[str]) -> list[dict[str, object]]:
    contract_text = CONTRACT.read_text(encoding="utf-8").lower()
    checks = [
        check(term, term in contract_text, str(CONTRACT))
        for term in REQUIRED_CONTRACT_TERMS
    ]
    for skill in route:
        path = skill_path(skill)
        text = path.read_text(encoding="utf-8").lower()
        checks.append(
            check(
                f"{skill} links shared contract",
                "arduino-skill-contract.md" in text,
                str(path),
            )
        )
    return checks


def validate_loop_artifacts(state: Any, ledger_text: str) -> list[str]:
    """Return invariant failures for a durable loop state and JSONL ledger."""
    errors: list[str] = []
    if not isinstance(state, dict):
        return ["loop state is not an object"]

    missing_state_keys = [key for key in LOOP_STATE_KEYS if key not in state]
    if missing_state_keys:
        errors.append(f"loop state missing keys: {', '.join(missing_state_keys)}")

    metric = state.get("primary_metric")
    if not isinstance(metric, dict):
        errors.append("primary_metric is not an object")
    else:
        if metric.get("direction") not in {"increase", "decrease", "lower", "higher"}:
            errors.append("primary_metric has no valid direction")
        if not metric.get("threshold"):
            errors.append("primary_metric has no acceptance threshold")

    for snapshot_name in ("baseline", "best_known_state"):
        snapshot = state.get(snapshot_name)
        if not isinstance(snapshot, dict):
            errors.append(f"{snapshot_name} is not an object")
            continue
        missing_snapshot_keys = [
            key for key in LOOP_STATE_SNAPSHOT_KEYS if not snapshot.get(key)
        ]
        if missing_snapshot_keys:
            errors.append(
                f"{snapshot_name} missing keys: {', '.join(missing_snapshot_keys)}"
            )

    history = state.get("experiment_history")
    if not isinstance(history, list) or not history:
        errors.append("experiment_history is empty")

    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(ledger_text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"ledger line {line_number} is invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"ledger line {line_number} is not an object")
            continue
        rows.append(row)
        missing_row_keys = [key for key in LOOP_LEDGER_KEYS if key not in row]
        if missing_row_keys:
            errors.append(
                f"ledger line {line_number} missing keys: {', '.join(missing_row_keys)}"
            )

    decisions = {row.get("acceptance_decision") for row in rows}
    if "baseline" not in decisions:
        errors.append("ledger has no baseline decision")
    if not decisions.intersection({"keep", "revert", "crash"}):
        errors.append("ledger has no evaluated experiment decision")
    return errors


def check_loop_engine_fixture() -> list[dict[str, object]]:
    valid_state_path = LOOP_FIXTURE_DIR / "loop-state.json"
    valid_ledger_path = LOOP_FIXTURE_DIR / "experiment-log.jsonl"
    invalid_state_path = LOOP_FIXTURE_DIR / "invalid-loop-state.json"
    invalid_ledger_path = LOOP_FIXTURE_DIR / "invalid-experiment-log.jsonl"
    checks: list[dict[str, object]] = []

    try:
        valid_state = load_json(valid_state_path)
        valid_ledger = valid_ledger_path.read_text(encoding="utf-8")
        valid_errors = validate_loop_artifacts(valid_state, valid_ledger)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        valid_errors = [str(exc)]
    checks.append(
        check(
            "valid loop artifacts satisfy the contract",
            not valid_errors,
            repr(valid_errors) if valid_errors else str(LOOP_FIXTURE_DIR),
        )
    )

    try:
        invalid_state = load_json(invalid_state_path)
        invalid_ledger = invalid_ledger_path.read_text(encoding="utf-8")
        invalid_errors = validate_loop_artifacts(invalid_state, invalid_ledger)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        invalid_errors = [str(exc)]
    checks.append(
        check(
            "invalid loop artifacts are rejected",
            bool(invalid_errors),
            repr(invalid_errors),
        )
    )
    return checks


def evaluate_assertion(assertion: dict[str, Any], case: dict[str, Any]) -> list[dict[str, object]]:
    assertion_type = assertion["type"]
    if assertion_type == "fixture_pin_declarations":
        return check_pin_fixture()
    if assertion_type == "fixture_pin_safety":
        return [check("physical output map", check_pin_fixture()[2]["passed"], "pin fixture hardware map")]
    if assertion_type == "skill_terms":
        return check_skill_terms(assertion["skill"], assertion["terms"])
    if assertion_type == "board_index_contract":
        return check_board_index_contract()
    if assertion_type == "board_lookup":
        return check_board_lookup(assertion)
    if assertion_type == "board_identity_contract":
        return check_board_identity(assertion)
    if assertion_type == "shared_output_contract":
        return check_shared_output_contract(case["route"])
    if assertion_type == "route_order":
        return check_route(case)
    if assertion_type == "trigger_precedence":
        return check_trigger_precedence()
    if assertion_type == "loop_engine_fixture":
        return check_loop_engine_fixture()
    raise ValueError(f"unknown assertion type: {assertion_type}")


def evaluate_case(case: dict[str, Any]) -> dict[str, object]:
    checks: list[dict[str, object]] = []
    prompt = case.get("prompt", "")
    checks.append(check("prompt is present", bool(prompt.strip()), "prompt consumed by forward harness"))
    checks.extend(check_route(case))
    for assertion in case.get("assertions", []):
        checks.extend(evaluate_assertion(assertion, case))
    return {
        "id": case["id"],
        "skill": case["skill"],
        "prompt": prompt,
        "expected_route": case["route"],
        "passed": all(item["passed"] for item in checks),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run declarative Arduino prompt contract evaluations")
    parser.add_argument("--output", default=str(ROOT / "evals/eval-results.json"))
    args = parser.parse_args()

    definition = load_json(EVALS)
    cases = [evaluate_case(case) for case in definition["evals"]]
    payload = {
        "suite": "arduino-skills",
        "evaluation_mode": definition.get("evaluation_mode", "forward-contract"),
        "prompt_count": len(cases),
        "cases": cases,
        "passed": all(case["passed"] for case in cases),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for case in cases:
        print(f"{'PASS' if case['passed'] else 'FAIL'} {case['id']}")
    print(f"Result: {sum(case['passed'] for case in cases)}/{len(cases)} cases passed")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
