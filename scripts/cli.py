from __future__ import annotations

import argparse
import csv
import importlib
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports" / "cli"
BASELINE_SMOKE_REPORT_DIR = ROOT / "reports" / "baseline_smoke"
ENV_VARS = ["PGHOST", "MYSQL_HOST", "SPARK_LOCAL_IP"]
SOURCE_REGISTRY = ROOT / "inventory" / "source_registry.csv"
CASE_REGISTRY = ROOT / "inventory" / "case_registry.csv"
ENGINE_ORDER = ("pg", "mysql", "spark")
ENGINE_IDS = set(ENGINE_ORDER)
CONTROL_BASELINE_IDS = {
    "NATIVE_IDENTITY",
    "HUMAN_REFERENCE_POSITIVE",
    "HARD_NEGATIVE_GUARD",
}
NATIVE_IDENTITY_CANARY_DEFAULT_CASES = ["PERF_0006", "PERF_0008"]
SQLGLOT_PG_CANARY_DEFAULT_CASES = ["PERF_0006", "PERF_0008"]
HUMAN_POSITIVE_PG_DEFAULT_CASES = [
    "PERF_0006",
    "PERF_0008",
    "PERF_0013",
    "PERF_0017",
    "PERF_0024",
    "PERF_0033",
    "PERF_0054",
    "CONS_0007",
    "CONS_0012",
]
PERF_CASE_ID_RE = re.compile(r"^PERF_\d{4}$")
PERF_TEMPLATE_CASE_ID = "PERF_0002"
PERF_TEMPLATE_DIR = ROOT / "cases" / "PERF" / PERF_TEMPLATE_CASE_ID
PERF_CASE_ROOT = ROOT / "cases" / "PERF"
PORT_CASE_ID_RE = re.compile(r"^PORT_\d{4}$")
PORT_TEMPLATE_CASE_ID = "PORT_0002"
PORT_TEMPLATE_DIR = ROOT / "cases" / "PORT" / PORT_TEMPLATE_CASE_ID
PORT_CASE_ROOT = ROOT / "cases" / "PORT"
CONS_CASE_ROOT = ROOT / "cases" / "CONS"

SOURCE_REQUIRED_FIELDS = [
    "source_id",
    "source_name",
    "source_family",
    "source_version",
    "owner_or_origin",
    "primary_pool",
    "secondary_pool_or_notes",
    "task_role",
    "expected_use_level",
    "coverage_sql_features",
    "coverage_plan_features",
    "coverage_realism_features",
    "coverage_portability_features",
    "access_type",
    "license_or_terms",
    "acquisition_status",
    "acquisition_priority",
    "batch",
    "three_engine_fit",
    "provenance_risk",
    "curation_risk",
    "decision_needed",
    "storage_path",
    "notes",
    "inspection_status",
    "current_real_status",
    "cases_materialized",
    "current_interpretation",
    "active_for_current_phase",
    "last_updated",
    "notes_link",
]

CASE_REQUIRED_FIELDS = [
    "case_id",
    "primary_pool",
    "source_family",
    "source_detail",
    "origin_kind",
    "current_maturity",
    "benchmark_line",
    "package_engineering_status",
    "validated_engines",
    "tri_engine_closure",
    "formal_skeleton_status",
    "release_grade_status",
    "admission_status",
    "next_gap",
    "current_role",
    "archetype_status",
    "dataset_line",
    "promotion_status",
    "admission_blockers",
    "last_review_doc",
    "last_updated",
    "notes_link",
]

