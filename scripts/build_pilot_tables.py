#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "pilot"


CASE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "PERF_0001": {
        "manifest": "cases/PERF/PERF_0001/manifest.yaml",
        "pool": "performance",
        "source_family": "manual_seed",
        "data_origin": "manual_smoke_anchor",
        "current_maturity": "stable_pilot_anchor",
        "admitted_or_staged": "anchor",
        "include_in_first_slice": "yes",
        "notes": "smoke/pipeline anchor",
        "validated_engines_fallback": "postgres;mysql;spark",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "PERF_0002": {
        "manifest": "cases/PERF/PERF_0002/manifest.yaml",
        "pool": "performance",
        "source_family": "TPC-DS",
        "data_origin": "query53_tpl_materialized",
        "current_maturity": "admitted_external_common_core",
        "admitted_or_staged": "admitted",
        "include_in_first_slice": "yes",
        "notes": "current strongest external performance case",
        "validated_engines_fallback": "postgres;mysql;spark",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "PERF_0003": {
        "manifest": "cases/PERF/PERF_0003/manifest.yaml",
        "pool": "performance",
        "source_family": "JOB",
        "data_origin": "job_27a",
        "current_maturity": "pg_only_staged_performance_draft",
        "admitted_or_staged": "staged",
        "include_in_first_slice": "no",
        "notes": "JOB line currently frozen as partial realized supplement",
        "validated_engines_fallback": "postgres",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "PERF_0004": {
        "manifest": "cases/PERF/PERF_0004/manifest.yaml",
        "pool": "performance",
        "source_family": "JOB",
        "data_origin": "job_30b",
        "current_maturity": "pg_validated_staged_performance_draft",
        "admitted_or_staged": "staged",
        "include_in_first_slice": "no",
        "notes": "JOB line currently frozen as partial realized supplement",
        "validated_engines_fallback": "postgres",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "LONGTAIL_0001": {
        "manifest": "cases/LONGTAIL/LONGTAIL_0001/manifest.yaml",
        "pool": "longtail",
        "source_family": "manual_seed",
        "data_origin": "manual_longtail_anchor",
        "current_maturity": "stable_pilot_anchor",
        "admitted_or_staged": "anchor",
        "include_in_first_slice": "yes",
        "notes": "structure-rich longtail anchor",
        "validated_engines_fallback": "postgres;mysql;spark",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "LONGTAIL_0002": {
        "manifest": "cases/LONGTAIL/LONGTAIL_0002/manifest.yaml",
        "pool": "longtail",
        "source_family": "SQLStorm",
        "data_origin": "source_12033",
        "current_maturity": "pg_validated_staged_longtail_draft",
        "admitted_or_staged": "staged",
        "include_in_first_slice": "no",
        "notes": "engine closure still missing",
        "validated_engines_fallback": "postgres",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "CONS_0001": {
        "manifest": "cases/CONS/CONS_0001/manifest.yaml",
        "pool": "consistency",
        "source_family": "manual_seed",
        "data_origin": "manual_consistency_anchor",
        "current_maturity": "stable_pilot_anchor",
        "admitted_or_staged": "anchor",
        "include_in_first_slice": "yes",
        "notes": "correctness anchor",
        "validated_engines_fallback": "postgres;mysql;spark",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "CONS_0002": {
        "manifest": "cases/CONS/CONS_0002/manifest.yaml",
        "pool": "consistency",
        "source_family": "Calcite",
        "data_origin": "new-decorr_iq_seed",
        "current_maturity": "pg_validated_staged_consistency_draft",
        "admitted_or_staged": "staged",
        "include_in_first_slice": "no",
        "notes": "broader engine validation still missing",
        "validated_engines_fallback": "postgres",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "CONS_0003": {
        "manifest": "cases/CONS/CONS_0003/manifest.yaml",
        "pool": "consistency",
        "source_family": "VeriEQL",
        "data_origin": "calcite_397_159",
        "current_maturity": "tri_engine_validated_staged_consistency_draft",
        "admitted_or_staged": "staged",
        "include_in_first_slice": "yes",
        "notes": "tri-engine validated but still not_yet_admitted",
        "validated_engines_fallback": "postgres;mysql;spark",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "CONS_0004": {
        "manifest": "cases/CONS/CONS_0004/manifest.yaml",
        "pool": "consistency",
        "source_family": "VeriEQL",
        "data_origin": "calcite_397_362",
        "current_maturity": "tri_engine_validated_staged_consistency_draft",
        "admitted_or_staged": "staged",
        "include_in_first_slice": "yes",
        "notes": "tri-engine validated but still not_yet_admitted",
        "validated_engines_fallback": "postgres;mysql;spark",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "PORT_0001": {
        "manifest": "cases/PORT/PORT_0001/manifest.yaml",
        "pool": "portability",
        "source_family": "manual_seed",
        "data_origin": "portability_anchor_package",
        "current_maturity": "stable_pilot_anchor",
        "admitted_or_staged": "anchor",
        "include_in_first_slice": "yes",
        "notes": "clean portability anchor",
        "validated_engines_fallback": "postgres;mysql;spark",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
    "PORT_0002": {
        "manifest": "cases/PORT/PORT_0002/manifest.yaml",
        "pool": "portability",
        "source_family": "PARROT",
        "data_origin": "bird_pg_res_json_0",
        "current_maturity": "admitted_external_common_core",
        "admitted_or_staged": "admitted",
        "include_in_first_slice": "yes",
        "notes": "current strongest external portability case",
        "validated_engines_fallback": "postgres;mysql;spark",
        "result_artifacts_present_fallback": "yes",
        "plan_artifacts_present_fallback": "yes",
    },
}

SOURCE_ROWS: List[Dict[str, str]] = [
    {
        "source_family": "manual_seed",
        "source_role": "internal_seed_family",
        "current_source_status": "active",
        "materialized_cases": "PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001",
        "active_pool_alignment": "performance;longtail;consistency;portability",
        "current_line_interpretation": "internal anchor source family",
        "first_slice_usage": "yes",
        "notes": "not a formal fifth pool",
    },
    {
        "source_family": "TPC-H",
        "source_role": "performance_base",
        "current_source_status": "staged_partial_inspection",
        "materialized_cases": "none",
        "active_pool_alignment": "performance",
        "current_line_interpretation": "target source without realized current case",
        "first_slice_usage": "no",
        "notes": "resource present but not yet materialized into active case line",
    },
    {
        "source_family": "TPC-DS",
        "source_role": "performance_base",
        "current_source_status": "staged_and_inspected",
        "materialized_cases": "PERF_0002",
        "active_pool_alignment": "performance",
        "current_line_interpretation": "strongest current external performance line",
        "first_slice_usage": "yes",
        "notes": "admitted external common-core case exists",
    },
    {
        "source_family": "SQLStorm",
        "source_role": "longtail_base",
        "current_source_status": "staged_and_inspected",
        "materialized_cases": "LONGTAIL_0002",
        "active_pool_alignment": "longtail",
        "current_line_interpretation": "primary longtail source but case line still staged",
        "first_slice_usage": "no",
        "notes": "current first-slice exclusion due to engine closure gap",
    },
    {
        "source_family": "Stack",
        "source_role": "longtail_realism_substrate",
        "current_source_status": "dumps_only_realism_substrate",
        "materialized_cases": "none",
        "active_pool_alignment": "longtail",
        "current_line_interpretation": "realism substrate only",
        "first_slice_usage": "no",
        "notes": "not a direct SQL query corpus in current version",
    },
    {
        "source_family": "Calcite",
        "source_role": "consistency_base",
        "current_source_status": "staged_and_inspected",
        "materialized_cases": "CONS_0002",
        "active_pool_alignment": "consistency",
        "current_line_interpretation": "base consistency seed line",
        "first_slice_usage": "no",
        "notes": "current case still PG-only staged draft",
    },
    {
        "source_family": "VeriEQL",
        "source_role": "consistency_supplement",
        "current_source_status": "accepted_and_materialized",
        "materialized_cases": "CONS_0003;CONS_0004",
        "active_pool_alignment": "consistency",
        "current_line_interpretation": "strongest current consistency supplement line",
        "first_slice_usage": "yes",
        "notes": "both staged drafts now have tri-engine closure",
    },
    {
        "source_family": "PARROT",
        "source_role": "portability_base",
        "current_source_status": "staged_and_inspected",
        "materialized_cases": "PORT_0002",
        "active_pool_alignment": "portability",
        "current_line_interpretation": "strongest current external portability line",
        "first_slice_usage": "yes",
        "notes": "admitted external common-core case exists",
    },
    {
        "source_family": "JOB",
        "source_role": "performance_supplement",
        "current_source_status": "partial_realized_frozen",
        "materialized_cases": "PERF_0003;PERF_0004",
        "active_pool_alignment": "performance",
        "current_line_interpretation": "partial realized supplement only",
        "first_slice_usage": "no",
        "notes": "do not deepen further in current phase",
    },
    {
        "source_family": "DSB",
        "source_role": "performance_realism_candidate",
        "current_source_status": "unresolved_not_started",
        "materialized_cases": "none",
        "active_pool_alignment": "performance",
        "current_line_interpretation": "still unresolved at source-decision layer",
        "first_slice_usage": "no",
        "notes": "no acquisition or inspection started",
    },
    {
        "source_family": "SQLEquiQuest",
        "source_role": "alternative_consistency_candidate",
        "current_source_status": "not_selected",
        "materialized_cases": "none",
        "active_pool_alignment": "consistency",
        "current_line_interpretation": "not active in current branch",
        "first_slice_usage": "no",
        "notes": "VeriEQL is the selected supplement source",
    },
]

SUMMARY_ROWS: List[Dict[str, str]] = [
    {
        "summary_group": "stable_pilot_anchor",
        "count": "4",
        "case_ids": "PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001",
        "include_in_first_slice": "yes",
        "notes": "four stable anchors across all four pools",
    },
    {
        "summary_group": "admitted_external_common_core",
        "count": "2",
        "case_ids": "PERF_0002;PORT_0002",
        "include_in_first_slice": "yes",
        "notes": "current admitted external common-core cases",
    },
    {
        "summary_group": "staged_tri_engine_validated_draft",
        "count": "2",
        "case_ids": "CONS_0003;CONS_0004",
        "include_in_first_slice": "yes",
        "notes": "tri-engine validated but still not_yet_admitted",
    },
    {
        "summary_group": "staged_partial_engine_closure_draft",
        "count": "4",
        "case_ids": "PERF_0003;PERF_0004;LONGTAIL_0002;CONS_0002",
        "include_in_first_slice": "no",
        "notes": "engine closure still incomplete or line intentionally kept partial",
    },
    {
        "summary_group": "total_repository_cases",
        "count": "12",
        "case_ids": "PERF_0001;PERF_0002;PERF_0003;PERF_0004;LONGTAIL_0001;LONGTAIL_0002;CONS_0001;CONS_0002;CONS_0003;CONS_0004;PORT_0001;PORT_0002",
        "include_in_first_slice": "n/a",
        "notes": "current tracked case universe",
    },
    {
        "summary_group": "first_slice_total",
        "count": "8",
        "case_ids": "PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001;PERF_0002;PORT_0002;CONS_0003;CONS_0004",
        "include_in_first_slice": "yes",
        "notes": "current pre-pilot evaluation slice",
    },
]


def load_yaml(rel_path: str) -> Dict[str, Any]:
    path = ROOT / rel_path
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def validated_engines_from_manifest(manifest: Dict[str, Any]) -> str:
    status = manifest.get("status", {})
    engines: List[str] = []
    for engine_name, key in [
        ("postgres", "exec_checked_pg"),
        ("mysql", "exec_checked_mysql"),
        ("spark", "exec_checked_spark"),
    ]:
        if status.get(key) is True:
            engines.append(engine_name)
    return ";".join(engines)


def value_or_fallback(value: str, fallback: str) -> str:
    return value if value else fallback


def result_artifacts_present(manifest: Dict[str, Any], fallback: str) -> str:
    artifacts = manifest.get("artifacts", {})
    result_keys = [k for k in artifacts if k.endswith("_result")]
    if not result_keys:
        return fallback
    ok = all((ROOT / artifacts[k]).exists() for k in result_keys)
    return "yes" if ok else "no"


def plan_artifacts_present(manifest: Dict[str, Any], fallback: str) -> str:
    artifacts = manifest.get("artifacts", {})
    plan_keys = [k for k in artifacts if k.endswith("_plan")]
    if not plan_keys:
        return fallback
    ok = all((ROOT / artifacts[k]).exists() for k in plan_keys)
    return "yes" if ok else "no"


def build_case_maturity_matrix() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for case_id, meta in CASE_REGISTRY.items():
        manifest = load_yaml(meta["manifest"])
        validated = value_or_fallback(
            validated_engines_from_manifest(manifest),
            meta["validated_engines_fallback"],
        )
        rows.append(
            {
                "case_id": case_id,
                "pool": meta["pool"],
                "source_family": meta["source_family"],
                "data_origin": meta["data_origin"],
                "current_maturity": meta["current_maturity"],
                "validated_engines": validated,
                "admitted_or_staged": meta["admitted_or_staged"],
                "include_in_first_slice": meta["include_in_first_slice"],
                "notes": meta["notes"],
            }
        )
    return rows


def build_engine_validation_summary() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for case_id, meta in CASE_REGISTRY.items():
        if meta["include_in_first_slice"] != "yes":
            continue

        manifest = load_yaml(meta["manifest"])
        validated = value_or_fallback(
            validated_engines_from_manifest(manifest),
            meta["validated_engines_fallback"],
        )
        engines = set(validated.split(";")) if validated else set()

        rows.append(
            {
                "case_id": case_id,
                "pool": meta["pool"],
                "current_maturity": meta["current_maturity"],
                "postgres_validated": "yes" if "postgres" in engines else "no",
                "mysql_validated": "yes" if "mysql" in engines else "no",
                "spark_validated": "yes" if "spark" in engines else "no",
                "result_artifacts_present": result_artifacts_present(
                    manifest, meta["result_artifacts_present_fallback"]
                ),
                "plan_artifacts_present": plan_artifacts_present(
                    manifest, meta["plan_artifacts_present_fallback"]
                ),
                "current_status": meta["admitted_or_staged"],
                "notes": meta["notes"],
            }
        )
    return rows


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    case_rows = build_case_maturity_matrix()
    engine_rows = build_engine_validation_summary()

    write_csv(
        REPORT_DIR / "case_maturity_matrix_v0.csv",
        case_rows,
        [
            "case_id",
            "pool",
            "source_family",
            "data_origin",
            "current_maturity",
            "validated_engines",
            "admitted_or_staged",
            "include_in_first_slice",
            "notes",
        ],
    )

    write_csv(
        REPORT_DIR / "source_to_case_mapping_v0.csv",
        SOURCE_ROWS,
        [
            "source_family",
            "source_role",
            "current_source_status",
            "materialized_cases",
            "active_pool_alignment",
            "current_line_interpretation",
            "first_slice_usage",
            "notes",
        ],
    )

    write_csv(
        REPORT_DIR / "admitted_vs_staged_summary_v0.csv",
        SUMMARY_ROWS,
        [
            "summary_group",
            "count",
            "case_ids",
            "include_in_first_slice",
            "notes",
        ],
    )

    write_csv(
        REPORT_DIR / "engine_validation_summary_v0.csv",
        engine_rows,
        [
            "case_id",
            "pool",
            "current_maturity",
            "postgres_validated",
            "mysql_validated",
            "spark_validated",
            "result_artifacts_present",
            "plan_artifacts_present",
            "current_status",
            "notes",
        ],
    )

    print("wrote reports/pilot/case_maturity_matrix_v0.csv")
    print("wrote reports/pilot/source_to_case_mapping_v0.csv")
    print("wrote reports/pilot/admitted_vs_staged_summary_v0.csv")
    print("wrote reports/pilot/engine_validation_summary_v0.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())