#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
RUN_DIR = Path(__file__).resolve().parent
FREEZE_DIR = REPO_ROOT / "reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1"
WORKSPACES_DIR = RUN_DIR / "workspaces"

DENOMINATOR_ID = "common_core_v0_40_same_engine_120"
TIE_EPSILON = 0.001


@dataclass
class SelectedCase:
    selected_id: str
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    outcome_type: str
    speedup_ratio: str
    selection_reason: str
    source_sql_artifact: str
    rewrite_sql_artifact: str
    schema_artifact: str
    timing_or_failure_artifact: str
    selected_status: str
    notes: str


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def render_markdown_table(rows: list[dict[str, Any]], fieldnames: list[str]) -> str:
    header = "| " + " | ".join(fieldnames) + " |"
    sep = "| " + " | ".join(["---"] * len(fieldnames)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(k, "")).replace("\n", " ") for k in fieldnames) + " |")
    return "\n".join([header, sep] + body)


def write_md(path: Path, title: str, intro_lines: list[str], rows: list[dict[str, Any]] | None = None, fieldnames: list[str] | None = None, extra_lines: list[str] | None = None) -> None:
    parts = [f"# {title}", ""]
    parts.extend(intro_lines)
    parts.append("")
    if rows is not None and fieldnames is not None:
        parts.append(render_markdown_table(rows, fieldnames))
        parts.append("")
    if extra_lines:
        parts.extend(extra_lines)
        parts.append("")
    path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def strip_sql_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    lines = []
    for line in text.splitlines():
        if re.match(r"^\s*--", line):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def case_dir_for(case_id: str) -> Path:
    prefix = case_id.split("_")[0]
    return REPO_ROOT / "cases" / prefix / case_id


def sql_text(path: Path) -> str:
    return strip_sql_comments(path.read_text(encoding="utf-8")).rstrip("; \n\t")


def load_timing_rows() -> list[dict[str, Any]]:
    files = [
        REPO_ROOT / "reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_timing_event_long.csv",
        REPO_ROOT / "reports/evaluation/common_core_v0/runs/sqlglot_full_per_case_timing_01/timing_event_long.csv",
        REPO_ROOT / "reports/evaluation/common_core_v0/runs/calcite_hep_93_exact_timing_01/timing_event_long.csv",
    ]
    rows: list[dict[str, Any]] = []
    for path in files:
        for row in read_csv(path):
            if row.get("timing_success", "").lower() not in {"true", "1", "yes"}:
                continue
            row = dict(row)
            row["_path"] = str(path)
            row["_speedup"] = float(row["speedup_ratio"])
            row["_abs_from_one"] = abs(row["_speedup"] - 1.0)
            rows.append(row)
    return rows


def select_cases() -> list[SelectedCase]:
    timing_rows = load_timing_rows()
    min_abs = min(row["_abs_from_one"] for row in timing_rows)

    speedup_row = max(
        timing_rows,
        key=lambda r: (r["_speedup"], 1 if r["engine"] == "pg" else 0, r["case_id"], r["route_id"]),
    )
    regression_row = min(
        timing_rows,
        key=lambda r: (r["_speedup"], 0 if r["engine"] == "pg" else 1, r["case_id"], r["route_id"]),
    )
    tie_candidates = [
        row for row in timing_rows if row["_abs_from_one"] <= min_abs + TIE_EPSILON
    ]
    tie_row = sorted(
        tie_candidates,
        key=lambda r: (0 if r["engine"] == "pg" else 1, r["_abs_from_one"], r["case_id"], r["route_id"]),
    )[0]

    sqlglot_rows = [row for row in timing_rows if row["method_id"] == "sqlglot"]
    sqlglot_extra = max(
        sqlglot_rows,
        key=lambda r: (r["_speedup"], 1 if r["engine"] == "pg" else 0, r["case_id"], r["route_id"]),
    )

    failure_row = None
    for row in read_csv(FREEZE_DIR / "table10_failure_exemplar_selection_v1.csv"):
        if row["selected"].lower() in {"true", "1", "yes"}:
            failure_row = row
            break
    if failure_row is None:
        raise RuntimeError("No selected failure exemplar found")

    selected: list[SelectedCase] = []

    def build_exact_selected(selected_id: str, row: dict[str, Any], outcome_type: str, reason: str) -> SelectedCase:
        case_dir = case_dir_for(row["case_id"])
        schema_suffix = "ddl_pg.sql" if row["engine"] == "pg" else "ddl_spark.sql"
        schema_artifact = row.get("schema_artifact") or str(case_dir / "schema" / schema_suffix)
        rewrite_path = row.get("final_candidate_sql_artifact") or row.get("candidate_sql_artifact") or row.get("rewrite_sql_artifact")
        return SelectedCase(
            selected_id=selected_id,
            case_id=row["case_id"],
            pool=row["pool"],
            engine=row["engine"],
            method_id=row["method_id"],
            route_id=row["route_id"],
            outcome_type=outcome_type,
            speedup_ratio=f"{row['_speedup']:.15f}".rstrip("0").rstrip("."),
            selection_reason=reason,
            source_sql_artifact=row["source_sql_artifact"],
            rewrite_sql_artifact=rewrite_path,
            schema_artifact=schema_artifact,
            timing_or_failure_artifact=row["_path"],
            selected_status="selected_for_plan_observability",
            notes="mechanical_selection_from_retained_timing_event",
        )

    selected.append(
        build_exact_selected(
            "sel_speedup_01",
            speedup_row,
            "speedup",
            "highest_retained_speedup_across_selected_exact_timed_rows_from_retained_event_packets",
        )
    )
    selected.append(
        build_exact_selected(
            "sel_regression_01",
            regression_row,
            "regression",
            "lowest_retained_speedup_across_selected_exact_timed_rows_from_retained_event_packets",
        )
    )
    selected.append(
        build_exact_selected(
            "sel_tie_01",
            tie_row,
            "tie",
            f"speedup_closest_to_1.0_with_pg_preference_among_rows_within_{TIE_EPSILON}_of_best_closeness",
        )
    )

    selected.append(
        SelectedCase(
            selected_id="sel_failure_01",
            case_id=failure_row["case_id"],
            pool=failure_row["pool"],
            engine=failure_row["engine"],
            method_id=failure_row["method_id"],
            route_id=failure_row["route_id"],
            outcome_type="failure",
            speedup_ratio="NA_not_applicable",
            selection_reason="existing_table10_failure_exemplar_selected_from_case_level_failure_export",
            source_sql_artifact=failure_row["source_artifacts"].split("|")[0].replace(
                "reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/workspaces/CONS_0024/pg/direct_llm_same_engine_rewrite/result_check.json",
                "cases/CONS/CONS_0024/source.sql",
            ) if False else str(REPO_ROOT / "cases/CONS/CONS_0024/source.sql"),
            rewrite_sql_artifact=str(REPO_ROOT / "reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/generated/CONS_0024/pg/direct_llm_same_engine_rewrite.sql"),
            schema_artifact=str(REPO_ROOT / "cases/CONS/CONS_0024/schema/ddl_pg.sql"),
            timing_or_failure_artifact=failure_row["source_artifacts"],
            selected_status="selected_for_plan_observability",
            notes="mechanical_failure_selection_from_table10_failure_exemplar_selection_v1",
        )
    )

    if not any(item.method_id == "sqlglot" for item in selected):
        selected.append(
            build_exact_selected(
                "sel_sqlglot_extra_01",
                sqlglot_extra,
                "speedup",
                "best_retained_sqlglot_speedup_row_added_because_sqlglot_was_not_covered_by_base_four_selection",
            )
        )

    if not any(item.method_id == "calcite_hep" for item in selected):
        calcite_rows = [row for row in timing_rows if row["method_id"] == "calcite_hep"]
        calcite_extra = max(
            calcite_rows,
            key=lambda r: (r["_speedup"], 1 if r["engine"] == "pg" else 0, r["case_id"], r["route_id"]),
        )
        selected.append(
            build_exact_selected(
                "sel_calcite_extra_01",
                calcite_extra,
                "speedup",
                "best_retained_calcite_speedup_row_added_because_calcite_was_not_covered_by_base_four_selection",
            )
        )

    return selected[:6]