CONTROLLED_FIELDS = {
    "source_registry": {
        "primary_pool": {"performance", "longtail", "consistency", "portability", "none_yet"},
        "acquisition_status": {"staged", "planned", "partial_realized", "not_selected", "in_use"},
        "acquisition_priority": {"high", "medium", "ongoing"},
        "three_engine_fit": {"good", "partial", "unknown"},
        "provenance_risk": {"low", "medium"},
        "curation_risk": {"low", "medium", "high"},
        "decision_needed": {"yes", "no"},
        "active_for_current_phase": {"yes", "no", "limited"},
    },
    "case_registry": {
        "primary_pool": {"performance", "longtail", "consistency", "portability"},
        "origin_kind": {"manual", "external"},
        "benchmark_line": {"pilot_anchor", "common-core", "staged"},
        "tri_engine_closure": {"yes", "no", "partial"},
        "formal_skeleton_status": {"complete", "pre_skeleton", "not_backfilled"},
        "release_grade_status": {"incomplete", "not_assessed"},
        "admission_status": {"none_needed", "admitted", "staged_not_yet_admitted"},
        "archetype_status": {"archetype_complete", "admitted_common_core", "witness_validated"},
        "dataset_line": {"common-core", "not_yet_admitted"},
        "promotion_status": {
            "not_applicable_anchor",
            "admitted_common_core",
            "not_under_review",
            "not_yet_admitted",
        },
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_report_dir() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def write_report(command: str, payload: dict[str, Any]) -> Path:
    ensure_report_dir()
    report_path = REPORT_DIR / f"{command}.json"
    payload["report_path"] = str(report_path.relative_to(ROOT))
    report_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report_path


def write_baseline_smoke_report(report_name: str, payload: dict[str, Any]) -> Path:
    BASELINE_SMOKE_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = BASELINE_SMOKE_REPORT_DIR / report_name
    payload["report_path"] = str(report_path.relative_to(ROOT))
    report_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report_path


def print_and_exit(payload: dict[str, Any], exit_code: int) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return exit_code


def read_registry(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def count_values(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row.get(field, "") for row in rows).items()))


def count_plain_values(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def median_int(values: list[int]) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) // 2


def normalize_baseline_smoke_output_name(value: str) -> str:
    path = Path(value)
    if path.parts[:2] == ("reports", "baseline_smoke"):
        return path.name
    return value


def normalize_sql_for_compare(sql_text: str) -> str:
    return re.sub(r"\s+", " ", sql_text).strip().lower()


def check_status(errors: list[dict[str, Any]], registry_name: str, *error_types: str) -> str:
    return "fail" if any(
        error.get("registry") == registry_name and error.get("type") in error_types
        for error in errors
    ) else "pass"


def parse_engine_set(value: str) -> list[str]:
    engines = {engine for engine in value.split("|") if engine}
    return [engine for engine in ENGINE_ORDER if engine in engines]


def validate_headers(
    registry_name: str,
    headers: list[str],
    required_fields: list[str],
    errors: list[dict[str, Any]],
) -> None:
    missing = [field for field in required_fields if field not in headers]
    extra = [field for field in headers if field not in required_fields]
    if missing:
        errors.append({"registry": registry_name, "type": "missing_fields", "fields": missing})
    if extra:
        errors.append({"registry": registry_name, "type": "unexpected_fields", "fields": extra})
    if headers != required_fields:
        errors.append(
            {
                "registry": registry_name,
                "type": "field_order_mismatch",
                "expected": required_fields,
                "actual": headers,
            }
        )


def validate_unique_ids(
    registry_name: str,
    rows: list[dict[str, str]],
    id_field: str,
    errors: list[dict[str, Any]],
) -> None:
    ids = [row.get(id_field, "") for row in rows]
    blank_rows = [index + 2 for index, value in enumerate(ids) if not value]
    duplicates = sorted(id_value for id_value, count in Counter(ids).items() if id_value and count > 1)
    if blank_rows:
        errors.append({"registry": registry_name, "type": "blank_ids", "rows": blank_rows})
    if duplicates:
        errors.append({"registry": registry_name, "type": "duplicate_ids", "ids": duplicates})


def validate_controlled_fields(
    registry_name: str,
    rows: list[dict[str, str]],
    controlled_fields: dict[str, set[str]],
    errors: list[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for field, allowed_values in controlled_fields.items():
        field_counts = Counter(row.get(field, "") for row in rows)
        counts[field] = dict(sorted(field_counts.items()))
        invalid = sorted(value for value in field_counts if value not in allowed_values)
        if invalid:
            errors.append(
                {
                    "registry": registry_name,
                    "type": "invalid_controlled_values",
                    "field": field,
                    "invalid_values": invalid,
                    "allowed_values": sorted(allowed_values),
                }
            )
    return counts


def validate_engine_values(rows: list[dict[str, str]], errors: list[dict[str, Any]]) -> None:
    invalid_rows = []
    for index, row in enumerate(rows, start=2):
        engines = [engine for engine in row.get("validated_engines", "").split("|") if engine]
        invalid = sorted(engine for engine in engines if engine not in ENGINE_IDS)
        if invalid:
            invalid_rows.append({"row": index, "case_id": row.get("case_id", ""), "invalid": invalid})
    if invalid_rows:
        errors.append(
            {
                "registry": "case_registry",
                "type": "invalid_validated_engines",
                "allowed_values": sorted(ENGINE_IDS),
                "rows": invalid_rows,
            }
        )


def relative_to_root(path: Path) -> str:
    return str(path.relative_to(ROOT))


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path.resolve()


def pool_case_root(pool: str) -> Path:
    if pool == "performance":
        return PERF_CASE_ROOT
    if pool == "portability":
        return PORT_CASE_ROOT
    if pool == "consistency":
        return CONS_CASE_ROOT
    raise ValueError(f"unsupported pool for baseline smoke preflight: {pool}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def first_existing_path(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.is_file():
            return path
    return None


def first_existing_dir(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.is_dir():
            return path
    return None


def baseline_smoke_input_paths(case_root: Path, baseline_id: str) -> list[str]:
    if baseline_id == "NATIVE_IDENTITY":
        rel_paths = ["source.sql", "manifest.yaml"]
    elif baseline_id == "HUMAN_REFERENCE_POSITIVE":
        rel_paths = ["source.sql", "rewrite_pos_01.sql", "manifest.yaml"]
    elif baseline_id == "HARD_NEGATIVE_GUARD":
        rel_paths = ["source.sql", "rewrite_neg_01.sql", "manifest.yaml"]
    elif baseline_id in {"SQLGLOT_OPT_SAME_DIALECT", "LLM_DIRECT_REWRITE_STRONG"}:
        rel_paths = ["source.sql", "manifest.yaml"]
    else:
        rel_paths = ["manifest.yaml"]
    return [relative_to_root(case_root / rel_path) for rel_path in rel_paths]


def baseline_smoke_output_paths(case_id: str, baseline_id: str) -> dict[str, str]:
    base = ROOT / "reports" / "baseline_smoke" / "planned_outputs" / case_id / baseline_id
    return {
        "generated_sql_path": relative_to_root(base / "generated.sql"),
        "record_path": relative_to_root(base / "record.json"),
    }


def baseline_status_record(spec: dict[str, Any]) -> dict[str, Any]:
    baseline_id = spec["baseline_id"]
    status = "ready_for_dry_run"
    blocker = ""
    if baseline_id == "SQLGLOT_OPT_SAME_DIALECT":
        status = "scaffold_only"
        blocker = "SQLGlot adapter command and SQL acceptance policy are not frozen"
    elif baseline_id == "LLM_DIRECT_REWRITE_STRONG":
        status = "scaffold_only"
        blocker = "LLM prompt freeze, model/version freeze, and token/cost logging are not frozen"

    return {
        "baseline_id": baseline_id,
        "smoke_role": spec["smoke_role"],
        "enabled_by_default": bool(spec["enabled_by_default"]),
        "requires_database": bool(spec["requires_database"]),
        "requires_llm": bool(spec["requires_llm"]),
        "requires_sqlglot": bool(spec["requires_sqlglot"]),
        "current_status": status,
        "blocker": blocker,
        "required_adapter": spec["required_adapter"],
    }


def load_json_if_present(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.is_file():
        return None
    try:
        return load_json(path)
    except (json.JSONDecodeError, OSError):
        return None


def recognized_check_signals(checks: dict[str, Any]) -> dict[str, bool]:
    signals = {
        "positive_equal": False,
        "negative_differs": False,
    }
    for key, value in checks.items():
        if not isinstance(value, bool) or not value:
            continue
        lowered = key.lower()
        if "positive" in lowered and ("equal" in lowered or "equals" in lowered):
            signals["positive_equal"] = True
        if "negative" in lowered and ("differ" in lowered or "differs" in lowered):
            signals["negative_differs"] = True
    return signals


def summarize_result_check(result_data: dict[str, Any] | None) -> dict[str, Any]:
    if not result_data:
        return {
            "present": False,
            "ok": None,
            "status": "",
            "schema_interpretation": "absent",
            "signals": {
                "positive_equal": False,
                "negative_differs": False,
            },
        }

    checks = result_data.get("checks")
    signals = recognized_check_signals(checks if isinstance(checks, dict) else {})
    if isinstance(checks, dict):
        interpretation = "recognized_checks" if any(signals.values()) else "unparsed"
    else:
        interpretation = "unparsed"
    return {
        "present": True,
        "ok": result_data.get("ok"),
        "status": result_data.get("status", ""),
        "schema_interpretation": interpretation,
        "signals": signals,
    }


def control_record_result_status(
    baseline_id: str,
    sql_file_exists: bool,
    result_summary: dict[str, Any],
    output_variant_exists: bool,
) -> tuple[str, str]:
    if not sql_file_exists:
        return "missing_evidence", "expected SQL file missing"

    if baseline_id == "NATIVE_IDENTITY":
        if result_summary["present"] or output_variant_exists:
            return "artifact_supported", ""
        return "missing_evidence", "no source result evidence located"

    if baseline_id == "HUMAN_REFERENCE_POSITIVE":
        if result_summary["signals"]["positive_equal"] or output_variant_exists:
            return "artifact_supported", ""
        return "missing_evidence", "no positive result evidence located"

    return "not_applicable", ""


def control_record_negative_status(
    baseline_id: str,
    sql_file_exists: bool,
    result_summary: dict[str, Any],
    output_variant_exists: bool,
) -> tuple[str, str]:
    if baseline_id != "HARD_NEGATIVE_GUARD":
        return "not_applicable", ""
    if not sql_file_exists:
        return "missing_evidence", "expected SQL file missing"
    if result_summary["signals"]["negative_differs"] or output_variant_exists:
        return "artifact_supported", ""
    return "missing_evidence", "no negative rejection evidence located"


def control_record_paths(case_root: Path, baseline_id: str) -> dict[str, Any]:
    result_candidates = [
        case_root / "runs" / "pg" / "result_check.json",
        case_root / "runs" / "result_check.json",
    ]
    plan_candidates = [
        case_root / "runs" / "pg" / "plans" / "plan_check.json",
        case_root / "runs" / "pg" / "plans" / "source.json",
        case_root / "runs" / "pg" / "plans" / "source.txt",
        case_root / "runs" / "plan_check.json",
    ]

    if baseline_id == "NATIVE_IDENTITY":
        variant_id = "source"
        expected_sql = case_root / "source.sql"
        output_candidates = [
            case_root / "runs" / "pg" / "source.tsv",
            case_root / "runs" / "source.tsv",
        ]
        plan_candidates = [
            case_root / "runs" / "pg" / "plans" / "source.json",
            case_root / "runs" / "pg" / "plans" / "source.txt",
            case_root / "runs" / "plan_check.json",
        ]
    elif baseline_id == "HUMAN_REFERENCE_POSITIVE":
        variant_id = "rewrite_pos_01"
        expected_sql = case_root / "rewrite_pos_01.sql"
        output_candidates = [
            case_root / "runs" / "pg" / "rewrite_pos_01.tsv",
            case_root / "runs" / "rewrite_pos_01.tsv",
        ]
        plan_candidates = [
            case_root / "runs" / "pg" / "plans" / "rewrite_pos_01.json",
            case_root / "runs" / "pg" / "plans" / "rewrite_pos_01.txt",
            case_root / "runs" / "plan_check.json",
        ]
    else:
        variant_id = "rewrite_neg_01"
        expected_sql = case_root / "rewrite_neg_01.sql"
        output_candidates = [
            case_root / "runs" / "pg" / "rewrite_neg_01.tsv",
            case_root / "runs" / "rewrite_neg_01.tsv",
        ]
        plan_candidates = [
            case_root / "runs" / "pg" / "plans" / "rewrite_neg_01.json",
            case_root / "runs" / "pg" / "plans" / "rewrite_neg_01.txt",
            case_root / "runs" / "plan_check.json",
        ]

    result_path = first_existing_path(result_candidates)
    plan_path = first_existing_path(plan_candidates)
    output_path = first_existing_path(output_candidates)

    if result_path == result_candidates[0]:
        result_scope = "pg_specific"
    elif result_path == result_candidates[1]:
        result_scope = "case_root"
    else:
        result_scope = "none"

    if plan_path and "runs/pg/plans" in str(plan_path):
        plan_scope = "pg_specific"
    elif plan_path:
        plan_scope = "case_root"
    else:
        plan_scope = "none"

    return {
        "variant_id": variant_id,
        "expected_sql_file": expected_sql.name,
        "expected_sql_path": expected_sql,
        "result_evidence_path": result_path,
        "result_evidence_scope": result_scope,
        "plan_evidence_path": plan_path,
        "plan_evidence_scope": plan_scope,
        "output_artifact_path": output_path,
    }


def build_control_record(case_spec: dict[str, Any], baseline_id: str) -> tuple[dict[str, Any], list[str]]:
    case_root = pool_case_root(case_spec["pool"]) / case_spec["case_id"]
    path_info = control_record_paths(case_root, baseline_id)
    sql_path = path_info["expected_sql_path"]
    sql_exists = sql_path.is_file()
    result_data = load_json_if_present(path_info["result_evidence_path"])
    result_summary = summarize_result_check(result_data)
    output_variant_exists = path_info["output_artifact_path"] is not None

    result_status, result_blocker = control_record_result_status(
        baseline_id,
        sql_exists,
        result_summary,
        output_variant_exists,
    )
    negative_status, negative_blocker = control_record_negative_status(
        baseline_id,
        sql_exists,
        result_summary,
        output_variant_exists,
    )
    plan_status = "artifact_supported" if path_info["plan_evidence_path"] else "missing_evidence"

    blocker = result_blocker or negative_blocker
    failure_category = "none"
    if not sql_exists:
        failure_category = "missing_required_sql"
    elif result_status == "missing_evidence" or negative_status == "missing_evidence":
        failure_category = "missing_evidence"

    notes: list[str] = [
        f"case caveat: {case_spec['caveat']}",
        f"result_check_schema_interpretation: {result_summary['schema_interpretation']}",
    ]
    if result_summary["present"]:
        if result_summary["status"]:
            notes.append(f"result_check_status: {result_summary['status']}")
        if result_summary["ok"] is not None:
            notes.append(f"result_check_ok: {result_summary['ok']}")
    if path_info["output_artifact_path"] is not None:
        notes.append(f"variant_output_artifact: {relative_to_root(path_info['output_artifact_path'])}")
    if path_info["plan_evidence_path"] is None:
        notes.append("no plan evidence artifact located")
    if path_info["result_evidence_path"] is None:
        notes.append("no result_check artifact located")

    record = {
        "baseline_id": baseline_id,
        "case_id": case_spec["case_id"],
        "pool": case_spec["pool"],
        "planned_engine": "postgres",
        "execution_mode": "artifact_record_only",
        "variant_id": path_info["variant_id"],
        "expected_sql_file": path_info["expected_sql_file"],
        "expected_sql_path": relative_to_root(sql_path),
        "sql_file_exists": sql_exists,
        "result_evidence_path": (
            relative_to_root(path_info["result_evidence_path"]) if path_info["result_evidence_path"] else ""
        ),
        "result_evidence_scope": path_info["result_evidence_scope"],
        "plan_evidence_path": (
            relative_to_root(path_info["plan_evidence_path"]) if path_info["plan_evidence_path"] else ""
        ),
        "plan_evidence_scope": path_info["plan_evidence_scope"],
        "result_consistency_status": result_status,
        "negative_rejection_status": negative_status,
        "plan_collection_status": plan_status,
        "failure_category": failure_category,
        "blocker": blocker,
        "notes": notes,
        "artifact_claim_boundary": "existing_artifact_only_no_execution",
    }
    warnings = []
    if result_status == "missing_evidence" or negative_status == "missing_evidence" or plan_status == "missing_evidence":
        warnings.append(f"{baseline_id}/{case_spec['case_id']}: artifact evidence incomplete")
    return record, warnings


def issue_view(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "baseline_id": record.get("baseline_id", ""),
        "case_id": record.get("case_id", ""),
        "pool": record.get("pool", ""),
        "variant_id": record.get("variant_id", ""),
        "failure_category": record.get("failure_category", ""),
        "blocker": record.get("blocker", ""),
        "result_consistency_status": record.get("result_consistency_status", ""),
        "negative_rejection_status": record.get("negative_rejection_status", ""),
        "plan_collection_status": record.get("plan_collection_status", ""),
        "execution_mode": record.get("execution_mode", ""),
        "artifact_claim_boundary": record.get("artifact_claim_boundary", ""),
    }


def pg_env_visibility() -> dict[str, bool]:
    required = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER"]
    visibility = {name: bool(os.environ.get(name)) for name in required}
    visibility["PGPASSWORD"] = bool(os.environ.get("PGPASSWORD"))
    return visibility


def native_identity_validation_schema(case_id: str, pool: str) -> str:
    if pool in {"performance", "consistency"}:
        return f"{case_id.lower()}_validation"
    return ""


def build_native_identity_record(
    case_id: str,
    pool: str,
    source_sql_path: Path | None,
    validation_schema: str,
    search_path_after_set: str,
    statement_timeout_ms: int,
    execution_mode: str,
    execution_status: str,
    pg_env_visible: bool,
    pg_password_present: bool | str,
    failure_category: str,
    blocker: str,
    notes: list[str],
    row_count: int | None = None,
    runtime_ms: int | None = None,
    error_message: str = "",
) -> dict[str, Any]:
    return {
        "baseline_id": "NATIVE_IDENTITY",
        "case_id": case_id,
        "pool": pool,
        "planned_engine": "postgres",
        "execution_mode": execution_mode,
        "source_sql_path": (
            relative_to_root(source_sql_path)
            if source_sql_path and source_sql_path.is_absolute() and source_sql_path.is_relative_to(ROOT)
            else ""
        ),
        "source_sql_exists": bool(source_sql_path and source_sql_path.is_file()),
        "validation_schema": validation_schema,
        "search_path_after_set": search_path_after_set,
        "pg_env_visible": pg_env_visible,
        "pg_password_present": pg_password_present,
        "statement_timeout_ms": statement_timeout_ms,
        "execution_status": execution_status,
        "row_count": row_count,
        "runtime_ms": runtime_ms,
        "result_materialization": "not_persisted",
        "output_scope": "reports_only_no_case_artifact_write",
        "failure_category": failure_category,
        "error_message": error_message,
        "artifact_claim_boundary": (
            "pg_canary_execution_not_benchmark_claim"
            if execution_mode == "pg_execute_canary"
            else "dry_run_no_execution"
        ),
        "notes": notes,
    }


def build_human_positive_record(
    case_id: str,
    pool: str,
    positive_sql_path: Path | None,
    validation_schema: str,
    search_path_after_set: str,
    statement_timeout_ms: int,
    execution_mode: str,
    execution_status: str,
    pg_env_visible: bool,
    pg_password_present: bool | str,
    failure_category: str,
    blocker: str,
    notes: list[str],
    row_count: int | None = None,
    runtime_ms: int | None = None,
    error_message: str = "",
) -> dict[str, Any]:
    return {
        "baseline_id": "HUMAN_REFERENCE_POSITIVE",
        "case_id": case_id,
        "pool": pool,
        "planned_engine": "postgres",
        "execution_mode": execution_mode,
        "positive_sql_path": (
            relative_to_root(positive_sql_path)
            if positive_sql_path and positive_sql_path.is_absolute() and positive_sql_path.is_relative_to(ROOT)
            else ""
        ),
        "positive_sql_exists": bool(positive_sql_path and positive_sql_path.is_file()),
        "validation_schema": validation_schema,
        "search_path_after_set": search_path_after_set,
        "pg_env_visible": pg_env_visible,
        "pg_password_present": pg_password_present,
        "statement_timeout_ms": statement_timeout_ms,
        "execution_status": execution_status,
        "row_count": row_count,
        "runtime_ms": runtime_ms,
        "result_materialization": "not_persisted",
        "output_scope": "reports_only_no_case_artifact_write",
        "failure_category": failure_category,
        "error_message": error_message,
        "artifact_claim_boundary": (
            "pg_positive_execution_not_benchmark_claim"
            if execution_mode == "pg_execute_positive"
            else "dry_run_no_execution"
        ),
        "notes": notes,
    }


def build_hard_negative_record(
    case_id: str,
    pool: str,
    negative_sql_path: Path | None,
    validation_schema: str,
    search_path_after_set: str,
    statement_timeout_ms: int,
    execution_mode: str,
    execution_status: str,
    pg_env_visible: bool,
    pg_password_present: bool | str,
    failure_category: str,
    blocker: str,
    notes: list[str],
    row_count: int | None = None,
    runtime_ms: int | None = None,
    error_message: str = "",
) -> dict[str, Any]:
    return {
        "baseline_id": "HARD_NEGATIVE_GUARD",
        "case_id": case_id,
        "pool": pool,
        "planned_engine": "postgres",
        "execution_mode": execution_mode,
        "negative_sql_path": (
            relative_to_root(negative_sql_path)
            if negative_sql_path and negative_sql_path.is_absolute() and negative_sql_path.is_relative_to(ROOT)
            else ""
        ),
        "negative_sql_exists": bool(negative_sql_path and negative_sql_path.is_file()),
        "validation_schema": validation_schema,
        "search_path_after_set": search_path_after_set,
        "pg_env_visible": pg_env_visible,
        "pg_password_present": pg_password_present,
        "statement_timeout_ms": statement_timeout_ms,
        "execution_status": execution_status,
        "row_count": row_count,
        "runtime_ms": runtime_ms,
        "result_materialization": "not_persisted",
        "output_scope": "reports_only_no_case_artifact_write",
        "failure_category": failure_category,
        "error_message": error_message,
        "artifact_claim_boundary": (
            "pg_negative_execution_not_benchmark_claim"
            if execution_mode == "pg_execute_negative"
            else "dry_run_no_execution"
        ),
        "notes": notes,
    }


def cmd_baseline_smoke_native_identity_pg(args: argparse.Namespace) -> int:
    if args.execute:
        payload = {
            "command": "baseline-smoke-native-identity-pg",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "message": "Use --execute-native-identity for the PG canary. --execute is intentionally not supported here.",
            "errors": [
                {
                    "type": "invalid_execute_flag",
                    "message": "only --execute-native-identity can enable the PG native-identity canary",
                }
            ],
        }
        write_baseline_smoke_report("native_identity_pg_execute_refused_v0.json", payload)
        return print_and_exit(payload, 1)

    config_path = resolve_repo_path(args.config)
    config = load_json(config_path)
    case_index = {case["case_id"]: case for case in config.get("cases", [])}

    selected_case_ids = args.case_id or list(NATIVE_IDENTITY_CANARY_DEFAULT_CASES)
    records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    invalid_cases = [case_id for case_id in selected_case_ids if case_id not in case_index]
    if invalid_cases:
        for case_id in invalid_cases:
            records.append(
                build_native_identity_record(
                    case_id=case_id,
                    pool="",
                    source_sql_path=None,
                    validation_schema="",
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="dry_run" if not args.execute_native_identity else "pg_execute_canary",
                    execution_status="skipped",
                    pg_env_visible=False,
                    pg_password_present="unknown",
                    failure_category="case_not_in_smoke_config",
                    blocker="case_id not found in docs/_scratch/baseline_smoke_common_core_v0.json",
                    notes=["selection refused: case is outside the current smoke config"],
                )
            )
            errors.append(
                {
                    "type": "case_not_in_smoke_config",
                    "case_id": case_id,
                }
            )

    valid_case_ids = [case_id for case_id in selected_case_ids if case_id in case_index]
    selected_specs = [case_index[case_id] for case_id in valid_case_ids]

    env_visibility = pg_env_visibility()
    required_env_visible = all(env_visibility[name] for name in ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER"])
    pg_password_present = env_visibility["PGPASSWORD"]

    if not args.execute_native_identity:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            source_sql_path = pool_case_root(pool) / case_id / "source.sql"
            validation_schema = native_identity_validation_schema(case_id, pool)
            if pool == "portability":
                records.append(
                    build_native_identity_record(
                        case_id=case_id,
                        pool=pool,
                        source_sql_path=source_sql_path,
                        validation_schema=validation_schema,
                        search_path_after_set="",
                        statement_timeout_ms=args.statement_timeout_ms,
                        execution_mode="dry_run",
                        execution_status="skipped",
                        pg_env_visible=required_env_visible,
                        pg_password_present="unknown",
                        failure_category="port_case_not_enabled",
                        blocker="PORT cases are intentionally skipped for the first PG native-identity canary",
                        notes=["dry-run skip: source-dialect portability cases are not enabled in this first PG canary"],
                    )
                )
                continue

            records.append(
                build_native_identity_record(
                    case_id=case_id,
                    pool=pool,
                    source_sql_path=source_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="dry_run",
                    execution_status="planned",
                    pg_env_visible=required_env_visible,
                    pg_password_present="unknown",
                    failure_category="none",
                    blocker="",
                    notes=["dry-run only; no PostgreSQL connection attempted"],
                )
            )

        payload = {
            "command": "baseline-smoke-native-identity-pg",
            "ok": not errors,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "NATIVE_IDENTITY",
            "case_count": len(records),
            "executed_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "skipped_count": sum(1 for record in records if record["execution_status"] == "skipped"),
            "env_blocked_count": 0,
            "records": records,
            "errors": errors,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "sqlglot_generation": "disabled",
                "case_artifact_write": "disabled",
            },
        }
        write_baseline_smoke_report("native_identity_pg_canary_v0.json", payload)
        return print_and_exit(payload, 0 if payload["ok"] else 1)

    if not required_env_visible:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            source_sql_path = pool_case_root(pool) / case_id / "source.sql"
            validation_schema = native_identity_validation_schema(case_id, pool)
            records.append(
                build_native_identity_record(
                    case_id=case_id,
                    pool=pool,
                    source_sql_path=source_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_canary",
                    execution_status="env_blocked",
                    pg_env_visible=False,
                    pg_password_present=pg_password_present,
                    failure_category="missing_pg_env",
                    blocker="required PostgreSQL environment variables are not fully visible",
                    notes=[
                        "execution not attempted",
                        "required env: PGHOST, PGPORT, PGDATABASE, PGUSER",
                    ],
                )
            )
        payload = {
            "command": "baseline-smoke-native-identity-pg",
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "NATIVE_IDENTITY",
            "case_count": len(records),
            "executed_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "skipped_count": 0,
            "env_blocked_count": len(records),
            "records": records,
            "errors": errors,
            "env_visibility": env_visibility,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "sqlglot_generation": "disabled",
                "case_artifact_write": "disabled",
            },
        }
        write_baseline_smoke_report("native_identity_pg_env_blocked_v0.json", payload)
        return print_and_exit(payload, 1)

    try:
        psycopg = importlib.import_module("psycopg")
    except ModuleNotFoundError:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            source_sql_path = pool_case_root(pool) / case_id / "source.sql"
            validation_schema = native_identity_validation_schema(case_id, pool)
            if pool == "portability":
                records.append(
                    build_native_identity_record(
                        case_id=case_id,
                        pool=pool,
                        source_sql_path=source_sql_path,
                        validation_schema=validation_schema,
                        search_path_after_set="",
                        statement_timeout_ms=args.statement_timeout_ms,
                        execution_mode="pg_execute_canary",
                        execution_status="skipped",
                        pg_env_visible=True,
                        pg_password_present=pg_password_present,
                        failure_category="port_case_not_enabled",
                        blocker="PORT cases are intentionally skipped for the first PG native-identity canary",
                        notes=["execution skip: portability source SQL is not enabled in this canary"],
                    )
                )
            else:
                records.append(
                    build_native_identity_record(
                        case_id=case_id,
                        pool=pool,
                        source_sql_path=source_sql_path,
                        validation_schema=validation_schema,
                        search_path_after_set="",
                        statement_timeout_ms=args.statement_timeout_ms,
                        execution_mode="pg_execute_canary",
                        execution_status="failed",
                        pg_env_visible=True,
                        pg_password_present=pg_password_present,
                        failure_category="psycopg_unavailable",
                        blocker="psycopg is not installed in the current environment",
                        notes=["execution not attempted because no PostgreSQL client library is available"],
                    )
                )
        payload = {
            "command": "baseline-smoke-native-identity-pg",
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "NATIVE_IDENTITY",
            "case_count": len(records),
            "executed_count": 0,
            "success_count": 0,
            "failed_count": sum(1 for record in records if record["execution_status"] == "failed"),
            "skipped_count": sum(1 for record in records if record["execution_status"] == "skipped"),
            "env_blocked_count": 0,
            "records": records,
            "errors": errors,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "sqlglot_generation": "disabled",
                "case_artifact_write": "disabled",
            },
        }
        write_baseline_smoke_report("native_identity_pg_canary_v0.json", payload)
        return print_and_exit(payload, 1)

    for case_spec in selected_specs:
        case_id = case_spec["case_id"]
        pool = case_spec["pool"]
        source_sql_path = pool_case_root(pool) / case_id / "source.sql"
        validation_schema = native_identity_validation_schema(case_id, pool)

        if pool == "portability":
            records.append(
                build_native_identity_record(
                    case_id=case_id,
                    pool=pool,
                    source_sql_path=source_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_canary",
                    execution_status="skipped",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category="port_case_not_enabled",
                    blocker="PORT cases are intentionally skipped for the first PG native-identity canary",
                    notes=["execution skip: portability source SQL is not enabled in this canary"],
                )
            )
            continue

        if not source_sql_path.is_file():
            records.append(
                build_native_identity_record(
                    case_id=case_id,
                    pool=pool,
                    source_sql_path=source_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_canary",
                    execution_status="failed",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category="missing_source_sql",
                    blocker="source.sql is missing",
                    notes=["execution not attempted because source.sql is absent"],
                )
            )
            continue

        sql_text = source_sql_path.read_text(encoding="utf-8")
        start = time.perf_counter()
        search_path_after_set = ""
        try:
            with psycopg.connect(
                host=os.environ["PGHOST"],
                port=os.environ["PGPORT"],
                dbname=os.environ["PGDATABASE"],
                user=os.environ["PGUSER"],
                password=os.environ.get("PGPASSWORD"),
                options=(
                    f"-c statement_timeout={args.statement_timeout_ms} "
                    "-c default_transaction_read_only=on"
                ),
            ) as conn:
                with conn.cursor() as cur:
                    if validation_schema:
                        cur.execute(
                            "SELECT to_regnamespace(%s)",
                            (validation_schema,),
                        )
                        schema_name = cur.fetchone()[0]
                        if not schema_name:
                            records.append(
                                build_native_identity_record(
                                    case_id=case_id,
                                    pool=pool,
                                    source_sql_path=source_sql_path,
                                    validation_schema=validation_schema,
                                    search_path_after_set="",
                                    statement_timeout_ms=args.statement_timeout_ms,
                                    execution_mode="pg_execute_canary",
                                    execution_status="failed",
                                    pg_env_visible=True,
                                    pg_password_present=pg_password_present,
                                    failure_category="missing_validation_schema",
                                    blocker="derived validation schema does not exist in PostgreSQL",
                                    notes=["execution attempted", "search_path not set because validation schema was missing"],
                                    runtime_ms=int((time.perf_counter() - start) * 1000),
                                    error_message=f"validation schema not found: {validation_schema}",
                                )
                            )
                            continue
                        cur.execute(
                            psycopg.sql.SQL("SET search_path TO {}, public").format(
                                psycopg.sql.Identifier(validation_schema)
                            )
                        )
                        cur.execute("SHOW search_path")
                        search_path_after_set = str(cur.fetchone()[0])
                    cur.execute(sql_text)
                    if cur.description is not None:
                        rows = cur.fetchall()
                        row_count = len(rows)
                    else:
                        row_count = cur.rowcount if cur.rowcount >= 0 else None
            runtime_ms = int((time.perf_counter() - start) * 1000)
            records.append(
                build_native_identity_record(
                    case_id=case_id,
                    pool=pool,
                    source_sql_path=source_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set=search_path_after_set,
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_canary",
                    execution_status="success",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category="none",
                    blocker="",
                    notes=["source.sql executed under read-only PG canary mode"],
                    row_count=row_count,
                    runtime_ms=runtime_ms,
                )
            )
        except Exception as exc:
            runtime_ms = int((time.perf_counter() - start) * 1000)
            records.append(
                build_native_identity_record(
                    case_id=case_id,
                    pool=pool,
                    source_sql_path=source_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set=search_path_after_set,
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_canary",
                    execution_status="failed",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category=type(exc).__name__,
                    blocker="PostgreSQL canary execution failed",
                    notes=["execution attempted", "no case-local artifacts were written"],
                    runtime_ms=runtime_ms,
                    error_message=str(exc),
                )
            )

    payload = {
        "command": "baseline-smoke-native-identity-pg",
        "ok": not errors and not any(record["execution_status"] == "failed" for record in records),
        "ran_at_utc": utc_now(),
        "config_path": relative_to_root(config_path),
        "engine_scope": "postgres",
        "baseline_id": "NATIVE_IDENTITY",
        "case_count": len(records),
        "executed_count": sum(1 for record in records if record["execution_status"] in {"success", "failed"}),
        "success_count": sum(1 for record in records if record["execution_status"] == "success"),
        "failed_count": sum(1 for record in records if record["execution_status"] == "failed"),
        "skipped_count": sum(1 for record in records if record["execution_status"] == "skipped"),
        "env_blocked_count": 0,
        "records": records,
        "errors": errors,
        "env_visibility": env_visibility,
        "guardrails": {
            "mysql_execution": "disabled",
            "spark_execution": "disabled",
            "llm_execution": "disabled",
            "sqlglot_generation": "disabled",
            "case_artifact_write": "disabled",
        },
    }
    write_baseline_smoke_report("native_identity_pg_canary_v0.json", payload)
    return print_and_exit(payload, 0 if payload["ok"] else 1)


def cmd_baseline_smoke_human_positive_pg(args: argparse.Namespace) -> int:
    if args.execute:
        payload = {
            "command": "baseline-smoke-human-positive-pg",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "message": "Use --execute-human-positive for the PG positive-reference canary. --execute is intentionally not supported here.",
            "errors": [
                {
                    "type": "invalid_execute_flag",
                    "message": "only --execute-human-positive can enable the PG positive-reference canary",
                }
            ],
        }
        write_baseline_smoke_report("human_reference_positive_pg_execute_refused_v0.json", payload)
        return print_and_exit(payload, 1)

    config_path = resolve_repo_path(args.config)
    config = load_json(config_path)
    case_index = {case["case_id"]: case for case in config.get("cases", [])}

    selected_case_ids = args.case_id or list(HUMAN_POSITIVE_PG_DEFAULT_CASES)
    records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    invalid_cases = [case_id for case_id in selected_case_ids if case_id not in case_index]
    if invalid_cases:
        for case_id in invalid_cases:
            records.append(
                build_human_positive_record(
                    case_id=case_id,
                    pool="",
                    positive_sql_path=None,
                    validation_schema="",
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="dry_run" if not args.execute_human_positive else "pg_execute_positive",
                    execution_status="skipped",
                    pg_env_visible=False,
                    pg_password_present="unknown",
                    failure_category="case_not_in_smoke_config",
                    blocker="case_id not found in docs/_scratch/baseline_smoke_common_core_v0.json",
                    notes=["selection refused: case is outside the current smoke config"],
                )
            )
            errors.append(
                {
                    "type": "case_not_in_smoke_config",
                    "case_id": case_id,
                }
            )

    valid_case_ids = [case_id for case_id in selected_case_ids if case_id in case_index]
    selected_specs = [case_index[case_id] for case_id in valid_case_ids]

    env_visibility = pg_env_visibility()
    required_env_visible = all(env_visibility[name] for name in ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER"])
    pg_password_present = env_visibility["PGPASSWORD"]

    if not args.execute_human_positive:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            positive_sql_path = pool_case_root(pool) / case_id / "rewrite_pos_01.sql"
            validation_schema = native_identity_validation_schema(case_id, pool)
            if pool == "portability":
                records.append(
                    build_human_positive_record(
                        case_id=case_id,
                        pool=pool,
                        positive_sql_path=positive_sql_path,
                        validation_schema=validation_schema,
                        search_path_after_set="",
                        statement_timeout_ms=args.statement_timeout_ms,
                        execution_mode="dry_run",
                        execution_status="skipped",
                        pg_env_visible=required_env_visible,
                        pg_password_present="unknown",
                        failure_category="port_case_not_enabled",
                        blocker="PORT cases are intentionally skipped for the first PG positive-reference canary",
                        notes=["dry-run skip: portability positive rewrites are not enabled in this first PG canary"],
                    )
                )
                continue

            records.append(
                build_human_positive_record(
                    case_id=case_id,
                    pool=pool,
                    positive_sql_path=positive_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="dry_run",
                    execution_status="planned",
                    pg_env_visible=required_env_visible,
                    pg_password_present="unknown",
                    failure_category="none",
                    blocker="",
                    notes=["dry-run only; no PostgreSQL connection attempted"],
                )
            )

        payload = {
            "command": "baseline-smoke-human-positive-pg",
            "ok": not errors,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "HUMAN_REFERENCE_POSITIVE",
            "case_count": len(records),
            "executed_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "skipped_count": sum(1 for record in records if record["execution_status"] == "skipped"),
            "env_blocked_count": 0,
            "records": records,
            "errors": errors,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "sqlglot_generation": "disabled",
                "case_artifact_write": "disabled",
            },
        }
        write_baseline_smoke_report("human_reference_positive_pg_v0.json", payload)
        return print_and_exit(payload, 0 if payload["ok"] else 1)

    if not required_env_visible:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            positive_sql_path = pool_case_root(pool) / case_id / "rewrite_pos_01.sql"
            validation_schema = native_identity_validation_schema(case_id, pool)
            records.append(
                build_human_positive_record(
                    case_id=case_id,
                    pool=pool,
                    positive_sql_path=positive_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_positive",
                    execution_status="env_blocked",
                    pg_env_visible=False,
                    pg_password_present=pg_password_present,
                    failure_category="missing_pg_env",
                    blocker="required PostgreSQL environment variables are not fully visible",
                    notes=["execution not attempted", "required env: PGHOST, PGPORT, PGDATABASE, PGUSER"],
                )
            )
        payload = {
            "command": "baseline-smoke-human-positive-pg",
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "HUMAN_REFERENCE_POSITIVE",
            "case_count": len(records),
            "executed_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "skipped_count": 0,
            "env_blocked_count": len(records),
            "records": records,
            "errors": errors,
            "env_visibility": env_visibility,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "sqlglot_generation": "disabled",
                "case_artifact_write": "disabled",
            },
        }
        write_baseline_smoke_report("human_reference_positive_pg_env_blocked_v0.json", payload)
        return print_and_exit(payload, 1)

    try:
        psycopg = importlib.import_module("psycopg")
    except ModuleNotFoundError:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            positive_sql_path = pool_case_root(pool) / case_id / "rewrite_pos_01.sql"
            validation_schema = native_identity_validation_schema(case_id, pool)
            if pool == "portability":
                records.append(
                    build_human_positive_record(
                        case_id=case_id,
                        pool=pool,
                        positive_sql_path=positive_sql_path,
                        validation_schema=validation_schema,
                        search_path_after_set="",
                        statement_timeout_ms=args.statement_timeout_ms,
                        execution_mode="pg_execute_positive",
                        execution_status="skipped",
                        pg_env_visible=True,
                        pg_password_present=pg_password_present,
                        failure_category="port_case_not_enabled",
                        blocker="PORT cases are intentionally skipped for the first PG positive-reference canary",
                        notes=["execution skip: portability positive rewrites are not enabled in this canary"],
                    )
                )
            else:
                records.append(
                    build_human_positive_record(
                        case_id=case_id,
                        pool=pool,
                        positive_sql_path=positive_sql_path,
                        validation_schema=validation_schema,
                        search_path_after_set="",
                        statement_timeout_ms=args.statement_timeout_ms,
                        execution_mode="pg_execute_positive",
                        execution_status="failed",
                        pg_env_visible=True,
                        pg_password_present=pg_password_present,
                        failure_category="psycopg_unavailable",
                        blocker="psycopg is not installed in the current environment",
                        notes=["execution not attempted because no PostgreSQL client library is available"],
                    )
                )
        payload = {
            "command": "baseline-smoke-human-positive-pg",
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "HUMAN_REFERENCE_POSITIVE",
            "case_count": len(records),
            "executed_count": 0,
            "success_count": 0,
            "failed_count": sum(1 for record in records if record["execution_status"] == "failed"),
            "skipped_count": sum(1 for record in records if record["execution_status"] == "skipped"),
            "env_blocked_count": 0,
            "records": records,
            "errors": errors,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "sqlglot_generation": "disabled",
                "case_artifact_write": "disabled",
            },
        }
        write_baseline_smoke_report("human_reference_positive_pg_v0.json", payload)
        return print_and_exit(payload, 1)

    for case_spec in selected_specs:
        case_id = case_spec["case_id"]
        pool = case_spec["pool"]
        positive_sql_path = pool_case_root(pool) / case_id / "rewrite_pos_01.sql"
        validation_schema = native_identity_validation_schema(case_id, pool)

        if pool == "portability":
            records.append(
                build_human_positive_record(
                    case_id=case_id,
                    pool=pool,
                    positive_sql_path=positive_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_positive",
                    execution_status="skipped",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category="port_case_not_enabled",
                    blocker="PORT cases are intentionally skipped for the first PG positive-reference canary",
                    notes=["execution skip: portability positive rewrites are not enabled in this canary"],
                )
            )
            continue

        if not positive_sql_path.is_file():
            records.append(
                build_human_positive_record(
                    case_id=case_id,
                    pool=pool,
                    positive_sql_path=positive_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_positive",
                    execution_status="failed",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category="missing_positive_sql",
                    blocker="rewrite_pos_01.sql is missing",
                    notes=["execution not attempted because rewrite_pos_01.sql is absent"],
                )
            )
            continue

        sql_text = positive_sql_path.read_text(encoding="utf-8")
        start = time.perf_counter()
        search_path_after_set = ""
        try:
            with psycopg.connect(
                host=os.environ["PGHOST"],
                port=os.environ["PGPORT"],
                dbname=os.environ["PGDATABASE"],
                user=os.environ["PGUSER"],
                password=os.environ.get("PGPASSWORD"),
                options=(
                    f"-c statement_timeout={args.statement_timeout_ms} "
                    "-c default_transaction_read_only=on"
                ),
            ) as conn:
                with conn.cursor() as cur:
                    if validation_schema:
                        cur.execute(
                            "SELECT to_regnamespace(%s)",
                            (validation_schema,),
                        )
                        schema_name = cur.fetchone()[0]
                        if not schema_name:
                            records.append(
                                build_human_positive_record(
                                    case_id=case_id,
                                    pool=pool,
                                    positive_sql_path=positive_sql_path,
                                    validation_schema=validation_schema,
                                    search_path_after_set="",
                                    statement_timeout_ms=args.statement_timeout_ms,
                                    execution_mode="pg_execute_positive",
                                    execution_status="failed",
                                    pg_env_visible=True,
                                    pg_password_present=pg_password_present,
                                    failure_category="missing_validation_schema",
                                    blocker="derived validation schema does not exist in PostgreSQL",
                                    notes=["execution attempted", "search_path not set because validation schema was missing"],
                                    runtime_ms=int((time.perf_counter() - start) * 1000),
                                    error_message=f"validation schema not found: {validation_schema}",
                                )
                            )
                            continue
                        cur.execute(
                            psycopg.sql.SQL("SET search_path TO {}, public").format(
                                psycopg.sql.Identifier(validation_schema)
                            )
                        )
                        cur.execute("SHOW search_path")
                        search_path_after_set = str(cur.fetchone()[0])
                    cur.execute(sql_text)
                    if cur.description is not None:
                        rows = cur.fetchall()
                        row_count = len(rows)
                    else:
                        row_count = cur.rowcount if cur.rowcount >= 0 else None
            runtime_ms = int((time.perf_counter() - start) * 1000)
            records.append(
                build_human_positive_record(
                    case_id=case_id,
                    pool=pool,
                    positive_sql_path=positive_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set=search_path_after_set,
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_positive",
                    execution_status="success",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category="none",
                    blocker="",
                    notes=["rewrite_pos_01.sql executed under read-only PG positive-reference mode"],
                    row_count=row_count,
                    runtime_ms=runtime_ms,
                )
            )
        except Exception as exc:
            runtime_ms = int((time.perf_counter() - start) * 1000)
            records.append(
                build_human_positive_record(
                    case_id=case_id,
                    pool=pool,
                    positive_sql_path=positive_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set=search_path_after_set,
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_positive",
                    execution_status="failed",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category=type(exc).__name__,
                    blocker="PostgreSQL positive-reference canary execution failed",
                    notes=["execution attempted", "no case-local artifacts were written"],
                    runtime_ms=runtime_ms,
                    error_message=str(exc),
                )
            )

    payload = {
        "command": "baseline-smoke-human-positive-pg",
        "ok": not errors and not any(record["execution_status"] == "failed" for record in records),
        "ran_at_utc": utc_now(),
        "config_path": relative_to_root(config_path),
        "engine_scope": "postgres",
        "baseline_id": "HUMAN_REFERENCE_POSITIVE",
        "case_count": len(records),
        "executed_count": sum(1 for record in records if record["execution_status"] in {"success", "failed"}),
        "success_count": sum(1 for record in records if record["execution_status"] == "success"),
        "failed_count": sum(1 for record in records if record["execution_status"] == "failed"),
        "skipped_count": sum(1 for record in records if record["execution_status"] == "skipped"),
        "env_blocked_count": 0,
        "records": records,
        "errors": errors,
        "env_visibility": env_visibility,
        "guardrails": {
            "mysql_execution": "disabled",
            "spark_execution": "disabled",
            "llm_execution": "disabled",
            "sqlglot_generation": "disabled",
            "case_artifact_write": "disabled",
        },
    }
    write_baseline_smoke_report("human_reference_positive_pg_v0.json", payload)
    return print_and_exit(payload, 0 if payload["ok"] else 1)


def cmd_baseline_smoke_hard_negative_pg(args: argparse.Namespace) -> int:
    if args.execute:
        payload = {
            "command": "baseline-smoke-hard-negative-pg",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "message": "Use --execute-hard-negative for the PG hard-negative canary. --execute is intentionally not supported here.",
            "errors": [
                {
                    "type": "invalid_execute_flag",
                    "message": "only --execute-hard-negative can enable the PG hard-negative canary",
                }
            ],
        }
        write_baseline_smoke_report("hard_negative_guard_pg_execute_refused_v0.json", payload)
        return print_and_exit(payload, 1)

    config_path = resolve_repo_path(args.config)
    config = load_json(config_path)
    case_index = {case["case_id"]: case for case in config.get("cases", [])}

    selected_case_ids = args.case_id or list(HUMAN_POSITIVE_PG_DEFAULT_CASES)
    records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    invalid_cases = [case_id for case_id in selected_case_ids if case_id not in case_index]
    if invalid_cases:
        for case_id in invalid_cases:
            records.append(
                build_hard_negative_record(
                    case_id=case_id,
                    pool="",
                    negative_sql_path=None,
                    validation_schema="",
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="dry_run" if not args.execute_hard_negative else "pg_execute_negative",
                    execution_status="skipped",
                    pg_env_visible=False,
                    pg_password_present="unknown",
                    failure_category="case_not_in_smoke_config",
                    blocker="case_id not found in docs/_scratch/baseline_smoke_common_core_v0.json",
                    notes=["selection refused: case is outside the current smoke config"],
                )
            )
            errors.append(
                {
                    "type": "case_not_in_smoke_config",
                    "case_id": case_id,
                }
            )

    valid_case_ids = [case_id for case_id in selected_case_ids if case_id in case_index]
    selected_specs = [case_index[case_id] for case_id in valid_case_ids]

    env_visibility = pg_env_visibility()
    required_env_visible = all(env_visibility[name] for name in ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER"])
    pg_password_present = env_visibility["PGPASSWORD"]

    if not args.execute_hard_negative:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            negative_sql_path = pool_case_root(pool) / case_id / "rewrite_neg_01.sql"
            validation_schema = native_identity_validation_schema(case_id, pool)
            if pool == "portability":
                records.append(
                    build_hard_negative_record(
                        case_id=case_id,
                        pool=pool,
                        negative_sql_path=negative_sql_path,
                        validation_schema=validation_schema,
                        search_path_after_set="",
                        statement_timeout_ms=args.statement_timeout_ms,
                        execution_mode="dry_run",
                        execution_status="skipped",
                        pg_env_visible=required_env_visible,
                        pg_password_present="unknown",
                        failure_category="port_case_not_enabled",
                        blocker="PORT cases are intentionally skipped for the first PG hard-negative canary",
                        notes=["dry-run skip: portability negative rewrites are not enabled in this first PG canary"],
                    )
                )
                continue

            records.append(
                build_hard_negative_record(
                    case_id=case_id,
                    pool=pool,
                    negative_sql_path=negative_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="dry_run",
                    execution_status="planned",
                    pg_env_visible=required_env_visible,
                    pg_password_present="unknown",
                    failure_category="none",
                    blocker="",
                    notes=["dry-run only; no PostgreSQL connection attempted"],
                )
            )

        payload = {
            "command": "baseline-smoke-hard-negative-pg",
            "ok": not errors,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "HARD_NEGATIVE_GUARD",
            "case_count": len(records),
            "executed_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "skipped_count": sum(1 for record in records if record["execution_status"] == "skipped"),
            "env_blocked_count": 0,
            "records": records,
            "errors": errors,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "sqlglot_generation": "disabled",
                "case_artifact_write": "disabled",
            },
        }
        write_baseline_smoke_report("hard_negative_guard_pg_v0.json", payload)
        return print_and_exit(payload, 0 if payload["ok"] else 1)

    if not required_env_visible:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            negative_sql_path = pool_case_root(pool) / case_id / "rewrite_neg_01.sql"
            validation_schema = native_identity_validation_schema(case_id, pool)
            records.append(
                build_hard_negative_record(
                    case_id=case_id,
                    pool=pool,
                    negative_sql_path=negative_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_negative",
                    execution_status="env_blocked",
                    pg_env_visible=False,
                    pg_password_present=pg_password_present,
                    failure_category="missing_pg_env",
                    blocker="required PostgreSQL environment variables are not fully visible",
                    notes=["execution not attempted", "required env: PGHOST, PGPORT, PGDATABASE, PGUSER"],
                )
            )
        payload = {
            "command": "baseline-smoke-hard-negative-pg",
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "HARD_NEGATIVE_GUARD",
            "case_count": len(records),
            "executed_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "skipped_count": 0,
            "env_blocked_count": len(records),
            "records": records,
            "errors": errors,
            "env_visibility": env_visibility,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "sqlglot_generation": "disabled",
                "case_artifact_write": "disabled",
            },
        }
        write_baseline_smoke_report("hard_negative_guard_pg_env_blocked_v0.json", payload)
        return print_and_exit(payload, 1)

    try:
        psycopg = importlib.import_module("psycopg")
    except ModuleNotFoundError:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            negative_sql_path = pool_case_root(pool) / case_id / "rewrite_neg_01.sql"
            validation_schema = native_identity_validation_schema(case_id, pool)
            if pool == "portability":
                records.append(
                    build_hard_negative_record(
                        case_id=case_id,
                        pool=pool,
                        negative_sql_path=negative_sql_path,
                        validation_schema=validation_schema,
                        search_path_after_set="",
                        statement_timeout_ms=args.statement_timeout_ms,
                        execution_mode="pg_execute_negative",
                        execution_status="skipped",
                        pg_env_visible=True,
                        pg_password_present=pg_password_present,
                        failure_category="port_case_not_enabled",
                        blocker="PORT cases are intentionally skipped for the first PG hard-negative canary",
                        notes=["execution skip: portability negative rewrites are not enabled in this canary"],
                    )
                )
            else:
                records.append(
                    build_hard_negative_record(
                        case_id=case_id,
                        pool=pool,
                        negative_sql_path=negative_sql_path,
                        validation_schema=validation_schema,
                        search_path_after_set="",
                        statement_timeout_ms=args.statement_timeout_ms,
                        execution_mode="pg_execute_negative",
                        execution_status="failed",
                        pg_env_visible=True,
                        pg_password_present=pg_password_present,
                        failure_category="psycopg_unavailable",
                        blocker="psycopg is not installed in the current environment",
                        notes=["execution not attempted because no PostgreSQL client library is available"],
                    )
                )
        payload = {
            "command": "baseline-smoke-hard-negative-pg",
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "HARD_NEGATIVE_GUARD",
            "case_count": len(records),
            "executed_count": 0,
            "success_count": 0,
            "failed_count": sum(1 for record in records if record["execution_status"] == "failed"),
            "skipped_count": sum(1 for record in records if record["execution_status"] == "skipped"),
            "env_blocked_count": 0,
            "records": records,
            "errors": errors,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "sqlglot_generation": "disabled",
                "case_artifact_write": "disabled",
            },
        }
        write_baseline_smoke_report("hard_negative_guard_pg_v0.json", payload)
        return print_and_exit(payload, 1)

    for case_spec in selected_specs:
        case_id = case_spec["case_id"]
        pool = case_spec["pool"]
        negative_sql_path = pool_case_root(pool) / case_id / "rewrite_neg_01.sql"
        validation_schema = native_identity_validation_schema(case_id, pool)

        if pool == "portability":
            records.append(
                build_hard_negative_record(
                    case_id=case_id,
                    pool=pool,
                    negative_sql_path=negative_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_negative",
                    execution_status="skipped",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category="port_case_not_enabled",
                    blocker="PORT cases are intentionally skipped for the first PG hard-negative canary",
                    notes=["execution skip: portability negative rewrites are not enabled in this canary"],
                )
            )
            continue

        if not negative_sql_path.is_file():
            records.append(
                build_hard_negative_record(
                    case_id=case_id,
                    pool=pool,
                    negative_sql_path=negative_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set="",
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_negative",
                    execution_status="failed",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category="missing_negative_sql",
                    blocker="rewrite_neg_01.sql is missing",
                    notes=["execution not attempted because rewrite_neg_01.sql is absent"],
                )
            )
            continue

        sql_text = negative_sql_path.read_text(encoding="utf-8")
        start = time.perf_counter()
        search_path_after_set = ""
        try:
            with psycopg.connect(
                host=os.environ["PGHOST"],
                port=os.environ["PGPORT"],
                dbname=os.environ["PGDATABASE"],
                user=os.environ["PGUSER"],
                password=os.environ.get("PGPASSWORD"),
                options=(
                    f"-c statement_timeout={args.statement_timeout_ms} "
                    "-c default_transaction_read_only=on"
                ),
            ) as conn:
                with conn.cursor() as cur:
                    if validation_schema:
                        cur.execute("SELECT to_regnamespace(%s)", (validation_schema,))
                        schema_name = cur.fetchone()[0]
                        if not schema_name:
                            records.append(
                                build_hard_negative_record(
                                    case_id=case_id,
                                    pool=pool,
                                    negative_sql_path=negative_sql_path,
                                    validation_schema=validation_schema,
                                    search_path_after_set="",
                                    statement_timeout_ms=args.statement_timeout_ms,
                                    execution_mode="pg_execute_negative",
                                    execution_status="failed",
                                    pg_env_visible=True,
                                    pg_password_present=pg_password_present,
                                    failure_category="missing_validation_schema",
                                    blocker="derived validation schema does not exist in PostgreSQL",
                                    notes=["execution attempted", "search_path not set because validation schema was missing"],
                                    runtime_ms=int((time.perf_counter() - start) * 1000),
                                    error_message=f"validation schema not found: {validation_schema}",
                                )
                            )
                            continue
                        cur.execute(
                            psycopg.sql.SQL("SET search_path TO {}, public").format(
                                psycopg.sql.Identifier(validation_schema)
                            )
                        )
                        cur.execute("SHOW search_path")
                        search_path_after_set = str(cur.fetchone()[0])
                    cur.execute(sql_text)
                    if cur.description is not None:
                        rows = cur.fetchall()
                        row_count = len(rows)
                    else:
                        row_count = cur.rowcount if cur.rowcount >= 0 else None
            runtime_ms = int((time.perf_counter() - start) * 1000)
            records.append(
                build_hard_negative_record(
                    case_id=case_id,
                    pool=pool,
                    negative_sql_path=negative_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set=search_path_after_set,
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_negative",
                    execution_status="success",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category="none",
                    blocker="",
                    notes=["rewrite_neg_01.sql executed under read-only PG hard-negative mode"],
                    row_count=row_count,
                    runtime_ms=runtime_ms,
                )
            )
        except Exception as exc:
            runtime_ms = int((time.perf_counter() - start) * 1000)
            records.append(
                build_hard_negative_record(
                    case_id=case_id,
                    pool=pool,
                    negative_sql_path=negative_sql_path,
                    validation_schema=validation_schema,
                    search_path_after_set=search_path_after_set,
                    statement_timeout_ms=args.statement_timeout_ms,
                    execution_mode="pg_execute_negative",
                    execution_status="failed",
                    pg_env_visible=True,
                    pg_password_present=pg_password_present,
                    failure_category=type(exc).__name__,
                    blocker="PostgreSQL hard-negative canary execution failed",
                    notes=["execution attempted", "no case-local artifacts were written"],
                    runtime_ms=runtime_ms,
                    error_message=str(exc),
                )
            )

    payload = {
        "command": "baseline-smoke-hard-negative-pg",
        "ok": not errors and not any(record["execution_status"] == "failed" for record in records),
        "ran_at_utc": utc_now(),
        "config_path": relative_to_root(config_path),
        "engine_scope": "postgres",
        "baseline_id": "HARD_NEGATIVE_GUARD",
        "case_count": len(records),
        "executed_count": sum(1 for record in records if record["execution_status"] in {"success", "failed"}),
        "success_count": sum(1 for record in records if record["execution_status"] == "success"),
        "failed_count": sum(1 for record in records if record["execution_status"] == "failed"),
        "skipped_count": sum(1 for record in records if record["execution_status"] == "skipped"),
        "env_blocked_count": 0,
        "records": records,
        "errors": errors,
        "env_visibility": env_visibility,
        "guardrails": {
            "mysql_execution": "disabled",
            "spark_execution": "disabled",
            "llm_execution": "disabled",
            "sqlglot_generation": "disabled",
            "case_artifact_write": "disabled",
        },
    }
    write_baseline_smoke_report("hard_negative_guard_pg_v0.json", payload)
    return print_and_exit(payload, 0 if payload["ok"] else 1)


