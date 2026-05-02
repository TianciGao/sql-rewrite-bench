from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
