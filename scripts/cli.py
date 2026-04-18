from __future__ import annotations

import argparse
import csv
import json
import os
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

    payload: dict[str, Any] = {
        "command": "registry-check",
        "cwd": str(ROOT),
        "ok": not errors,
        "ran_at_utc": utc_now(),
        "registries": {
            "source_registry": {
                "path": str(SOURCE_REGISTRY.relative_to(ROOT)),
                "row_count": len(source_rows),
                "field_count": len(source_headers),
                "controlled_field_counts": source_controlled_counts,
            },
            "case_registry": {
                "path": str(CASE_REGISTRY.relative_to(ROOT)),
                "row_count": len(case_rows),
                "field_count": len(case_headers),
                "controlled_field_counts": case_controlled_counts,
                "validated_engine_counts": count_values(case_rows, "validated_engines"),
            },
        },
        "errors": errors,
    }
    write_report("registry-check", payload)
    return print_and_exit(payload, 0 if not errors else 1)


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
            if engine in engine_case_counts:
                engine_case_counts[engine] += 1

    payload: dict[str, Any] = {
        "command": "current-snapshot",
        "cwd": str(ROOT),
        "ok": True,
        "ran_at_utc": utc_now(),
        "source_basis": str(SOURCE_REGISTRY.relative_to(ROOT)),
        "case_basis": str(CASE_REGISTRY.relative_to(ROOT)),
        "sources": {
            "total": len(source_rows),
            "by_status": count_values(source_rows, "acquisition_status"),
            "by_current_real_status": count_values(source_rows, "current_real_status"),
        },
        "cases": {
            "total": len(case_rows),
            "by_pool": count_values(case_rows, "primary_pool"),
            "by_admission_status": count_values(case_rows, "admission_status"),
            "by_promotion_status": count_values(case_rows, "promotion_status"),
            "by_dataset_line": count_values(case_rows, "dataset_line"),
            "by_validated_engine_set": dict(sorted(engine_sets.items())),
            "validated_engine_coverage": {
                "case_count_by_engine": engine_case_counts,
                "tri_engine_validated_case_count": tri_engine_validated,
            },
        },
    }
    write_report("current-snapshot", payload)
    return print_and_exit(payload, 0)


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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