def cmd_baseline_smoke_control_records(args: argparse.Namespace) -> int:
    if args.execute:
        payload = {
            "command": "baseline-smoke-control-records",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "execution_mode": "execute_requested_but_blocked",
            "message": "Non-dry-run execution is intentionally not implemented yet. Use artifact-only control record generation.",
            "errors": [
                {
                    "type": "execution_not_implemented",
                    "message": "control baseline record scaffold currently supports artifact_record_only mode",
                }
            ],
        }
        write_baseline_smoke_report("control_records_execute_refused_common_core_v0.json", payload)
        return print_and_exit(payload, 1)

    config_path = resolve_repo_path(args.config)
    config = load_json(config_path)
    selected_baselines = list(dict.fromkeys(args.baseline_id or sorted(CONTROL_BASELINE_IDS)))

    unsupported_requested = [baseline_id for baseline_id in selected_baselines if baseline_id not in CONTROL_BASELINE_IDS]
    if unsupported_requested:
        payload = {
            "command": "baseline-smoke-control-records",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "execution_mode": "artifact_record_only",
            "config_path": relative_to_root(config_path),
            "message": "Unsupported baselines were requested for control-record generation.",
            "errors": [
                {
                    "type": "unsupported_baseline_ids",
                    "baseline_ids": unsupported_requested,
                    "supported_baseline_ids": sorted(CONTROL_BASELINE_IDS),
                }
            ],
        }
        write_baseline_smoke_report("control_records_common_core_v0.json", payload)
        return print_and_exit(payload, 1)

    config_baselines = {item["baseline_id"] for item in config["baselines"]}
    missing_from_config = [baseline_id for baseline_id in selected_baselines if baseline_id not in config_baselines]
    if missing_from_config:
        payload = {
            "command": "baseline-smoke-control-records",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "execution_mode": "artifact_record_only",
            "config_path": relative_to_root(config_path),
            "message": "Required control baselines are missing from the smoke config.",
            "errors": [
                {
                    "type": "missing_config_baseline_ids",
                    "baseline_ids": missing_from_config,
                }
            ],
        }
        write_baseline_smoke_report("control_records_common_core_v0.json", payload)
        return print_and_exit(payload, 1)

    warnings: list[str] = []
    skipped_config_baselines = sorted(config_baselines - CONTROL_BASELINE_IDS)
    if skipped_config_baselines:
        warnings.append(
            "skipped non-control baselines from config: " + ", ".join(skipped_config_baselines)
        )

    selected_cases = config["cases"]
    records: list[dict[str, Any]] = []
    for case_spec in selected_cases:
        for baseline_id in selected_baselines:
            record, record_warnings = build_control_record(case_spec, baseline_id)
            records.append(record)
            warnings.extend(record_warnings)

    payload = {
        "command": "baseline-smoke-control-records",
        "cwd": str(ROOT),
        "ok": True,
        "ran_at_utc": utc_now(),
        "config_path": relative_to_root(config_path),
        "engine_scope": config["engine_scope"],
        "execution_mode": "artifact_record_only",
        "case_count": len(selected_cases),
        "baseline_count": len(selected_baselines),
        "record_count": len(records),
        "baseline_ids": selected_baselines,
        "cases": [case["case_id"] for case in selected_cases],
        "counts_by_result_consistency_status": count_values(records, "result_consistency_status"),
        "counts_by_negative_rejection_status": count_values(records, "negative_rejection_status"),
        "counts_by_plan_collection_status": count_values(records, "plan_collection_status"),
        "warnings": warnings,
        "records": records,
    }
    write_baseline_smoke_report("control_records_common_core_v0.json", payload)
    return print_and_exit(payload, 0)


