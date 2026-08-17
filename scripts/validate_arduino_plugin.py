#!/usr/bin/env python3
"""Validate the Arduino plugin package and its deterministic eval surface."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    from validate_board_references import collect_errors as collect_board_reference_errors
except ImportError:  # pragma: no cover - direct package execution fallback
    collect_board_reference_errors = None


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
TRIGGER_QUERIES = ROOT / "evals" / "board-support-trigger-queries.json"
BASELINE_SKILLS = {
    "arduino-cli-skill",
    "arduino-code-generator",
    "arduino-project-builder",
    "arduino-serial-monitor",
    "arduino-workflow-router",
    "battery-selector",
    "bom-generator",
    "circuit-debugger",
    "code-review-facilitator",
    "datasheet-interpreter",
    "enclosure-designer",
    "error-message-explainer",
    "field-power-and-connectivity-triager",
    "freertos-patterns",
    "i2c-bringup-diagnostician",
    "mermaid-diagram-generator",
    "ota-deployment-guardian",
    "power-budget-calculator",
    "readme-generator",
    "sensor-calibration-workbench",
}
NEW_SKILLS = {
    "pin-assignment",
    "board-support",
    "board-selection",
    "wiring-safety-check",
    "non-blocking-patterns",
    "library-selection",
    "memory-budgeting",
    "hardware-tdd",
    "embedded-project-loop",
    "sensor-signal-filtering",
}
BOARD_FILES = {
    "arduino-uno-r3.md": ("docs.arduino.cc", "microchip.com"),
    "arduino-uno-r4.md": ("docs.arduino.cc",),
    "esp32-devkit.md": ("espressif.com", "docs.espressif.com"),
    "esp32-s3-devkit.md": ("espressif.com", "docs.espressif.com"),
    "pico-pico-w.md": ("raspberrypi.com", "github.com/earlephilhower"),
}
FRONTMATTER_NAME = re.compile(r"^name:\s*(.+?)\s*$")
FRONTMATTER_DESCRIPTION = re.compile(r"^description:\s*(.*)$")
MARKDOWN_LINK = re.compile(r"\]\(([^)]+)\)")
BACKTICK_PATH = re.compile(r"`([^`]+)`")


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing JSON file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    return None


def frontmatter(path: Path, errors: list[str]) -> tuple[str, str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"{path.relative_to(ROOT)}: missing frontmatter")
        return "", "", ""
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        errors.append(f"{path.relative_to(ROOT)}: unterminated frontmatter")
        return "", "", ""
    raw = "\n".join(lines[1:end])
    name = ""
    description = ""
    description_lines: list[str] = []
    in_description_block = False
    for line in lines[1:end]:
        if in_description_block and line.startswith((" ", "\t")):
            description_lines.append(line.strip())
            continue
        in_description_block = False
        name_match = FRONTMATTER_NAME.match(line)
        description_match = FRONTMATTER_DESCRIPTION.match(line)
        if name_match:
            name = name_match.group(1).strip().strip('"').strip("'")
        if description_match:
            value = description_match.group(1).strip().strip('"').strip("'")
            if value in {"|", ">"}:
                in_description_block = True
            else:
                description = value
    if description_lines:
        description = " ".join(description_lines)
    return name, description, raw


def resolve_reference(skill_dir: Path, token: str) -> Path | None:
    token = token.strip().strip('"').strip("'").split("#", 1)[0]
    if not token or token.startswith(("http://", "https://", "mailto:")):
        return None
    if token.startswith(("./", "../")):
        return (skill_dir / token).resolve()
    if token.startswith("skills/"):
        return (ROOT / token).resolve()
    if token.startswith("docs/") or token.startswith("references/"):
        if token.startswith("references/"):
            return (skill_dir / token).resolve()
        return (ROOT / token).resolve()
    if token.startswith(("scripts/", "rules/", "workflow/", "templates/", "assets/", "examples/")):
        return (skill_dir / token).resolve()
    return None


def validate_skill_files(errors: list[str], warnings: list[str]) -> list[str]:
    paths = sorted(SKILLS.glob("*/SKILL.md"))
    names: list[str] = []
    for path in paths:
        name, description, raw_frontmatter = frontmatter(path, errors)
        names.append(name)
        if name != path.parent.name:
            errors.append(f"{path.relative_to(ROOT)}: name does not match directory")
        if not description:
            errors.append(f"{path.relative_to(ROOT)}: missing description")
        if "when" not in description.lower() and "request" not in description.lower():
            errors.append(f"{path.relative_to(ROOT)}: description has no trigger condition")
        if len(path.read_text(encoding="utf-8").splitlines()) > 500:
            errors.append(f"{path.relative_to(ROOT)}: exceeds 500 lines")
        if "triggers:" not in raw_frontmatter:
            errors.append(f"{path.relative_to(ROOT)}: missing metadata triggers")

        content = path.read_text(encoding="utf-8")
        tokens = MARKDOWN_LINK.findall(content) + BACKTICK_PATH.findall(content)
        for token in tokens:
            resolved = resolve_reference(path.parent, token)
            if resolved is not None and not resolved.is_file() and not resolved.is_dir():
                errors.append(f"{path.relative_to(ROOT)}: broken reference `{token}`")

        if name != "arduino-workflow-router" and "arduino-skill-contract.md" not in content:
            errors.append(f"{path.relative_to(ROOT)}: missing shared contract link")

    if len(names) != len(set(names)):
        errors.append("duplicate skill names or ambiguous entrypoint names")
    missing = BASELINE_SKILLS - set(names)
    if missing:
        errors.append(f"baseline skills missing: {', '.join(sorted(missing))}")
    if not NEW_SKILLS.issubset(set(names)):
        errors.append(f"new skills missing: {', '.join(sorted(NEW_SKILLS - set(names)))}")
    if "serial-debugging" in set(names):
        errors.append("duplicate serial-debugging skill exists; serial monitor should own this route")
    return names


def validate_manifests(errors: list[str]) -> None:
    root_manifest = load_json(ROOT / "plugin.json", errors)
    codex_manifest = load_json(ROOT / ".codex-plugin/plugin.json", errors)
    claude_manifest = load_json(ROOT / ".claude-plugin/plugin.json", errors)
    cursor_manifest = load_json(ROOT / ".cursor-plugin/plugin.json", errors)
    if isinstance(root_manifest, dict) and root_manifest.get("skills") != "./skills/":
        errors.append("root plugin.json must point to ./skills/")
    if isinstance(codex_manifest, dict):
        if codex_manifest.get("name") != "arduino-skills":
            errors.append("Codex manifest name mismatch")
        if codex_manifest.get("skills") != "./skills/":
            errors.append("Codex manifest must point to ./skills/")
        interface = codex_manifest.get("interface", {})
        for field in ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities", "defaultPrompt"):
            if field not in interface:
                errors.append(f"Codex manifest missing interface.{field}")
        if "hooks" in codex_manifest:
            errors.append("Codex manifest must not declare unsupported hooks")
    for label, manifest in (("Claude", claude_manifest), ("Cursor", cursor_manifest)):
        if isinstance(manifest, dict) and manifest.get("name") != "arduino-skills":
            errors.append(f"{label} manifest name mismatch")

    for path, kind in ((ROOT / ".agents/plugins/marketplace.json", "Codex"), (ROOT / ".claude-plugin/marketplace.json", "Claude"), (ROOT / ".cursor-plugin/marketplace.json", "Cursor")):
        marketplace = load_json(path, errors)
        if not isinstance(marketplace, dict):
            continue
        plugins = marketplace.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            errors.append(f"{kind} marketplace has no plugins")
            continue
        matches = [item for item in plugins if isinstance(item, dict) and item.get("name") == "arduino-skills"]
        if len(matches) != 1:
            errors.append(f"{kind} marketplace must contain exactly one arduino-skills entry")
            continue
        entry = matches[0]
        if kind == "Codex":
            source = entry.get("source")
            if not isinstance(source, dict):
                errors.append("Codex marketplace source must be an object")
            elif source.get("source") != "local" or source.get("path") != "./":
                errors.append("Codex marketplace source must be {source: local, path: ./}")
            policy = entry.get("policy", {})
            if policy.get("installation") not in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}:
                errors.append("Codex marketplace installation policy is invalid")
            if policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
                errors.append("Codex marketplace authentication policy is invalid")
            if not entry.get("category"):
                errors.append("Codex marketplace category is missing")
        elif entry.get("source") != "./":
            errors.append(f"{kind} marketplace source must be ./")

    nested_marketplaces = sorted(SKILLS.glob("*/.claude-plugin/marketplace.json"))
    if nested_marketplaces:
        errors.append(
            "nested per-skill Claude marketplace metadata is forbidden; use the root adapter"
        )


def validate_boards(errors: list[str]) -> None:
    board_dir = ROOT / "references/boards"
    for filename, domains in BOARD_FILES.items():
        path = board_dir / filename
        if not path.is_file():
            errors.append(f"missing board reference: references/boards/{filename}")
            continue
        content = path.read_text(encoding="utf-8")
        urls = re.findall(r"https://[^) \t\r\n]+", content)
        for domain in domains:
            if not any(domain in url for url in urls):
                errors.append(f"{filename}: missing source domain {domain}")
        if len(urls) < 2:
            errors.append(f"{filename}: fewer than two source URLs")
        if "## Fact-to-source map" not in content:
            errors.append(f"{filename}: missing fact-to-source map")
        if "Source status:" not in content:
            errors.append(f"{filename}: missing source status")
    s3 = (board_dir / "esp32-s3-devkit.md").read_text(encoding="utf-8")
    if "Do not carry the classic ESP32 GPIO34-39 input-only rule" not in s3:
        errors.append("ESP32-S3 reference lacks the classic-ESP32 distinction")
    research = Path("/Users/wed/.codex/workflows/arduino-mainstream-plugin-2026-08-10/research/board-specs.md")
    if research.is_file() and "GPIO34-39 are input-only on ESP32-S3" in research.read_text(encoding="utf-8"):
        errors.append("board research still claims classic GPIO34-39 input-only behavior on S3")
    ledger = board_dir / "source-ledger.md"
    if not ledger.is_file():
        errors.append("missing board source ledger: references/boards/source-ledger.md")
    else:
        ledger_text = ledger.read_text(encoding="utf-8")
        for label in ("Uno R3", "Uno R4", "Classic ESP32", "ESP32-S3", "Pico/Pico W"):
            if label not in ledger_text:
                errors.append(f"board source ledger missing profile row: {label}")
    if collect_board_reference_errors is None:
        errors.append("board index validator could not be imported")
    else:
        index_errors, _ = collect_board_reference_errors(ROOT)
        errors.extend(f"board index: {error}" for error in index_errors)


def validate_contract_and_fixtures(errors: list[str]) -> None:
    contract = ROOT / "docs/arduino-skill-contract.md"
    content = contract.read_text(encoding="utf-8") if contract.is_file() else ""
    for term in ("constexpr int", "fixed numeric order", "Physical-world gate", "unverified yes"):
        if term.lower() not in content.lower():
            errors.append(f"shared contract missing {term}")
    evals = load_json(ROOT / "evals/evals.json", errors)
    if not isinstance(evals, dict) or len(evals.get("evals", [])) < 10:
        errors.append("evals/evals.json must contain scenarios for all new/modified entrypoints")
    elif not isinstance(evals.get("evals"), list):
        errors.append("evals/evals.json evals must be a list")
    else:
        known_skills = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        case_ids: set[str] = set()
        supported_assertions = {
            "fixture_pin_declarations",
            "fixture_pin_safety",
            "skill_terms",
            "shared_output_contract",
            "route_order",
            "trigger_precedence",
            "loop_engine_fixture",
            "board_index_contract",
            "board_lookup",
            "board_identity_contract",
        }
        for case in evals["evals"]:
            if not isinstance(case, dict):
                errors.append("each behavioral eval must be an object")
                continue
            case_id = case.get("id")
            if not isinstance(case_id, str) or not case_id:
                errors.append("each behavioral eval needs a non-empty id")
            elif case_id in case_ids:
                errors.append(f"duplicate behavioral eval id: {case_id}")
            else:
                case_ids.add(case_id)
            if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                errors.append(f"{case_id}: missing prompt")
            route = case.get("route")
            if not isinstance(route, list) or not route or any(skill not in known_skills for skill in route):
                errors.append(f"{case_id}: route must list existing skills")
            assertions = case.get("assertions")
            if not isinstance(assertions, list) or not assertions:
                errors.append(f"{case_id}: missing declarative assertions")
            else:
                for assertion in assertions:
                    if not isinstance(assertion, dict) or assertion.get("type") not in supported_assertions:
                        errors.append(f"{case_id}: unsupported assertion declaration")
                        continue
                    assertion_type = assertion["type"]
                    if assertion_type == "skill_terms":
                        if assertion.get("skill") not in known_skills or not isinstance(assertion.get("terms"), list) or not assertion["terms"]:
                            errors.append(f"{case_id}: skill_terms assertion is incomplete")
        if "loop-engine-evidence-contract" not in case_ids:
            errors.append("evals/evals.json must include loop-engine-evidence-contract")
        for fixture in (
            "evals/fixtures/loop-engine/loop-state.json",
            "evals/fixtures/loop-engine/experiment-log.jsonl",
            "evals/fixtures/loop-engine/invalid-loop-state.json",
            "evals/fixtures/loop-engine/invalid-experiment-log.jsonl",
        ):
            if not (ROOT / fixture).is_file():
                errors.append(f"missing loop-engine eval fixture: {fixture}")
    trigger_queries = load_json(TRIGGER_QUERIES, errors)
    if isinstance(trigger_queries, dict):
        queries = trigger_queries.get("queries")
        if trigger_queries.get("skill_name") != "board-support":
            errors.append("board-support trigger corpus has the wrong skill_name")
        if not isinstance(queries, list) or len(queries) < 16:
            errors.append("board-support trigger corpus needs at least 16 queries")
        else:
            trigger_ids: set[str] = set()
            positive = 0
            negative = 0
            splits: dict[str, int] = {}
            for query in queries:
                if not isinstance(query, dict):
                    errors.append("board-support trigger query must be an object")
                    continue
                query_id = query.get("id")
                if not isinstance(query_id, str) or not query_id:
                    errors.append("board-support trigger query needs an id")
                elif query_id in trigger_ids:
                    errors.append(f"duplicate board-support trigger query id: {query_id}")
                else:
                    trigger_ids.add(query_id)
                if not isinstance(query.get("query"), str) or not query["query"].strip():
                    errors.append(f"{query_id}: trigger query text is missing")
                if not isinstance(query.get("should_trigger"), bool):
                    errors.append(f"{query_id}: should_trigger must be boolean")
                elif query["should_trigger"]:
                    positive += 1
                else:
                    negative += 1
                split = query.get("split")
                if split not in {"train", "validation"}:
                    errors.append(f"{query_id}: trigger split must be train or validation")
                else:
                    splits[split] = splits.get(split, 0) + 1
            if positive < 8 or negative < 8:
                errors.append("board-support trigger corpus must include at least 8 positive and 8 negative queries")
            if not all(splits.get(split, 0) for split in ("train", "validation")):
                errors.append("board-support trigger corpus must contain train and validation queries")
            if trigger_queries.get("status") != "dataset-ready-model-run-pending":
                errors.append("board-support trigger corpus must declare model-run status")
    if not (ROOT / "scripts/resolve_board_profile.py").is_file():
        errors.append("missing deterministic board resolver")
    fixture = ROOT / "evals/fixtures/esp32-buttons-leds.txt"
    if fixture.is_file():
        lines = fixture.read_text(encoding="utf-8").splitlines()
        if lines != [
            "constexpr int btn_esc = 101;",
            "constexpr int btn_enter = 102;",
            "constexpr int btn_next = 103;",
            "constexpr int btn_back = 104;",
            "constexpr int led_status = 105;",
            "constexpr int led_error = 106;",
        ]:
            errors.append("pin fixture violates the raw ordered constexpr convention")
    else:
        errors.append("missing pin behavior fixture")
    for path in (ROOT / "AGENTS.md", ROOT / "CLAUDE.md", ROOT / "GEMINI.md", ROOT / ".cursor/rules/arduino-skills.mdc"):
        if not path.is_file():
            errors.append(f"missing host wrapper: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    names = validate_skill_files(errors, warnings)
    validate_manifests(errors)
    validate_boards(errors)
    validate_contract_and_fixtures(errors)
    if not (ROOT / "skills/arduino-serial-monitor/SKILL.md").read_text(encoding="utf-8").startswith("---\n"):
        errors.append("serial monitor frontmatter is missing")
    result = {
        "skills_checked": len(names),
        "baseline_skills_preserved": BASELINE_SKILLS.issubset(set(names)),
        "new_skills_present": NEW_SKILLS.issubset(set(names)),
        "errors": errors,
        "warnings": warnings,
        "passed": not errors,
    }
    print(json.dumps(result, indent=2))
    if errors:
        print(f"Plugin validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Plugin validation passed: {len(names)} skills, 0 errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
