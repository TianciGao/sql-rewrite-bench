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
ENV_VARS = ["PGHOST", "MYSQL_HOST", "SPARK_LOCAL_IP"]
SOURCE_REGISTRY = ROOT / "inventory" / "source_registry.csv"
CASE_REGISTRY = ROOT / "inventory" / "case_registry.csv"
ENGINE_ORDER = ("pg", "mysql", "spark")
ENGINE_IDS = set(ENGINE_ORDER)
PERF_CASE_ID_RE = re.compile(r"^PERF_\d{4}$")
PERF_TEMPLATE_CASE_ID = "PERF_0002"
PERF_TEMPLATE_DIR = ROOT / "cases" / "PERF" / PERF_TEMPLATE_CASE_ID
PERF_CASE_ROOT = ROOT / "cases" / "PERF"
PORT_CASE_ID_RE = re.compile(r"^PORT_\d{4}$")
PORT_TEMPLATE_CASE_ID = "PORT_0002"
PORT_TEMPLATE_DIR = ROOT / "cases" / "PORT" / PORT_TEMPLATE_CASE_ID
PORT_CASE_ROOT = ROOT / "cases" / "PORT"

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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