def cmd_baseline_smoke_control_summary(args: argparse.Namespace) -> int:
    if args.execute:
        payload = {
            "command": "baseline-smoke-control-summary",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "input_path": relative_to_root(resolve_repo_path(args.input)),
            "execution_mode": "execute_requested_but_blocked",
            "message": "Execution is not supported for control summary. This command only summarizes an existing artifact report.",
            "errors": [
                {
                    "type": "execution_not_supported",
                    "message": "baseline-smoke-control-summary is read-only and does not support execution mode",
                }
            ],
        }
        write_baseline_smoke_report("control_records_summary_execute_refused_common_core_v0.json", payload)
        return print_and_exit(payload, 1)

    input_path = resolve_repo_path(args.input)
    output_name = args.output
    errors: list[dict[str, Any]] = []

    if not input_path.is_file():
        payload = {
            "command": "baseline-smoke-control-summary",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "input_path": relative_to_root(input_path),
            "output_path": f"reports/baseline_smoke/{output_name}",
            "message": "Input control-record report does not exist.",
            "errors": [
                {
                    "type": "missing_input_report",
                    "path": relative_to_root(input_path),
                }
            ],
        }
        write_baseline_smoke_report(output_name, payload)
        return print_and_exit(payload, 1)

    try:
        source_report = load_json(input_path)
    except (json.JSONDecodeError, OSError) as exc:
        payload = {
            "command": "baseline-smoke-control-summary",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "input_path": relative_to_root(input_path),
            "output_path": f"reports/baseline_smoke/{output_name}",
            "message": "Input control-record report could not be parsed.",
            "errors": [
                {
                    "type": "invalid_input_report",
                    "detail": str(exc),
                }
            ],
        }
        write_baseline_smoke_report(output_name, payload)
        return print_and_exit(payload, 1)

    required_fields = ["records", "case_count", "baseline_count", "record_count", "execution_mode"]
    missing_fields = [field for field in required_fields if field not in source_report]
    if missing_fields:
        payload = {
            "command": "baseline-smoke-control-summary",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "input_path": relative_to_root(input_path),
            "output_path": f"reports/baseline_smoke/{output_name}",
            "message": "Input control-record report is missing required fields.",
            "errors": [
                {
                    "type": "missing_required_fields",
                    "fields": missing_fields,
                }
            ],
        }
        write_baseline_smoke_report(output_name, payload)
        return print_and_exit(payload, 1)

    records = source_report.get("records")
    if not isinstance(records, list):
        payload = {
            "command": "baseline-smoke-control-summary",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "input_path": relative_to_root(input_path),
            "output_path": f"reports/baseline_smoke/{output_name}",
            "message": "Input control-record report has a non-list records field.",
            "errors": [
                {
                    "type": "invalid_records_field",
                    "actual_type": type(records).__name__,
                }
            ],
        }
        write_baseline_smoke_report(output_name, payload)
        return print_and_exit(payload, 1)

    missing_result_evidence_records = [
        issue_view(record)
        for record in records
        if record.get("baseline_id") in {"NATIVE_IDENTITY", "HUMAN_REFERENCE_POSITIVE"}
        and record.get("result_consistency_status") == "missing_evidence"
    ]
    missing_negative_evidence_records = [
        issue_view(record)
        for record in records
        if record.get("baseline_id") == "HARD_NEGATIVE_GUARD"
        and record.get("negative_rejection_status") == "missing_evidence"
    ]
    missing_plan_evidence_records = [
        issue_view(record)
        for record in records
        if record.get("plan_collection_status") == "missing_evidence"
    ]
    blocked_records = [
        issue_view(record)
        for record in records
        if record.get("blocker")
    ]
    non_none_failure_records = [
        issue_view(record)
        for record in records
        if record.get("failure_category") not in {"", "none"}
    ]
    unexpected_execution_mode_records = [
        issue_view(record)
        for record in records
        if record.get("execution_mode") != "artifact_record_only"
    ]
    unexpected_artifact_boundary_records = [
        issue_view(record)
        for record in records
        if record.get("artifact_claim_boundary") != "existing_artifact_only_no_execution"
    ]

    if source_report.get("record_count") != len(records):
        errors.append(
            {
                "type": "record_count_mismatch",
                "expected": source_report.get("record_count"),
                "actual": len(records),
            }
        )

    ok = not any(
        [
            errors,
            non_none_failure_records,
            unexpected_execution_mode_records,
            unexpected_artifact_boundary_records,
            missing_plan_evidence_records,
            missing_result_evidence_records,
            missing_negative_evidence_records,
        ]
    )

    payload = {
        "command": "baseline-smoke-control-summary",
        "ok": ok,
        "ran_at_utc": utc_now(),
        "input_path": relative_to_root(input_path),
        "output_path": f"reports/baseline_smoke/{output_name}",
        "source_report_execution_mode": source_report.get("execution_mode", ""),
        "case_count": source_report.get("case_count", 0),
        "baseline_count": source_report.get("baseline_count", 0),
        "record_count": source_report.get("record_count", 0),
        "baseline_ids": source_report.get("baseline_ids", []),
        "case_ids": source_report.get("cases", []),
        "counts_by_baseline_id": count_values(records, "baseline_id"),
        "counts_by_case_id": count_values(records, "case_id"),
        "counts_by_pool": count_values(records, "pool"),
        "counts_by_result_consistency_status": count_values(records, "result_consistency_status"),
        "counts_by_negative_rejection_status": count_values(records, "negative_rejection_status"),
        "counts_by_plan_collection_status": count_values(records, "plan_collection_status"),
        "counts_by_failure_category": count_values(records, "failure_category"),
        "counts_by_result_evidence_scope": count_values(records, "result_evidence_scope"),
        "counts_by_plan_evidence_scope": count_values(records, "plan_evidence_scope"),
        "counts_by_artifact_claim_boundary": count_values(records, "artifact_claim_boundary"),
        "missing_result_evidence_records": missing_result_evidence_records,
        "missing_negative_evidence_records": missing_negative_evidence_records,
        "missing_plan_evidence_records": missing_plan_evidence_records,
        "blocked_records": blocked_records,
        "non_none_failure_records": non_none_failure_records,
        "unexpected_execution_mode_records": unexpected_execution_mode_records,
        "unexpected_artifact_boundary_records": unexpected_artifact_boundary_records,
        "warnings": source_report.get("warnings", []),
        "errors": errors,
    }
    write_baseline_smoke_report(output_name, payload)
    return print_and_exit(payload, 0 if ok else 1)


