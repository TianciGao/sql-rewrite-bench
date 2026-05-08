#!/usr/bin/env python3
"""Human-run validator for the formal R-Bot run-path artifact contract."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[3]

RUN_PLAN_PATH = REPO_ROOT / "reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_run_plan_v1.json"
CANDIDATE_MATRIX_PATH = REPO_ROOT / "reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_candidate_matrix.csv"
EXPECTED_PATHS_PATH = PACKAGE_DIR / "formal_artifact_expected_paths.json"
CONTRACT_MATRIX_PATH = PACKAGE_DIR / "formal_artifact_contract_matrix.csv"
REPORT_MD_PATH = PACKAGE_DIR / "formal_artifact_contract_validation_report.md"
REPORT_JSON_PATH = PACKAGE_DIR / "formal_artifact_contract_validation_report.json"


class ValidationError(Exception):
    def __init__(self, status: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


@dataclass
class ValidationResult:
    status: str
    message: str
    current_benchmark_gate_ready: bool
    formal_generation_may_start_from_artifact_contract_perspective: bool
    checks: list[dict[str, Any]]
    summary: dict[str, Any]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def ensure(condition: bool, status: str, message: str) -> None:
    if not condition:
        raise ValidationError(status, message)


def render_template(run_root: str, template: str, case_id: str, engine: str) -> str:
    return f"{run_root}/{template.format(case_id=case_id, engine=engine)}"


def scan_text_for_secrets(text: str, forbidden_substrings: list[str]) -> str | None:
    for token in forbidden_substrings:
        if token in text:
            return token
    return None


def validate_expected_paths_spec(spec: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    ensure(spec.get("spec_version") == "formal_artifact_expected_paths_v1", "invalid_expected_paths_version", "Unexpected expected-paths spec version.")

    contract = spec.get("contract")
    ensure(isinstance(contract, dict), "missing_contract_section", "Expected-paths spec is missing the contract section.")
    ensure(contract.get("planned_rows") == 120, "planned_row_count_mismatch", "Expected-paths spec must freeze planned_rows = 120.")
    ensure(contract.get("case_count") == 40, "planned_case_count_mismatch", "Expected-paths spec must freeze case_count = 40.")
    ensure(contract.get("engines") == ["pg", "mysql", "spark"], "planned_engine_set_mismatch", "Expected-paths spec must freeze engines = [pg, mysql, spark].")
    ensure(contract.get("method_id") == "r_bot", "method_id_mismatch", "Expected-paths spec must freeze method_id = r_bot.")
    ensure(contract.get("route_id") == "r_bot_same_engine_rewrite", "route_id_mismatch", "Expected-paths spec must freeze route_id = r_bot_same_engine_rewrite.")
    checks.append({"name": "contract_constants", "status": "pass"})

    row_statuses = spec.get("row_statuses", {})
    required_statuses = row_statuses.get("required_enumeration", [])
    for status in ["generated", "failed", "blocked", "unsupported", "skipped"]:
        ensure(status in required_statuses, "missing_row_status_enum", f"Expected-paths spec is missing row status {status}.")
    ensure(row_statuses.get("rows_must_remain_visible_in_run_event_long_for_all_statuses") is True, "row_visibility_rule_missing", "Expected-paths spec must freeze denominator-preserving row visibility.")
    checks.append({"name": "row_statuses", "status": "pass"})

    row_artifacts = spec.get("row_artifacts", {})
    required_row_artifacts = {
        "generated_sql",
        "selected_rules",
        "retrieval_trace",
        "prompt_text",
        "raw_response",
        "token_cost_provider",
        "environment_snapshot",
        "row_run_metadata",
    }
    ensure(set(row_artifacts.keys()) == required_row_artifacts, "row_artifact_set_mismatch", "Expected-paths spec must define exactly the required row-level artifacts.")
    for artifact_name, artifact_spec in row_artifacts.items():
        ensure("path_template" in artifact_spec, "missing_row_path_template", f"{artifact_name} is missing path_template.")
        if artifact_name not in {"generated_sql", "prompt_text", "raw_response"}:
            ensure(bool(artifact_spec.get("required_schema_keys")), "missing_row_schema_keys", f"{artifact_name} is missing required_schema_keys.")
    checks.append({"name": "row_artifacts", "status": "pass"})

    package_artifacts = spec.get("package_artifacts", {})
    for artifact_name in ["run_results", "run_event_long", "generation_summary"]:
        ensure(artifact_name in package_artifacts, "package_artifact_missing", f"Expected-paths spec is missing package artifact {artifact_name}.")
    ensure(bool(package_artifacts["run_results"].get("required_schema_keys")), "missing_run_results_schema", "run_results required_schema_keys missing.")
    ensure(bool(package_artifacts["run_event_long"].get("required_columns")), "missing_run_event_long_columns", "run_event_long required_columns missing.")
    ensure(bool(package_artifacts["generation_summary"].get("required_columns")), "missing_generation_summary_columns", "generation_summary required_columns missing.")
    checks.append({"name": "package_artifacts", "status": "pass"})

    secret_hygiene = spec.get("secret_hygiene", {})
    forbidden_substrings = secret_hygiene.get("forbidden_substrings", [])
    ensure(bool(forbidden_substrings), "missing_secret_hygiene_rules", "Expected-paths spec must define forbidden secret substrings.")
    serialized = json.dumps(spec, sort_keys=True)
    forbidden_in_spec = scan_text_for_secrets(serialized, forbidden_substrings)
    ensure(forbidden_in_spec is None, "secret_pattern_in_contract_spec", f"Expected-paths spec contains forbidden token {forbidden_in_spec}.")
    checks.append({"name": "secret_hygiene_spec", "status": "pass"})
    return checks


def validate_matrix_against_plan(
    run_plan: dict[str, Any],
    candidate_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    spec: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    ensure(len(candidate_rows) == 120, "candidate_matrix_row_count_mismatch", f"Candidate matrix should have 120 rows, found {len(candidate_rows)}.")
    ensure(len(contract_rows) == 120, "contract_matrix_row_count_mismatch", f"Contract matrix should have 120 rows, found {len(contract_rows)}.")
    ensure(run_plan.get("planned_rows") == 120, "run_plan_row_count_mismatch", "Run plan must freeze planned_rows = 120.")
    checks.append({"name": "row_count", "status": "pass"})

    expected_engines = {"pg", "mysql", "spark"}
    candidate_cases = {row["case_id"] for row in candidate_rows}
    contract_cases = {row["case_id"] for row in contract_rows}
    ensure(len(candidate_cases) == 40, "candidate_case_count_mismatch", f"Candidate matrix should have 40 unique cases, found {len(candidate_cases)}.")
    ensure(candidate_cases == contract_cases, "case_set_mismatch", "Contract matrix case set does not match candidate matrix.")

    seen_pairs: set[tuple[str, str]] = set()
    counts_by_engine = {"pg": 0, "mysql": 0, "spark": 0}
    contract_lookup = {(row["case_id"], row["engine"]): row for row in contract_rows}
    run_root = spec["contract"]["planned_run_root"]
    row_artifacts = spec["row_artifacts"]
    for candidate in candidate_rows:
        pair = (candidate["case_id"], candidate["engine"])
        ensure(candidate["engine"] in expected_engines, "unexpected_engine", f"Unexpected engine in candidate matrix: {candidate['engine']}.")
        ensure(pair not in seen_pairs, "duplicate_candidate_pair", f"Duplicate candidate row {pair}.")
        seen_pairs.add(pair)
        counts_by_engine[candidate["engine"]] += 1

        contract = contract_lookup.get(pair)
        ensure(contract is not None, "missing_contract_row", f"Contract matrix is missing row {pair}.")
        ensure(contract["row_id"] == f"{candidate['case_id']}:{candidate['engine']}", "row_id_mismatch", f"Contract row_id mismatch for {pair}.")
        for key in ["denominator_id", "method_id", "route_id", "pool"]:
            ensure(contract[key] == candidate[key], "row_identity_mismatch", f"Contract matrix field {key} mismatches candidate matrix for {pair}.")

        expected_paths = {
            "generated_sql_path": render_template(run_root, row_artifacts["generated_sql"]["path_template"], candidate["case_id"], candidate["engine"]),
            "selected_rules_path": render_template(run_root, row_artifacts["selected_rules"]["path_template"], candidate["case_id"], candidate["engine"]),
            "retrieval_trace_path": render_template(run_root, row_artifacts["retrieval_trace"]["path_template"], candidate["case_id"], candidate["engine"]),
            "prompt_path": render_template(run_root, row_artifacts["prompt_text"]["path_template"], candidate["case_id"], candidate["engine"]),
            "raw_response_path": render_template(run_root, row_artifacts["raw_response"]["path_template"], candidate["case_id"], candidate["engine"]),
            "token_cost_provider_path": render_template(run_root, row_artifacts["token_cost_provider"]["path_template"], candidate["case_id"], candidate["engine"]),
            "environment_snapshot_path": render_template(run_root, row_artifacts["environment_snapshot"]["path_template"], candidate["case_id"], candidate["engine"]),
            "row_run_metadata_path": render_template(run_root, row_artifacts["row_run_metadata"]["path_template"], candidate["case_id"], candidate["engine"]),
        }
        for key, expected_value in expected_paths.items():
            ensure(contract[key] == expected_value, "matrix_path_mismatch", f"Contract matrix field {key} mismatches expected path for {pair}.")

        statuses = set(contract["supported_non_success_statuses"].split("|"))
        for required_status in ["generated", "failed", "blocked", "unsupported", "skipped"]:
            ensure(required_status in statuses, "non_success_status_coverage_missing", f"Contract matrix missing representable status {required_status} for {pair}.")
        ensure(
            contract["row_presence_rule"] == "row_must_remain_present_in_run_event_long_even_if_no_generated_sql",
            "row_presence_rule_mismatch",
            f"Contract matrix row presence rule mismatch for {pair}.",
        )
    ensure(seen_pairs == set(contract_lookup.keys()), "extra_contract_row", "Contract matrix contains rows not present in the denominator candidate matrix.")
    ensure(all(counts_by_engine[engine] == 40 for engine in expected_engines), "engine_row_count_mismatch", f"Expected 40 rows per engine, found {counts_by_engine}.")
    checks.append({"name": "matrix_alignment", "status": "pass", "counts_by_engine": counts_by_engine})
    return checks


def validate_existing_outputs_if_present(spec: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    run_root = REPO_ROOT / spec["contract"]["planned_run_root"]
    if not run_root.exists():
        checks.append({"name": "existing_output_scan", "status": "not_applicable", "reason": "planned run root does not exist yet"})
        return checks

    forbidden_substrings = spec["secret_hygiene"]["forbidden_substrings"]
    package_artifacts = spec["package_artifacts"]

    run_results_path = run_root / package_artifacts["run_results"]["relative_path"]
    if run_results_path.exists():
        text = run_results_path.read_text(encoding="utf-8")
        forbidden = scan_text_for_secrets(text, forbidden_substrings)
        ensure(forbidden is None, "existing_artifact_secret_detected", f"Forbidden token {forbidden} found in {run_results_path}.")
        payload = json.loads(text)
        for key in package_artifacts["run_results"]["required_schema_keys"]:
            ensure(key in payload, "existing_run_results_schema_mismatch", f"{run_results_path} is missing required key {key}.")
        checks.append({"name": "existing_run_results", "status": "pass"})
    else:
        checks.append({"name": "existing_run_results", "status": "not_present"})

    run_event_long_path = run_root / package_artifacts["run_event_long"]["relative_path"]
    if run_event_long_path.exists():
        text = run_event_long_path.read_text(encoding="utf-8")
        forbidden = scan_text_for_secrets(text, forbidden_substrings)
        ensure(forbidden is None, "existing_artifact_secret_detected", f"Forbidden token {forbidden} found in {run_event_long_path}.")
        with run_event_long_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = reader.fieldnames or []
        for column in package_artifacts["run_event_long"]["required_columns"]:
            ensure(column in fieldnames, "existing_run_event_long_schema_mismatch", f"{run_event_long_path} is missing required column {column}.")
        checks.append({"name": "existing_run_event_long", "status": "pass"})
    else:
        checks.append({"name": "existing_run_event_long", "status": "not_present"})
    return checks


def build_markdown_report(result: ValidationResult) -> str:
    lines = [
        "# Formal Artifact Contract Validation Report v1",
        "",
        f"- `status = {result.status}`",
        f"- `message = {result.message}`",
        f"- `current_benchmark_gate_ready = {str(result.current_benchmark_gate_ready).lower()}`",
        f"- `formal_generation_may_start_from_artifact_contract_perspective = {str(result.formal_generation_may_start_from_artifact_contract_perspective).lower()}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in result.summary.items():
        lines.append(f"- `{key} = {value}`")
    lines.extend(["", "## Checks", ""])
    for check in result.checks:
        details = ", ".join(f"{key}={value}" for key, value in check.items() if key != "name")
        lines.append(f"- `{check['name']}`: {details}")
    lines.extend(
        [
            "",
            "## Decision Boundary",
            "",
            "- This validator is pre-generation only.",
            "- It does not run R-Bot or call any API.",
            "- A passing result closes the retained artifact-contract blocker only.",
            "- Denominator-aware formal run evidence remains a separate downstream gate.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_reports(result: ValidationResult) -> None:
    REPORT_JSON_PATH.write_text(
        json.dumps(
            {
                "status": result.status,
                "message": result.message,
                "current_benchmark_gate_ready": result.current_benchmark_gate_ready,
                "formal_generation_may_start_from_artifact_contract_perspective": result.formal_generation_may_start_from_artifact_contract_perspective,
                "checks": result.checks,
                "summary": result.summary,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    REPORT_MD_PATH.write_text(build_markdown_report(result), encoding="utf-8")


def main() -> int:
    try:
        run_plan = load_json(RUN_PLAN_PATH)
        candidate_rows = load_csv_rows(CANDIDATE_MATRIX_PATH)
        contract_rows = load_csv_rows(CONTRACT_MATRIX_PATH)
        spec = load_json(EXPECTED_PATHS_PATH)

        checks: list[dict[str, Any]] = []
        checks.extend(validate_expected_paths_spec(spec))
        checks.extend(validate_matrix_against_plan(run_plan, candidate_rows, contract_rows, spec))
        checks.extend(validate_existing_outputs_if_present(spec))

        result = ValidationResult(
            status="artifact_contract_definition_valid",
            message="Formal run-path artifact contract is internally consistent and ready for human-run validation.",
            current_benchmark_gate_ready=False,
            formal_generation_may_start_from_artifact_contract_perspective=True,
            checks=checks,
            summary={
                "denominator_id": spec["contract"]["denominator_id"],
                "planned_rows": spec["contract"]["planned_rows"],
                "case_count": spec["contract"]["case_count"],
                "engine_count": len(spec["contract"]["engines"]),
                "contract_matrix_rows": len(contract_rows),
                "candidate_matrix_rows": len(candidate_rows),
                "formal_chroma_index_identifier_path": spec["contract"]["formal_chroma_index_identifier_path"],
            },
        )
        write_reports(result)
        return 0
    except ValidationError as exc:
        result = ValidationResult(
            status=exc.status,
            message=exc.message,
            current_benchmark_gate_ready=False,
            formal_generation_may_start_from_artifact_contract_perspective=False,
            checks=[],
            summary={},
        )
        write_reports(result)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