def pg_schema_name(selected_id: str) -> str:
    cleaned = re.sub(r"[^a-z0-9_]", "_", selected_id.lower())
    return f"selplan_{cleaned}"[:55]


def run_subprocess(cmd: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
        cwd=REPO_ROOT,
    )


def extract_pg_plan(selected: SelectedCase, workspace: Path, plan_side: str, query_path: Path, schema_path: Path, witness_path: Path) -> tuple[bool, Path, Path, str]:
    schema_name = pg_schema_name(selected.selected_id)
    setup_sql = (
        f"drop schema if exists {schema_name} cascade;\n"
        f"create schema {schema_name};\n"
        f"set search_path to {schema_name};\n"
        f"\\i {schema_path}\n"
        f"\\i {witness_path}\n"
    )
    setup = run_subprocess(["psql", "-X", "-v", "ON_ERROR_STOP=1"], input_text=setup_sql)
    (workspace / f"{plan_side}.setup.stdout.log").write_text(setup.stdout, encoding="utf-8")
    (workspace / f"{plan_side}.setup.stderr.log").write_text(setup.stderr, encoding="utf-8")
    if setup.returncode != 0:
        return False, workspace / f"{plan_side}_plan.json", workspace / f"{plan_side}.stderr.log", f"pg_setup_failed: {setup.stderr.strip()}"

    explain_sql = (
        f"set search_path to {schema_name};\n"
        "explain (format json)\n"
        f"{sql_text(query_path)}\n"
    )
    result = run_subprocess(["psql", "-X", "-q", "-v", "ON_ERROR_STOP=1", "-A", "-t"], input_text=explain_sql)
    stdout_log = workspace / f"{plan_side}.stdout.log"
    stderr_log = workspace / f"{plan_side}.stderr.log"
    stdout_log.write_text(result.stdout, encoding="utf-8")
    stderr_log.write_text(result.stderr, encoding="utf-8")
    plan_path = workspace / f"{plan_side}_plan.json"
    if result.returncode == 0:
        plan_path.write_text(result.stdout.strip() + "\n", encoding="utf-8")
        return True, plan_path, stderr_log, ""
    return False, plan_path, stderr_log, result.stderr.strip() or "pg_explain_failed"


def read_spark_statements(path: Path) -> list[str]:
    text = strip_sql_comments(path.read_text(encoding="utf-8"))
    return [stmt.strip() for stmt in text.split(";") if stmt.strip()]