def cmd_baseline_smoke_pg_control_summary(args: argparse.Namespace) -> int:
    output_name = normalize_baseline_smoke_output_name(args.output)
    input_paths = {
        "native": resolve_repo_path(args.native_report),
        "positive": resolve_repo_path(args.positive_report),
        "negative": resolve_repo_path(args.negative_report),
    }
    input_report_refs = {name: relative_to_root(path) for name, path in input_paths.items()}

    if args.execute:
        payload = {
            "command": "baseline-smoke-pg-control-summary",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "input_reports": input_report_refs,
            "output_path": f"reports/baseline_smoke/{normalize_baseline_smoke_output_name('pg_control_smoke_summary_execute_refused_v0.json')}",
            "claim_boundary": "execution_summary_only_not_correctness_scoring",
            "message": "Execution is not supported for PG control smoke summary. Use the existing PG control execution commands if new execution is needed.",
            "issues": [
                {
                    "type": "execution_not_supported",
                    "message": "baseline-smoke-pg-control-summary is read-only and does not execute baselines",
                }
            ],
        }
        write_baseline_smoke_report("pg_control_smoke_summary_execute_refused_v0.json", payload)
        return print_and_exit(payload, 1)

    reports: dict[str, dict[str, Any]] = {}
    issues: list[dict[str, Any]] = []
    expected = {
        "native": {"baseline_id": "NATIVE_IDENTITY", "execution_mode": "pg_execute_canary"},
        "positive": {"baseline_id": "HUMAN_REFERENCE_POSITIVE", "execution_mode": "pg_execute_positive"},
        "negative": {"baseline_id": "HARD_NEGATIVE_GUARD", "execution_mode": "pg_execute_negative"},
    }
    required_fields = ["baseline_id", "records", "success_count", "failed_count", "executed_count"]

    for name, path in input_paths.items():
        if not path.is_file():
            issues.append(
                {
                    "type": "missing_input",
                    "report": name,
                    "path": relative_to_root(path),
                }
            )
            continue
        try:
            report = load_json(path)
        except (json.JSONDecodeError, OSError) as exc:
            issues.append(
                {
                    "type": "malformed_input",
                    "report": name,
                    "path": relative_to_root(path),
                    "detail": str(exc),
                }
            )
            continue

        missing_fields = [field for field in required_fields if field not in report]
        if missing_fields:
            issues.append(
                {
                    "type": "missing_required_fields",
                    "report": name,
                    "path": relative_to_root(path),
                    "fields": missing_fields,
                }
            )
            continue

        if not isinstance(report.get("records"), list):
            issues.append(
                {
                    "type": "malformed_input",
                    "report": name,
                    "path": relative_to_root(path),
                    "detail": "records field is not a list",
                }
            )
            continue

        reports[name] = report
        if report.get("baseline_id") != expected[name]["baseline_id"]:
            issues.append(
                {
                    "type": "unexpected_baseline_id",
                    "report": name,
                    "expected": expected[name]["baseline_id"],
                    "actual": report.get("baseline_id"),
                }
            )

    native_report = reports.get("native")
    positive_report = reports.get("positive")
    negative_report = reports.get("negative")

    def index_records(report: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
        if not report:
            return {}
        return {
            record.get("case_id", ""): record
            for record in report.get("records", [])
            if isinstance(record, dict) and record.get("case_id")
        }

    native_records = index_records(native_report)
    positive_records = index_records(positive_report)
    negative_records = index_records(negative_report)
    all_case_ids = sorted(set(native_records) | set(positive_records) | set(negative_records))

    case_summaries: list[dict[str, Any]] = []
    execution_status_values: list[str] = []
    row_count_observation_values: list[str] = []
    negative_row_count_observation_values: list[str] = []

    for case_id in all_case_ids:
        native = native_records.get(case_id)
        positive = positive_records.get(case_id)
        negative = negative_records.get(case_id)
        pool = (
            (native or {}).get("pool")
            or (positive or {}).get("pool")
            or (negative or {}).get("pool")
            or ""
        )

        missing_parts: list[str] = []
        anomaly_notes: list[str] = []
        if native is None:
            missing_parts.append("native")
        if positive is None:
            missing_parts.append("positive")
        if negative is None:
            missing_parts.append("negative")

        native_status = (native or {}).get("execution_status", "")
        positive_status = (positive or {}).get("execution_status", "")
        negative_status = (negative or {}).get("execution_status", "")

        if missing_parts:
            execution_layer_status = "missing_record"
            anomaly_notes.append(f"missing records: {', '.join(missing_parts)}")
        elif native_status != "success":
            execution_layer_status = "source_failed"
        elif positive_status != "success":
            execution_layer_status = "positive_failed"
        elif negative_status != "success":
            execution_layer_status = "negative_failed"
        elif all(status == "success" for status in [native_status, positive_status, negative_status]):
            execution_layer_status = "all_three_succeeded"
        else:
            execution_layer_status = "mixed"

        native_row_count = (native or {}).get("row_count")
        positive_row_count = (positive or {}).get("row_count")
        negative_row_count = (negative or {}).get("row_count")

        if execution_layer_status != "all_three_succeeded":
            row_count_observation = "not_scored"
            negative_row_count_observation = "not_scored"
        elif native_row_count is None or positive_row_count is None:
            row_count_observation = "missing_row_count"
            negative_row_count_observation = (
                "missing_row_count" if native_row_count is None or negative_row_count is None else "not_scored"
            )
        else:
            if native_row_count == positive_row_count:
                row_count_observation = "source_positive_same_row_count"
            else:
                row_count_observation = "source_positive_different_row_count"
                anomaly_notes.append("source and positive row counts differ; needs_followup_if_unexpected")

            if native_row_count is None or negative_row_count is None:
                negative_row_count_observation = "missing_row_count"
            elif native_row_count == negative_row_count:
                negative_row_count_observation = "negative_same_row_count_as_source"
            else:
                negative_row_count_observation = "negative_different_row_count_from_source"
                anomaly_notes.append("negative and source row counts differ; needs_followup_if_unexpected")

        if native and not native.get("validation_schema"):
            anomaly_notes.append("native missing validation_schema")
        if positive and not positive.get("validation_schema"):
            anomaly_notes.append("positive missing validation_schema")
        if negative and not negative.get("validation_schema"):
            anomaly_notes.append("negative missing validation_schema")
        if native and not native.get("search_path_after_set"):
            anomaly_notes.append("native missing search_path_after_set")
        if positive and not positive.get("search_path_after_set"):
            anomaly_notes.append("positive missing search_path_after_set")
        if negative and not negative.get("search_path_after_set"):
            anomaly_notes.append("negative missing search_path_after_set")

        row = {
            "case_id": case_id,
            "pool": pool,
            "native_execution_status": native_status,
            "positive_execution_status": positive_status,
            "negative_execution_status": negative_status,
            "native_row_count": native_row_count,
            "positive_row_count": positive_row_count,
            "negative_row_count": negative_row_count,
            "native_runtime_ms": (native or {}).get("runtime_ms"),
            "positive_runtime_ms": (positive or {}).get("runtime_ms"),
            "negative_runtime_ms": (negative or {}).get("runtime_ms"),
            "native_validation_schema": (native or {}).get("validation_schema", ""),
            "positive_validation_schema": (positive or {}).get("validation_schema", ""),
            "negative_validation_schema": (negative or {}).get("validation_schema", ""),
            "native_search_path_after_set": (native or {}).get("search_path_after_set", ""),
            "positive_search_path_after_set": (positive or {}).get("search_path_after_set", ""),
            "negative_search_path_after_set": (negative or {}).get("search_path_after_set", ""),
            "execution_layer_status": execution_layer_status,
            "row_count_observation": row_count_observation,
            "negative_row_count_observation": negative_row_count_observation,
            "anomaly_notes": anomaly_notes,
        }
        case_summaries.append(row)
        execution_status_values.append(execution_layer_status)
        row_count_observation_values.append(row_count_observation)
        negative_row_count_observation_values.append(negative_row_count_observation)

    def total_runtime(report: dict[str, Any] | None) -> int:
        if not report:
            return 0
        return sum(
            runtime
            for runtime in (
                record.get("runtime_ms")
                for record in report.get("records", [])
                if isinstance(record, dict)
            )
            if isinstance(runtime, int)
        )

    def median_runtime(report: dict[str, Any] | None) -> int | None:
        if not report:
            return None
        values = [
            runtime
            for runtime in (
                record.get("runtime_ms")
                for record in report.get("records", [])
                if isinstance(record, dict)
            )
            if isinstance(runtime, int)
        ]
        return median_int(values)

    native_success_count = int((native_report or {}).get("success_count", 0))
    positive_success_count = int((positive_report or {}).get("success_count", 0))
    negative_success_count = int((negative_report or {}).get("success_count", 0))

    all_three_succeeded_count = sum(1 for row in case_summaries if row["execution_layer_status"] == "all_three_succeeded")
    source_failed_count = sum(1 for row in case_summaries if row["execution_layer_status"] == "source_failed")
    positive_failed_count = sum(1 for row in case_summaries if row["execution_layer_status"] == "positive_failed")
    negative_failed_count = sum(1 for row in case_summaries if row["execution_layer_status"] == "negative_failed")
    missing_record_count = sum(1 for row in case_summaries if row["execution_layer_status"] == "missing_record")

    for row in case_summaries:
        if row["execution_layer_status"] == "missing_record":
            issues.append(
                {
                    "type": "missing_record",
                    "case_id": row["case_id"],
                    "detail": row["anomaly_notes"],
                }
            )
        if not row["native_validation_schema"] or not row["positive_validation_schema"] or not row["negative_validation_schema"]:
            issues.append(
                {
                    "type": "missing_validation_schema",
                    "case_id": row["case_id"],
                }
            )
        if (
            not row["native_search_path_after_set"]
            or not row["positive_search_path_after_set"]
            or not row["negative_search_path_after_set"]
        ):
            issues.append(
                {
                    "type": "missing_search_path_after_set",
                    "case_id": row["case_id"],
                }
            )

    ok = (
        len(reports) == 3
        and not issues
        and all_three_succeeded_count == len(case_summaries)
        and len(case_summaries) > 0
    )

    payload = {
        "command": "baseline-smoke-pg-control-summary",
        "ok": ok,
        "ran_at_utc": utc_now(),
        "input_reports": input_report_refs,
        "output_path": f"reports/baseline_smoke/{output_name}",
        "case_count": len(case_summaries),
        "native_success_count": native_success_count,
        "positive_success_count": positive_success_count,
        "negative_success_count": negative_success_count,
        "all_three_succeeded_count": all_three_succeeded_count,
        "source_failed_count": source_failed_count,
        "positive_failed_count": positive_failed_count,
        "negative_failed_count": negative_failed_count,
        "missing_record_count": missing_record_count,
        "counts_by_execution_layer_status": count_plain_values(execution_status_values),
        "counts_by_row_count_observation": count_plain_values(row_count_observation_values),
        "counts_by_negative_row_count_observation": count_plain_values(negative_row_count_observation_values),
        "total_runtime_ms_by_baseline": {
            "NATIVE_IDENTITY": total_runtime(native_report),
            "HUMAN_REFERENCE_POSITIVE": total_runtime(positive_report),
            "HARD_NEGATIVE_GUARD": total_runtime(negative_report),
        },
        "median_runtime_ms_by_baseline": {
            "NATIVE_IDENTITY": median_runtime(native_report),
            "HUMAN_REFERENCE_POSITIVE": median_runtime(positive_report),
            "HARD_NEGATIVE_GUARD": median_runtime(negative_report),
        },
        "case_summaries": case_summaries,
        "issues": issues,
        "guardrails": {
            "database_execution": "disabled_for_summary",
            "mysql_execution": "disabled",
            "spark_execution": "disabled",
            "sqlglot_generation": "disabled",
            "llm_execution": "disabled",
            "case_artifact_write": "disabled",
        },
        "claim_boundary": "execution_summary_only_not_correctness_scoring",
    }
    write_baseline_smoke_report(output_name, payload)
    return print_and_exit(payload, 0 if ok else 1)


def cmd_baseline_smoke_sqlglot_preflight(args: argparse.Namespace) -> int:
    output_name = normalize_baseline_smoke_output_name("sqlglot_same_dialect_preflight_v0.json")

    if args.execute:
        payload = {
            "command": "baseline-smoke-sqlglot-preflight",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(resolve_repo_path(args.config)),
            "engine_scope": "postgres",
            "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
            "output_path": "reports/baseline_smoke/sqlglot_same_dialect_execute_refused_v0.json",
            "claim_boundary": "sqlglot_preflight_only_no_execution",
            "message": "Execution is not supported for SQLGlot preflight. This command only parses and generates same-dialect candidate SQL strings.",
            "issues": [
                {
                    "type": "execution_not_supported",
                    "message": "baseline-smoke-sqlglot-preflight is read-only and does not execute generated SQL",
                }
            ],
            "guardrails": {
                "database_execution": "disabled",
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "generated_sql_execution": "disabled",
                "case_artifact_write": "disabled",
            },
        }
        write_baseline_smoke_report("sqlglot_same_dialect_execute_refused_v0.json", payload)
        return print_and_exit(payload, 1)

    config_path = resolve_repo_path(args.config)
    config = load_json(config_path)
    case_index = {case["case_id"]: case for case in config.get("cases", [])}
    selected_case_ids = args.case_id or list(HUMAN_POSITIVE_PG_DEFAULT_CASES)
    records: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    invalid_cases = [case_id for case_id in selected_case_ids if case_id not in case_index]
    for case_id in invalid_cases:
        records.append(
            {
                "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                "case_id": case_id,
                "pool": "",
                "planned_engine": "postgres",
                "execution_mode": "preflight_no_execution",
                "source_sql_path": "",
                "source_sql_exists": False,
                "sqlglot_available": False,
                "parse_status": "skipped",
                "generation_status": "skipped",
                "generated_sql_empty": "unknown",
                "generated_sql_same_as_source_normalized": "unknown",
                "generated_sql_preview": "",
                "failure_category": "case_not_in_smoke_config",
                "error_message": "",
                "artifact_claim_boundary": "sqlglot_preflight_only_no_execution",
                "notes": ["selection refused: case is outside the current smoke config"],
            }
        )
        issues.append(
            {
                "type": "case_not_in_smoke_config",
                "case_id": case_id,
            }
        )

    valid_case_ids = [case_id for case_id in selected_case_ids if case_id in case_index]
    selected_specs = [case_index[case_id] for case_id in valid_case_ids]

    sqlglot_available = True
    sqlglot_error = ""
    try:
        sqlglot = importlib.import_module("sqlglot")
    except ModuleNotFoundError as exc:
        sqlglot_available = False
        sqlglot_error = str(exc)
        sqlglot = None
        issues.append(
            {
                "type": "missing_sqlglot",
                "detail": str(exc),
            }
        )

    generated_dir = BASELINE_SMOKE_REPORT_DIR / "generated_sqlglot"
    if args.write_generated:
        generated_dir.mkdir(parents=True, exist_ok=True)

    for case_spec in selected_specs:
        case_id = case_spec["case_id"]
        pool = case_spec["pool"]
        source_sql_path = pool_case_root(pool) / case_id / "source.sql"
        source_sql_exists = source_sql_path.is_file()
        generated_sql_preview = ""
        generated_sql_empty: bool | str = "unknown"
        generated_sql_same = "unknown"
        parse_status = "skipped"
        generation_status = "skipped"
        failure_category = "none"
        error_message = ""
        notes: list[str] = []

        if not source_sql_exists:
            parse_status = "skipped"
            generation_status = "skipped"
            generated_sql_empty = "unknown"
            generated_sql_same = "unknown"
            failure_category = "missing_source_sql"
            notes.append("source.sql is missing")
        elif not sqlglot_available:
            parse_status = "skipped"
            generation_status = "skipped"
            generated_sql_empty = "unknown"
            generated_sql_same = "unknown"
            failure_category = "sqlglot_unavailable"
            error_message = sqlglot_error
            notes.append("sqlglot is not importable in the current environment")
        else:
            source_sql = source_sql_path.read_text(encoding="utf-8")
            try:
                parsed = sqlglot.parse_one(source_sql, dialect=args.dialect)
                parse_status = "success"
            except Exception as exc:
                parsed = None
                parse_status = "failed"
                generation_status = "skipped"
                generated_sql_empty = "unknown"
                generated_sql_same = "unknown"
                failure_category = type(exc).__name__
                error_message = str(exc)
                notes.append("sqlglot parse failed")

            if parse_status == "success":
                try:
                    generated_sql = parsed.sql(dialect=args.dialect)
                    generation_status = "success"
                    generated_sql_empty = len(generated_sql.strip()) == 0
                    generated_sql_preview = generated_sql[:500]
                    if generated_sql_empty:
                        failure_category = "empty_generated_sql"
                        notes.append("generated SQL string was empty")
                    else:
                        generated_sql_same = (
                            normalize_sql_for_compare(source_sql)
                            == normalize_sql_for_compare(generated_sql)
                        )
                        notes.append("sqlglot generated same-dialect candidate SQL")
                        if args.write_generated:
                            generated_path = generated_dir / f"{case_id}.sql"
                            generated_path.write_text(generated_sql, encoding="utf-8")
                            notes.append(f"generated SQL written to {relative_to_root(generated_path)}")
                except Exception as exc:
                    generation_status = "failed"
                    generated_sql_empty = "unknown"
                    generated_sql_same = "unknown"
                    failure_category = type(exc).__name__
                    error_message = str(exc)
                    notes.append("sqlglot generation failed")

        records.append(
            {
                "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                "case_id": case_id,
                "pool": pool,
                "planned_engine": "postgres",
                "execution_mode": "preflight_no_execution",
                "source_sql_path": relative_to_root(source_sql_path) if source_sql_path.is_absolute() else str(source_sql_path),
                "source_sql_exists": source_sql_exists,
                "sqlglot_available": sqlglot_available,
                "parse_status": parse_status,
                "generation_status": generation_status,
                "generated_sql_empty": generated_sql_empty,
                "generated_sql_same_as_source_normalized": generated_sql_same,
                "generated_sql_preview": generated_sql_preview,
                "failure_category": failure_category,
                "error_message": error_message,
                "artifact_claim_boundary": "sqlglot_preflight_only_no_execution",
                "notes": notes,
            }
        )

    parse_success_count = sum(1 for r in records if r["parse_status"] == "success")
    parse_failed_count = sum(1 for r in records if r["parse_status"] == "failed")
    generation_success_count = sum(1 for r in records if r["generation_status"] == "success")
    generation_failed_count = sum(1 for r in records if r["generation_status"] == "failed")
    empty_generated_sql_count = sum(1 for r in records if r["generated_sql_empty"] is True)
    identical_to_source_count = sum(1 for r in records if r["generated_sql_same_as_source_normalized"] is True)
    different_from_source_count = sum(1 for r in records if r["generated_sql_same_as_source_normalized"] is False)
    skipped_count = sum(1 for r in records if r["parse_status"] == "skipped" or r["generation_status"] == "skipped")

    ok = (
        sqlglot_available
        and not issues
        and all(record["source_sql_exists"] for record in records)
        and all(record["parse_status"] == "success" for record in records)
        and all(record["generation_status"] == "success" for record in records)
        and all(record["generated_sql_empty"] is False for record in records)
    )

    payload = {
        "command": "baseline-smoke-sqlglot-preflight",
        "ok": ok,
        "ran_at_utc": utc_now(),
        "config_path": relative_to_root(config_path),
        "engine_scope": "postgres",
        "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
        "case_count": len(records),
        "sqlglot_available": sqlglot_available,
        "parse_success_count": parse_success_count,
        "parse_failed_count": parse_failed_count,
        "generation_success_count": generation_success_count,
        "generation_failed_count": generation_failed_count,
        "empty_generated_sql_count": empty_generated_sql_count,
        "identical_to_source_count": identical_to_source_count,
        "different_from_source_count": different_from_source_count,
        "skipped_count": skipped_count,
        "records": records,
        "issues": issues,
        "guardrails": {
            "database_execution": "disabled",
            "mysql_execution": "disabled",
            "spark_execution": "disabled",
            "llm_execution": "disabled",
            "generated_sql_execution": "disabled",
            "case_artifact_write": "disabled",
        },
    }
    write_baseline_smoke_report(output_name, payload)
    return print_and_exit(payload, 0 if ok else 1)


def cmd_baseline_smoke_sqlglot_pg_canary(args: argparse.Namespace) -> int:
    output_name = normalize_baseline_smoke_output_name("sqlglot_same_dialect_pg_canary_v0.json")

    if args.execute:
        payload = {
            "command": "baseline-smoke-sqlglot-pg-canary",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(resolve_repo_path(args.config)),
            "engine_scope": "postgres",
            "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
            "output_path": "reports/baseline_smoke/sqlglot_same_dialect_pg_execute_refused_v0.json",
            "message": "Use --execute-sqlglot for the PG SQLGlot canary. --execute is intentionally not supported here.",
            "issues": [
                {
                    "type": "invalid_execute_flag",
                    "message": "only --execute-sqlglot can enable the PG SQLGlot canary",
                }
            ],
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "case_artifact_write": "disabled",
                "generated_sql_case_write": "disabled",
            },
        }
        write_baseline_smoke_report("sqlglot_same_dialect_pg_execute_refused_v0.json", payload)
        return print_and_exit(payload, 1)

    config_path = resolve_repo_path(args.config)
    config = load_json(config_path)
    case_index = {case["case_id"]: case for case in config.get("cases", [])}
    selected_case_ids = args.case_id or list(SQLGLOT_PG_CANARY_DEFAULT_CASES)
    records: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    invalid_cases = [case_id for case_id in selected_case_ids if case_id not in case_index]
    for case_id in invalid_cases:
        records.append(
            {
                "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                "case_id": case_id,
                "pool": "",
                "planned_engine": "postgres",
                "execution_mode": "dry_run" if not args.execute_sqlglot else "pg_execute_sqlglot_canary",
                "source_sql_path": "",
                "source_sql_exists": False,
                "sqlglot_available": False,
                "parse_status": "skipped",
                "generation_status": "skipped",
                "generated_sql_empty": "unknown",
                "generated_sql_same_as_source_normalized": "unknown",
                "generated_sql_preview": "",
                "pg_env_visible": False,
                "pg_password_present": "unknown",
                "validation_schema": "",
                "search_path_after_set": "",
                "statement_timeout_ms": args.statement_timeout_ms,
                "execution_status": "skipped",
                "row_count": None,
                "runtime_ms": None,
                "result_materialization": "not_persisted",
                "output_scope": "reports_only_no_case_artifact_write",
                "failure_category": "case_not_in_smoke_config",
                "error_message": "",
                "artifact_claim_boundary": (
                    "sqlglot_pg_canary_execution_not_benchmark_claim"
                    if args.execute_sqlglot
                    else "dry_run_no_execution"
                ),
                "notes": ["selection refused: case is outside the current smoke config"],
            }
        )
        issues.append({"type": "case_not_in_smoke_config", "case_id": case_id})

    valid_case_ids = [case_id for case_id in selected_case_ids if case_id in case_index]
    selected_specs = [case_index[case_id] for case_id in valid_case_ids]

    env_visibility = pg_env_visibility()
    required_env_visible = all(env_visibility[name] for name in ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER"])
    pg_password_present = env_visibility["PGPASSWORD"]

    sqlglot_available = True
    sqlglot_error = ""
    try:
        sqlglot = importlib.import_module("sqlglot")
    except ModuleNotFoundError as exc:
        sqlglot_available = False
        sqlglot_error = str(exc)
        sqlglot = None
        issues.append({"type": "missing_sqlglot", "detail": str(exc)})

    if not args.execute_sqlglot:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            source_sql_path = pool_case_root(pool) / case_id / "source.sql"
            source_sql_exists = source_sql_path.is_file()
            validation_schema = native_identity_validation_schema(case_id, pool)
            parse_status = "skipped"
            generation_status = "skipped"
            generated_sql_empty: bool | str = "unknown"
            generated_sql_same: bool | str = "unknown"
            generated_sql_preview = ""
            failure_category = "none"
            error_message = ""
            notes: list[str] = []

            if pool == "portability":
                records.append(
                    {
                        "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                        "case_id": case_id,
                        "pool": pool,
                        "planned_engine": "postgres",
                        "execution_mode": "dry_run",
                        "source_sql_path": relative_to_root(source_sql_path),
                        "source_sql_exists": source_sql_exists,
                        "sqlglot_available": sqlglot_available,
                        "parse_status": "skipped",
                        "generation_status": "skipped",
                        "generated_sql_empty": "unknown",
                        "generated_sql_same_as_source_normalized": "unknown",
                        "generated_sql_preview": "",
                        "pg_env_visible": required_env_visible,
                        "pg_password_present": "unknown",
                        "validation_schema": validation_schema,
                        "search_path_after_set": "",
                        "statement_timeout_ms": args.statement_timeout_ms,
                        "execution_status": "skipped",
                        "row_count": None,
                        "runtime_ms": None,
                        "result_materialization": "not_persisted",
                        "output_scope": "reports_only_no_case_artifact_write",
                        "failure_category": "port_case_not_enabled",
                        "error_message": "",
                        "artifact_claim_boundary": "dry_run_no_execution",
                        "notes": ["dry-run skip: portability cases are not enabled in this PG SQLGlot canary"],
                    }
                )
                continue

            if not source_sql_exists:
                failure_category = "missing_source_sql"
                notes.append("source.sql is missing")
            elif not sqlglot_available:
                failure_category = "sqlglot_unavailable"
                error_message = sqlglot_error
                notes.append("sqlglot is not importable in the current environment")
            else:
                source_sql = source_sql_path.read_text(encoding="utf-8")
                try:
                    parsed = sqlglot.parse_one(source_sql, dialect=args.dialect)
                    parse_status = "success"
                except Exception as exc:
                    parsed = None
                    parse_status = "failed"
                    failure_category = type(exc).__name__
                    error_message = str(exc)
                    notes.append("sqlglot parse failed")

                if parse_status == "success":
                    try:
                        generated_sql = parsed.sql(dialect=args.dialect)
                        generation_status = "success"
                        generated_sql_empty = len(generated_sql.strip()) == 0
                        generated_sql_preview = generated_sql[:500]
                        if generated_sql_empty:
                            failure_category = "empty_generated_sql"
                            notes.append("generated SQL string was empty")
                        else:
                            generated_sql_same = (
                                normalize_sql_for_compare(source_sql)
                                == normalize_sql_for_compare(generated_sql)
                            )
                            notes.append("sqlglot generated same-dialect candidate SQL")
                    except Exception as exc:
                        generation_status = "failed"
                        failure_category = type(exc).__name__
                        error_message = str(exc)
                        notes.append("sqlglot generation failed")

            records.append(
                {
                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "execution_mode": "dry_run",
                    "source_sql_path": relative_to_root(source_sql_path),
                    "source_sql_exists": source_sql_exists,
                    "sqlglot_available": sqlglot_available,
                    "parse_status": parse_status,
                    "generation_status": generation_status,
                    "generated_sql_empty": generated_sql_empty,
                    "generated_sql_same_as_source_normalized": generated_sql_same,
                    "generated_sql_preview": generated_sql_preview,
                    "pg_env_visible": required_env_visible,
                    "pg_password_present": "unknown",
                    "validation_schema": validation_schema,
                    "search_path_after_set": "",
                    "statement_timeout_ms": args.statement_timeout_ms,
                    "execution_status": "planned",
                    "row_count": None,
                    "runtime_ms": None,
                    "result_materialization": "not_persisted",
                    "output_scope": "reports_only_no_case_artifact_write",
                    "failure_category": failure_category,
                    "error_message": error_message,
                    "artifact_claim_boundary": "dry_run_no_execution",
                    "notes": notes or ["dry-run only; no PostgreSQL connection attempted"],
                }
            )

        payload = {
            "command": "baseline-smoke-sqlglot-pg-canary",
            "ok": (
                sqlglot_available
                and not issues
                and all(record["source_sql_exists"] for record in records if record["execution_status"] != "skipped")
                and all(record["parse_status"] == "success" for record in records if record["execution_status"] != "skipped")
                and all(record["generation_status"] == "success" for record in records if record["execution_status"] != "skipped")
                and all(record["generated_sql_empty"] is False for record in records if record["execution_status"] != "skipped")
            ),
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
            "case_count": len(records),
            "sqlglot_available": sqlglot_available,
            "parse_success_count": sum(1 for r in records if r["parse_status"] == "success"),
            "parse_failed_count": sum(1 for r in records if r["parse_status"] == "failed"),
            "generation_success_count": sum(1 for r in records if r["generation_status"] == "success"),
            "generation_failed_count": sum(1 for r in records if r["generation_status"] == "failed"),
            "identical_to_source_count": sum(1 for r in records if r["generated_sql_same_as_source_normalized"] is True),
            "different_from_source_count": sum(1 for r in records if r["generated_sql_same_as_source_normalized"] is False),
            "executed_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "skipped_count": sum(1 for r in records if r["execution_status"] == "skipped"),
            "env_blocked_count": 0,
            "records": records,
            "issues": issues,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "case_artifact_write": "disabled",
                "generated_sql_case_write": "disabled",
            },
        }
        write_baseline_smoke_report(output_name, payload)
        return print_and_exit(payload, 0 if payload["ok"] else 1)

    if not sqlglot_available:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            source_sql_path = pool_case_root(pool) / case_id / "source.sql"
            records.append(
                {
                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "execution_mode": "pg_execute_sqlglot_canary",
                    "source_sql_path": relative_to_root(source_sql_path),
                    "source_sql_exists": source_sql_path.is_file(),
                    "sqlglot_available": False,
                    "parse_status": "skipped",
                    "generation_status": "skipped",
                    "generated_sql_empty": "unknown",
                    "generated_sql_same_as_source_normalized": "unknown",
                    "generated_sql_preview": "",
                    "pg_env_visible": required_env_visible,
                    "pg_password_present": pg_password_present,
                    "validation_schema": native_identity_validation_schema(case_id, pool),
                    "search_path_after_set": "",
                    "statement_timeout_ms": args.statement_timeout_ms,
                    "execution_status": "failed",
                    "row_count": None,
                    "runtime_ms": None,
                    "result_materialization": "not_persisted",
                    "output_scope": "reports_only_no_case_artifact_write",
                    "failure_category": "sqlglot_unavailable",
                    "error_message": sqlglot_error,
                    "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                    "notes": ["execution not attempted because sqlglot is unavailable"],
                }
            )
        payload = {
            "command": "baseline-smoke-sqlglot-pg-canary",
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
            "case_count": len(records),
            "sqlglot_available": False,
            "parse_success_count": 0,
            "parse_failed_count": 0,
            "generation_success_count": 0,
            "generation_failed_count": 0,
            "identical_to_source_count": 0,
            "different_from_source_count": 0,
            "executed_count": 0,
            "success_count": 0,
            "failed_count": len(records),
            "skipped_count": 0,
            "env_blocked_count": 0,
            "records": records,
            "issues": issues,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "case_artifact_write": "disabled",
                "generated_sql_case_write": "disabled",
            },
        }
        write_baseline_smoke_report(output_name, payload)
        return print_and_exit(payload, 1)

    try:
        psycopg = importlib.import_module("psycopg")
    except ModuleNotFoundError as exc:
        issues.append({"type": "missing_psycopg", "detail": str(exc)})
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            source_sql_path = pool_case_root(pool) / case_id / "source.sql"
            records.append(
                {
                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "execution_mode": "pg_execute_sqlglot_canary",
                    "source_sql_path": relative_to_root(source_sql_path),
                    "source_sql_exists": source_sql_path.is_file(),
                    "sqlglot_available": True,
                    "parse_status": "skipped",
                    "generation_status": "skipped",
                    "generated_sql_empty": "unknown",
                    "generated_sql_same_as_source_normalized": "unknown",
                    "generated_sql_preview": "",
                    "pg_env_visible": required_env_visible,
                    "pg_password_present": pg_password_present,
                    "validation_schema": native_identity_validation_schema(case_id, pool),
                    "search_path_after_set": "",
                    "statement_timeout_ms": args.statement_timeout_ms,
                    "execution_status": "failed",
                    "row_count": None,
                    "runtime_ms": None,
                    "result_materialization": "not_persisted",
                    "output_scope": "reports_only_no_case_artifact_write",
                    "failure_category": "psycopg_unavailable",
                    "error_message": str(exc),
                    "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                    "notes": ["execution not attempted because psycopg is unavailable"],
                }
            )
        payload = {
            "command": "baseline-smoke-sqlglot-pg-canary",
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
            "case_count": len(records),
            "sqlglot_available": True,
            "parse_success_count": 0,
            "parse_failed_count": 0,
            "generation_success_count": 0,
            "generation_failed_count": 0,
            "identical_to_source_count": 0,
            "different_from_source_count": 0,
            "executed_count": 0,
            "success_count": 0,
            "failed_count": len(records),
            "skipped_count": 0,
            "env_blocked_count": 0,
            "records": records,
            "issues": issues,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "case_artifact_write": "disabled",
                "generated_sql_case_write": "disabled",
            },
        }
        write_baseline_smoke_report(output_name, payload)
        return print_and_exit(payload, 1)

    if not required_env_visible:
        for case_spec in selected_specs:
            case_id = case_spec["case_id"]
            pool = case_spec["pool"]
            source_sql_path = pool_case_root(pool) / case_id / "source.sql"
            records.append(
                {
                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "execution_mode": "pg_execute_sqlglot_canary",
                    "source_sql_path": relative_to_root(source_sql_path),
                    "source_sql_exists": source_sql_path.is_file(),
                    "sqlglot_available": True,
                    "parse_status": "skipped",
                    "generation_status": "skipped",
                    "generated_sql_empty": "unknown",
                    "generated_sql_same_as_source_normalized": "unknown",
                    "generated_sql_preview": "",
                    "pg_env_visible": False,
                    "pg_password_present": pg_password_present,
                    "validation_schema": native_identity_validation_schema(case_id, pool),
                    "search_path_after_set": "",
                    "statement_timeout_ms": args.statement_timeout_ms,
                    "execution_status": "env_blocked",
                    "row_count": None,
                    "runtime_ms": None,
                    "result_materialization": "not_persisted",
                    "output_scope": "reports_only_no_case_artifact_write",
                    "failure_category": "missing_pg_env",
                    "error_message": "",
                    "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                    "notes": ["execution not attempted", "required env: PGHOST, PGPORT, PGDATABASE, PGUSER"],
                }
            )
        payload = {
            "command": "baseline-smoke-sqlglot-pg-canary",
            "ok": False,
            "ran_at_utc": utc_now(),
            "config_path": relative_to_root(config_path),
            "engine_scope": "postgres",
            "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
            "case_count": len(records),
            "sqlglot_available": True,
            "parse_success_count": 0,
            "parse_failed_count": 0,
            "generation_success_count": 0,
            "generation_failed_count": 0,
            "identical_to_source_count": 0,
            "different_from_source_count": 0,
            "executed_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "skipped_count": 0,
            "env_blocked_count": len(records),
            "records": records,
            "issues": issues,
            "guardrails": {
                "mysql_execution": "disabled",
                "spark_execution": "disabled",
                "llm_execution": "disabled",
                "case_artifact_write": "disabled",
                "generated_sql_case_write": "disabled",
            },
        }
        write_baseline_smoke_report("sqlglot_same_dialect_pg_env_blocked_v0.json", payload)
        return print_and_exit(payload, 1)

    for case_spec in selected_specs:
        case_id = case_spec["case_id"]
        pool = case_spec["pool"]
        source_sql_path = pool_case_root(pool) / case_id / "source.sql"
        source_sql_exists = source_sql_path.is_file()
        validation_schema = native_identity_validation_schema(case_id, pool)
        generated_sql_preview = ""
        search_path_after_set = ""
        parse_status = "skipped"
        generation_status = "skipped"
        generated_sql_empty: bool | str = "unknown"
        generated_sql_same: bool | str = "unknown"
        failure_category = "none"
        error_message = ""
        notes: list[str] = []
        row_count = None
        runtime_ms = None

        if pool == "portability":
            records.append(
                {
                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "execution_mode": "pg_execute_sqlglot_canary",
                    "source_sql_path": relative_to_root(source_sql_path),
                    "source_sql_exists": source_sql_exists,
                    "sqlglot_available": True,
                    "parse_status": "skipped",
                    "generation_status": "skipped",
                    "generated_sql_empty": "unknown",
                    "generated_sql_same_as_source_normalized": "unknown",
                    "generated_sql_preview": "",
                    "pg_env_visible": True,
                    "pg_password_present": pg_password_present,
                    "validation_schema": validation_schema,
                    "search_path_after_set": "",
                    "statement_timeout_ms": args.statement_timeout_ms,
                    "execution_status": "skipped",
                    "row_count": None,
                    "runtime_ms": None,
                    "result_materialization": "not_persisted",
                    "output_scope": "reports_only_no_case_artifact_write",
                    "failure_category": "port_case_not_enabled",
                    "error_message": "",
                    "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                    "notes": ["execution skip: portability cases are not enabled in this PG SQLGlot canary"],
                }
            )
            continue

        if not source_sql_exists:
            records.append(
                {
                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "execution_mode": "pg_execute_sqlglot_canary",
                    "source_sql_path": relative_to_root(source_sql_path),
                    "source_sql_exists": False,
                    "sqlglot_available": True,
                    "parse_status": "skipped",
                    "generation_status": "skipped",
                    "generated_sql_empty": "unknown",
                    "generated_sql_same_as_source_normalized": "unknown",
                    "generated_sql_preview": "",
                    "pg_env_visible": True,
                    "pg_password_present": pg_password_present,
                    "validation_schema": validation_schema,
                    "search_path_after_set": "",
                    "statement_timeout_ms": args.statement_timeout_ms,
                    "execution_status": "failed",
                    "row_count": None,
                    "runtime_ms": None,
                    "result_materialization": "not_persisted",
                    "output_scope": "reports_only_no_case_artifact_write",
                    "failure_category": "missing_source_sql",
                    "error_message": "",
                    "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                    "notes": ["execution not attempted because source.sql is absent"],
                }
            )
            continue

        source_sql = source_sql_path.read_text(encoding="utf-8")
        try:
            parsed = sqlglot.parse_one(source_sql, dialect=args.dialect)
            parse_status = "success"
        except Exception as exc:
            records.append(
                {
                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "execution_mode": "pg_execute_sqlglot_canary",
                    "source_sql_path": relative_to_root(source_sql_path),
                    "source_sql_exists": True,
                    "sqlglot_available": True,
                    "parse_status": "failed",
                    "generation_status": "skipped",
                    "generated_sql_empty": "unknown",
                    "generated_sql_same_as_source_normalized": "unknown",
                    "generated_sql_preview": "",
                    "pg_env_visible": True,
                    "pg_password_present": pg_password_present,
                    "validation_schema": validation_schema,
                    "search_path_after_set": "",
                    "statement_timeout_ms": args.statement_timeout_ms,
                    "execution_status": "failed",
                    "row_count": None,
                    "runtime_ms": None,
                    "result_materialization": "not_persisted",
                    "output_scope": "reports_only_no_case_artifact_write",
                    "failure_category": type(exc).__name__,
                    "error_message": str(exc),
                    "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                    "notes": ["sqlglot parse failed"],
                }
            )
            continue

        try:
            generated_sql = parsed.sql(dialect=args.dialect)
            generation_status = "success"
            generated_sql_empty = len(generated_sql.strip()) == 0
            generated_sql_preview = generated_sql[:500]
            if generated_sql_empty:
                records.append(
                    {
                        "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                        "case_id": case_id,
                        "pool": pool,
                        "planned_engine": "postgres",
                        "execution_mode": "pg_execute_sqlglot_canary",
                        "source_sql_path": relative_to_root(source_sql_path),
                        "source_sql_exists": True,
                        "sqlglot_available": True,
                        "parse_status": parse_status,
                        "generation_status": "success",
                        "generated_sql_empty": True,
                        "generated_sql_same_as_source_normalized": "unknown",
                        "generated_sql_preview": generated_sql_preview,
                        "pg_env_visible": True,
                        "pg_password_present": pg_password_present,
                        "validation_schema": validation_schema,
                        "search_path_after_set": "",
                        "statement_timeout_ms": args.statement_timeout_ms,
                        "execution_status": "failed",
                        "row_count": None,
                        "runtime_ms": None,
                        "result_materialization": "not_persisted",
                        "output_scope": "reports_only_no_case_artifact_write",
                        "failure_category": "empty_generated_sql",
                        "error_message": "",
                        "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                        "notes": ["generated SQL string was empty"],
                    }
                )
                continue
            generated_sql_same = (
                normalize_sql_for_compare(source_sql)
                == normalize_sql_for_compare(generated_sql)
            )
        except Exception as exc:
            records.append(
                {
                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "execution_mode": "pg_execute_sqlglot_canary",
                    "source_sql_path": relative_to_root(source_sql_path),
                    "source_sql_exists": True,
                    "sqlglot_available": True,
                    "parse_status": parse_status,
                    "generation_status": "failed",
                    "generated_sql_empty": "unknown",
                    "generated_sql_same_as_source_normalized": "unknown",
                    "generated_sql_preview": generated_sql_preview,
                    "pg_env_visible": True,
                    "pg_password_present": pg_password_present,
                    "validation_schema": validation_schema,
                    "search_path_after_set": "",
                    "statement_timeout_ms": args.statement_timeout_ms,
                    "execution_status": "failed",
                    "row_count": None,
                    "runtime_ms": None,
                    "result_materialization": "not_persisted",
                    "output_scope": "reports_only_no_case_artifact_write",
                    "failure_category": type(exc).__name__,
                    "error_message": str(exc),
                    "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                    "notes": ["sqlglot generation failed"],
                }
            )
            continue

        start = time.perf_counter()
        try:
            with psycopg.connect(
                host=os.environ["PGHOST"],
                port=os.environ["PGPORT"],
                dbname=os.environ["PGDATABASE"],
                user=os.environ["PGUSER"],
                password=os.environ.get("PGPASSWORD"),
                options=(
                    f"-c statement_timeout={args.statement_timeout_ms} "
                    "-c default_transaction_read_only=on"
                ),
            ) as conn:
                with conn.cursor() as cur:
                    if validation_schema:
                        cur.execute("SELECT to_regnamespace(%s)", (validation_schema,))
                        schema_name = cur.fetchone()[0]
                        if not schema_name:
                            runtime_ms = int((time.perf_counter() - start) * 1000)
                            records.append(
                                {
                                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                                    "case_id": case_id,
                                    "pool": pool,
                                    "planned_engine": "postgres",
                                    "execution_mode": "pg_execute_sqlglot_canary",
                                    "source_sql_path": relative_to_root(source_sql_path),
                                    "source_sql_exists": True,
                                    "sqlglot_available": True,
                                    "parse_status": parse_status,
                                    "generation_status": generation_status,
                                    "generated_sql_empty": False,
                                    "generated_sql_same_as_source_normalized": generated_sql_same,
                                    "generated_sql_preview": generated_sql_preview,
                                    "pg_env_visible": True,
                                    "pg_password_present": pg_password_present,
                                    "validation_schema": validation_schema,
                                    "search_path_after_set": "",
                                    "statement_timeout_ms": args.statement_timeout_ms,
                                    "execution_status": "failed",
                                    "row_count": None,
                                    "runtime_ms": runtime_ms,
                                    "result_materialization": "not_persisted",
                                    "output_scope": "reports_only_no_case_artifact_write",
                                    "failure_category": "missing_validation_schema",
                                    "error_message": f"validation schema not found: {validation_schema}",
                                    "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                                    "notes": ["execution attempted", "search_path not set because validation schema was missing"],
                                }
                            )
                            continue
                        cur.execute(
                            psycopg.sql.SQL("SET search_path TO {}, public").format(
                                psycopg.sql.Identifier(validation_schema)
                            )
                        )
                        cur.execute("SHOW search_path")
                        search_path_after_set = str(cur.fetchone()[0])
                    cur.execute(generated_sql)
                    if cur.description is not None:
                        rows = cur.fetchall()
                        row_count = len(rows)
                    else:
                        row_count = cur.rowcount if cur.rowcount >= 0 else None
            runtime_ms = int((time.perf_counter() - start) * 1000)
            records.append(
                {
                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "execution_mode": "pg_execute_sqlglot_canary",
                    "source_sql_path": relative_to_root(source_sql_path),
                    "source_sql_exists": True,
                    "sqlglot_available": True,
                    "parse_status": parse_status,
                    "generation_status": generation_status,
                    "generated_sql_empty": False,
                    "generated_sql_same_as_source_normalized": generated_sql_same,
                    "generated_sql_preview": generated_sql_preview,
                    "pg_env_visible": True,
                    "pg_password_present": pg_password_present,
                    "validation_schema": validation_schema,
                    "search_path_after_set": search_path_after_set,
                    "statement_timeout_ms": args.statement_timeout_ms,
                    "execution_status": "success",
                    "row_count": row_count,
                    "runtime_ms": runtime_ms,
                    "result_materialization": "not_persisted",
                    "output_scope": "reports_only_no_case_artifact_write",
                    "failure_category": "none",
                    "error_message": "",
                    "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                    "notes": ["sqlglot generated SQL executed under read-only PG canary mode"],
                }
            )
        except Exception as exc:
            runtime_ms = int((time.perf_counter() - start) * 1000)
            records.append(
                {
                    "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "execution_mode": "pg_execute_sqlglot_canary",
                    "source_sql_path": relative_to_root(source_sql_path),
                    "source_sql_exists": True,
                    "sqlglot_available": True,
                    "parse_status": parse_status,
                    "generation_status": generation_status,
                    "generated_sql_empty": False,
                    "generated_sql_same_as_source_normalized": generated_sql_same,
                    "generated_sql_preview": generated_sql_preview,
                    "pg_env_visible": True,
                    "pg_password_present": pg_password_present,
                    "validation_schema": validation_schema,
                    "search_path_after_set": search_path_after_set,
                    "statement_timeout_ms": args.statement_timeout_ms,
                    "execution_status": "failed",
                    "row_count": None,
                    "runtime_ms": runtime_ms,
                    "result_materialization": "not_persisted",
                    "output_scope": "reports_only_no_case_artifact_write",
                    "failure_category": type(exc).__name__,
                    "error_message": str(exc),
                    "artifact_claim_boundary": "sqlglot_pg_canary_execution_not_benchmark_claim",
                    "notes": ["execution attempted", "no case-local artifacts were written"],
                }
            )

    payload = {
        "command": "baseline-smoke-sqlglot-pg-canary",
        "ok": (
            sqlglot_available
            and not issues
            and all(record["parse_status"] == "success" for record in records if record["execution_status"] != "skipped")
            and all(record["generation_status"] == "success" for record in records if record["execution_status"] != "skipped")
            and all(record["execution_status"] == "success" for record in records if record["execution_status"] != "skipped")
        ),
        "ran_at_utc": utc_now(),
        "config_path": relative_to_root(config_path),
        "engine_scope": "postgres",
        "baseline_id": "SQLGLOT_OPT_SAME_DIALECT",
        "case_count": len(records),
        "sqlglot_available": sqlglot_available,
        "parse_success_count": sum(1 for r in records if r["parse_status"] == "success"),
        "parse_failed_count": sum(1 for r in records if r["parse_status"] == "failed"),
        "generation_success_count": sum(1 for r in records if r["generation_status"] == "success"),
        "generation_failed_count": sum(1 for r in records if r["generation_status"] == "failed"),
        "identical_to_source_count": sum(1 for r in records if r["generated_sql_same_as_source_normalized"] is True),
        "different_from_source_count": sum(1 for r in records if r["generated_sql_same_as_source_normalized"] is False),
        "executed_count": sum(1 for r in records if r["execution_status"] in {"success", "failed"}),
        "success_count": sum(1 for r in records if r["execution_status"] == "success"),
        "failed_count": sum(1 for r in records if r["execution_status"] == "failed"),
        "skipped_count": sum(1 for r in records if r["execution_status"] == "skipped"),
        "env_blocked_count": sum(1 for r in records if r["execution_status"] == "env_blocked"),
        "records": records,
        "issues": issues,
        "guardrails": {
            "mysql_execution": "disabled",
            "spark_execution": "disabled",
            "llm_execution": "disabled",
            "case_artifact_write": "disabled",
            "generated_sql_case_write": "disabled",
        },
    }
    write_baseline_smoke_report(output_name, payload)
    return print_and_exit(payload, 0 if payload["ok"] else 1)


