#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
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
PACKET_ID = "pg_plan_attribution_113"
PLAN_READY_SOURCE = FREEZE_DIR / "tag_coverage_pg_attribution_ready_113_v1.csv"
CANDIDATE_POOL_SOURCE = FREEZE_DIR / "pg_plan_attribution_candidate_pool_v1.csv"
TABLE5_V5_SOURCE = FREEZE_DIR / "table5_observability_coverage_matrix_v5.csv"
TABLE10_FAILURE_SOURCE = FREEZE_DIR / "table10_failure_exemplar_selection_v1.csv"
RECOMMENDATION_SOURCE = FREEZE_DIR / "tag_aware_observability_recommendation_v1.md"

MAIN_ROUTES = [
    ("direct_llm", "direct_llm_same_engine_rewrite"),
    ("direct_llm", "direct_llm_execute_repair_1shot"),
    ("sqlglot", "sqlglot_transpile_same_dialect_noop"),
    ("sqlglot", "sqlglot_optimize_same_dialect"),
    ("calcite_hep", "calcite_hep_fail_closed_120"),
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
    "normalized_tags",
    "tag_families_present",
    "plan_parse_success",
    "feature_parse_success",
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
    "root_total_cost",
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
    normalized_tags: str
    tag_families_present: str
    tag_source: str
    raw_tags: str


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


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def normalize_case_path(value: str) -> str:
    return (
        value.replace("\\", "/")
        .replace("cases/Performance/", "cases/PERF/")
        .replace("cases/Consistency/", "cases/CONS/")
        .replace("cases/Portability/", "cases/PORT/")
        .replace("cases/Longtail/", "cases/LONGTAIL/")
    )


def repo_path(value: str) -> Path:
    return REPO_ROOT / normalize_case_path(value)


def relative_str(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


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


def schema_name(candidate_id: str) -> str:
    cleaned = re.sub(r"[^a-z0-9_]", "_", candidate_id.lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return f"attr113_{cleaned}"[:60]


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
    families_present = [
        family
        for family in ["scan", "join", "aggregate", "sort", "materialize", "other"]
        if family_counter.get(family, 0) > 0
    ]
    return {
        "plan_parse_success": True,
        "feature_parse_success": True,
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
        "root_total_cost": float(root.get("Total Cost", 0.0) or 0.0),
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


def outcome_bucket(speedup: str) -> str:
    if speedup in {"", "NA_not_exact_timed", "NA_not_available"}:
        return "unknown"
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
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isinf(value) or math.isnan(value):
            return ""
        return f"{value:.15f}".rstrip("0").rstrip(".")
    return str(value)


def classify_delta(
    source: dict[str, Any] | None,
    rewrite: dict[str, Any] | None,
    retained_speedup: str,
) -> tuple[dict[str, Any], str]:
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
            "node_delta_success": False,
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

    operator_changes = [scan_delta != "no_change", join_delta != "no_change", agg_delta != "no_change", sort_delta != "no_change"]
    change_count = sum(operator_changes)
    if change_count > 1:
        delta_class = "mixed_operator_change"
    elif scan_delta != "no_change":
        delta_class = "scan_strategy_change"
    elif join_delta != "no_change":
        delta_class = "join_strategy_change"
    elif agg_delta != "no_change":
        delta_class = "aggregate_strategy_change"
    elif sort_delta != "no_change":
        delta_class = "sort_or_limit_change"
    elif node_count_delta != 0:
        delta_class = "node_count_change"
    elif any(abs(x) > 0.000001 for x in [planning_delta, execution_delta, shared_read_delta, shared_hit_delta]):
        delta_class = "buffer_or_runtime_delta_without_operator_change"
    else:
        delta_class = "no_major_plan_delta"

    retained = None
    if retained_speedup not in {"", "NA_not_available", "NA_not_exact_timed"}:
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
        elif 0.95 <= retained <= 1.05 and abs(execution_delta) < max(1.0, abs(source["execution_time_ms"]) * 0.2):
            plausible_direction = True

    if delta_class == "plan_extraction_failed":
        confidence = "none"
    elif delta_class in {
        "scan_strategy_change",
        "join_strategy_change",
        "aggregate_strategy_change",
        "sort_or_limit_change",
        "node_count_change",
        "mixed_operator_change",
    } and plausible_direction:
        confidence = "medium"
    elif delta_class == "buffer_or_runtime_delta_without_operator_change" and (
        abs(execution_delta) > max(1.0, abs(source["execution_time_ms"]) * 0.5) or abs(shared_read_delta) > 10 or abs(shared_hit_delta) > 100
    ):
        confidence = "low"
    else:
        confidence = "low"

    interpretation_map = {
        "scan_strategy_change": "Source and rewrite use different scan operators or scan families; this is selected-case attribution evidence only.",
        "join_strategy_change": "Source and rewrite use different join operators; this gives selected-case attribution evidence when direction also matches runtime or buffer movement.",
        "aggregate_strategy_change": "Aggregate operator families differ across source and rewrite; this is selected-case attribution evidence only.",
        "sort_or_limit_change": "Sort or materialize behavior differs across source and rewrite; selected-case attribution only.",
        "node_count_change": "Major node count differs while operator families are similar; this suggests structural plan simplification or expansion for this row only.",
        "mixed_operator_change": "Multiple operator-family changes are visible at once; this is stronger selected-case evidence but still not denominator-wide attribution.",
        "buffer_or_runtime_delta_without_operator_change": "Operator families are similar but runtime or buffer counters differ; this is weak attribution evidence.",
        "no_major_plan_delta": "Plans look broadly similar at the retained feature level, so causal interpretation should stay cautious.",
    }
    interpretation = interpretation_map[delta_class]

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
        "node_delta_success": True,
    }, interpretation


def copy_artifact(src: Path, dst: Path) -> None:
    ensure_parent(dst)
    shutil.copyfile(src, dst)


def load_candidates() -> tuple[list[Candidate], list[dict[str, Any]]]:
    tag_rows = read_csv(PLAN_READY_SOURCE)
    pool_rows = read_csv(CANDIDATE_POOL_SOURCE)
    pool_by_id = {row["candidate_id"]: row for row in pool_rows}

    issues: list[dict[str, Any]] = []
    candidate_ids = [row["candidate_id"] for row in tag_rows]
    dup_ids = [cid for cid, count in Counter(candidate_ids).items() if count > 1]
    if dup_ids:
        issues.append({"candidate_id": "|".join(sorted(dup_ids)), "failure_category": "duplicate_candidate_id", "failure_detail": "duplicate IDs in tag_coverage_pg_attribution_ready_113_v1.csv"})

    selected: list[Candidate] = []
    for row in tag_rows:
        pool = pool_by_id.get(row["candidate_id"])
        if pool is None:
            issues.append({"candidate_id": row["candidate_id"], "failure_category": "candidate_missing_from_pool", "failure_detail": "candidate_id absent from pg_plan_attribution_candidate_pool_v1.csv"})
            continue
        if pool["plan_attribution_ready"].lower() != "true":
            issues.append({"candidate_id": row["candidate_id"], "failure_category": "candidate_not_ready_in_pool", "failure_detail": "candidate is not plan_attribution_ready=true in pool"})
            continue
        if pool["engine"] != "pg":
            issues.append({"candidate_id": row["candidate_id"], "failure_category": "non_pg_candidate", "failure_detail": f"engine={pool['engine']}"})
            continue
        selected.append(
            Candidate(
                candidate_id=pool["candidate_id"],
                case_id=pool["case_id"],
                pool=pool["pool"],
                engine=pool["engine"],
                method_id=pool["method_id"],
                route_id=pool["route_id"],
                outcome_type_hint=pool["outcome_type_hint"],
                retained_speedup=pool["retained_speedup"],
                timing_source_artifact=normalize_case_path(pool["timing_source_artifact"]),
                source_sql_artifact=normalize_case_path(pool["source_sql_artifact"]),
                rewrite_sql_artifact=normalize_case_path(pool["rewrite_sql_artifact"]),
                schema_artifact=normalize_case_path(pool["schema_artifact"]),
                witness_data_artifact=normalize_case_path(pool["witness_data_artifact"]),
                exact_evidence_artifact=normalize_case_path(pool["exact_evidence_artifact"]),
                plan_attribution_ready=pool["plan_attribution_ready"],
                blocking_reason=pool["blocking_reason"],
                recommended_priority=pool["recommended_priority"],
                recommended_role_for_table10=pool["recommended_role_for_table10"],
                notes=pool["notes"],
                normalized_tags=row["normalized_tags"],
                tag_families_present=row["tag_families_present"],
                tag_source=row["tag_source"],
                raw_tags=row["raw_tags"],
            )
        )
    return selected, issues


def verify_candidate_artifacts(candidates: list[Candidate]) -> list[dict[str, Any]]:
    missing: list[dict[str, Any]] = []
    for candidate in candidates:
        for field in [
            "source_sql_artifact",
            "rewrite_sql_artifact",
            "schema_artifact",
            "witness_data_artifact",
            "exact_evidence_artifact",
        ]:
            rel = getattr(candidate, field)
            path = repo_path(rel)
            if not path.exists():
                missing.append(
                    {
                        "candidate_id": candidate.candidate_id,
                        "failure_category": "missing_artifact",
                        "failure_detail": f"{field}={rel}",
                    }
                )
    return missing


def explain_sql(schema: str, query_relpath: str) -> str:
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


def log_excerpt(*paths: Path, limit: int = 1000) -> str:
    for path in paths:
        if path.exists():
            text = path.read_text(encoding="utf-8").strip()
            if text:
                return text[:limit]
    return ""


def route_key(candidate: Candidate | dict[str, Any]) -> tuple[str, str]:
    return candidate.method_id, candidate.route_id  # type: ignore[attr-defined]


def build_tag_frequency_rows(scope: str, rows: list[dict[str, Any]], key_fields: dict[str, str]) -> list[dict[str, Any]]:
    counter = Counter()
    unique_cases = set()
    for row in rows:
        unique_cases.add(row["case_id"])
        tags = [] if row["normalized_tags"] in {"", "NA_not_found"} else row["normalized_tags"].split("|")
        for tag in set(tags):
            counter[tag] += 1
    tag_count = len(counter)
    return [
        {
            "summary_scope": scope,
            **key_fields,
            "metric_type": "tag_frequency",
            "tag_or_family": tag,
            "count": count,
            "denominator": len(rows),
            "unique_case_count": len(unique_cases),
            "tag_count": tag_count,
            "notes": "",
        }
        for tag, count in sorted(counter.items())
    ]


def build_packet() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)

    candidates, preflight_issues = load_candidates()
    manifest_rows: list[dict[str, Any]] = []
    for order, candidate in enumerate(candidates, start=1):
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
                "normalized_tags": candidate.normalized_tags,
                "tag_families_present": candidate.tag_families_present,
                "selected_status": "selected_pg_ready_113",
                "notes": candidate.notes,
            }
        )
    manifest_fields = list(manifest_rows[0].keys()) if manifest_rows else []

    missing_artifacts = verify_candidate_artifacts(candidates)
    if preflight_issues or missing_artifacts or len(candidates) != 113:
        failure_rows = preflight_issues + missing_artifacts
        write_csv(RUN_DIR / "selected_candidate_manifest.csv", manifest_rows or [{"selected_order": "", "candidate_id": "", "case_id": "", "pool": "", "engine": "", "method_id": "", "route_id": "", "outcome_type_hint": "", "retained_speedup": "", "source_sql_artifact": "", "rewrite_sql_artifact": "", "schema_artifact": "", "witness_data_artifact": "", "exact_evidence_artifact": "", "timing_source_artifact": "", "normalized_tags": "", "tag_families_present": "", "selected_status": "", "notes": ""}], manifest_fields or ["selected_order","candidate_id","case_id","pool","engine","method_id","route_id","outcome_type_hint","retained_speedup","source_sql_artifact","rewrite_sql_artifact","schema_artifact","witness_data_artifact","exact_evidence_artifact","timing_source_artifact","normalized_tags","tag_families_present","selected_status","notes"])
        write_csv(
            RUN_DIR / "explain_analyze_failures.csv",
            failure_rows or [{"candidate_id": "", "failure_category": "", "failure_detail": ""}],
            ["candidate_id", "failure_category", "failure_detail"],
        )
        write_md(
            RUN_DIR / "README.md",
            "PG Plan Attribution 113 Packet",
            [
                "This run packet failed closed at preflight because at least one candidate was missing or duplicated.",
                "No candidate was silently dropped.",
                "中文说明：preflight 失败时直接 fail closed，不会偷偷删掉 rows。",
            ],
        )
        write_md(
            RUN_DIR / "pg_plan_attribution_113_policy_v1.md",
            "PG Plan Attribution 113 Policy V1",
            [
                "Retained denominator target: exactly 113 PostgreSQL attribution-ready rows.",
                "If any candidate artifact is missing, the packet must fail closed and retain a failure summary.",
            ],
        )
        json_dump(
            RUN_DIR / "run_results.json",
            {
                "packet_id": PACKET_ID,
                "status": "preflight_failed",
                "loaded_candidates": len(candidates),
                "expected_candidates": 113,
                "preflight_issues": failure_rows,
            },
        )
        json_dump(
            RUN_DIR / "validation_report.json",
            {
                "status": "preflight_failed",
                "loaded_candidates": len(candidates),
                "expected_candidates": 113,
                "preflight_issue_count": len(failure_rows),
            },
        )
        return 1

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
        source_sql_path.write_text(explain_sql(schema, candidate.source_sql_artifact), encoding="utf-8", newline="\n")
        rewrite_sql_path.write_text(explain_sql(schema, candidate.rewrite_sql_artifact), encoding="utf-8", newline="\n")

        command_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "case_id": candidate.case_id,
                "method_id": candidate.method_id,
                "route_id": candidate.route_id,
                "schema_name": schema,
                "statement_timeout": STATEMENT_TIMEOUT,
                "setup_sql": relative_str(setup_sql_path),
                "source_explain_sql": relative_str(source_sql_path),
                "rewrite_explain_sql": relative_str(rewrite_sql_path),
            }
        )

        setup_stdout = workspace / "setup.stdout.log"
        setup_stderr = workspace / "setup.stderr.log"
        setup_res = run_psql_file(setup_sql_path, setup_stdout, setup_stderr)

        source_plan_success = False
        rewrite_plan_success = False
        feature_parse_success = False
        source_summary: dict[str, Any] | None = None
        rewrite_summary: dict[str, Any] | None = None
        failure_category = ""
        failure_detail = ""

        source_stdout = workspace / "source_plan.stdout.json"
        source_stderr = workspace / "source_plan.stderr.log"
        rewrite_stdout = workspace / "rewrite_plan.stdout.json"
        rewrite_stderr = workspace / "rewrite_plan.stderr.log"
        source_plan_artifact = workspace / "source_plan.json"
        rewrite_plan_artifact = workspace / "rewrite_plan.json"
        cleanup_sql_path = workspace / "cleanup.sql"
        cleanup_sql_path.write_text(cleanup_sql(schema), encoding="utf-8", newline="\n")

        if setup_res.returncode != 0:
            failure_category = "schema_or_witness_load_failed"
            failure_detail = log_excerpt(setup_stderr, setup_stdout)
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
                    failure_category = "source_feature_parse_failed"
                    failure_detail = str(exc)
            else:
                failure_category = "source_explain_failed"
                failure_detail = log_excerpt(source_stderr, source_stdout)

            rewrite_res = run_psql_file(rewrite_sql_path, rewrite_stdout, rewrite_stderr)
            rewrite_plan_success = rewrite_res.returncode == 0
            if rewrite_plan_success:
                try:
                    rewrite_payload = extract_plan_payload(rewrite_stdout)
                    json_dump(rewrite_plan_artifact, rewrite_payload)
                    rewrite_summary = summarize_plan(rewrite_payload)
                except Exception as exc:  # noqa: BLE001
                    rewrite_plan_success = False
                    if not failure_category:
                        failure_category = "rewrite_feature_parse_failed"
                        failure_detail = str(exc)
            elif not failure_category:
                failure_category = "rewrite_explain_failed"
                failure_detail = log_excerpt(rewrite_stderr, rewrite_stdout)

        cleanup_stdout = workspace / "cleanup.stdout.log"
        cleanup_stderr = workspace / "cleanup.stderr.log"
        run_psql_file(cleanup_sql_path, cleanup_stdout, cleanup_stderr)

        feature_parse_success = bool(source_summary and rewrite_summary)
        delta_payload, interpretation = classify_delta(source_summary, rewrite_summary, candidate.retained_speedup)
        if not failure_category and delta_payload["main_plan_delta_class"] == "plan_extraction_failed":
            failure_category = "plan_extraction_failed"
            failure_detail = "source or rewrite plan was not available for delta analysis"

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
                    "plan_artifact": relative_str(source_plan_artifact),
                    "normalized_tags": candidate.normalized_tags,
                    "tag_families_present": candidate.tag_families_present,
                }
            )
            feature_rows.append({k: normalize_float(feature_payload.get(k, "")) for k in FEATURE_FIELDS})
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
                    "plan_artifact": relative_str(rewrite_plan_artifact),
                    "normalized_tags": candidate.normalized_tags,
                    "tag_families_present": candidate.tag_families_present,
                }
            )
            feature_rows.append({k: normalize_float(feature_payload.get(k, "")) for k in FEATURE_FIELDS})
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
            "normalized_tags": candidate.normalized_tags,
            "tag_families_present": candidate.tag_families_present,
            **delta_payload,
            "paper_safe_interpretation": interpretation,
            "forbidden_overclaim": "Do not claim denominator-wide plan attribution cross-engine attribution or global causal attribution from this PG-only frontier.",
            "evidence_artifacts": "|".join(
                filter(
                    None,
                    [
                        relative_str(source_plan_artifact) if source_plan_artifact.exists() else "",
                        relative_str(rewrite_plan_artifact) if rewrite_plan_artifact.exists() else "",
                        candidate.timing_source_artifact,
                    ],
                )
            ),
            "notes": "pg_only_explain_analyze_buffers_frontier_113",
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
                "normalized_tags": candidate.normalized_tags,
                "tag_families_present": candidate.tag_families_present,
                "source_plan_attempted": "true",
                "source_plan_success": str(source_plan_success).lower(),
                "rewrite_plan_attempted": "true",
                "rewrite_plan_success": str(rewrite_plan_success).lower(),
                "feature_parse_success": str(feature_parse_success).lower(),
                "node_delta_success": str(delta_payload["node_delta_success"]).lower(),
                "source_plan_artifact": relative_str(source_plan_artifact) if source_plan_artifact.exists() else "",
                "rewrite_plan_artifact": relative_str(rewrite_plan_artifact) if rewrite_plan_artifact.exists() else "",
                "source_sql_artifact": candidate.source_sql_artifact,
                "rewrite_sql_artifact": candidate.rewrite_sql_artifact,
                "schema_artifact": candidate.schema_artifact,
                "witness_data_artifact": candidate.witness_data_artifact,
                "exact_evidence_artifact": candidate.exact_evidence_artifact,
                "main_plan_delta_class": delta_payload["main_plan_delta_class"],
                "attribution_confidence": delta_payload["attribution_confidence"],
                "failure_category": failure_category,
                "failure_detail": failure_detail,
                "notes": "pg_only_explain_analyze_buffers_frontier_113",
            }
        )

        result_manifest_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "workspace": relative_str(workspace),
                "setup_stdout": relative_str(setup_stdout),
                "setup_stderr": relative_str(setup_stderr),
                "source_stdout": relative_str(source_stdout),
                "source_stderr": relative_str(source_stderr),
                "rewrite_stdout": relative_str(rewrite_stdout),
                "rewrite_stderr": relative_str(rewrite_stderr),
                "source_plan_artifact": relative_str(source_plan_artifact) if source_plan_artifact.exists() else "",
                "rewrite_plan_artifact": relative_str(rewrite_plan_artifact) if rewrite_plan_artifact.exists() else "",
            }
        )

        if failure_category:
            failure_rows.append(
                {
                    "candidate_id": candidate.candidate_id,
                    "case_id": candidate.case_id,
                    "pool": candidate.pool,
                    "method_id": candidate.method_id,
                    "route_id": candidate.route_id,
                    "failure_category": failure_category,
                    "failure_detail": failure_detail,
                    "setup_stderr": relative_str(setup_stderr),
                    "source_stderr": relative_str(source_stderr),
                    "rewrite_stderr": relative_str(rewrite_stderr),
                }
            )

    # Core run outputs.
    write_csv(RUN_DIR / "selected_candidate_manifest.csv", manifest_rows, manifest_fields)
    write_csv(RUN_DIR / "explain_analyze_command_matrix.csv", command_rows, list(command_rows[0].keys()))
    write_csv(RUN_DIR / "explain_analyze_event_long.csv", event_rows, list(event_rows[0].keys()))
    write_csv(
        RUN_DIR / "explain_analyze_failures.csv",
        failure_rows,
        ["candidate_id", "case_id", "pool", "method_id", "route_id", "failure_category", "failure_detail", "setup_stderr", "source_stderr", "rewrite_stderr"],
    )
    write_csv(RUN_DIR / "pg_plan_feature_summary.csv", feature_rows or [{field: "" for field in FEATURE_FIELDS}], FEATURE_FIELDS)
    write_csv(RUN_DIR / "pg_plan_node_delta.csv", delta_rows, list(delta_rows[0].keys()))

    # Summary tables.
    delta_counter = Counter(row["main_plan_delta_class"] for row in event_rows)
    conf_counter = Counter(row["attribution_confidence"] for row in event_rows)
    summary_rows: list[dict[str, Any]] = []

    def add_summary_row(summary_scope: str, summary_name: str, rows: list[dict[str, Any]]) -> None:
        summary_rows.append(
            {
                "summary_scope": summary_scope,
                "summary_name": summary_name,
                "planned_candidates": len(rows),
                "source_plan_success": sum(row["source_plan_success"] == "true" for row in rows),
                "rewrite_plan_success": sum(row["rewrite_plan_success"] == "true" for row in rows),
                "both_plan_success": sum(row["source_plan_success"] == "true" and row["rewrite_plan_success"] == "true" for row in rows),
                "feature_parse_success": sum(row["feature_parse_success"] == "true" for row in rows),
                "node_delta_success": sum(row["node_delta_success"] == "true" for row in rows),
                "failed_candidates": sum(bool(row["failure_category"]) for row in rows),
                "delta_class_distribution": "|".join(f"{name}:{count}" for name, count in sorted(Counter(row["main_plan_delta_class"] for row in rows).items())),
                "attribution_confidence_distribution": "|".join(f"{name}:{count}" for name, count in sorted(Counter(row["attribution_confidence"] for row in rows).items())),
                "tag_coverage_count": len({tag for row in rows for tag in ([] if row["normalized_tags"] in {"", "NA_not_found"} else row["normalized_tags"].split("|"))}),
                "notes": "",
            }
        )

    add_summary_row("overall", PACKET_ID, event_rows)
    route_groups = defaultdict(list)
    pool_groups = defaultdict(list)
    for row in event_rows:
        route_groups[(row["method_id"], row["route_id"])].append(row)
        pool_groups[row["pool"]].append(row)
    for (method_id, route_id), rows in sorted(route_groups.items()):
        add_summary_row("route", f"{method_id} / {route_id}", rows)
    for pool, rows in sorted(pool_groups.items()):
        add_summary_row("pool", pool, rows)
    write_csv(RUN_DIR / "pg_plan_attribution_summary.csv", summary_rows, list(summary_rows[0].keys()))

    # Tag coverage summaries.
    tag_summary_rows: list[dict[str, Any]] = []
    tag_summary_rows.append(
        {
            "summary_scope": "overall",
            "summary_name": PACKET_ID,
            "planned_candidates": len(event_rows),
            "both_plan_success": sum(row["source_plan_success"] == "true" and row["rewrite_plan_success"] == "true" for row in event_rows),
            "tagged_candidates": sum(row["normalized_tags"] not in {"", "NA_not_found"} for row in event_rows),
            "tag_count": len({tag for row in event_rows for tag in ([] if row["normalized_tags"] in {"", "NA_not_found"} else row["normalized_tags"].split("|"))}),
            "tag_families_present": "|".join(sorted({tag.split(":", 1)[0] for row in event_rows for tag in ([] if row["normalized_tags"] in {"", "NA_not_found"} else row["normalized_tags"].split("|"))})),
            "missing_tags_after_execution": "none_within_executed_frontier" if not failure_rows else "possible_if_failed_rows_carry_unique_tags",
            "notes": "overall frontier tag coverage summary",
        }
    )
    for pool, rows in sorted(pool_groups.items()):
        tags = {tag for row in rows for tag in ([] if row["normalized_tags"] in {"", "NA_not_found"} else row["normalized_tags"].split("|"))}
        tag_summary_rows.append(
            {
                "summary_scope": "pool",
                "summary_name": pool,
                "planned_candidates": len(rows),
                "both_plan_success": sum(row["source_plan_success"] == "true" and row["rewrite_plan_success"] == "true" for row in rows),
                "tagged_candidates": sum(row["normalized_tags"] not in {"", "NA_not_found"} for row in rows),
                "tag_count": len(tags),
                "tag_families_present": "|".join(sorted({tag.split(":", 1)[0] for tag in tags})),
                "missing_tags_after_execution": "none_within_pool_frontier" if all(row["source_plan_success"] == "true" and row["rewrite_plan_success"] == "true" for row in rows) else "see_failures",
                "notes": "",
            }
        )
    write_csv(RUN_DIR / "pg_plan_tag_coverage_summary.csv", tag_summary_rows, list(tag_summary_rows[0].keys()))

    route_tag_rows: list[dict[str, Any]] = []
    selected24_rows = read_csv(FREEZE_DIR / "pg_plan_attribution_24_manifest_v1.csv")
    selected24_route_tags: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in selected24_rows:
        tags = [] if row.get("normalized_tags", "") in {"", "NA_not_found"} else row["normalized_tags"].split("|")
        if not tags:
            # older manifest does not carry tags; recover from ready source by candidate or case.
            for candidate in candidates:
                if candidate.candidate_id == row["candidate_id"]:
                    tags = [] if candidate.normalized_tags in {"", "NA_not_found"} else candidate.normalized_tags.split("|")
                    break
        selected24_route_tags[(row["method_id"], row["route_id"])].update(tags)

    global_missing_from_24 = set()
    # Reconstruct using common-core tag audit output if present.
    common_core_tag_rows = read_csv(FREEZE_DIR / "tag_coverage_common_core40_v1.csv")
    pg24_tag_rows = read_csv(FREEZE_DIR / "tag_coverage_pg_attribution_24_v1.csv")
    cc_tag_set = {tag for row in common_core_tag_rows for tag in ([] if row["normalized_tags"] in {"", "NA_not_found"} else row["normalized_tags"].split("|"))}
    pg24_tag_set = {tag for row in pg24_tag_rows for tag in ([] if row["normalized_tags"] in {"", "NA_not_found"} else row["normalized_tags"].split("|"))}
    global_missing_from_24 = cc_tag_set - pg24_tag_set

    for (method_id, route_id), rows in sorted(route_groups.items()):
        ready_tags = {tag for row in rows for tag in ([] if row["normalized_tags"] in {"", "NA_not_found"} else row["normalized_tags"].split("|"))}
        observed_tags = {tag for row in rows if row["source_plan_success"] == "true" and row["rewrite_plan_success"] == "true" for tag in ([] if row["normalized_tags"] in {"", "NA_not_found"} else row["normalized_tags"].split("|"))}
        route_tag_rows.append(
            {
                "method_id": method_id,
                "route_id": route_id,
                "planned_candidates": len(rows),
                "both_plan_success": sum(row["source_plan_success"] == "true" and row["rewrite_plan_success"] == "true" for row in rows),
                "ready_tag_count": len(ready_tags),
                "observed_tag_count_after_success": len(observed_tags),
                "recovered_common_core_missing_tags": "|".join(sorted(observed_tags & global_missing_from_24)) or "none",
                "missing_tag_after_execution": "|".join(sorted(ready_tags - observed_tags)) or "none",
                "delta_class_distribution": "|".join(f"{name}:{count}" for name, count in sorted(Counter(row["main_plan_delta_class"] for row in rows).items())),
                "attribution_confidence_distribution": "|".join(f"{name}:{count}" for name, count in sorted(Counter(row["attribution_confidence"] for row in rows).items())),
                "notes": "",
            }
        )
    write_csv(RUN_DIR / "pg_plan_route_tag_coverage_summary.csv", route_tag_rows, list(route_tag_rows[0].keys()))

    # Table 5 preview.
    table5_v5_rows = read_csv(TABLE5_V5_SOURCE)
    selected_pg_counts = {
        ("direct_llm", "direct_llm_same_engine_rewrite"): 6,
        ("direct_llm", "direct_llm_execute_repair_1shot"): 2,
        ("sqlglot", "sqlglot_transpile_same_dialect_noop"): 5,
        ("sqlglot", "sqlglot_optimize_same_dialect"): 5,
        ("calcite_hep", "calcite_hep_fail_closed_120"): 6,
    }
    preview_rows: list[dict[str, Any]] = []
    for method_id, route_id in MAIN_ROUTES:
        event_subset = route_groups[(method_id, route_id)]
        route_summary = next(row for row in route_tag_rows if row["method_id"] == method_id and row["route_id"] == route_id)
        preview_rows.append(
            {
                "method_id": method_id,
                "route_id": route_id,
                "planned_same_engine_pg_rows": 40,
                "pg_attribution_ready_rows": len(event_subset),
                "pg_attribution_executed_rows": len(event_subset),
                "source_plan_success_rows": sum(row["source_plan_success"] == "true" for row in event_subset),
                "rewrite_plan_success_rows": sum(row["rewrite_plan_success"] == "true" for row in event_subset),
                "parsed_plan_rows": sum(row["feature_parse_success"] == "true" for row in event_subset),
                "ready_tag_count": route_summary["ready_tag_count"],
                "observed_tag_count_after_execution": route_summary["observed_tag_count_after_success"],
                "recovered_common_core_missing_tags": route_summary["recovered_common_core_missing_tags"],
                "remaining_tag_gaps": route_summary["missing_tag_after_execution"],
                "delta_class_summary": route_summary["delta_class_distribution"],
                "attribution_confidence_summary": route_summary["attribution_confidence_distribution"],
                "paper_safe_use": "selected_pg_attribution_frontier_and_tag_coverage_only_not_denominator_wide_plan_attribution",
            }
        )

    # Table 10 candidate selection after 113.
    delta_by_id = {row["candidate_id"]: row for row in delta_rows}
    successful_candidates = [row for row in delta_rows if row["main_plan_delta_class"] != "plan_extraction_failed"]

    def score_row(row: dict[str, Any]) -> tuple[int, float, float]:
        conf_order = {"none": 0, "low": 1, "medium": 2, "high": 3}
        exec_delta = abs(float(row["execution_time_delta_ms"] or 0.0))
        blk_delta = abs(float(row["shared_blks_read_delta"] or 0.0)) + abs(float(row["shared_blks_hit_delta"] or 0.0))
        return conf_order.get(row["attribution_confidence"], 0), exec_delta, blk_delta

    def choose_best(predicate) -> dict[str, Any] | None:
        matches = [row for row in successful_candidates if predicate(row)]
        if not matches:
            return None
        return sorted(matches, key=score_row, reverse=True)[0]

    table10_candidates: list[dict[str, Any]] = []
    used_ids: set[str] = set()

    def append_candidate(row: dict[str, Any] | None, why: str, tag_value: str) -> None:
        if row is None or row["candidate_id"] in used_ids:
            return
        used_ids.add(row["candidate_id"])
        table10_candidates.append(
            {
                "candidate_id": row["candidate_id"],
                "case_id": row["case_id"],
                "pool": row["pool"],
                "method_id": row["method_id"],
                "route_id": row["route_id"],
                "outcome_type_hint": row["outcome_type_hint"],
                "main_delta_class": row["main_plan_delta_class"],
                "attribution_confidence": row["attribution_confidence"],
                "retained_speedup": row["retained_speedup"],
                "normalized_tags": row["normalized_tags"],
                "tag_diagnostic_value": tag_value,
                "why_selected": why,
                "paper_safe_interpretation": row["paper_safe_interpretation"],
                "forbidden_overclaim": "Do not claim denominator-wide or global causal attribution from this candidate.",
            }
        )

    append_candidate(choose_best(lambda r: r["main_plan_delta_class"] == "join_strategy_change"), "strongest_join_strategy_change_case", "join_strategy_change")
    append_candidate(choose_best(lambda r: r["main_plan_delta_class"] == "scan_strategy_change"), "strongest_scan_strategy_change_case", "scan_strategy_change")
    append_candidate(choose_best(lambda r: r["main_plan_delta_class"] == "node_count_change"), "strongest_node_count_change_case", "node_count_change")
    append_candidate(choose_best(lambda r: r["main_plan_delta_class"] == "buffer_or_runtime_delta_without_operator_change"), "strongest_buffer_runtime_only_case", "buffer_or_runtime_delta_without_operator_change")
    append_candidate(choose_best(lambda r: "portability:" in r["normalized_tags"]), "strongest_portability_tag_diagnostic_case", "portability_tag_diagnostic")
    append_candidate(choose_best(lambda r: "sql_feature:primary:subquery_in_from" in r["normalized_tags"]), "strongest_subquery_in_from_diagnostic_case", "subquery_in_from_diagnostic")

    failure_exemplar_rows = [row for row in read_csv(TABLE10_FAILURE_SOURCE) if row["selected"].lower() == "true"]
    if failure_exemplar_rows:
        failure = failure_exemplar_rows[0]
        table10_candidates.append(
            {
                "candidate_id": f"{failure['method_id']}__{failure['route_id']}__{failure['case_id']}__{failure['engine']}__failure",
                "case_id": failure["case_id"],
                "pool": failure["pool"],
                "method_id": failure["method_id"],
                "route_id": failure["route_id"],
                "outcome_type_hint": "failure_diagnostic",
                "main_delta_class": "failure_diagnostic",
                "attribution_confidence": "none",
                "retained_speedup": "NA_failure_only",
                "normalized_tags": next((c.normalized_tags for c in candidates if c.case_id == failure["case_id"]), "NA_not_found"),
                "tag_diagnostic_value": "failure_diagnostic",
                "why_selected": "strongest_failure_side_diagnostic_remains_separate",
                "paper_safe_interpretation": "Keep the failure-side diagnostic separate from exact-timed attribution rows.",
                "forbidden_overclaim": "Do not merge this failure exemplar into the 113-row exact-timed attribution denominator.",
            }
        )

    # Gap summary.
    absent_after_113_rows = read_csv(FREEZE_DIR / "tag_coverage_gap_summary_v1.csv")
    absent_tags = next((row["affected_tags"] for row in absent_after_113_rows if row["gap_id"] == "tag_gap_04"), "unknown")
    gap_rows = [
        {
            "gap_id": "attr113_gap_01",
            "scope_name": "pg_only_frontier_scope",
            "current_status": "resolved_for_pg_ready_113_frontier_only",
            "remaining_gap": "not_full_120_and_not_cross_engine",
            "requires_new_execution": "yes",
            "priority": "medium",
            "notes": "This packet is PG-only and frontier-based, not denominator-wide or cross-engine attribution.",
        },
        {
            "gap_id": "attr113_gap_02",
            "scope_name": "global_causal_attribution",
            "current_status": "still_unresolved",
            "remaining_gap": "no_denominator_wide_causal_attribution",
            "requires_new_execution": "yes",
            "priority": "high",
            "notes": "Even with 113 rows, attribution remains PG-only and selected-frontier evidence.",
        },
        {
            "gap_id": "attr113_gap_03",
            "scope_name": "remaining_tag_absence",
            "current_status": "still_visible_after_113",
            "remaining_gap": absent_tags,
            "requires_new_execution": "yes",
            "priority": "medium",
            "notes": "The boolean_semantics_gap slice remains absent after the 113-row PG-ready frontier.",
        },
    ]

    # Run packet docs.
    write_md(
        RUN_DIR / "README.md",
        "PG Plan Attribution 113 Packet",
        [
            "This run packet collects PostgreSQL-only EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) artifacts for the full retained 113-row PG attribution-ready frontier.",
            "It is not a generation run, checker run, timing rerun, verifier task, or cross-engine packet.",
            "中文说明：这个 packet 只扩展 PG attribution frontier，不替代 Table 6 timing，也不支持 full-denominator causal attribution。",
        ],
    )
    write_md(
        RUN_DIR / "pg_plan_attribution_113_policy_v1.md",
        "PG Plan Attribution 113 Policy V1",
        [
            "Retained denominator: exactly 113 PostgreSQL attribution-ready candidates from the freeze folder.",
            f"Plan command: `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` with `statement_timeout={STATEMENT_TIMEOUT}` inside a read-only transaction when possible.",
            "Candidates are never silently dropped. Failures remain in the denominator and are recorded explicitly.",
            "Attribution is conservative and remains `none`, `low`, `medium`, or `high`, although this packet uses no stronger than retained evidence supports.",
            "中文说明：这里的目标是 route x frontier x tag coverage，不是 full 120 plan attribution，也不是 global causal attribution。",
        ],
    )

    overall_summary = summary_rows[0]
    json_dump(
        RUN_DIR / "run_results.json",
        {
            "packet_id": PACKET_ID,
            "planned_candidates": len(candidates),
            "loaded_candidates": len(candidates),
            "source_plan_success_count": int(overall_summary["source_plan_success"]),
            "rewrite_plan_success_count": int(overall_summary["rewrite_plan_success"]),
            "both_plan_success_count": int(overall_summary["both_plan_success"]),
            "feature_parse_success_count": int(overall_summary["feature_parse_success"]),
            "node_delta_success_count": int(overall_summary["node_delta_success"]),
            "delta_class_distribution": dict(delta_counter),
            "attribution_confidence_distribution": dict(conf_counter),
            "failed_candidates": failure_rows,
        },
    )
    json_dump(
        RUN_DIR / "validation_report.json",
        {
            "status": "ok" if len(candidates) == 113 else "warning",
            "expected_candidates": 113,
            "loaded_candidates": len(candidates),
            "event_rows": len(event_rows),
            "failure_rows": len(failure_rows),
            "source_plan_success_count": int(overall_summary["source_plan_success"]),
            "rewrite_plan_success_count": int(overall_summary["rewrite_plan_success"]),
            "both_plan_success_count": int(overall_summary["both_plan_success"]),
            "feature_parse_success_count": int(overall_summary["feature_parse_success"]),
            "node_delta_success_count": int(overall_summary["node_delta_success"]),
        },
    )

    # Freeze CSV copies.
    freeze_map = {
        "selected_candidate_manifest.csv": "pg_plan_attribution_113_manifest_v1.csv",
        "explain_analyze_event_long.csv": "pg_plan_attribution_113_event_long_v1.csv",
        "pg_plan_feature_summary.csv": "pg_plan_attribution_113_feature_summary_v1.csv",
        "pg_plan_node_delta.csv": "pg_plan_attribution_113_node_delta_v1.csv",
        "pg_plan_attribution_summary.csv": "pg_plan_attribution_113_summary_v1.csv",
        "pg_plan_tag_coverage_summary.csv": "pg_plan_attribution_113_tag_coverage_summary_v1.csv",
        "pg_plan_route_tag_coverage_summary.csv": "pg_plan_attribution_113_route_tag_coverage_summary_v1.csv",
    }
    for src_name, dst_name in freeze_map.items():
        shutil.copyfile(RUN_DIR / src_name, FREEZE_DIR / dst_name)

    for csv_name, title, intro in [
        ("pg_plan_attribution_113_manifest_v1.csv", "PG Plan Attribution 113 Manifest V1", [
            "This file lists the full retained 113-row PostgreSQL attribution-ready frontier and its artifact paths.",
            "中文说明：这是 113 行 PG frontier 清单，不代表 full 120 或 cross-engine attribution。",
        ]),
        ("pg_plan_attribution_113_event_long_v1.csv", "PG Plan Attribution 113 Event Long V1", [
            "This file records per-candidate source and rewrite PostgreSQL plan extraction success or failure.",
            "中文说明：失败 rows 保持在分母里，不会被静默丢弃。",
        ]),
        ("pg_plan_attribution_113_feature_summary_v1.csv", "PG Plan Attribution 113 Feature Summary V1", [
            "This file summarizes extracted PostgreSQL JSON plan features for the 113-row frontier.",
            "中文说明：这些特征只支持 PG frontier observability，不支持 full-denominator causal attribution。",
        ]),
        ("pg_plan_attribution_113_node_delta_v1.csv", "PG Plan Attribution 113 Node Delta V1", [
            "This file contains conservative node-level deltas and attribution confidence labels for the 113-row frontier.",
            "中文说明：delta class 是保守分类，不等于全局因果解释。",
        ]),
        ("pg_plan_attribution_113_summary_v1.csv", "PG Plan Attribution 113 Summary V1", [
            "This file summarizes the 113-row PG frontier overall, by route, and by pool.",
            "中文说明：这是 frontier packet 汇总，不是最终 paper leaderboard。",
        ]),
        ("pg_plan_attribution_113_tag_coverage_summary_v1.csv", "PG Plan Attribution 113 Tag Coverage Summary V1", [
            "This file summarizes tag coverage after executing the 113-row PG frontier.",
            "中文说明：tag coverage 只是 PG frontier 的 retained scope，不是 full common-core attribution completion。",
        ]),
        ("pg_plan_attribution_113_route_tag_coverage_summary_v1.csv", "PG Plan Attribution 113 Route Tag Coverage Summary V1", [
            "This file summarizes route x tag coverage after executing the 113-row PG frontier.",
            "中文说明：后续 Table 5 v6 PREVIEW 应以这个 route x frontier x tag coverage 层为基础。",
        ]),
    ]:
        rows = read_csv(FREEZE_DIR / csv_name)
        write_md(FREEZE_DIR / csv_name.replace(".csv", ".md"), title, intro, rows, list(rows[0].keys()))

    write_csv(FREEZE_DIR / "table5_observability_coverage_matrix_v6_PREVIEW.csv", preview_rows, list(preview_rows[0].keys()))
    write_md(
        FREEZE_DIR / "table5_observability_coverage_matrix_v6_PREVIEW.md",
        "Table 5 Observability Coverage Matrix V6 Preview",
        [
            "This preview redesigns Table 5 around route x PG attribution frontier x tag coverage.",
            "It is preview-only and keeps denominator-wide plan attribution out of scope.",
            "中文说明：这是 Table 5 预览稿，只是为了评估 route x frontier x tag coverage 是否足够清晰。",
        ],
        preview_rows,
        list(preview_rows[0].keys()),
    )

    write_csv(
        FREEZE_DIR / "table10_tag_aware_case_selection_candidates_after_113_v1.csv",
        table10_candidates,
        list(table10_candidates[0].keys()),
    )
    write_md(
        FREEZE_DIR / "table10_tag_aware_case_selection_candidates_after_113_v1.md",
        "Table 10 Tag-aware Case Selection Candidates After 113 V1",
        [
            "This file recommends candidate cases for a later tag-aware Table 10 redesign after the 113-row PG frontier packet.",
            "The failure-side diagnostic remains separate from exact-timed attribution rows.",
            "中文说明：这里是 Table 10 候选诊断行，不是最终 Table 10 定稿。",
        ],
        table10_candidates,
        list(table10_candidates[0].keys()),
    )

    write_csv(FREEZE_DIR / "plan_attribution_113_gap_summary_v1.csv", gap_rows, list(gap_rows[0].keys()))
    write_md(
        FREEZE_DIR / "plan_attribution_113_gap_summary_v1.md",
        "Plan Attribution 113 Gap Summary V1",
        [
            "This file records what the 113-row PG frontier resolves and what still remains out of scope.",
            "中文说明：113 行 PG frontier 虽然大幅扩展了 tag-aware observability，但仍然不是 full-denominator 或 global causal attribution。",
        ],
        gap_rows,
        list(gap_rows[0].keys()),
    )

    readme_lines = [
        "# Common-core v0 Paper Results Readme V9 Preview",
        "",
        "This preview layer adds the full retained 113-row PostgreSQL attribution-ready frontier packet.",
        "",
        "- `Table 5 v6 PREVIEW` reorganizes observability around route x PG attribution frontier x tag coverage.",
        "- `Table 10` is not refreshed yet, but candidate recommendations after the 113-row packet are retained.",
        "- This remains PG-only attribution evidence.",
        "- This does not create denominator-wide plan attribution, cross-engine attribution, or global causal attribution.",
        f"- Remaining absent tag after 113: `{absent_tags}`.",
        "",
        "中文说明：v9 preview 的核心增量是 113 行 PG attribution frontier。它的价值在于 route x tag coverage，而不是把 observability 夸大成 full-denominator causal attribution。",
        "",
    ]
    (FREEZE_DIR / "common_core_v0_paper_results_readme_v9_PREVIEW.md").write_text(
        "\n".join(readme_lines), encoding="utf-8", newline="\n"
    )

    return 0


def main() -> int:
    return build_packet()


if __name__ == "__main__":
    sys.exit(main())
