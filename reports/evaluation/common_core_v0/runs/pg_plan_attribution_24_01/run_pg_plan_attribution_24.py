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
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
RUN_DIR = Path(__file__).resolve().parent
FREEZE_DIR = REPO_ROOT / "reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1"
WORKSPACES_DIR = RUN_DIR / "workspaces"

STATEMENT_TIMEOUT = "60s"
DENOMINATOR_ID = "common_core_v0_40_same_engine_120"
PACKET_ID = "pg_plan_attribution_24"
REVIEWED_IDS = [
    "direct_llm__direct_llm_same_engine_rewrite__PERF_0007__pg",
    "direct_llm__direct_llm_same_engine_rewrite__CONS_0012__pg",
    "direct_llm__direct_llm_same_engine_rewrite__PERF_0008__pg",
    "direct_llm__direct_llm_same_engine_rewrite__PORT_0003__pg",
    "direct_llm__direct_llm_same_engine_rewrite__CONS_0037__pg",
    "direct_llm__direct_llm_same_engine_rewrite__PERF_0034__pg",
    "direct_llm__direct_llm_execute_repair_1shot__LONGTAIL_0023__pg",
    "direct_llm__direct_llm_execute_repair_1shot__PERF_0019__pg",
    "sqlglot__sqlglot_transpile_same_dialect_noop__CONS_0005__pg",
    "sqlglot__sqlglot_transpile_same_dialect_noop__LONGTAIL_0011__pg",
    "sqlglot__sqlglot_transpile_same_dialect_noop__PERF_0082__pg",
    "sqlglot__sqlglot_transpile_same_dialect_noop__PERF_0017__pg",
    "sqlglot__sqlglot_transpile_same_dialect_noop__PERF_0035__pg",
    "sqlglot__sqlglot_optimize_same_dialect__LONGTAIL_0011__pg",
    "sqlglot__sqlglot_optimize_same_dialect__LONGTAIL_0022__pg",
    "sqlglot__sqlglot_optimize_same_dialect__PERF_0082__pg",
    "sqlglot__sqlglot_optimize_same_dialect__CONS_0010__pg",
    "sqlglot__sqlglot_optimize_same_dialect__CONS_0037__pg",
    "calcite_hep__calcite_hep_fail_closed_120__PERF_0007__pg",
    "calcite_hep__calcite_hep_fail_closed_120__CONS_0011__pg",
    "calcite_hep__calcite_hep_fail_closed_120__LONGTAIL_0013__pg",
    "calcite_hep__calcite_hep_fail_closed_120__PERF_0013__pg",
    "calcite_hep__calcite_hep_fail_closed_120__PERF_0054__pg",
    "calcite_hep__calcite_hep_fail_closed_120__PERF_0024__pg",
]
MAIN_ROUTE_LABELS = {
    "direct_llm_same_engine_rewrite": "Direct LLM",
    "direct_llm_execute_repair_1shot": "Direct LLM + Execute-and-Repair-1",
    "sqlglot_transpile_same_dialect_noop": "SQLGlot no-op / same-dialect",
    "sqlglot_optimize_same_dialect": "SQLGlot optimize",
    "calcite_hep_fail_closed_120": "Calcite HEP",
}
FEATURE_FIELDS = [
    "candidate_id",
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "outcome_type_hint",
    "plan_side",
    "plan_artifact",
    "plan_parse_success",
    "root_node_type",
    "node_count",
    "scan_node_count",
    "join_node_count",
    "aggregate_node_count",
    "sort_node_count",
    "materialize_node_count",
    "planning_time_ms",
    "execution_time_ms",
    "total_actual_time_root_ms",
    "total_shared_blks_hit",
    "total_shared_blks_read",
    "total_shared_blks_dirtied",
    "total_shared_blks_written",
    "root_plan_rows",
    "root_actual_rows",
    "max_row_estimate_error_node_type",
    "max_row_estimate_error_ratio",
    "main_operator_families",
    "scan_types",
    "join_types",
    "aggregate_types",
    "sort_types",
    "materialize_types",
]