def cmd_baseline_smoke_preflight(args: argparse.Namespace) -> int:
    if args.execute:
        payload = {
            "command": "baseline-smoke-preflight",
            "cwd": str(ROOT),
            "ok": False,
            "ran_at_utc": utc_now(),
            "execution_mode": "execute_requested_but_blocked",
            "message": "Non-dry-run execution is intentionally not implemented yet. Use dry-run preflight only.",
            "errors": [
                {
                    "type": "execution_not_implemented",
                    "message": "baseline smoke scaffold currently supports dry-run planning only",
                }
            ],
        }
        write_baseline_smoke_report("preflight_execute_refused_common_core_v0.json", payload)
        return print_and_exit(payload, 1)

    config_path = resolve_repo_path(args.config)
    config = load_json(config_path)
    _, case_rows = read_registry(CASE_REGISTRY)
    case_index = {row["case_id"]: row for row in case_rows}

    case_records: list[dict[str, Any]] = []
    matrix_records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    baseline_records = [baseline_status_record(spec) for spec in config["baselines"]]
    baseline_index = {record["baseline_id"]: record for record in baseline_records}

    for case_spec in config["cases"]:
        case_id = case_spec["case_id"]
        pool = case_spec["pool"]
        case_root = pool_case_root(pool) / case_id
        registry_row = case_index.get(case_id)
        case_errors: list[dict[str, Any]] = []
        if registry_row is None:
            case_errors.append(
                {
                    "type": "missing_registry_row",
                    "message": "case_id not found in inventory/case_registry.csv",
                    "case_id": case_id,
                }
            )

        presence_checks = []
        expected_paths = {
            "case_dir": case_root,
            "manifest": case_root / "manifest.yaml",
            "source_sql": case_root / "source.sql",
            "rewrite_pos_01": case_root / "rewrite_pos_01.sql",
            "rewrite_neg_01": case_root / "rewrite_neg_01.sql",
            "pg_result_check": case_root / "runs" / "pg" / "result_check.json",
            "pg_plan_dir": case_root / "runs" / "pg" / "plans",
            "case_result_check": case_root / "runs" / "result_check.json",
            "case_plan_check": case_root / "runs" / "plan_check.json",
        }
        for label, path in expected_paths.items():
            exists = path.is_dir() if label in {"case_dir", "pg_plan_dir"} else path.is_file()
            presence_checks.append(
                {
                    "label": label,
                    "path": relative_to_root(path),
                    "exists": exists,
                    "required": label in {"case_dir", "manifest", "source_sql"},
                }
            )
            if label in {"case_dir", "manifest", "source_sql"} and not exists:
                case_errors.append(
                    {
                        "type": "missing_required_case_path",
                        "case_id": case_id,
                        "label": label,
                        "path": relative_to_root(path),
                    }
                )

        case_record = {
            "case_id": case_id,
            "pool": pool,
            "registry_found": registry_row is not None,
            "registry_validated_engines": registry_row.get("validated_engines", "") if registry_row else "",
            "registry_admission_status": registry_row.get("admission_status", "") if registry_row else "",
            "smoke_role": case_spec["smoke_role"],
            "why_selected": case_spec["why_selected"],
            "caveat": case_spec["caveat"],
            "presence_checks": presence_checks,
            "ok": not case_errors,
            "errors": case_errors,
        }
        case_records.append(case_record)
        errors.extend(case_errors)

        file_exists = {item["label"]: item["exists"] for item in presence_checks}
        for baseline_spec in config["baselines"]:
            baseline_id = baseline_spec["baseline_id"]
            baseline_state = baseline_index[baseline_id]
            eligibility_status = "eligible_for_dry_run"
            blocker = ""
            notes = []

            if not case_record["ok"]:
                eligibility_status = "blocked"
                blocker = "required case package files missing"
            elif baseline_id == "HUMAN_REFERENCE_POSITIVE" and not file_exists.get("rewrite_pos_01", False):
                eligibility_status = "blocked"
                blocker = "rewrite_pos_01.sql missing"
            elif baseline_id == "HARD_NEGATIVE_GUARD" and not file_exists.get("rewrite_neg_01", False):
                eligibility_status = "blocked"
                blocker = "rewrite_neg_01.sql missing"
            elif baseline_state["current_status"] == "scaffold_only":
                eligibility_status = "planned_but_blocked"
                blocker = baseline_state["blocker"]

            if not file_exists.get("pg_result_check", False):
                notes.append("PG result_check.json not present under runs/pg")
            if not file_exists.get("pg_plan_dir", False):
                notes.append("PG plan directory not present under runs/pg/plans")
            if baseline_id in {"SQLGLOT_OPT_SAME_DIALECT", "LLM_DIRECT_REWRITE_STRONG"}:
                notes.append("dry-run only; no generation will occur")

            if baseline_id == "NATIVE_IDENTITY":
                planned_variant = "source"
            elif baseline_id == "HUMAN_REFERENCE_POSITIVE":
                planned_variant = "rewrite_pos_01"
            elif baseline_id == "HARD_NEGATIVE_GUARD":
                planned_variant = "rewrite_neg_01"
            elif baseline_id == "SQLGLOT_OPT_SAME_DIALECT":
                planned_variant = "generated_same_dialect_candidate"
            else:
                planned_variant = "generated_llm_candidate"

            matrix_records.append(
                {
                    "baseline_id": baseline_id,
                    "case_id": case_id,
                    "pool": pool,
                    "planned_engine": "postgres",
                    "planned_variant": planned_variant,
                    "execution_mode": "dry_run",
                    "expected_input_files": baseline_smoke_input_paths(case_root, baseline_id),
                    "expected_output_paths": baseline_smoke_output_paths(case_id, baseline_id),
                    "eligibility_status": eligibility_status,
                    "blocker": blocker,
                    "notes": notes,
                }
            )

    payload = {
        "command": "baseline-smoke-preflight",
        "cwd": str(ROOT),
        "ok": not any(record["eligibility_status"] == "blocked" for record in matrix_records),
        "ran_at_utc": utc_now(),
        "execution_mode": "dry_run",
        "config_path": relative_to_root(config_path),
        "engine_scope": config["engine_scope"],
        "case_count": len(case_records),
        "baseline_count": len(baseline_records),
        "matrix_record_count": len(matrix_records),
        "baseline_roster": baseline_records,
        "case_roster_validation": case_records,
        "planned_matrix": matrix_records,
        "errors": errors,
        "guardrails": {
            "database_execution": "disabled",
            "llm_execution": "disabled",
            "non_dry_run_execution": "not_implemented",
        },
    }
    write_baseline_smoke_report("preflight_common_core_v0.json", payload)
    return print_and_exit(payload, 0 if payload["ok"] else 1)