def extract_spark_plans(selected: SelectedCase, workspace: Path, source_sql: Path, rewrite_sql: Path, schema_path: Path, witness_path: Path) -> tuple[dict[str, Any], list[dict[str, str]]]:
    from pyspark.sql import SparkSession

    failures: list[dict[str, str]] = []
    warehouse_dir = Path(tempfile.mkdtemp(prefix=f"{selected.case_id.lower()}_plan_obs_"))
    spark_local_ip = os.environ.get("SPARK_LOCAL_IP")
    if not spark_local_ip:
        try:
            spark_local_ip = subprocess.check_output(["bash", "-lc", "hostname -I | awk '{print $1}'"], text=True, cwd=REPO_ROOT).strip()
        except Exception:  # noqa: BLE001
            spark_local_ip = "127.0.0.1"
    spark = (
        SparkSession.builder.master("local[*]")
        .appName(f"{selected.selected_id}_plan_observability")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.sql.warehouse.dir", str(warehouse_dir))
        .config("spark.driver.host", spark_local_ip)
        .config("spark.driver.bindAddress", spark_local_ip)
        .config("spark.driver.memory", os.environ.get("SPARK_DRIVER_MEMORY", "8g"))
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    out: dict[str, Any] = {}
    try:
        for statement in read_spark_statements(schema_path):
            spark.sql(statement)
        for statement in read_spark_statements(witness_path):
            spark.sql(statement)
        for side, path in [("source", source_sql), ("rewrite", rewrite_sql)]:
            try:
                query = sql_text(path)
                rows = spark.sql(f"EXPLAIN FORMATTED {query}").collect()
                text = "\n".join(str(row[0]) for row in rows)
                plan_path = workspace / f"{side}_plan.txt"
                plan_path.write_text(text + "\n", encoding="utf-8")
                (workspace / f"{side}.stdout.log").write_text(text + "\n", encoding="utf-8")
                (workspace / f"{side}.stderr.log").write_text("", encoding="utf-8")
                out[side] = {
                    "success": True,
                    "plan_path": plan_path,
                    "failure": "",
                }
            except Exception as exc:  # noqa: BLE001
                msg = f"spark_explain_failed: {exc}"
                (workspace / f"{side}.stderr.log").write_text(msg + "\n", encoding="utf-8")
                out[side] = {
                    "success": False,
                    "plan_path": workspace / f"{side}_plan.txt",
                    "failure": msg,
                }
                failures.append(
                    {
                        "selected_id": selected.selected_id,
                        "plan_side": side,
                        "failure_category": "planning_failure",
                        "failure_detail": msg,
                        "log_artifact": str(workspace / f"{side}.stderr.log"),
                        "notes": "spark_plan_extraction",
                    }
                )
    finally:
        spark.stop()
        shutil.rmtree(warehouse_dir, ignore_errors=True)
    return out, failures


def parse_pg_plan(plan_path: Path) -> dict[str, Any]:
    raw = plan_path.read_text(encoding="utf-8").strip()
    data = json.loads(raw)
    if isinstance(data, list):
        plan_root = data[0]["Plan"]
    else:
        plan_root = data["Plan"]

    node_types: list[str] = []
    filters: list[str] = []

    def walk(node: dict[str, Any]) -> None:
        node_type = node.get("Node Type", "unknown")
        node_types.append(node_type)
        for key in ["Filter", "Join Filter", "Index Cond", "Hash Cond", "Merge Cond", "Recheck Cond"]:
            if key in node:
                filters.append(key)
        for child in node.get("Plans", []):
            walk(child)

    walk(plan_root)
    scans = sorted({nt for nt in node_types if "Scan" in nt})
    joins = sorted({nt for nt in node_types if "Join" in nt or nt == "Nested Loop"})
    aggs = sorted({nt for nt in node_types if "Aggregate" in nt or nt in {"Group", "GroupAggregate", "HashAggregate"}})
    sorts = sorted({nt for nt in node_types if nt in {"Sort", "Limit"} or "Limit" in nt})
    feature = {
        "plan_format": "pg_json",
        "top_operator": plan_root.get("Node Type", "unknown"),
        "scan_summary": ", ".join(scans) if scans else "none",
        "join_summary": ", ".join(joins) if joins else "none",
        "aggregate_summary": ", ".join(aggs) if aggs else "none",
        "sort_limit_summary": ", ".join(sorts) if sorts else "none",
        "filter_summary": ", ".join(sorted(set(filters))) if filters else "none_visible",
        "node_count": str(len(node_types)),
        "parse_confidence": "medium",
        "notes": "parsed_from_pg_json",
    }
    feature["_raw_node_types"] = node_types
    return feature


SPARK_SCAN_KEYWORDS = ["Scan", "FileScan", "BatchScan", "TableScan"]
SPARK_JOIN_KEYWORDS = ["Join", "BroadcastHashJoin", "SortMergeJoin", "BroadcastNestedLoopJoin", "CartesianProduct", "NestedLoopJoin"]
SPARK_AGG_KEYWORDS = ["Aggregate", "HashAggregate", "SortAggregate", "ObjectHashAggregate"]
SPARK_SORT_KEYWORDS = ["Sort", "Limit", "TakeOrderedAndProject", "GlobalLimit", "LocalLimit"]
SPARK_FILTER_KEYWORDS = ["Filter", "Condition"]


def parse_spark_plan(plan_path: Path) -> dict[str, Any]:
    text = plan_path.read_text(encoding="utf-8")
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    op_lines = [line for line in lines if any(keyword in line for keyword in SPARK_SCAN_KEYWORDS + SPARK_JOIN_KEYWORDS + SPARK_AGG_KEYWORDS + SPARK_SORT_KEYWORDS + SPARK_FILTER_KEYWORDS)]
    top_operator = "unavailable"
    for line in op_lines:
        cleaned = re.sub(r"^[\s\|\+\-:()*]+", "", line)
        m = re.match(r"([A-Za-z][A-Za-z0-9]+(?:\s+[A-Za-z][A-Za-z0-9]+)*)", cleaned)
        if m:
            top_operator = m.group(1)
            break
    def collect_keywords(keywords: list[str]) -> list[str]:
        found = []
        for keyword in keywords:
            if keyword in text:
                found.append(keyword)
        return found

    feature = {
        "plan_format": "spark_text",
        "top_operator": top_operator,
        "scan_summary": ", ".join(collect_keywords(SPARK_SCAN_KEYWORDS)) or "none_visible",
        "join_summary": ", ".join(collect_keywords(SPARK_JOIN_KEYWORDS)) or "none_visible",
        "aggregate_summary": ", ".join(collect_keywords(SPARK_AGG_KEYWORDS)) or "none_visible",
        "sort_limit_summary": ", ".join(collect_keywords(SPARK_SORT_KEYWORDS)) or "none_visible",
        "filter_summary": ", ".join(collect_keywords(SPARK_FILTER_KEYWORDS)) or "none_visible",
        "node_count": str(len(op_lines)) if op_lines else "NA_not_derivable",
        "parse_confidence": "low",
        "notes": "parsed_from_spark_formatted_text",
    }
    return feature


def summarize_plan_pattern(feature: dict[str, Any]) -> str:
    return (
        f"top={feature['top_operator']}; "
        f"scan={feature['scan_summary']}; "
        f"join={feature['join_summary']}; "
        f"agg={feature['aggregate_summary']}; "
        f"sort_limit={feature['sort_limit_summary']}"
    )


def classify_delta(selected: SelectedCase, source_feature: dict[str, Any] | None, rewrite_feature: dict[str, Any] | None, source_success: bool, rewrite_success: bool) -> tuple[str, str, str, str]:
    if selected.outcome_type == "failure" and not rewrite_success:
        return (
            "execution_or_planning_failure",
            "not_applicable",
            "failure row has no usable rewrite plan; retain mismatch artifact but do not fabricate a causal plan delta",
            "Do not claim operator-level attribution or node alignment.",
        )
    if not source_success or not rewrite_success or source_feature is None or rewrite_feature is None:
        return (
            "unsupported_plan_format",
            "low",
            "selected-case plan extraction is incomplete, so only bounded observability is supported",
            "Do not claim full-denominator observability or causal attribution.",
        )

    if selected.outcome_type == "failure":
        if source_feature is None or rewrite_feature is None:
            return (
                "execution_or_planning_failure",
                "not_applicable",
                "failure row retains the mismatch artifact but does not retain a complete source/rewrite plan pair",
                "Do not fabricate a plan delta or attribution story for this failure row.",
            )
        return (
            "no_major_plan_delta",
            "low",
            "the selected failure row retains both plans, but this lightweight feature summary does not by itself explain the semantic mismatch outcome",
            "Do not claim the mismatch is causally explained by this bounded plan snapshot.",
        )

    if source_feature["join_summary"] != rewrite_feature["join_summary"]:
        return (
            "join_change",
            "low",
            "source and rewrite plans expose different join structures in the retained selected-case pair",
            "Do not claim global causal attribution or node-level alignment from this selected pair alone.",
        )
    if source_feature["aggregate_summary"] != rewrite_feature["aggregate_summary"]:
        return (
            "aggregate_change",
            "medium" if selected.engine == "pg" else "low",
            "the selected source/rewrite pair changes visible aggregate structure",
            "Do not generalize this aggregate delta beyond the selected case.",
        )
    if source_feature["sort_limit_summary"] != rewrite_feature["sort_limit_summary"]:
        return (
            "sort_limit_change",
            "low",
            "the retained selected pair changes visible sort/limit structure",
            "Do not turn this selected-case delta into full-denominator attribution.",
        )
    if source_feature["filter_summary"] != rewrite_feature["filter_summary"]:
        return (
            "filter_pushdown_change",
            "low",
            "predicate visibility differs between source and rewrite plans in the selected pair",
            "Do not overclaim exact pushdown semantics without node alignment.",
        )
    if source_feature["scan_summary"] != rewrite_feature["scan_summary"]:
        return (
            "scan_change",
            "low",
            "scan operators differ across the selected source/rewrite plan pair",
            "Do not claim a global scan-level causal model.",
        )
    if source_feature["node_count"] != rewrite_feature["node_count"]:
        return (
            "node_count_change",
            "low",
            "major operator families are similar but visible node count differs",
            "Do not equate node-count change with full causal attribution.",
        )
    return (
        "no_major_plan_delta",
        "low",
        "the selected source/rewrite plans look broadly similar at this lightweight feature level",
        "Do not overread lightweight similarity as proof of no physical-plan difference.",
    )


def runtime_effect(selected: SelectedCase) -> str:
    if selected.outcome_type == "failure":
        return "mismatch; exact_match=false; sorted_match=false"
    if selected.outcome_type == "speedup":
        return f"speedup_{selected.speedup_ratio}x"
    if selected.outcome_type == "regression":
        return f"slowdown_to_{selected.speedup_ratio}x"
    return f"near_neutral_{selected.speedup_ratio}x"


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)

    selected = select_cases()
    selected_rows = [item.__dict__ for item in selected]

    extraction_events: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    delta_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    command_rows: list[dict[str, Any]] = []

    manifest_fields = [
        "selected_id",
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "outcome_type",
        "speedup_ratio",
        "selection_reason",
        "source_sql_artifact",
        "rewrite_sql_artifact",
        "schema_artifact",
        "timing_or_failure_artifact",
        "selected_status",
        "notes",
    ]
    write_csv(RUN_DIR / "selected_case_manifest.csv", selected_rows, manifest_fields)

    for item in selected:
        workspace = WORKSPACES_DIR / item.selected_id
        workspace.mkdir(parents=True, exist_ok=True)

        source_sql_path = REPO_ROOT / item.source_sql_artifact
        rewrite_sql_path = REPO_ROOT / item.rewrite_sql_artifact
        schema_path = REPO_ROOT / item.schema_artifact
        case_dir = case_dir_for(item.case_id)
        witness_path = case_dir / "validation" / ("pg_witness_data.sql" if item.engine == "pg" else "spark_witness_data.sql")

        shutil.copyfile(source_sql_path, workspace / "source.sql")
        shutil.copyfile(rewrite_sql_path, workspace / "rewrite.sql")
        shutil.copyfile(schema_path, workspace / schema_path.name)
        if witness_path.exists():
            shutil.copyfile(witness_path, workspace / witness_path.name)

        command_rows.append(
            {
                "selected_id": item.selected_id,
                "engine": item.engine,
                "command_role": "source_and_rewrite_plan_extraction",
                "command_preview": "psql EXPLAIN (FORMAT JSON)" if item.engine == "pg" else "spark EXPLAIN FORMATTED",
                "workspace": str(workspace),
                "notes": item.selection_reason,
            }
        )

        source_success = False
        rewrite_success = False
        source_plan_path = workspace / "source_plan.unavailable"
        rewrite_plan_path = workspace / "rewrite_plan.unavailable"
        plan_format = "unavailable"
        source_feature = None
        rewrite_feature = None
        plan_parse_status = "not_attempted"
        failure_category = ""

        if item.engine == "pg":
            source_success, source_plan_path, source_log_path, source_failure = extract_pg_plan(
                item, workspace, "source", source_sql_path, schema_path, witness_path
            )
            rewrite_success, rewrite_plan_path, rewrite_log_path, rewrite_failure = extract_pg_plan(
                item, workspace, "rewrite", rewrite_sql_path, schema_path, witness_path
            )
            if source_failure:
                failure_rows.append(
                    {
                        "selected_id": item.selected_id,
                        "plan_side": "source",
                        "failure_category": "planning_failure",
                        "failure_detail": source_failure,
                        "log_artifact": str(source_log_path),
                        "notes": item.case_id,
                    }
                )
            if rewrite_failure:
                failure_rows.append(
                    {
                        "selected_id": item.selected_id,
                        "plan_side": "rewrite",
                        "failure_category": "planning_failure",
                        "failure_detail": rewrite_failure,
                        "log_artifact": str(rewrite_log_path),
                        "notes": item.case_id,
                    }
                )
            plan_format = "pg_json"
        elif item.engine == "spark":
            spark_out, spark_failures = extract_spark_plans(item, workspace, source_sql_path, rewrite_sql_path, schema_path, witness_path)
            source_success = spark_out["source"]["success"]
            rewrite_success = spark_out["rewrite"]["success"]
            source_plan_path = spark_out["source"]["plan_path"]
            rewrite_plan_path = spark_out["rewrite"]["plan_path"]
            failure_rows.extend(spark_failures)
            plan_format = "spark_text"

        if source_success:
            source_feature = parse_pg_plan(source_plan_path) if plan_format == "pg_json" else parse_spark_plan(source_plan_path)
            source_feature_json = dict(source_feature)
            source_feature_json.pop("_raw_node_types", None)
            (workspace / "source_plan_feature_summary.json").write_text(json.dumps(source_feature_json, indent=2) + "\n", encoding="utf-8")
            feature_rows.append(
                {
                    "selected_id": item.selected_id,
                    "plan_side": "source",
                    **{k: v for k, v in source_feature.items() if not k.startswith("_")},
                }
            )
        if rewrite_success:
            rewrite_feature = parse_pg_plan(rewrite_plan_path) if plan_format == "pg_json" else parse_spark_plan(rewrite_plan_path)
            rewrite_feature_json = dict(rewrite_feature)
            rewrite_feature_json.pop("_raw_node_types", None)
            (workspace / "rewrite_plan_feature_summary.json").write_text(json.dumps(rewrite_feature_json, indent=2) + "\n", encoding="utf-8")
            feature_rows.append(
                {
                    "selected_id": item.selected_id,
                    "plan_side": "rewrite",
                    **{k: v for k, v in rewrite_feature.items() if not k.startswith("_")},
                }
            )

        if source_success and rewrite_success:
            plan_parse_status = "parsed"
        elif source_success or rewrite_success:
            plan_parse_status = "partial"
        else:
            plan_parse_status = "failed"
            failure_category = "execution_or_planning_failure"

        delta_class, attr_conf, interpretation, forbidden = classify_delta(
            item, source_feature, rewrite_feature, source_success, rewrite_success
        )
        if not failure_category and delta_class == "execution_or_planning_failure":
            failure_category = "execution_or_planning_failure"

        delta_payload = {
            "selected_id": item.selected_id,
            "case_id": item.case_id,
            "engine": item.engine,
            "method_id": item.method_id,
            "route_id": item.route_id,
            "outcome_type": item.outcome_type,
            "runtime_effect": runtime_effect(item),
            "source_plan_pattern": summarize_plan_pattern(source_feature) if source_feature else "unavailable",
            "rewrite_plan_pattern": summarize_plan_pattern(rewrite_feature) if rewrite_feature else "unavailable",
            "main_plan_delta": delta_class,
            "attribution_confidence": attr_conf,
            "evidence_artifacts": "|".join(
                [
                    item.timing_or_failure_artifact,
                    str(source_plan_path) if source_success else "",
                    str(rewrite_plan_path) if rewrite_success else "",
                ]
            ).strip("|"),
            "paper_safe_interpretation": interpretation,
            "forbidden_overclaim": forbidden,
            "notes": item.selection_reason,
        }
        (workspace / "plan_delta.json").write_text(json.dumps(delta_payload, indent=2) + "\n", encoding="utf-8")
        delta_rows.append(delta_payload)

        extraction_events.append(
            {
                "selected_id": item.selected_id,
                "case_id": item.case_id,
                "engine": item.engine,
                "method_id": item.method_id,
                "route_id": item.route_id,
                "outcome_type": item.outcome_type,
                "source_plan_attempted": "true",
                "source_plan_success": str(source_success).lower(),
                "rewrite_plan_attempted": "true",
                "rewrite_plan_success": str(rewrite_success).lower(),
                "source_plan_artifact": str(source_plan_path) if source_success else "NA_not_collected",
                "rewrite_plan_artifact": str(rewrite_plan_path) if rewrite_success else "NA_not_collected",
                "plan_format": plan_format if (source_success or rewrite_success) else "unavailable",
                "plan_parse_status": plan_parse_status,
                "failure_category": failure_category if failure_category else "NA_not_applicable",
                "notes": item.selection_reason,
            }
        )

    feature_fields = [
        "selected_id",
        "plan_side",
        "plan_format",
        "top_operator",
        "scan_summary",
        "join_summary",
        "aggregate_summary",
        "sort_limit_summary",
        "filter_summary",
        "node_count",
        "parse_confidence",
        "notes",
    ]
    event_fields = [
        "selected_id",
        "case_id",
        "engine",
        "method_id",
        "route_id",
        "outcome_type",
        "source_plan_attempted",
        "source_plan_success",
        "rewrite_plan_attempted",
        "rewrite_plan_success",
        "source_plan_artifact",
        "rewrite_plan_artifact",
        "plan_format",
        "plan_parse_status",
        "failure_category",
        "notes",
    ]
    delta_fields = [
        "selected_id",
        "case_id",
        "engine",
        "method_id",
        "route_id",
        "outcome_type",
        "runtime_effect",
        "source_plan_pattern",
        "rewrite_plan_pattern",
        "main_plan_delta",
        "attribution_confidence",
        "evidence_artifacts",
        "paper_safe_interpretation",
        "forbidden_overclaim",
        "notes",
    ]
    failure_fields = ["selected_id", "plan_side", "failure_category", "failure_detail", "log_artifact", "notes"]
    command_fields = ["selected_id", "engine", "command_role", "command_preview", "workspace", "notes"]

    write_csv(RUN_DIR / "plan_extraction_command_matrix.csv", command_rows, command_fields)
    write_csv(RUN_DIR / "plan_extraction_event_long.csv", extraction_events, event_fields)
    write_csv(RUN_DIR / "plan_feature_summary.csv", feature_rows, feature_fields)
    write_csv(RUN_DIR / "plan_delta_classification.csv", delta_rows, delta_fields)
    write_csv(RUN_DIR / "plan_extraction_failures.csv", failure_rows or [{
        "selected_id": "NA_no_failures",
        "plan_side": "NA_not_applicable",
        "failure_category": "NA_not_applicable",
        "failure_detail": "no_plan_extraction_failures",
        "log_artifact": "NA_not_applicable",
        "notes": "all_selected_cases_planned_successfully",
    }], failure_fields)

    # Freeze copies.
    write_csv(FREEZE_DIR / "selected_plan_observability_manifest_v1.csv", selected_rows, manifest_fields)
    write_csv(FREEZE_DIR / "selected_plan_observability_event_long_v1.csv", extraction_events, event_fields)
    write_csv(FREEZE_DIR / "selected_plan_feature_summary_v1.csv", feature_rows, feature_fields)
    write_csv(FREEZE_DIR / "selected_plan_delta_classification_v1.csv", delta_rows, delta_fields)

    # Table 5 summary by route.
    by_route: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    event_by_selected = {row["selected_id"]: row for row in extraction_events}
    delta_by_selected = {row["selected_id"]: row for row in delta_rows}
    for item in selected:
        by_route[(item.method_id, item.route_id)].append(item.__dict__)

    table5_rows: list[dict[str, Any]] = []
    for (method_id, route_id), items in by_route.items():
        ids = [item["selected_id"] for item in items]
        source_ok = sum(event_by_selected[idx]["source_plan_success"] == "true" for idx in ids)
        rewrite_ok = sum(event_by_selected[idx]["rewrite_plan_success"] == "true" for idx in ids)
        parsed = sum(event_by_selected[idx]["plan_parse_status"] == "parsed" for idx in ids)
        classified = sum(delta_by_selected[idx]["main_plan_delta"] != "unsupported_plan_format" for idx in ids)
        attr = sum(delta_by_selected[idx]["attribution_confidence"] in {"low", "medium"} for idx in ids)
        table5_rows.append(
            {
                "method_or_route": f"{method_id} / {route_id}",
                "selected_cases": len(ids),
                "source_plan_extracted": source_ok,
                "rewrite_plan_extracted": rewrite_ok,
                "plan_parse_success": parsed,
                "delta_classified": classified,
                "attribution_cases": attr,
                "attribution_confidence_scope": "selected_case_only_low_to_medium",
                "observability_notes": "selected-case plan packet only; no denominator-wide node alignment or causal coverage",
                "source_artifacts": "|".join(sorted({delta_by_selected[idx]["evidence_artifacts"] for idx in ids})),
            }
        )

    table5_fields = [
        "method_or_route",
        "selected_cases",
        "source_plan_extracted",
        "rewrite_plan_extracted",
        "plan_parse_success",
        "delta_classified",
        "attribution_cases",
        "attribution_confidence_scope",
        "observability_notes",
        "source_artifacts",
    ]
    write_csv(FREEZE_DIR / "table5_observability_plan_artifact_v2.csv", table5_rows, table5_fields)

    # Table 10 v3 uses selected delta rows.
    table10_rows = []
    for row in delta_rows:
        table10_rows.append(
            {
                "case_id": row["case_id"],
                "method_or_route": f"{row['method_id']} / {row['route_id']}",
                "engine": row["engine"],
                "outcome_type": row["outcome_type"],
                "runtime_effect": row["runtime_effect"],
                "source_plan_pattern": row["source_plan_pattern"],
                "rewrite_plan_pattern": row["rewrite_plan_pattern"],
                "main_plan_delta": row["main_plan_delta"],
                "attribution_confidence": row["attribution_confidence"],
                "evidence_artifacts": row["evidence_artifacts"],
                "paper_safe_interpretation": row["paper_safe_interpretation"],
            }
        )
    table10_fields = [
        "case_id",
        "method_or_route",
        "engine",
        "outcome_type",
        "runtime_effect",
        "source_plan_pattern",
        "rewrite_plan_pattern",
        "main_plan_delta",
        "attribution_confidence",
        "evidence_artifacts",
        "paper_safe_interpretation",
    ]
    write_csv(FREEZE_DIR / "table10_plan_observability_case_study_v3.csv", table10_rows, table10_fields)

    gap_rows = [
        {
            "gap_id": "obs_gap_01",
            "affected_table": "Table 5",
            "current_status": "selected_case_observability_packet_retained",
            "gap_description": "selected representative source/rewrite plan pairs are now retained",
            "resolved_by_this_packet": "yes",
            "remaining_gap": "not full denominator plan extraction",
            "requires_new_execution": "yes",
            "priority": "medium",
            "notes": "This packet improves observability evidence but does not create denominator-wide coverage metrics.",
        },
        {
            "gap_id": "obs_gap_02",
            "affected_table": "Table 10",
            "current_status": "selected_case_plan_fields_backfilled",
            "gap_description": "speedup/regression/tie/failure rows now have retained plan artifacts and bounded delta classes",
            "resolved_by_this_packet": "yes",
            "remaining_gap": "no full node alignment",
            "requires_new_execution": "yes",
            "priority": "high",
            "notes": "Failure exemplar identity was already resolved; this packet resolves the missing selected-case plan pair layer.",
        },
        {
            "gap_id": "obs_gap_03",
            "affected_table": "Table 10",
            "current_status": "selected_case_only",
            "gap_description": "operator-level attribution remains bounded and low/medium confidence only",
            "resolved_by_this_packet": "partial",
            "remaining_gap": "causal attribution not denominator-wide and not node-aligned",
            "requires_new_execution": "yes",
            "priority": "high",
            "notes": "Do not turn lightweight plan-feature deltas into global causal claims.",
        },
        {
            "gap_id": "obs_gap_04",
            "affected_table": "RQ2_overall",
            "current_status": "selected_case_support_available",
            "gap_description": "selected-case observability is now stronger than raw latency labels alone",
            "resolved_by_this_packet": "partial",
            "remaining_gap": "no full PlanParseRate or NodeAlignmentCoverage metric",
            "requires_new_execution": "yes",
            "priority": "medium",
            "notes": "This packet supports qualitative observability evidence only.",
        },
    ]
    gap_fields = [
        "gap_id",
        "affected_table",
        "current_status",
        "gap_description",
        "resolved_by_this_packet",
        "remaining_gap",
        "requires_new_execution",
        "priority",
        "notes",
    ]
    write_csv(FREEZE_DIR / "plan_observability_case_study_gap_matrix_v3.csv", gap_rows, gap_fields)

    # Remaining experiment gaps v6.
    prior_gaps = read_csv(FREEZE_DIR / "paper_remaining_experiment_gaps_v5.csv")
    updated_gaps = []
    for row in prior_gaps:
        row = dict(row)
        if row["gap_id"] == "gap_10":
            row["current_status"] = "selected_case_plan_observability_packet_retained"
            row["required_next_artifact_or_experiment"] = "only_needed_if_future_work_demands_broader_than_selected_case_plan_coverage"
            row["priority"] = "medium"
            row["paper_risk_if_not_done"] = "low"
            row["notes"] = "Selected-case source/rewrite plan artifacts are now retained for speedup, regression, tie, failure, and one SQLGlot exemplar; denominator-wide plan extraction is still open."
        elif row["gap_id"] == "gap_11":
            row["current_status"] = "lowered_after_selected_case_plan_delta_packet"
            row["required_next_artifact_or_experiment"] = "denominator_wide_node_alignment_and_operator_level_attribution_only_if_future_work_demands_it"
            row["paper_risk_if_not_done"] = "medium"
            row["notes"] = "Selected cases now have bounded plan delta classes, but no full node alignment or global causal attribution exists."
        updated_gaps.append(row)
    gap_v6_fields = list(updated_gaps[0].keys())
    write_csv(FREEZE_DIR / "paper_remaining_experiment_gaps_v6.csv", updated_gaps, gap_v6_fields)

    # Markdown and run metadata.
    README = """# Selected Plan Observability 01

This run packet is a selected-case observability packet only.

- It uses mechanically selected retained rows.
- It extracts source/rewrite plans for those selected rows only.
- It does not run timing, generation, verifier, or LLM calls.
- It does not support full-denominator PlanParseRate, NodeAlignmentCoverage, or AttributionCoverage claims.
"""
    (RUN_DIR / "README.md").write_text(README, encoding="utf-8")

    policy = f"""# Plan Observability Policy V1

- Selection base: retained exact-timed rows from Direct LLM repair timing, SQLGlot per-case timing, and Calcite 93-row timing, plus the retained Table 10 failure exemplar.
- Speedup selection: highest retained speedup across the selected exact-timed packets.
- Regression selection: lowest retained speedup across the selected exact-timed packets.
- Tie selection: speedup closest to 1.0; rows within {TIE_EPSILON} of the best closeness are tie-candidates, and PostgreSQL is preferred inside that band.
- Extra coverage: add one SQLGlot row if SQLGlot is absent from the base four; add one Calcite row if Calcite is absent from the base four.
- Plan extraction: PostgreSQL uses EXPLAIN (FORMAT JSON); Spark uses EXPLAIN FORMATTED.
- Attribution: selected-case only, low/medium confidence only, no node alignment claim.
"""
    (RUN_DIR / "plan_observability_policy_v1.md").write_text(policy, encoding="utf-8")

    run_results = {
        "selected_cases": selected_rows,
        "source_plan_success_count": sum(row["source_plan_success"] == "true" for row in extraction_events),
        "rewrite_plan_success_count": sum(row["rewrite_plan_success"] == "true" for row in extraction_events),
        "plan_parse_success_count": sum(row["plan_parse_status"] == "parsed" for row in extraction_events),
        "main_plan_delta_classes": sorted(Counter(row["main_plan_delta"] for row in delta_rows).items()),
    }
    (RUN_DIR / "run_results.json").write_text(json.dumps(run_results, indent=2) + "\n", encoding="utf-8")

    validation = {
        "status": "ok" if all(row["source_plan_success"] == "true" for row in extraction_events) and all(row["rewrite_plan_success"] == "true" for row in extraction_events) else "warning",
        "selected_rows": len(selected_rows),
        "source_plan_success_count": sum(row["source_plan_success"] == "true" for row in extraction_events),
        "rewrite_plan_success_count": sum(row["rewrite_plan_success"] == "true" for row in extraction_events),
        "plan_parse_success_count": sum(row["plan_parse_status"] == "parsed" for row in extraction_events),
        "outcome_types": sorted({row["outcome_type"] for row in delta_rows}),
        "delta_classes": Counter(row["main_plan_delta"] for row in delta_rows),
    }
    (RUN_DIR / "validation_report.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")

    # Freeze markdown files.
    intro_common = [
        "这个文件回答 selected-case plan observability 现在具体保留了哪些证据。",
        "只使用机械选择出来的代表行，不支持 full-denominator observability。",
        "本步骤运行了 plan extraction / EXPLAIN，但没有运行 timing、generation、verifier 或 LLM。",
    ]
    write_md(
        FREEZE_DIR / "selected_plan_observability_manifest_v1.md",
        "Selected Plan Observability Manifest V1",
        intro_common + ["Selected cases are the deterministic speedup / regression / tie / failure set plus one SQLGlot coverage row."],
        selected_rows,
        manifest_fields,
        [
            "不能说的话：不能把这 5 个 case 的 plan artifact 外推成 full-denominator PlanParseRate、NodeAlignmentCoverage 或 AttributionCoverage。"
        ],
    )
    write_md(
        FREEZE_DIR / "selected_plan_observability_event_long_v1.md",
        "Selected Plan Observability Event Long V1",
        intro_common + ["这里记录 source / rewrite plan 是否成功提取，以及 plan format 和 parse status。"],
        extraction_events,
        event_fields,
        [
            "如果某一侧 plan 没有成功提取，这里会直接暴露出来，而不是被静默省略。"
        ],
    )
    write_md(
        FREEZE_DIR / "selected_plan_feature_summary_v1.md",
        "Selected Plan Feature Summary V1",
        intro_common + ["这里给出轻量级 plan feature，不做 full node alignment。"],
        feature_rows,
        feature_fields,
        [
            "这些 feature 只支持 selected-case 级别的可观察性描述，不支持全量归因。"
        ],
    )
    write_md(
        FREEZE_DIR / "selected_plan_delta_classification_v1.md",
        "Selected Plan Delta Classification V1",
        intro_common + ["这里给出 bounded vocabulary 下的 main plan delta class 和保守解释。"],
        delta_rows,
        delta_fields,
        [
            "不能说的话：不能把 lightweight delta class 直接升级成 global causal attribution。"
        ],
    )
    write_md(
        FREEZE_DIR / "table5_observability_plan_artifact_v2.md",
        "Table 5 Observability Plan Artifact V2",
        [
            "这个文件回答：当前 paper-safe 的 selected-case observability packet 覆盖了哪些 method/route。",
            "它是 selected-case coverage 表，不是 full denominator coverage 表。",
            "没有运行 timing、generation、verifier 或 LLM。"
        ],
        table5_rows,
        table5_fields,
        [
            "不能说的话：不能从这里推出 full-denominator PlanParseRate 或 AttributionCoverage。"
        ],
    )
    write_md(
        FREEZE_DIR / "table10_plan_observability_case_study_v3.md",
        "Table 10 Plan Observability Case Study V3",
        [
            "这个文件回答：speedup / regression / tie / failure 代表行现在有哪些可保留的 source/rewrite plan 证据。",
            "这些 row 是机械选择的代表 case，不是 cherry-pick 之后再反推的。",
            "没有声称 full node alignment 或 global attribution。"
        ],
        table10_rows,
        table10_fields,
        [
            "失败例如果没有有效 rewrite plan，需要诚实保留为 execution_or_planning_failure；这里不能捏造 plan delta。"
        ],
    )
    write_md(
        FREEZE_DIR / "plan_observability_case_study_gap_matrix_v3.md",
        "Plan Observability Case Study Gap Matrix V3",
        [
            "这个文件回答：selected-case observability packet 解决了哪些 gap，还剩哪些 gap。",
            "它只更新 observability gap，不改变 correctness / timing 结论。"
        ],
        gap_rows,
        gap_fields,
        [
            "仍然不能说 full-denominator node alignment、AttributionCoverage 或 global causal attribution。"
        ],
    )
    write_md(
        FREEZE_DIR / "paper_remaining_experiment_gaps_v6.md",
        "Paper Remaining Experiment Gaps V6",
        [
            "这是在 selected-case plan observability packet 之后的剩余实验缺口表。",
            "与前一版相比，method-specific selected-case plan extraction gap 已明显降低，但 denominator-wide observability 仍未完成。"
        ],
        updated_gaps,
        gap_v6_fields,
        [
            "仍然保留的高优先级缺口包括：accepted generated candidate false-accept audit、PORT bounded denominator expansion、以及 denominator-wide node alignment if future work needs it."
        ],
    )

    readme_v6 = """# Common-core v0 Paper Results README v6

这是一次 **selected-case plan observability packet** 刷新。

## What Changed

- 新增了机械选择的 5 个 representative rows。
- 对这些 selected rows 保留了 source/rewrite plan artifact。
- Table 5 现在能明确展示 selected-case plan coverage。
- Table 10 v3 现在不再只有 failure 身份信息，而是补上了 speedup / regression / tie / failure 的 bounded plan evidence。

## What This Supports

- selected-case observability evidence
- bounded plan-delta classes
- 比单纯 latency label 更可解释的 outcome narrative

## What This Does Not Support

- full-denominator PlanParseRate
- full NodeAlignmentCoverage
- full AttributionCoverage
- global causal attribution
- final ranked leaderboard
- SpeedupTransferRate

## Reading Order

1. `selected_plan_observability_manifest_v1.csv`
2. `table5_observability_plan_artifact_v2.csv`
3. `table10_plan_observability_case_study_v3.csv`
4. `selected_plan_delta_classification_v1.csv`
5. `plan_observability_case_study_gap_matrix_v3.csv`
6. `paper_remaining_experiment_gaps_v6.csv`

## Core Boundary

这套 packet 的价值在于：对代表性的 speedup / regression / tie / failure 行，paper 现在能保留 source/rewrite plan artifact 和保守的 delta class。
它**不是**一个 full plan-alignment benchmark，也不支持 full-denominator observability claim。
"""
    (FREEZE_DIR / "common_core_v0_paper_results_readme_v6.md").write_text(readme_v6, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