@dataclass
class Candidate:
    candidate_id: str
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    outcome_type_hint: str
    retained_speedup: str
    timing_source_artifact: str
    source_sql_artifact: str
    rewrite_sql_artifact: str
    schema_artifact: str
    witness_data_artifact: str
    exact_evidence_artifact: str
    plan_attribution_ready: str
    blocking_reason: str
    recommended_priority: str
    recommended_role_for_table10: str
    notes: str


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def render_md_table(rows: list[dict[str, Any]], fieldnames: list[str]) -> str:
    def esc(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    header = "| " + " | ".join(fieldnames) + " |"
    sep = "| " + " | ".join(["---"] * len(fieldnames)) + " |"
    body = [
        "| " + " | ".join(esc(row.get(field, "")) for field in fieldnames) + " |"
        for row in rows
    ]
    return "\n".join([header, sep] + body)


def write_md(
    path: Path,
    title: str,
    intro_lines: list[str],
    rows: list[dict[str, Any]] | None = None,
    fieldnames: list[str] | None = None,
    extra_lines: list[str] | None = None,
) -> None:
    parts = [f"# {title}", ""]
    parts.extend(intro_lines)
    parts.append("")
    if rows is not None and fieldnames is not None:
        parts.append(render_md_table(rows, fieldnames))
        parts.append("")
    if extra_lines:
        parts.extend(extra_lines)
        parts.append("")
    path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8", newline="\n")


def json_dump(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8", newline="\n")


def strip_sql_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    lines = []
    for line in text.splitlines():
        if re.match(r"^\s*--", line):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def repo_path(value: str) -> Path:
    candidate = REPO_ROOT / value
    if candidate.exists():
        return candidate
    normalized = (
        value.replace("cases/Performance/", "cases/PERF/")
        .replace("cases/Consistency/", "cases/CONS/")
        .replace("cases/Portability/", "cases/PORT/")
        .replace("cases/Longtail/", "cases/LONGTAIL/")
    )
    return REPO_ROOT / normalized


def psql_base() -> list[str]:
    return ["psql", "-X", "-v", "ON_ERROR_STOP=1"]


def psql_query() -> list[str]:
    return ["psql", "-X", "-q", "-A", "-t", "-v", "ON_ERROR_STOP=1"]


def run_psql_file(sql_path: Path, stdout_path: Path, stderr_path: Path) -> subprocess.CompletedProcess[str]:
    with stdout_path.open("w", encoding="utf-8") as out, stderr_path.open("w", encoding="utf-8") as err:
        return subprocess.run(
            psql_query() + ["-f", str(sql_path)],
            cwd=REPO_ROOT,
            text=True,
            stdout=out,
            stderr=err,
            check=False,
        )


def run_psql_text(sql_text: str, stdout_path: Path, stderr_path: Path) -> subprocess.CompletedProcess[str]:
    with stdout_path.open("w", encoding="utf-8") as out, stderr_path.open("w", encoding="utf-8") as err:
        return subprocess.run(
            psql_base(),
            cwd=REPO_ROOT,
            text=True,
            input=sql_text,
            stdout=out,
            stderr=err,
            check=False,
        )


def schema_name(candidate_id: str) -> str:
    cleaned = re.sub(r"[^a-z0-9_]", "_", candidate_id.lower())
    return f"attr24_{cleaned}"[:60]


def extract_plan_payload(stdout_path: Path) -> list[dict[str, Any]]:
    text = stdout_path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("empty explain output")
    return json.loads(text)


def walk_plan(plan: dict[str, Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []

    def visit(node: dict[str, Any]) -> None:
        nodes.append(node)
        for child in node.get("Plans", []) or []:
            visit(child)

    visit(plan)
    return nodes


def classify_node_family(node_type: str) -> str:
    lowered = node_type.lower()
    if "scan" in lowered:
        return "scan"
    if "join" in lowered or lowered in {"nested loop", "hash join", "merge join"}:
        return "join"
    if "aggregate" in lowered or lowered in {"group", "groupaggregate", "hashaggregate"}:
        return "aggregate"
    if "sort" in lowered or "limit" in lowered:
        return "sort"
    if "material" in lowered:
        return "materialize"
    return "other"


def compute_estimate_error(node: dict[str, Any]) -> float | None:
    plan_rows = node.get("Plan Rows")
    actual_rows = node.get("Actual Rows")
    if plan_rows is None or actual_rows is None:
        return None
    plan_rows = max(float(plan_rows), 1.0)
    actual_rows = max(float(actual_rows), 1.0)
    return max(actual_rows / plan_rows, plan_rows / actual_rows)


def summarize_plan(plan_payload: list[dict[str, Any]]) -> dict[str, Any]:
    root = plan_payload[0]["Plan"]
    nodes = walk_plan(root)
    family_counter = Counter()
    node_types_by_family: dict[str, set[str]] = defaultdict(set)
    shared_hits = 0.0
    shared_reads = 0.0
    shared_dirtied = 0.0
    shared_written = 0.0
    max_est_err = -1.0
    max_est_node_type = "NA_not_computable"
    for node in nodes:
        node_type = str(node.get("Node Type", "UNKNOWN"))
        family = classify_node_family(node_type)
        family_counter[family] += 1
        node_types_by_family[family].add(node_type)
        shared_hits += float(node.get("Shared Hit Blocks", 0.0) or 0.0)
        shared_reads += float(node.get("Shared Read Blocks", 0.0) or 0.0)
        shared_dirtied += float(node.get("Shared Dirtied Blocks", 0.0) or 0.0)
        shared_written += float(node.get("Shared Written Blocks", 0.0) or 0.0)
        err = compute_estimate_error(node)
        if err is not None and err > max_est_err:
            max_est_err = err
            max_est_node_type = node_type
    families_present = [family for family in ["scan", "join", "aggregate", "sort", "materialize", "other"] if family_counter.get(family, 0) > 0]
    return {
        "plan_parse_success": True,
        "root_node_type": root.get("Node Type", "UNKNOWN"),
        "node_count": len(nodes),
        "scan_node_count": family_counter.get("scan", 0),
        "join_node_count": family_counter.get("join", 0),
        "aggregate_node_count": family_counter.get("aggregate", 0),
        "sort_node_count": family_counter.get("sort", 0),
        "materialize_node_count": family_counter.get("materialize", 0),
        "planning_time_ms": float(plan_payload[0].get("Planning Time", 0.0) or 0.0),
        "execution_time_ms": float(plan_payload[0].get("Execution Time", 0.0) or 0.0),
        "total_actual_time_root_ms": float(root.get("Actual Total Time", 0.0) or 0.0),
        "total_shared_blks_hit": shared_hits,
        "total_shared_blks_read": shared_reads,
        "total_shared_blks_dirtied": shared_dirtied,
        "total_shared_blks_written": shared_written,
        "root_plan_rows": float(root.get("Plan Rows", 0.0) or 0.0),
        "root_actual_rows": float(root.get("Actual Rows", 0.0) or 0.0),
        "max_row_estimate_error_node_type": max_est_node_type,
        "max_row_estimate_error_ratio": None if max_est_err < 0 else max_est_err,
        "main_operator_families": ",".join(families_present),
        "scan_types": ",".join(sorted(node_types_by_family["scan"])),
        "join_types": ",".join(sorted(node_types_by_family["join"])),
        "aggregate_types": ",".join(sorted(node_types_by_family["aggregate"])),
        "sort_types": ",".join(sorted(node_types_by_family["sort"])),
        "materialize_types": ",".join(sorted(node_types_by_family["materialize"])),
    }


def diff_string(lhs: str, rhs: str) -> str:
    if lhs == rhs:
        return "no_change"
    return f"{lhs or 'none'} -> {rhs or 'none'}"


def ratio(value: float, baseline: float) -> float | None:
    if baseline == 0:
        return None
    return value / baseline


def classify_delta(source: dict[str, Any] | None, rewrite: dict[str, Any] | None, retained_speedup: str) -> tuple[dict[str, Any], str]:
    if source is None or rewrite is None:
        return {
            "source_node_count": source.get("node_count", "") if source else "",
            "rewrite_node_count": rewrite.get("node_count", "") if rewrite else "",
            "node_count_delta": "",
            "planning_time_delta_ms": "",
            "execution_time_delta_ms": "",
            "shared_blks_read_delta": "",
            "shared_blks_hit_delta": "",
            "row_estimate_error_delta": "",
            "scan_strategy_delta": "plan_missing",
            "join_strategy_delta": "plan_missing",
            "aggregate_strategy_delta": "plan_missing",
            "sort_or_materialize_delta": "plan_missing",
            "main_plan_delta_class": "plan_extraction_failed",
            "heuristic_node_alignment_pairs": "none",
            "heuristic_node_alignment_coverage": "0.0",
            "attribution_confidence": "none",
        }, "Plan extraction failed for source or rewrite, so no node-level attribution is defensible."

    node_count_delta = int(rewrite["node_count"]) - int(source["node_count"])
    planning_delta = float(rewrite["planning_time_ms"]) - float(source["planning_time_ms"])
    execution_delta = float(rewrite["execution_time_ms"]) - float(source["execution_time_ms"])
    shared_read_delta = float(rewrite["total_shared_blks_read"]) - float(source["total_shared_blks_read"])
    shared_hit_delta = float(rewrite["total_shared_blks_hit"]) - float(source["total_shared_blks_hit"])
    src_err = source.get("max_row_estimate_error_ratio")
    rw_err = rewrite.get("max_row_estimate_error_ratio")
    err_delta = "" if src_err is None or rw_err is None else float(rw_err) - float(src_err)
    scan_delta = diff_string(source["scan_types"], rewrite["scan_types"])
    join_delta = diff_string(source["join_types"], rewrite["join_types"])
    agg_delta = diff_string(source["aggregate_types"], rewrite["aggregate_types"])
    sort_delta = diff_string(
        ",".join(filter(None, [source["sort_types"], source["materialize_types"]])),
        ",".join(filter(None, [rewrite["sort_types"], rewrite["materialize_types"]])),
    )
    src_families = set(filter(None, source["main_operator_families"].split(",")))
    rw_families = set(filter(None, rewrite["main_operator_families"].split(",")))
    overlap = src_families & rw_families
    union = src_families | rw_families
    coverage = 1.0 if not union else len(overlap) / len(union)
    alignment_pairs = ["root:root"]
    for family in sorted(overlap):
        alignment_pairs.append(f"{family}:{family}")

    if scan_delta != "no_change":
        delta_class = "scan_strategy_change"
    elif join_delta != "no_change":
        delta_class = "join_strategy_change"
    elif agg_delta != "no_change":
        delta_class = "aggregate_strategy_change"
    elif sort_delta != "no_change":
        delta_class = "sort_or_materialize_change"
    elif node_count_delta != 0:
        delta_class = "node_count_change"
    elif any(abs(x) > 0.000001 for x in [planning_delta, execution_delta, shared_read_delta, shared_hit_delta]):
        delta_class = "buffer_or_runtime_delta_without_operator_change"
    else:
        delta_class = "no_major_plan_delta"

    retained = None
    if retained_speedup not in {"", "NA_not_available"}:
        try:
            retained = float(retained_speedup)
        except ValueError:
            retained = None
    plausible_direction = False
    if retained is not None:
        if retained > 1.05 and execution_delta < 0:
            plausible_direction = True
        elif retained < 0.95 and execution_delta > 0:
            plausible_direction = True
        elif 0.95 <= retained <= 1.05 and abs(execution_delta) < max(1.0, abs(source["execution_time_ms"]) * 0.1):
            plausible_direction = True
    if delta_class == "plan_extraction_failed":
        confidence = "none"
    elif delta_class in {
        "scan_strategy_change",
        "join_strategy_change",
        "aggregate_strategy_change",
        "sort_or_materialize_change",
        "node_count_change",
    } and plausible_direction:
        confidence = "medium"
    else:
        confidence = "low"

    interp = {
        "scan_strategy_change": "Source and rewrite use different scan operators or scan families; this is plausible selected-case attribution evidence but not denominator-wide proof.",
        "join_strategy_change": "Source and rewrite use different join operators; this gives medium-strength selected-case attribution only when direction also matches runtime/buffer movement.",
        "aggregate_strategy_change": "Aggregate operator families differ across source and rewrite; this is selected-case attribution evidence only.",
        "sort_or_materialize_change": "Sort/materialize behavior differs across source and rewrite; selected-case attribution only.",
        "node_count_change": "Major node count differs while operator families are similar; this suggests structural plan simplification or expansion for this row only.",
        "buffer_or_runtime_delta_without_operator_change": "Operator families are similar but runtime or buffer counters differ; this is weak attribution evidence.",
        "no_major_plan_delta": "Plans look broadly similar at the retained feature level, so causal interpretation should stay cautious.",
    }[delta_class]

    return {
        "source_node_count": source["node_count"],
        "rewrite_node_count": rewrite["node_count"],
        "node_count_delta": node_count_delta,
        "planning_time_delta_ms": planning_delta,
        "execution_time_delta_ms": execution_delta,
        "shared_blks_read_delta": shared_read_delta,
        "shared_blks_hit_delta": shared_hit_delta,
        "row_estimate_error_delta": err_delta,
        "scan_strategy_delta": scan_delta,
        "join_strategy_delta": join_delta,
        "aggregate_strategy_delta": agg_delta,
        "sort_or_materialize_delta": sort_delta,
        "main_plan_delta_class": delta_class,
        "heuristic_node_alignment_pairs": ";".join(alignment_pairs),
        "heuristic_node_alignment_coverage": f"{coverage:.3f}",
        "attribution_confidence": confidence,
    }, interp


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_artifact(src: Path, dst: Path) -> None:
    ensure_parent(dst)
    shutil.copyfile(src, dst)


def load_candidates() -> list[Candidate]:
    rows = read_csv(FREEZE_DIR / "pg_plan_attribution_candidate_pool_v1.csv")
    by_id = {row["candidate_id"]: row for row in rows}
    missing = [candidate_id for candidate_id in REVIEWED_IDS if candidate_id not in by_id]
    if missing:
        raise RuntimeError(f"Reviewed candidate IDs missing from pool: {missing}")
    selected: list[Candidate] = []
    for candidate_id in REVIEWED_IDS:
        row = by_id[candidate_id]
        if row["engine"] != "pg":
            raise RuntimeError(f"{candidate_id} is not PostgreSQL")
        selected.append(Candidate(**row))
    return selected


def verify_candidate_artifacts(candidates: list[Candidate]) -> None:
    for candidate in candidates:
        for field in [
            "source_sql_artifact",
            "rewrite_sql_artifact",
            "schema_artifact",
            "witness_data_artifact",
            "exact_evidence_artifact",
        ]:
            path = repo_path(getattr(candidate, field))
            if not path.exists():
                raise RuntimeError(f"{candidate.candidate_id} missing {field}: {path}")


def explain_sql(candidate: Candidate, schema: str, query_relpath: str) -> str:
    query_path = repo_path(query_relpath)
    query_sql = query_path.read_text(encoding="utf-8").rstrip()
    if not query_sql.endswith(";"):
        query_sql += ";"
    return "\n".join(
        [
            f"set search_path to {schema};",
            "begin read only;",
            f"set local statement_timeout = '{STATEMENT_TIMEOUT}';",
            "explain (analyze, buffers, format json)",
            query_sql.strip(),
            "rollback;",
            "",
        ]
    )


def setup_sql(candidate: Candidate, schema: str) -> str:
    return "\n".join(
        [
            f"drop schema if exists {schema} cascade;",
            f"create schema {schema};",
            f"set search_path to {schema};",
            f"\\i {repo_path(candidate.schema_artifact)}",
            f"\\i {repo_path(candidate.witness_data_artifact)}",
            "",
        ]
    )


def cleanup_sql(schema: str) -> str:
    return f"drop schema if exists {schema} cascade;\n"


def outcome_bucket(speedup: str) -> str:
    value = float(speedup)
    if value > 1.05:
        return "speedup"
    if value < 0.95:
        return "regression"
    return "neutral"


def normalize_float(value: Any) -> str:
    if value == "" or value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
            return ""
        return f"{value:.15f}".rstrip("0").rstrip(".")
    return str(value)


def build_packet() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)
    candidates = load_candidates()
    verify_candidate_artifacts(candidates)

    manifest_rows: list[dict[str, Any]] = []
    command_rows: list[dict[str, Any]] = []
    event_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    delta_rows: list[dict[str, Any]] = []
    result_manifest_rows: list[dict[str, Any]] = []

    for order, candidate in enumerate(candidates, start=1):
        workspace = WORKSPACES_DIR / candidate.candidate_id
        workspace.mkdir(parents=True, exist_ok=True)
        schema = schema_name(candidate.candidate_id)

        source_src = repo_path(candidate.source_sql_artifact)
        rewrite_src = repo_path(candidate.rewrite_sql_artifact)
        ddl_src = repo_path(candidate.schema_artifact)
        witness_src = repo_path(candidate.witness_data_artifact)
        exact_src = repo_path(candidate.exact_evidence_artifact)

        copy_artifact(source_src, workspace / "source.sql")
        copy_artifact(rewrite_src, workspace / "rewrite.sql")
        copy_artifact(ddl_src, workspace / "ddl_pg.sql")
        copy_artifact(witness_src, workspace / "pg_witness_data.sql")
        copy_artifact(exact_src, workspace / "exact_evidence_artifact.json")

        setup_sql_path = workspace / "setup.sql"
        source_sql_path = workspace / "source_explain.sql"
        rewrite_sql_path = workspace / "rewrite_explain.sql"
        setup_sql_path.write_text(setup_sql(candidate, schema), encoding="utf-8", newline="\n")
        source_sql_path.write_text(explain_sql(candidate, schema, candidate.source_sql_artifact), encoding="utf-8", newline="\n")
        rewrite_sql_path.write_text(explain_sql(candidate, schema, candidate.rewrite_sql_artifact), encoding="utf-8", newline="\n")

        manifest_rows.append(
            {
                "selected_order": order,
                "candidate_id": candidate.candidate_id,
                "case_id": candidate.case_id,
                "pool": candidate.pool,
                "engine": candidate.engine,
                "method_id": candidate.method_id,
                "route_id": candidate.route_id,
                "outcome_type_hint": candidate.outcome_type_hint,
                "retained_speedup": candidate.retained_speedup,
                "source_sql_artifact": candidate.source_sql_artifact,
                "rewrite_sql_artifact": candidate.rewrite_sql_artifact,
                "schema_artifact": candidate.schema_artifact,
                "witness_data_artifact": candidate.witness_data_artifact,
                "exact_evidence_artifact": candidate.exact_evidence_artifact,
                "timing_source_artifact": candidate.timing_source_artifact,
                "selected_status": "selected_reviewed_24",
                "notes": candidate.notes,
            }
        )
        command_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "schema_name": schema,
                "statement_timeout": STATEMENT_TIMEOUT,
                "setup_sql": str(setup_sql_path.relative_to(REPO_ROOT)),
                "source_explain_sql": str(source_sql_path.relative_to(REPO_ROOT)),
                "rewrite_explain_sql": str(rewrite_sql_path.relative_to(REPO_ROOT)),
            }
        )

        setup_stdout = workspace / "setup.stdout.log"
        setup_stderr = workspace / "setup.stderr.log"
        setup_res = run_psql_text(setup_sql_path.read_text(encoding="utf-8"), setup_stdout, setup_stderr)

        source_plan_success = False
        rewrite_plan_success = False
        plan_parse_success = False
        source_summary: dict[str, Any] | None = None
        rewrite_summary: dict[str, Any] | None = None
        delta_payload: dict[str, Any]
        interpretation = ""
        failure_reason = ""

        source_stdout = workspace / "source_plan.stdout.json"
        source_stderr = workspace / "source_plan.stderr.log"
        rewrite_stdout = workspace / "rewrite_plan.stdout.json"
        rewrite_stderr = workspace / "rewrite_plan.stderr.log"
        source_plan_artifact = workspace / "source_plan.json"
        rewrite_plan_artifact = workspace / "rewrite_plan.json"

        if setup_res.returncode != 0:
            failure_reason = "schema_or_witness_load_failed"
        else:
            source_res = run_psql_file(source_sql_path, source_stdout, source_stderr)
            source_plan_success = source_res.returncode == 0
            if source_plan_success:
                try:
                    source_payload = extract_plan_payload(source_stdout)
                    json_dump(source_plan_artifact, source_payload)
                    source_summary = summarize_plan(source_payload)
                except Exception as exc:  # noqa: BLE001
                    source_plan_success = False
                    failure_reason = f"source_plan_parse_failed: {exc}"
            else:
                failure_reason = "source_explain_failed"

            rewrite_res = run_psql_file(rewrite_sql_path, rewrite_stdout, rewrite_stderr)
            rewrite_plan_success = rewrite_res.returncode == 0
            if rewrite_plan_success:
                try:
                    rewrite_payload = extract_plan_payload(rewrite_stdout)
                    json_dump(rewrite_plan_artifact, rewrite_payload)
                    rewrite_summary = summarize_plan(rewrite_payload)
                except Exception as exc:  # noqa: BLE001
                    rewrite_plan_success = False
                    failure_reason = f"rewrite_plan_parse_failed: {exc}"
            elif not failure_reason:
                failure_reason = "rewrite_explain_failed"

            if source_plan_success and rewrite_plan_success and source_summary and rewrite_summary:
                plan_parse_success = True

        cleanup_stdout = workspace / "cleanup.stdout.log"
        cleanup_stderr = workspace / "cleanup.stderr.log"
        run_psql_text(cleanup_sql(schema), cleanup_stdout, cleanup_stderr)

        delta_payload, interpretation = classify_delta(source_summary, rewrite_summary, candidate.retained_speedup)
        if not failure_reason and delta_payload["main_plan_delta_class"] == "plan_extraction_failed":
            failure_reason = "plan_extraction_failed"

        if source_summary:
            feature_payload = dict(source_summary)
            feature_payload.update(
                {
                    "candidate_id": candidate.candidate_id,
                    "case_id": candidate.case_id,
                    "pool": candidate.pool,
                    "engine": candidate.engine,
                    "method_id": candidate.method_id,
                    "route_id": candidate.route_id,
                    "outcome_type_hint": candidate.outcome_type_hint,
                    "plan_side": "source",
                    "plan_artifact": str(source_plan_artifact.relative_to(REPO_ROOT)),
                }
            )
            feature_rows.append({k: normalize_float(v) for k, v in feature_payload.items()})
            json_dump(workspace / "source_plan_feature_summary.json", feature_payload)
        if rewrite_summary:
            feature_payload = dict(rewrite_summary)
            feature_payload.update(
                {
                    "candidate_id": candidate.candidate_id,
                    "case_id": candidate.case_id,
                    "pool": candidate.pool,
                    "engine": candidate.engine,
                    "method_id": candidate.method_id,
                    "route_id": candidate.route_id,
                    "outcome_type_hint": candidate.outcome_type_hint,
                    "plan_side": "rewrite",
                    "plan_artifact": str(rewrite_plan_artifact.relative_to(REPO_ROOT)),
                }
            )
            feature_rows.append({k: normalize_float(v) for k, v in feature_payload.items()})
            json_dump(workspace / "rewrite_plan_feature_summary.json", feature_payload)

        node_delta_payload = {
            "candidate_id": candidate.candidate_id,
            "case_id": candidate.case_id,
            "pool": candidate.pool,
            "engine": candidate.engine,
            "method_id": candidate.method_id,
            "route_id": candidate.route_id,
            "outcome_type_hint": candidate.outcome_type_hint,
            "retained_speedup": candidate.retained_speedup,
            **delta_payload,
            "paper_safe_interpretation": interpretation,
            "forbidden_overclaim": "Do not claim denominator-wide node alignment or global causal attribution from this selected 24-row PG packet.",
            "evidence_artifacts": "|".join(
                filter(
                    None,
                    [
                        str(source_plan_artifact.relative_to(REPO_ROOT)) if source_plan_artifact.exists() else "",
                        str(rewrite_plan_artifact.relative_to(REPO_ROOT)) if rewrite_plan_artifact.exists() else "",
                        candidate.timing_source_artifact,
                    ],
                )
            ),
            "notes": "selected_pg_explain_analyze_buffers_packet",
        }
        delta_rows.append({k: normalize_float(v) for k, v in node_delta_payload.items()})
        json_dump(workspace / "plan_delta.json", node_delta_payload)

        event_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "case_id": candidate.case_id,
                "pool": candidate.pool,
                "engine": candidate.engine,
                "method_id": candidate.method_id,
                "route_id": candidate.route_id,
                "outcome_type_hint": candidate.outcome_type_hint,
                "retained_speedup": candidate.retained_speedup,
                "source_plan_attempted": "true",
                "source_plan_success": str(source_plan_success).lower(),
                "rewrite_plan_attempted": "true",
                "rewrite_plan_success": str(rewrite_plan_success).lower(),
                "plan_parse_success": str(plan_parse_success).lower(),
                "source_plan_artifact": str(source_plan_artifact.relative_to(REPO_ROOT)) if source_plan_artifact.exists() else "",
                "rewrite_plan_artifact": str(rewrite_plan_artifact.relative_to(REPO_ROOT)) if rewrite_plan_artifact.exists() else "",
                "source_sql_artifact": candidate.source_sql_artifact,
                "rewrite_sql_artifact": candidate.rewrite_sql_artifact,
                "schema_artifact": candidate.schema_artifact,
                "witness_data_artifact": candidate.witness_data_artifact,
                "exact_evidence_artifact": candidate.exact_evidence_artifact,
                "main_plan_delta_class": delta_payload["main_plan_delta_class"],
                "attribution_confidence": delta_payload["attribution_confidence"],
                "failure_reason": failure_reason,
                "notes": "selected_pg_explain_analyze_buffers_packet",
            }
        )

        result_manifest_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "workspace": str(workspace.relative_to(REPO_ROOT)),
                "setup_stdout": str(setup_stdout.relative_to(REPO_ROOT)),
                "setup_stderr": str(setup_stderr.relative_to(REPO_ROOT)),
                "source_stdout": str(source_stdout.relative_to(REPO_ROOT)),
                "source_stderr": str(source_stderr.relative_to(REPO_ROOT)),
                "rewrite_stdout": str(rewrite_stdout.relative_to(REPO_ROOT)),
                "rewrite_stderr": str(rewrite_stderr.relative_to(REPO_ROOT)),
                "source_plan_artifact": str(source_plan_artifact.relative_to(REPO_ROOT)) if source_plan_artifact.exists() else "",
                "rewrite_plan_artifact": str(rewrite_plan_artifact.relative_to(REPO_ROOT)) if rewrite_plan_artifact.exists() else "",
            }
        )

        if failure_reason:
            failure_rows.append(
                {
                    "candidate_id": candidate.candidate_id,
                    "case_id": candidate.case_id,
                    "method_id": candidate.method_id,
                    "route_id": candidate.route_id,
                    "failure_reason": failure_reason,
                    "setup_stderr": str(setup_stderr.relative_to(REPO_ROOT)),
                    "source_stderr": str(source_stderr.relative_to(REPO_ROOT)),
                    "rewrite_stderr": str(rewrite_stderr.relative_to(REPO_ROOT)),
                }
            )

    manifest_fields = list(manifest_rows[0].keys())
    write_csv(RUN_DIR / "selected_candidate_manifest.csv", manifest_rows, manifest_fields)
    write_csv(RUN_DIR / "explain_analyze_command_matrix.csv", command_rows, list(command_rows[0].keys()))
    write_csv(RUN_DIR / "explain_analyze_event_long.csv", event_rows, list(event_rows[0].keys()))
    write_csv(
        RUN_DIR / "explain_analyze_failures.csv",
        failure_rows or [{"candidate_id": "", "case_id": "", "method_id": "", "route_id": "", "failure_reason": "", "setup_stderr": "", "source_stderr": "", "rewrite_stderr": ""}],
        ["candidate_id", "case_id", "method_id", "route_id", "failure_reason", "setup_stderr", "source_stderr", "rewrite_stderr"],
    )
    write_csv(RUN_DIR / "pg_plan_feature_summary.csv", feature_rows or [{field: "" for field in FEATURE_FIELDS}], FEATURE_FIELDS)
    write_csv(RUN_DIR / "pg_plan_node_delta.csv", delta_rows, list(delta_rows[0].keys()))

    by_route: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in event_rows:
        by_route[(row["method_id"], row["route_id"])].append(row)
    summary_rows: list[dict[str, Any]] = []
    for (method_id, route_id), rows in sorted(by_route.items()):
        deltas = [row["main_plan_delta_class"] for row in rows]
        confidence = Counter(row["attribution_confidence"] for row in rows)
        summary_rows.append(
            {
                "method_id": method_id,
                "route_id": route_id,
                "selected_rows": len(rows),
                "successful_source_plans": sum(row["source_plan_success"] == "true" for row in rows),
                "successful_rewrite_plans": sum(row["rewrite_plan_success"] == "true" for row in rows),
                "plan_parse_success_rows": sum(row["plan_parse_success"] == "true" for row in rows),
                "plan_parse_success_rate": normalize_float(sum(row["plan_parse_success"] == "true" for row in rows) / len(rows)),
                "main_delta_classes_observed": "|".join(f"{name}:{count}" for name, count in sorted(Counter(deltas).items())),
                "attribution_confidence_distribution": "|".join(f"{name}:{count}" for name, count in sorted(confidence.items())),
                "notes": "selected_24_pg_explain_analyze_buffers_summary",
            }
        )
    overall = {
        "method_id": "overall",
        "route_id": PACKET_ID,
        "selected_rows": len(event_rows),
        "successful_source_plans": sum(row["source_plan_success"] == "true" for row in event_rows),
        "successful_rewrite_plans": sum(row["rewrite_plan_success"] == "true" for row in event_rows),
        "plan_parse_success_rows": sum(row["plan_parse_success"] == "true" for row in event_rows),
        "plan_parse_success_rate": normalize_float(sum(row["plan_parse_success"] == "true" for row in event_rows) / len(event_rows)),
        "main_delta_classes_observed": "|".join(f"{name}:{count}" for name, count in sorted(Counter(row["main_plan_delta_class"] for row in event_rows).items())),
        "attribution_confidence_distribution": "|".join(f"{name}:{count}" for name, count in sorted(Counter(row["attribution_confidence"] for row in event_rows).items())),
        "notes": "overall_selected_24_pg_explain_analyze_buffers_summary",
    }
    summary_rows = [overall] + summary_rows
    write_csv(RUN_DIR / "pg_plan_attribution_summary.csv", summary_rows, list(summary_rows[0].keys()))
    write_csv(RUN_DIR / "hard_result_manifest_unused.csv", result_manifest_rows, list(result_manifest_rows[0].keys()))
    (RUN_DIR / "hard_result_manifest_unused.csv").unlink()

    # Run packet docs
    write_md(
        RUN_DIR / "README.md",
        "PG Plan Attribution 24 Packet",
        [
            "This run packet collects PostgreSQL-only EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) artifacts for the reviewed 24-row attribution subset.",
            "It is a selected-case attribution packet only. It does not rerun generation, checker, timing, verifier, or cross-engine work.",
            "中文说明：这个 packet 只做 PG 计划归因采样，不替代 Table 6 时延结果，也不支持 full-denominator attribution。",
        ],
    )
    write_md(
        RUN_DIR / "pg_plan_attribution_policy_v1.md",
        "PG Plan Attribution Policy V1",
        [
            "Reviewed denominator: exactly 24 PostgreSQL candidate IDs from the preflight recommendation.",
            f"Plan command: `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` inside `BEGIN READ ONLY` with `statement_timeout={STATEMENT_TIMEOUT}`.",
            "Attribution is conservative: only `medium`, `low`, or `none` confidence is used; no denominator-wide node alignment is claimed.",
            "中文说明：这里的 node delta 仅用于 selected-case 可观察性，不是全量因果归因基准。",
        ],
    )
    json_dump(
        RUN_DIR / "run_results.json",
        {
            "packet_id": PACKET_ID,
            "reviewed_candidate_count": len(REVIEWED_IDS),
            "manifest_rows": len(manifest_rows),
            "event_rows": len(event_rows),
            "source_plan_success_count": sum(row["source_plan_success"] == "true" for row in event_rows),
            "rewrite_plan_success_count": sum(row["rewrite_plan_success"] == "true" for row in event_rows),
            "plan_parse_success_count": sum(row["plan_parse_success"] == "true" for row in event_rows),
            "delta_class_distribution": dict(Counter(row["main_plan_delta_class"] for row in event_rows)),
            "attribution_confidence_distribution": dict(Counter(row["attribution_confidence"] for row in event_rows)),
            "failed_candidates": failure_rows,
        },
    )
    json_dump(
        RUN_DIR / "validation_report.json",
        {
            "status": "ok" if len(event_rows) == 24 and not failure_rows else "warning",
            "expected_candidates": 24,
            "manifest_rows": len(manifest_rows),
            "event_rows": len(event_rows),
            "failure_rows": len(failure_rows),
            "source_plan_success_count": sum(row["source_plan_success"] == "true" for row in event_rows),
            "rewrite_plan_success_count": sum(row["rewrite_plan_success"] == "true" for row in event_rows),
            "plan_parse_success_count": sum(row["plan_parse_success"] == "true" for row in event_rows),
        },
    )

    # Freeze copies
    freeze_map = {
        "selected_candidate_manifest.csv": "pg_plan_attribution_24_manifest_v1.csv",
        "explain_analyze_event_long.csv": "pg_plan_attribution_24_event_long_v1.csv",
        "pg_plan_feature_summary.csv": "pg_plan_attribution_24_feature_summary_v1.csv",
        "pg_plan_node_delta.csv": "pg_plan_attribution_24_node_delta_v1.csv",
        "pg_plan_attribution_summary.csv": "pg_plan_attribution_24_summary_v1.csv",
    }
    for src_name, dst_name in freeze_map.items():
        shutil.copyfile(RUN_DIR / src_name, FREEZE_DIR / dst_name)

    for csv_name, title, intro in [
        ("pg_plan_attribution_24_manifest_v1.csv", "PG Plan Attribution 24 Manifest V1", [
            "This file lists the reviewed 24 PostgreSQL attribution candidates and their retained artifacts.",
            "中文说明：这是 24 行 PG 归因 packet 的固定清单，不代表全量 denominator。",
        ]),
        ("pg_plan_attribution_24_event_long_v1.csv", "PG Plan Attribution 24 Event Long V1", [
            "This file records per-candidate plan extraction success or failure for source and rewrite.",
            "中文说明：这里只记录计划提取事件，不替代 timing 或 checker。",
        ]),
        ("pg_plan_attribution_24_feature_summary_v1.csv", "PG Plan Attribution 24 Feature Summary V1", [
            "This file summarizes retained source/rewrite PostgreSQL JSON plan features for the selected 24 rows.",
            "中文说明：这些特征用于 selected-case 计划观察，不支持全量 node attribution。",
        ]),
        ("pg_plan_attribution_24_node_delta_v1.csv", "PG Plan Attribution 24 Node Delta V1", [
            "This file contains conservative node-level deltas and attribution confidence labels for the selected 24 PG rows.",
            "中文说明：这里只做保守 delta 分类，不做全量因果解释。",
        ]),
        ("pg_plan_attribution_24_summary_v1.csv", "PG Plan Attribution 24 Summary V1", [
            "This file summarizes the 24-row packet overall and by main route.",
            "中文说明：这是 packet 级别汇总，不是最终 paper claim matrix。",
        ]),
    ]:
        rows = read_csv(FREEZE_DIR / csv_name)
        write_md(FREEZE_DIR / csv_name.replace(".csv", ".md"), title, intro, rows, list(rows[0].keys()))

    # Table 5 v4
    table5_rows = read_csv(FREEZE_DIR / "table5_observability_coverage_matrix_v3.csv")
    route_counts = {
        "direct_llm_same_engine_rewrite": 6,
        "direct_llm_execute_repair_1shot": 2,
        "sqlglot_transpile_same_dialect_noop": 5,
        "sqlglot_optimize_same_dialect": 5,
        "calcite_hep_fail_closed_120": 6,
    }
    updated_t5: list[dict[str, Any]] = []
    for row in table5_rows:
        row = dict(row)
        route_id = row["route_id"]
        row["selected_pg_attribution_rows"] = str(route_counts.get(route_id, 0))
        if route_id in route_counts:
            row["plan_artifact_scope"] = row["plan_artifact_scope"] + f"; selected_pg_explain_analyze_buffers_{route_counts[route_id]}_rows"
            if route_id == "direct_llm_execute_repair_1shot":
                row["attribution_coverage"] = "selected_pg_packet_2_rows_only_for_newly_repaired_pg_rows; no_denominator_wide_attribution"
            else:
                row["attribution_coverage"] = f"selected_pg_packet_{route_counts[route_id]}_rows_with_node_level_plan_deltas; no_denominator_wide_attribution"
            row["observability_level"] = row["observability_level"] + "_plus_selected_pg_node_delta_packet"
            row["notes"] = row["notes"] + f" This route now has {route_counts[route_id]} reviewed PostgreSQL EXPLAIN ANALYZE BUFFERS attribution rows."
        else:
            row["selected_pg_attribution_rows"] = "0"
        updated_t5.append(row)
    table5_fields = list(updated_t5[0].keys())
    write_csv(FREEZE_DIR / "table5_observability_coverage_matrix_v4.csv", updated_t5, table5_fields)
    write_md(
        FREEZE_DIR / "table5_observability_coverage_matrix_v4.md",
        "Table 5 Observability Coverage Matrix V4",
        [
            "This route-level Table 5 keeps the v3 observability framing and adds selected PostgreSQL attribution coverage for the 5 main routes.",
            "This is still selected-case PG attribution, not full 120-row plan coverage.",
            "中文说明：新版本 Table 5 强化了 route 级 evidence，但依然不能声称 full-denominator plan attribution。",
        ],
        updated_t5,
        table5_fields,
    )

    # Table 10 v4
    delta_by_candidate = {row["candidate_id"]: row for row in delta_rows}
    route_to_rows: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in event_rows:
        route_to_rows[(row["method_id"], row["route_id"])].append(row)

    def pick_rep(rows: list[dict[str, Any]], bucket: str, mode: str) -> str:
        candidates_local = []
        for row in rows:
            if row["retained_speedup"] in {"", "NA_not_available"}:
                continue
            val = float(row["retained_speedup"])
            if bucket == "speedup" and val > 1.05:
                candidates_local.append((val, row["candidate_id"]))
            elif bucket == "regression" and val < 0.95:
                candidates_local.append((val, row["candidate_id"]))
            elif bucket == "neutral" and 0.95 <= val <= 1.05:
                candidates_local.append((abs(val - 1.0), row["candidate_id"]))
        if not candidates_local:
            return "NA_not_available"
        if bucket == "speedup":
            return max(candidates_local)[1]
        if bucket == "regression":
            return min(candidates_local)[1]
        return min(candidates_local)[1]

    def strongest_delta(rows: list[dict[str, Any]]) -> str:
        precedence = [
            "join_strategy_change",
            "scan_strategy_change",
            "aggregate_strategy_change",
            "sort_or_materialize_change",
            "node_count_change",
            "buffer_or_runtime_delta_without_operator_change",
            "no_major_plan_delta",
            "plan_extraction_failed",
        ]
        ranked = []
        for row in rows:
            delta = delta_by_candidate[row["candidate_id"]]["main_plan_delta_class"]
            conf = delta_by_candidate[row["candidate_id"]]["attribution_confidence"]
            ranked.append((0 if conf == "medium" else 1 if conf == "low" else 2, precedence.index(delta), row["candidate_id"], delta))
        ranked.sort()
        best = ranked[0]
        return f"{best[3]} via {best[2]}"

    table10_rows: list[dict[str, Any]] = []
    for (method_id, route_id), rows in sorted(route_to_rows.items()):
        parse_success = sum(r["plan_parse_success"] == "true" for r in rows)
        dist = Counter(delta_by_candidate[r["candidate_id"]]["attribution_confidence"] for r in rows)
        delta_dist = Counter(delta_by_candidate[r["candidate_id"]]["main_plan_delta_class"] for r in rows)
        table10_rows.append(
            {
                "method_or_route": MAIN_ROUTE_LABELS[route_id],
                "route_id": route_id,
                "selected_rows": str(len(rows)),
                "successful_source_plans": str(sum(r["source_plan_success"] == "true" for r in rows)),
                "successful_rewrite_plans": str(sum(r["rewrite_plan_success"] == "true" for r in rows)),
                "plan_parse_success_rate": normalize_float(parse_success / len(rows)),
                "main_delta_classes_observed": "|".join(f"{k}:{v}" for k, v in sorted(delta_dist.items())),
                "representative_speedup_case": pick_rep(rows, "speedup", "max"),
                "representative_regression_case": pick_rep(rows, "regression", "min"),
                "representative_neutral_case": pick_rep(rows, "neutral", "closest"),
                "strongest_observed_plan_delta": strongest_delta(rows),
                "attribution_confidence_distribution": "|".join(f"{k}:{v}" for k, v in sorted(dist.items())),
                "paper_safe_interpretation": "Selected PG EXPLAIN ANALYZE BUFFERS rows now show route-specific plan deltas beyond scalar speedup labels, but only for this reviewed subset.",
                "forbidden_overclaim": "Do not claim denominator-wide node alignment, global causal attribution, or that this packet replaces Table 6 timing.",
                "source_artifacts": f"reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/pg_plan_attribution_24_node_delta_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/pg_plan_attribution_24_feature_summary_v1.csv",
                "notes": "Failure diagnostic row remains separate from this exact-timed 24-row denominator.",
            }
        )
    write_csv(FREEZE_DIR / "table10_plan_attribution_case_study_v4.csv", table10_rows, list(table10_rows[0].keys()))
    write_md(
        FREEZE_DIR / "table10_plan_attribution_case_study_v4.md",
        "Table 10 Plan Attribution Case Study V4",
        [
            "This table aggregates the reviewed 24-row PostgreSQL EXPLAIN ANALYZE BUFFERS attribution packet by main method route.",
            "The previous failure diagnostic row remains separate; this table is only for the exact-timed selected PG attribution denominator.",
            "中文说明：这里是 24 行 selected PG attribution 的聚合，不代表 full-denominator causal attribution。",
        ],
        table10_rows,
        list(table10_rows[0].keys()),
    )

    gap_rows = [
        {
            "gap_id": "plan_attr_gap_01",
            "affected_table": "Table 5 v4",
            "current_status": "selected_pg_packet_added",
            "gap_description": "Main routes now have reviewed PG node-delta coverage on 24 exact-timed rows, but denominator-wide plan coverage is still unavailable.",
            "resolved_by_this_packet": "selected_pg_attribution_rows_for_5_main_routes",
            "remaining_gap": "no_full_denominator_plan_coverage",
            "requires_new_execution": "yes",
            "priority": "medium",
            "notes": "Future expansion would need a larger reviewed PG plan packet or separate engine-specific packets.",
        },
        {
            "gap_id": "plan_attr_gap_02",
            "affected_table": "Table 10 v4",
            "current_status": "selected_case_node_delta_strengthened",
            "gap_description": "Route-level plan deltas are now retained for 24 exact-timed PG rows.",
            "resolved_by_this_packet": "node_level_pg_explain_analyze_buffers_artifacts",
            "remaining_gap": "failure_diagnostic_row_still_separate",
            "requires_new_execution": "yes",
            "priority": "medium",
            "notes": "Failure observability should remain in the separate failure-side Table 10 lineage.",
        },
        {
            "gap_id": "plan_attr_gap_03",
            "affected_table": "Table 10 v4",
            "current_status": "still_selected_case_only",
            "gap_description": "Heuristic node alignment and attribution confidence are packet-local only.",
            "resolved_by_this_packet": "partial_only",
            "remaining_gap": "no_global_node_alignment_or_causal_attribution",
            "requires_new_execution": "yes",
            "priority": "high",
            "notes": "Do not overclaim beyond medium/low confidence for selected rows.",
        },
    ]
    write_csv(FREEZE_DIR / "plan_attribution_gap_summary_v2.csv", gap_rows, list(gap_rows[0].keys()))
    write_md(
        FREEZE_DIR / "plan_attribution_gap_summary_v2.md",
        "Plan Attribution Gap Summary V2",
        [
            "This gap summary records what the reviewed 24-row PG attribution packet resolved and what remains out of scope.",
            "中文说明：24 行 packet 已经增强 selected-case 归因，但 full-denominator attribution 仍然没有解决。",
        ],
        gap_rows,
        list(gap_rows[0].keys()),
    )

    readme_v7 = [
        "# Common-core v0 Paper Results Readme V7",
        "",
        "This version adds the reviewed 24-row PostgreSQL EXPLAIN ANALYZE BUFFERS attribution packet.",
        "",
        "- Table 5 v4 keeps the route-level observability framing and adds selected PG attribution coverage for the 5 main routes.",
        "- Table 10 v4 aggregates the 24-row PG packet into route-level plan-delta evidence.",
        "- This packet does not replace Table 6 timing and does not justify denominator-wide node alignment or global causal attribution.",
        "",
        "中文说明：v7 的核心增量是 24 行 PG 计划归因 packet。它增强了 selected-case observability，但仍然不是 full-denominator attribution benchmark。",
        "",
    ]
    (FREEZE_DIR / "common_core_v0_paper_results_readme_v7.md").write_text("\n".join(readme_v7), encoding="utf-8", newline="\n")

    return 0 if len(event_rows) == 24 else 1


if __name__ == "__main__":
    sys.exit(build_packet())