def validate_scaffold_request(
    case_id: str,
    out: str,
    case_id_re: re.Pattern[str],
    case_id_message: str,
    case_root: Path,
    case_root_message: str,
) -> tuple[Path, list[dict[str, Any]]]:
    output_path = resolve_repo_path(out)
    errors: list[dict[str, Any]] = []

    if not case_id_re.fullmatch(case_id):
        errors.append(
            {
                "type": "invalid_case_id",
                "message": case_id_message,
                "value": case_id,
            }
        )

    try:
        output_path.relative_to(case_root.resolve())
    except ValueError:
        errors.append(
            {
                "type": "invalid_output_path",
                "message": case_root_message,
                "value": out,
            }
        )

    if output_path.exists():
        errors.append(
            {
                "type": "output_exists",
                "message": "existing directories or files must not be overwritten",
                "value": str(output_path),
            }
        )

    return output_path, errors


def build_scaffold_payload(
    command: str,
    case_id: str,
    output_path: Path,
    template_case_id: str,
    template_dir: Path,
    planned_directories: list[str],
    planned_files: list[str],
    auto_fillable_fields: dict[str, Any],
    human_required_fields: list[str],
    source_lineage_and_provenance: dict[str, list[str]],
    forbidden_automatic_decisions: list[str],
    errors: list[dict[str, Any]],
    mode: str = "dry-run",
    created_files: list[str] | None = None,
    extra_sections: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "command": command,
        "cwd": str(ROOT),
        "ok": not errors,
        "ran_at_utc": utc_now(),
        "mode": mode,
        "case_id": case_id,
        "output_path": relative_to_root(output_path) if output_path.is_relative_to(ROOT) else str(output_path),
        "template_basis": {
            "case_id": template_case_id,
            "path": relative_to_root(template_dir),
        },
        "planned_directories": planned_directories,
        "planned_files": planned_files,
        "auto_fillable_fields": auto_fillable_fields,
        "human_required_fields": human_required_fields,
        "source_lineage_and_provenance": source_lineage_and_provenance,
        "forbidden_automatic_decisions": forbidden_automatic_decisions,
        "created_files": created_files or [],
        "updated_registries": [],
        "admission_or_review_claims": [],
        "errors": errors,
    }
    if extra_sections:
        payload.update(extra_sections)
    return payload


def validate_case_id_not_in_registry(case_id: str, errors: list[dict[str, Any]]) -> None:
    _, rows = read_registry(CASE_REGISTRY)
    if any(row.get("case_id") == case_id for row in rows):
        errors.append(
            {
                "type": "case_id_exists",
                "message": "case_id already exists in inventory/case_registry.csv",
                "value": case_id,
            }
        )


def build_perf_registry_row_candidate(
    case_id: str,
    output_path: Path,
    mode: str,
) -> dict[str, Any]:
    manifest_path = output_path / "manifest.yaml"
    row = {field: "" for field in CASE_REQUIRED_FIELDS}
    row.update(
        {
            "case_id": case_id,
            "primary_pool": "performance",
            "current_maturity": f"draft scaffold candidate ({mode}); human review required",
            "benchmark_line": "staged",
            "package_engineering_status": "scaffold report candidate only; no registry writeback",
            "tri_engine_closure": "no",
            "formal_skeleton_status": "pre_skeleton",
            "release_grade_status": "incomplete",
            "admission_status": "staged_not_yet_admitted",
            "next_gap": "human must fill source/provenance, rewrites, schema/data/checker, execution, and plan evidence",
            "current_role": "draft_perf_scaffold_candidate",
            "archetype_status": "draft_constructed",
            "dataset_line": "not_yet_admitted",
            "promotion_status": "not_under_review",
            "admission_blockers": "missing_source_provenance_rewrites_validation_and_review",
            "last_review_doc": "NA_not_reviewed",
            "notes_link": (
                relative_to_root(manifest_path)
                if manifest_path.is_relative_to(ROOT)
                else str(manifest_path)
            ),
        }
    )
    return {
        "registry_row_candidate": {
            "columns": CASE_REQUIRED_FIELDS,
            "values": [row[field] for field in CASE_REQUIRED_FIELDS],
            "row": row,
        },
        "registry_row_human_required_fields": [
            "source_family",
            "source_detail",
            "origin_kind",
            "validated_engines",
            "last_updated",
            "human review of all conservative draft/status defaults before registry writeback",
        ],
        "registry_row_noninferable_fields": [
            "source_family",
            "source_detail",
            "origin_kind",
            "source registry truth",
            "source lineage and provenance facts",
            "validated engine evidence",
            "equivalence or divergence evidence",
            "plan evidence",
            "admission or promotion beyond conservative draft defaults",
            "archetype completion",
            "review-history basis",
        ],
    }


def write_placeholder_case(output_path: Path, placeholder_files: dict[str, str]) -> list[str]:
    output_root = output_path.resolve()
    for rel_path in placeholder_files:
        target = (output_path / rel_path).resolve()
        target.relative_to(output_root)
        if target.exists():
            raise FileExistsError(str(target))

    created_files: list[str] = []
    output_path.mkdir()
    for rel_path, content in placeholder_files.items():
        target = output_path / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        created_files.append(relative_to_root(target))
    return created_files


def env_visibility() -> dict[str, bool]:
    return {name: bool(os.environ.get(name)) for name in ENV_VARS}


def run_subprocess(command: str, argv: list[str]) -> tuple[dict[str, Any], int]:
    completed = subprocess.run(
        argv,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    payload: dict[str, Any] = {
        "command": command,
        "cwd": str(ROOT),
        "ok": completed.returncode == 0,
        "ran_at_utc": utc_now(),
        "returncode": completed.returncode,
        "stderr": completed.stderr,
        "stdout": completed.stdout,
        "subprocess_argv": argv,
        "visible": env_visibility(),
    }
    write_report(command, payload)
    return payload, completed.returncode


def cmd_env_check(_: argparse.Namespace) -> int:
    checks = env_visibility()
    ok = all(checks.values())
    payload: dict[str, Any] = {
        "command": "env-check",
        "cwd": str(ROOT),
        "ok": ok,
        "ran_at_utc": utc_now(),
        "visible": checks,
    }
    write_report("env-check", payload)
    return print_and_exit(payload, 0 if ok else 1)


def cmd_pg_check(_: argparse.Namespace) -> int:
    payload, exit_code = run_subprocess(
        "pg-check",
        ["bash", "scripts/check_postgres.sh"],
    )
    return print_and_exit(payload, exit_code)


def cmd_mysql_check(_: argparse.Namespace) -> int:
    payload, exit_code = run_subprocess(
        "mysql-check",
        ["bash", "scripts/check_mysql.sh"],
    )
    return print_and_exit(payload, exit_code)


def cmd_spark_check(_: argparse.Namespace) -> int:
    payload, exit_code = run_subprocess(
        "spark-check",
        [sys.executable, "scripts/smoke_spark.py"],
    )
    return print_and_exit(payload, exit_code)


def cmd_artifact_preflight(_: argparse.Namespace) -> int:
    required_paths = [
        "benchmark_spec/benchmark_spec_v0.md",
        "benchmark_spec/case_schema_v0.1.yaml",
        "taxonomy/coverage_taxonomy_v0.1.yaml",
        "cases/PERF/PERF_0001/manifest.yaml",
        "runs/smoke_case/",
        "runs/plans/",
    ]

    checks: list[dict[str, Any]] = []
    ok = True

    for rel_path in required_paths:
        normalized = rel_path.rstrip("/")
        path = ROOT / normalized
        is_dir = rel_path.endswith("/")
        exists = path.is_dir() if is_dir else path.is_file()
        ok = ok and exists
        checks.append(
            {
                "exists": exists,
                "path": rel_path,
                "type": "directory" if is_dir else "file",
            }
        )

    payload: dict[str, Any] = {
        "command": "artifact-preflight",
        "cwd": str(ROOT),
        "ok": ok,
        "ran_at_utc": utc_now(),
        "checks": checks,
    }
    write_report("artifact-preflight", payload)
    return print_and_exit(payload, 0 if ok else 1)


def cmd_registry_check(_: argparse.Namespace) -> int:
    source_headers, source_rows = read_registry(SOURCE_REGISTRY)
    case_headers, case_rows = read_registry(CASE_REGISTRY)
    errors: list[dict[str, Any]] = []

    validate_headers("source_registry", source_headers, SOURCE_REQUIRED_FIELDS, errors)
    validate_headers("case_registry", case_headers, CASE_REQUIRED_FIELDS, errors)
    validate_unique_ids("source_registry", source_rows, "source_id", errors)
    validate_unique_ids("case_registry", case_rows, "case_id", errors)
    source_controlled_counts = validate_controlled_fields(
        "source_registry",
        source_rows,
        CONTROLLED_FIELDS["source_registry"],
        errors,
    )
    case_controlled_counts = validate_controlled_fields(
        "case_registry",
        case_rows,
        CONTROLLED_FIELDS["case_registry"],
        errors,
    )
    validate_engine_values(case_rows, errors)
    ok = not errors

    checks = [
        {
            "check": "headers",
            "registry": "source_registry",
            "status": check_status(
                errors,
                "source_registry",
                "missing_fields",
                "unexpected_fields",
                "field_order_mismatch",
            ),
            "details": {
                "expected_field_count": len(SOURCE_REQUIRED_FIELDS),
                "actual_field_count": len(source_headers),
            },
        },
        {
            "check": "headers",
            "registry": "case_registry",
            "status": check_status(
                errors,
                "case_registry",
                "missing_fields",
                "unexpected_fields",
                "field_order_mismatch",
            ),
            "details": {
                "expected_field_count": len(CASE_REQUIRED_FIELDS),
                "actual_field_count": len(case_headers),
            },
        },
        {
            "check": "unique_ids",
            "registry": "source_registry",
            "status": check_status(errors, "source_registry", "blank_ids", "duplicate_ids"),
            "details": {"id_field": "source_id"},
        },
        {
            "check": "unique_ids",
            "registry": "case_registry",
            "status": check_status(errors, "case_registry", "blank_ids", "duplicate_ids"),
            "details": {"id_field": "case_id"},
        },
        {
            "check": "controlled_fields",
            "registry": "source_registry",
            "status": check_status(errors, "source_registry", "invalid_controlled_values"),
            "details": {"fields": sorted(CONTROLLED_FIELDS["source_registry"])},
        },
        {
            "check": "controlled_fields",
            "registry": "case_registry",
            "status": check_status(errors, "case_registry", "invalid_controlled_values"),
            "details": {"fields": sorted(CONTROLLED_FIELDS["case_registry"])},
        },
        {
            "check": "validated_engines",
            "registry": "case_registry",
            "status": check_status(errors, "case_registry", "invalid_validated_engines"),
            "details": {"allowed_values": list(ENGINE_ORDER)},
        },
    ]

    payload: dict[str, Any] = {
        "command": "registry-check",
        "cwd": str(ROOT),
        "ok": ok,
        "ran_at_utc": utc_now(),
        "error_count": len(errors),
        "checks": checks,
        "registries": {
            "source_registry": {
                "path": str(SOURCE_REGISTRY.relative_to(ROOT)),
                "row_count": len(source_rows),
                "field_count": len(source_headers),
                "schema": {
                    "expected_fields": SOURCE_REQUIRED_FIELDS,
                    "actual_fields": source_headers,
                    "field_order_ok": source_headers == SOURCE_REQUIRED_FIELDS,
                },
                "controlled_field_counts": source_controlled_counts,
            },
            "case_registry": {
                "path": str(CASE_REGISTRY.relative_to(ROOT)),
                "row_count": len(case_rows),
                "field_count": len(case_headers),
                "schema": {
                    "expected_fields": CASE_REQUIRED_FIELDS,
                    "actual_fields": case_headers,
                    "field_order_ok": case_headers == CASE_REQUIRED_FIELDS,
                },
                "controlled_field_counts": case_controlled_counts,
                "validated_engine_counts": count_values(case_rows, "validated_engines"),
            },
        },
        "errors": errors,
    }
    write_report("registry-check", payload)
    return print_and_exit(payload, 0 if ok else 1)


def cmd_current_snapshot(_: argparse.Namespace) -> int:
    _, source_rows = read_registry(SOURCE_REGISTRY)
    _, case_rows = read_registry(CASE_REGISTRY)

    engine_case_counts = {engine: 0 for engine in ENGINE_ORDER}
    tri_engine_validated = 0
    engine_sets: Counter[str] = Counter()

    for row in case_rows:
        engines = parse_engine_set(row.get("validated_engines", ""))
        engine_sets["|".join(engines) if engines else "none"] += 1
        if set(engines) == ENGINE_IDS:
            tri_engine_validated += 1
        for engine in engines:
            engine_case_counts[engine] += 1

    payload: dict[str, Any] = {
        "command": "current-snapshot",
        "cwd": str(ROOT),
        "ok": True,
        "ran_at_utc": utc_now(),
        "basis": {
            "sources": str(SOURCE_REGISTRY.relative_to(ROOT)),
            "cases": str(CASE_REGISTRY.relative_to(ROOT)),
        },
        "sources": {
            "total": len(source_rows),
            "counts": {
                "by_acquisition_status": count_values(source_rows, "acquisition_status"),
                "by_current_real_status": count_values(source_rows, "current_real_status"),
            },
        },
        "cases": {
            "total": len(case_rows),
            "counts": {
                "by_pool": count_values(case_rows, "primary_pool"),
                "by_admission_status": count_values(case_rows, "admission_status"),
                "by_promotion_status": count_values(case_rows, "promotion_status"),
                "by_dataset_line": count_values(case_rows, "dataset_line"),
                "by_validated_engine_set": dict(sorted(engine_sets.items())),
            },
            "engine_coverage": {
                "case_count_by_engine": engine_case_counts,
                "tri_engine_validated_case_count": tri_engine_validated,
            },
        },
    }
    write_report("current-snapshot", payload)
    return print_and_exit(payload, 0)


def cmd_scaffold_perf_case(args: argparse.Namespace) -> int:
    output_path, errors = validate_scaffold_request(
        args.case_id,
        args.out,
        PERF_CASE_ID_RE,
        "case_id must match PERF_####",
        PERF_CASE_ROOT,
        "output path must stay under cases/PERF/",
    )

    planned_directories = [
        "provenance",
        "schema",
        "metadata",
        "validation",
        "analysis",
    ]
    planned_files = [
        "manifest.yaml",
        "source.sql",
        "rewrite_pos_01.sql",
        "rewrite_neg_01.sql",
        "taxonomy_trial_v0.2.yaml",
        "data_profile.json",
        "schema/ddl_pg.sql",
        "schema/ddl_mysql.sql",
        "schema/ddl_spark.sql",
        "metadata/engine_metadata.yaml",
        "validation/checker.yaml",
        "validation/witness_dataset.yaml",
        "provenance/raw_record.json",
        "provenance/provenance_notes.txt",
        "analysis/canonical_ast.json",
        "analysis/logical_ir.json",
        "analysis/sql_span_logical_map.json",
        "analysis/logical_physical_map.json",
    ]
    auto_fillable_fields = {
        "manifest": {
            "case_id": args.case_id,
            "pool": "performance",
            "source": {"file": "source.sql"},
            "variants": {
                "positives": ["rewrite_pos_01.sql"],
                "negatives": ["rewrite_neg_01.sql"],
            },
            "targets": {"engines": ["postgres", "mysql", "spark"]},
            "schema": {
                "pg_ddl": "schema/ddl_pg.sql",
                "mysql_ddl": "schema/ddl_mysql.sql",
                "spark_ddl": "schema/ddl_spark.sql",
            },
            "metadata": {"engine_metadata": "metadata/engine_metadata.yaml"},
            "validation": {
                "checker": "validation/checker.yaml",
                "witness_dataset": "validation/witness_dataset.yaml",
            },
            "status_defaults": {
                "parse_checked": False,
                "exec_checked_pg": False,
                "exec_checked_mysql": False,
                "exec_checked_spark": False,
                "plan_checked": False,
                "schema_ready": False,
                "validation_ready": False,
                "release_grade": False,
            },
        },
        "metadata": {
            "source_dialect": "TODO",
            "target_engines": ["postgres", "mysql", "spark"],
            "validated_engines": [],
        },
        "checker": {
            "type": "value_normalized_result_equivalence_checker",
            "expectations": {
                "equal": ["source.sql", "rewrite_pos_01.sql"],
                "not_equal": ["source.sql", "rewrite_neg_01.sql"],
            },
        },
    }
    human_required_fields = [
        "source SQL text",
        "positive rewrite SQL text",
        "negative rewrite SQL text",
        "source_id and seed lineage",
        "source template and materialization command",
        "required tables",
        "SQL feature tags",
        "rewrite opportunity tags",
        "pool-specific taxonomy tags",
        "PostgreSQL/MySQL/Spark DDL content",
        "data profile facts",
        "witness dataset details",
        "checker semantics beyond generic source/positive/negative shape",
        "execution result artifact paths",
        "plan artifact paths",
        "analysis artifacts",
        "all validation status flags",
    ]
    source_lineage_and_provenance = {
        "always_human_required": [
            "source_id",
            "source_family",
            "source_name",
            "source query identifier or template name",
            "source entry path or workload query path",
            "seed identifier when applicable",
            "materialization command or extraction path",
            "scale factor or data-generation context when applicable",
            "parameter substitution details when applicable",
            "source-to-source.sql freezing notes",
            "license/access pointer back to source registry",
            "case-local provenance notes",
        ],
        "placeholder_fields": [
            "provenance/",
            "provenance/raw_record.json",
            "provenance/provenance_notes.txt",
            "manifest.provenance.source_id: TODO",
            "manifest.provenance.seed_id: TODO",
            "manifest.provenance.source_name: TODO",
            "manifest.provenance.source_entry: TODO",
            "manifest.provenance.raw_record_file: TODO",
            "manifest.provenance.provenance_notes: TODO",
        ],
        "never_auto_infer": [
            "source identity",
            "source registry truth",
            "source family",
            "source query number or template",
            "seed ID",
            "scale factor",
            "materialization correctness",
            "license/access status",
            "provenance completeness",
            "whether template provenance applies to this case",
        ],
    }
    forbidden_automatic_decisions = [
        "admission status",
        "promotion status",
        "common-core or extended dataset line",
        "registry truth",
        "ground-truth equivalence",
        "positive rewrite validity",
        "negative rewrite invalidity",
        "execution success",
        "plan sufficiency",
        "archetype completion",
        "source acquisition or workload curation",
    ]
    mode = "write" if args.write else "dry-run"
    created_files: list[str] = []

    if args.write:
        validate_case_id_not_in_registry(args.case_id, errors)

    placeholder_files = {
        "manifest.yaml": f"""case_id: {args.case_id}
pool: performance
provenance:
  source_id: TODO
  seed_id: TODO
  source_name: TODO
  source_entry: TODO
  raw_record_file: provenance/raw_record.json
  provenance_notes: provenance/provenance_notes.txt
source:
  file: source.sql
variants:
  positives:
    - rewrite_pos_01.sql
  negatives:
    - rewrite_neg_01.sql
targets:
  engines:
    - postgres
    - mysql
    - spark
required_tables: []
features: []
status:
  parse_checked: false
  exec_checked_pg: false
  exec_checked_mysql: false
  exec_checked_spark: false
  plan_checked: false
  schema_ready: false
  validation_ready: false
  release_grade: false
schema:
  pg_ddl: schema/ddl_pg.sql
  mysql_ddl: schema/ddl_mysql.sql
  spark_ddl: schema/ddl_spark.sql
data_profile:
  file: data_profile.json
metadata:
  engine_metadata: metadata/engine_metadata.yaml
validation:
  checker: validation/checker.yaml
  witness_dataset: validation/witness_dataset.yaml
notes:
  - TODO: Human must fill source lineage, SQL text, rewrites, data, validation, artifacts, and review status.
""",
        "source.sql": "-- TODO: Human must fill source SQL. Do not infer source facts automatically.\n",
        "rewrite_pos_01.sql": "-- TODO: Human must fill positive rewrite SQL and validate equivalence.\n",
        "rewrite_neg_01.sql": "-- TODO: Human must fill negative rewrite SQL and validate divergence.\n",
        "taxonomy_trial_v0.2.yaml": "case_id: TODO\npool: performance\nlabels: []\nnotes:\n  - TODO: Human must fill taxonomy tags.\n",
        "data_profile.json": '{\n  "status": "TODO",\n  "notes": "Human must fill data profile facts."\n}\n',
        "schema/ddl_pg.sql": "-- TODO: Human must fill PostgreSQL DDL.\n",
        "schema/ddl_mysql.sql": "-- TODO: Human must fill MySQL DDL.\n",
        "schema/ddl_spark.sql": "-- TODO: Human must fill Spark DDL.\n",
        "metadata/engine_metadata.yaml": "source_dialect: TODO\ntarget_engines:\n  - postgres\n  - mysql\n  - spark\nvalidated_engines: []\nnotes:\n  - TODO: Human must fill engine metadata and validation evidence.\n",
        "validation/checker.yaml": "type: value_normalized_result_equivalence_checker\nexpectations:\n  equal:\n    - source.sql\n    - rewrite_pos_01.sql\n  not_equal:\n    - source.sql\n    - rewrite_neg_01.sql\nexpected_results: TODO\nnotes:\n  - TODO: Human must fill checker semantics and expected results.\n",
        "validation/witness_dataset.yaml": "status: TODO\nnotes:\n  - TODO: Human must fill witness or data subset details.\n",
        "provenance/raw_record.json": '{\n  "status": "TODO",\n  "notes": "Human must fill or attach raw source record. Do not copy template provenance automatically."\n}\n',
        "provenance/provenance_notes.txt": "TODO: Human must fill source lineage, source registry pointer, materialization, and freezing notes.\n",
        "analysis/canonical_ast.json": '{\n  "status": "TODO",\n  "notes": "Human must fill canonical AST artifact."\n}\n',
        "analysis/logical_ir.json": '{\n  "status": "TODO",\n  "notes": "Human must fill logical IR artifact."\n}\n',
        "analysis/sql_span_logical_map.json": '{\n  "status": "TODO",\n  "notes": "Human must fill SQL span to logical mapping artifact."\n}\n',
        "analysis/logical_physical_map.json": '{\n  "status": "TODO",\n  "notes": "Human must fill logical to physical mapping artifact."\n}\n',
    }

    if args.write and not errors:
        try:
            created_files = write_placeholder_case(output_path, placeholder_files)
        except OSError as exc:
            errors.append(
                {
                    "type": "write_failed",
                    "message": "failed to create placeholder performance scaffold",
                    "value": str(exc),
                }
            )

    extra_sections = (
        build_perf_registry_row_candidate(args.case_id, output_path, mode)
        if not errors
        else None
    )
    payload = build_scaffold_payload(
        "scaffold-perf-case",
        args.case_id,
        output_path,
        PERF_TEMPLATE_CASE_ID,
        PERF_TEMPLATE_DIR,
        planned_directories,
        planned_files,
        auto_fillable_fields,
        human_required_fields,
        source_lineage_and_provenance,
        forbidden_automatic_decisions,
        errors,
        mode,
        created_files,
        extra_sections,
    )
    write_report("scaffold-perf-case", payload)
    return print_and_exit(payload, 0 if payload["ok"] else 1)


def cmd_scaffold_port_case(args: argparse.Namespace) -> int:
    output_path, errors = validate_scaffold_request(
        args.case_id,
        args.out,
        PORT_CASE_ID_RE,
        "case_id must match PORT_####",
        PORT_CASE_ROOT,
        "output path must stay under cases/PORT/",
    )

    planned_directories = [
        "provenance",
        "schema",
        "metadata",
        "validation",
    ]
    planned_files = [
        "manifest.yaml",
        "source.sql",
        "rewrite_pos_01.sql",
        "rewrite_neg_01.sql",
        "rewrite_pos_02_spark.sql",
        "rewrite_neg_02_spark.sql",
        "taxonomy_trial_v0.2.yaml",
        "data_profile.json",
        "schema/ddl_pg.sql",
        "schema/ddl_mysql.sql",
        "schema/ddl_spark.sql",
        "metadata/engine_metadata.yaml",
        "validation/checker.yaml",
        "validation/witness_dataset.yaml",
        "provenance/raw_record.json",
        "provenance/provenance_notes.txt",
    ]
    auto_fillable_fields = {
        "manifest": {
            "case_id": args.case_id,
            "pool": "portability",
            "source": {"dialect": "TODO", "file": "source.sql"},
            "variants": {
                "positives": ["rewrite_pos_01.sql", "rewrite_pos_02_spark.sql"],
                "negatives": ["rewrite_neg_01.sql", "rewrite_neg_02_spark.sql"],
            },
            "targets": {"engines": ["postgres", "mysql", "spark"]},
            "schema": {
                "pg_ddl": "schema/ddl_pg.sql",
                "mysql_ddl": "schema/ddl_mysql.sql",
                "spark_ddl": "schema/ddl_spark.sql",
            },
            "metadata": {"engine_metadata": "metadata/engine_metadata.yaml"},
            "validation": {
                "checker": "validation/checker.yaml",
                "witness_dataset": "validation/witness_dataset.yaml",
            },
            "status_defaults": {
                "seed_localized": False,
                "source_frozen": False,
                "rewrite_variants_ready": False,
                "parse_checked": False,
                "exec_checked_pg": False,
                "exec_checked_mysql": False,
                "exec_checked_spark": False,
                "plan_checked": False,
                "taxonomy_trial_ready": False,
                "schema_ready": False,
                "validation_ready": False,
                "release_grade": False,
            },
        },
        "metadata": {
            "source_dialect": "TODO",
            "target_engines": ["postgres", "mysql", "spark"],
            "validated_engines": [],
        },
        "checker": {
            "type": "cross_engine_portability_checker",
            "normalization": {
                "sort_rows": True,
                "trim_whitespace": True,
                "normalize_tabs": True,
                "normalize_numeric_format": True,
                "normalize_null": True,
            },
            "reference": {"postgres_source": "source.sql"},
            "comparisons": {
                "mysql": {
                    "equal_to_reference": ["rewrite_pos_01.sql"],
                    "not_equal_to_reference": ["rewrite_neg_01.sql"],
                },
                "spark": {
                    "equal_to_reference": ["rewrite_pos_02_spark.sql"],
                    "not_equal_to_reference": ["rewrite_neg_02_spark.sql"],
                },
            },
        },
    }
    human_required_fields = [
        "source SQL text",
        "source dialect classification",
        "MySQL positive rewrite SQL text",
        "MySQL negative rewrite SQL text",
        "Spark positive rewrite SQL text",
        "Spark negative rewrite SQL text",
        "source_id and seed lineage",
        "source family and source entry",
        "raw source record and provenance notes",
        "required tables",
        "PostgreSQL/MySQL/Spark DDL content",
        "witness dataset details",
        "PostgreSQL source-side expected result",
        "MySQL target-side positive and negative expected results",
        "Spark target-side positive and negative expected results",
        "portability taxonomy tags",
        "dialect-specific semantic mapping notes",
        "source-side plan and result artifact paths",
        "target-side plan and result artifact paths",
        "all validation status flags",
    ]
    source_lineage_and_provenance = {
        "always_human_required": [
            "source_id",
            "source_family",
            "source_name",
            "source subset",
            "source entry locator",
            "seed identifier when applicable",
            "raw source record",
            "provenance notes",
            "source dialect classification",
            "source-side reference engine",
            "target dialect rewrite derivation notes",
            "dialect-specific semantic mapping notes",
            "source-side and target-side artifact lineage",
            "license/access pointer back to source registry",
        ],
        "placeholder_fields": [
            "provenance/",
            "provenance/raw_record.json",
            "provenance/provenance_notes.txt",
            "manifest.provenance.source_id: TODO",
            "manifest.provenance.seed_id: TODO",
            "manifest.provenance.source_name: TODO",
            "manifest.provenance.source_subset: TODO",
            "manifest.provenance.source_entry: TODO",
            "manifest.provenance.raw_record_file: TODO",
            "manifest.provenance.provenance_notes: TODO",
            "manifest.source.dialect: TODO",
            "metadata.source_dialect: TODO",
        ],
        "never_auto_infer": [
            "source identity",
            "source registry truth",
            "source dialect truth",
            "target dialect mapping correctness",
            "raw record identity",
            "source entry index",
            "semantic equivalence across dialects",
            "target rewrite preservation",
            "negative rewrite divergence",
            "expected results",
            "provenance completeness",
            "whether template provenance applies to this case",
        ],
    }
    portability_specific_requirements = [
        "source dialect vs target dialect rewrites must be explicit",
        "portability checker must compare target rewrites against a source-side reference",
        "source-side and target-side plan evidence must be recorded separately",
        "positive target rewrites must preserve the source-side result under documented normalization",
        "negative target rewrites must demonstrate documented divergence",
        "dialect-specific semantic mappings must be human reviewed",
    ]
    forbidden_automatic_decisions = [
        "admission status",
        "promotion status",
        "common-core or extended dataset line",
        "registry truth",
        "source dialect truth",
        "ground-truth equivalence",
        "target rewrite semantic preservation",
        "negative rewrite divergence",
        "execution success",
        "plan sufficiency",
        "taxonomy finality",
        "archetype completion",
        "source acquisition or workload curation",
    ]

    payload = build_scaffold_payload(
        "scaffold-port-case",
        args.case_id,
        output_path,
        PORT_TEMPLATE_CASE_ID,
        PORT_TEMPLATE_DIR,
        planned_directories,
        planned_files,
        auto_fillable_fields,
        human_required_fields,
        source_lineage_and_provenance,
        forbidden_automatic_decisions,
        errors,
        extra_sections={"portability_specific_requirements": portability_specific_requirements},
    )
    write_report("scaffold-port-case", payload)
    return print_and_exit(payload, 0 if payload["ok"] else 1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m scripts.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    env_parser = subparsers.add_parser("env-check")
    env_parser.set_defaults(func=cmd_env_check)

    pg_parser = subparsers.add_parser("pg-check")
    pg_parser.set_defaults(func=cmd_pg_check)

    mysql_parser = subparsers.add_parser("mysql-check")
    mysql_parser.set_defaults(func=cmd_mysql_check)

    spark_parser = subparsers.add_parser("spark-check")
    spark_parser.set_defaults(func=cmd_spark_check)

    artifact_parser = subparsers.add_parser("artifact-preflight")
    artifact_parser.set_defaults(func=cmd_artifact_preflight)

    registry_parser = subparsers.add_parser("registry-check")
    registry_parser.set_defaults(func=cmd_registry_check)

    snapshot_parser = subparsers.add_parser("current-snapshot")
    snapshot_parser.set_defaults(func=cmd_current_snapshot)

    scaffold_parser = subparsers.add_parser("scaffold-perf-case")
    scaffold_parser.add_argument("--case-id", required=True)
    scaffold_parser.add_argument("--out", required=True)
    scaffold_parser.add_argument("--dry-run", action="store_true", default=True)
    scaffold_parser.add_argument("--write", action="store_true", default=False)
    scaffold_parser.set_defaults(func=cmd_scaffold_perf_case)

    port_scaffold_parser = subparsers.add_parser("scaffold-port-case")
    port_scaffold_parser.add_argument("--case-id", required=True)
    port_scaffold_parser.add_argument("--out", required=True)
    port_scaffold_parser.add_argument("--dry-run", action="store_true", default=True)
    port_scaffold_parser.set_defaults(func=cmd_scaffold_port_case)

    baseline_smoke_parser = subparsers.add_parser("baseline-smoke-preflight")
    baseline_smoke_parser.add_argument(
        "--config",
        default="docs/_scratch/baseline_smoke_common_core_v0.json",
    )
    baseline_smoke_parser.add_argument("--execute", action="store_true", default=False)
    baseline_smoke_parser.set_defaults(func=cmd_baseline_smoke_preflight)

    control_records_parser = subparsers.add_parser("baseline-smoke-control-records")
    control_records_parser.add_argument(
        "--config",
        default="docs/_scratch/baseline_smoke_common_core_v0.json",
    )
    control_records_parser.add_argument(
        "--baseline-id",
        action="append",
        default=[],
    )
    control_records_parser.add_argument("--execute", action="store_true", default=False)
    control_records_parser.set_defaults(func=cmd_baseline_smoke_control_records)

    control_summary_parser = subparsers.add_parser("baseline-smoke-control-summary")
    control_summary_parser.add_argument(
        "--input",
        default="reports/baseline_smoke/control_records_common_core_v0.json",
    )
    control_summary_parser.add_argument(
        "--output",
        default="control_records_summary_common_core_v0.json",
    )
    control_summary_parser.add_argument("--execute", action="store_true", default=False)
    control_summary_parser.set_defaults(func=cmd_baseline_smoke_control_summary)

    native_identity_pg_parser = subparsers.add_parser("baseline-smoke-native-identity-pg")
    native_identity_pg_parser.add_argument(
        "--config",
        default="docs/_scratch/baseline_smoke_common_core_v0.json",
    )
    native_identity_pg_parser.add_argument("--case-id", action="append", default=[])
    native_identity_pg_parser.add_argument("--statement-timeout-ms", type=int, default=30000)
    native_identity_pg_parser.add_argument("--execute", action="store_true", default=False)
    native_identity_pg_parser.add_argument(
        "--execute-native-identity",
        action="store_true",
        default=False,
    )
    native_identity_pg_parser.set_defaults(func=cmd_baseline_smoke_native_identity_pg)

    human_positive_pg_parser = subparsers.add_parser("baseline-smoke-human-positive-pg")
    human_positive_pg_parser.add_argument(
        "--config",
        default="docs/_scratch/baseline_smoke_common_core_v0.json",
    )
    human_positive_pg_parser.add_argument("--case-id", action="append", default=[])
    human_positive_pg_parser.add_argument("--statement-timeout-ms", type=int, default=30000)
    human_positive_pg_parser.add_argument("--execute", action="store_true", default=False)
    human_positive_pg_parser.add_argument(
        "--execute-human-positive",
        action="store_true",
        default=False,
    )
    human_positive_pg_parser.set_defaults(func=cmd_baseline_smoke_human_positive_pg)

    hard_negative_pg_parser = subparsers.add_parser("baseline-smoke-hard-negative-pg")
    hard_negative_pg_parser.add_argument(
        "--config",
        default="docs/_scratch/baseline_smoke_common_core_v0.json",
    )
    hard_negative_pg_parser.add_argument("--case-id", action="append", default=[])
    hard_negative_pg_parser.add_argument("--statement-timeout-ms", type=int, default=30000)
    hard_negative_pg_parser.add_argument("--execute", action="store_true", default=False)
    hard_negative_pg_parser.add_argument(
        "--execute-hard-negative",
        action="store_true",
        default=False,
    )
    hard_negative_pg_parser.set_defaults(func=cmd_baseline_smoke_hard_negative_pg)

    pg_control_summary_parser = subparsers.add_parser("baseline-smoke-pg-control-summary")
    pg_control_summary_parser.add_argument(
        "--native-report",
        default="reports/baseline_smoke/native_identity_pg_canary_v0.json",
    )
    pg_control_summary_parser.add_argument(
        "--positive-report",
        default="reports/baseline_smoke/human_reference_positive_pg_v0.json",
    )
    pg_control_summary_parser.add_argument(
        "--negative-report",
        default="reports/baseline_smoke/hard_negative_guard_pg_v0.json",
    )
    pg_control_summary_parser.add_argument(
        "--output",
        default="pg_control_smoke_summary_v0.json",
    )
    pg_control_summary_parser.add_argument("--execute", action="store_true", default=False)
    pg_control_summary_parser.set_defaults(func=cmd_baseline_smoke_pg_control_summary)

    sqlglot_preflight_parser = subparsers.add_parser("baseline-smoke-sqlglot-preflight")
    sqlglot_preflight_parser.add_argument(
        "--config",
        default="docs/_scratch/baseline_smoke_common_core_v0.json",
    )
    sqlglot_preflight_parser.add_argument("--case-id", action="append", default=[])
    sqlglot_preflight_parser.add_argument("--dialect", default="postgres")
    sqlglot_preflight_parser.add_argument("--write-generated", action="store_true", default=False)
    sqlglot_preflight_parser.add_argument("--execute", action="store_true", default=False)
    sqlglot_preflight_parser.set_defaults(func=cmd_baseline_smoke_sqlglot_preflight)

    sqlglot_pg_canary_parser = subparsers.add_parser("baseline-smoke-sqlglot-pg-canary")
    sqlglot_pg_canary_parser.add_argument(
        "--config",
        default="docs/_scratch/baseline_smoke_common_core_v0.json",
    )
    sqlglot_pg_canary_parser.add_argument("--case-id", action="append", default=[])
    sqlglot_pg_canary_parser.add_argument("--dialect", default="postgres")
    sqlglot_pg_canary_parser.add_argument("--statement-timeout-ms", type=int, default=30000)
    sqlglot_pg_canary_parser.add_argument("--execute", action="store_true", default=False)
    sqlglot_pg_canary_parser.add_argument("--execute-sqlglot", action="store_true", default=False)
    sqlglot_pg_canary_parser.set_defaults(func=cmd_baseline_smoke_sqlglot_pg_canary)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
