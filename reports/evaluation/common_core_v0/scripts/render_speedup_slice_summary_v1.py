#!/usr/bin/env python3
"""Regenerate Common-core v0 speedup slice summary from retained artifacts.

This is a static aggregation script. It reads retained timing artifacts only and
does not run database engines, LLM/model calls, verifier tools, PORT9, EXPLAIN,
or timing collection.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = REPO_ROOT / "reports/evaluation/common_core_v0"
OUT_DIR = BASE / "19_SPEEDUP_SUMMARY_REGENERATION_V1"

TABLE6 = BASE / "00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv"
CANONICAL_CASE_LEVEL = BASE / "11_TIMING_OBSERVABILITY_V1/method_timing_case_level_v1.csv"
RETAINED_TARGET = BASE / "11_TIMING_OBSERVABILITY_V1/speedup_slice_summary_v1.csv"

RAW_TIMING_INPUTS = [
    BASE / "runs/direct_llm_same_engine_timing_resolved_01/timing_event_long.csv",
    BASE / "runs/sqlglot_full_per_case_timing_01/timing_event_long.csv",
    BASE / "runs/calcite_hep_93_exact_timing_01/timing_event_long.csv",
    BASE / "runs/direct_llm_execute_repair_1shot_01/repair_timing_event_long.csv",
    BASE / "runs/r_bot_pg15_timing_expansion_02/run_results.json",
]

OUTPUT_SUMMARY = OUT_DIR / "speedup_slice_summary_regenerated_v1.csv"
OUTPUT_DIFF = OUT_DIR / "speedup_slice_summary_regeneration_diff_v1.csv"
OUTPUT_README = OUT_DIR / "speedup_slice_summary_regeneration_readme_v1.md"

WIN_THRESHOLD = 1.05
LOSS_THRESHOLD = 0.95
REGRESSION_20_THRESHOLD = 0.8
FLOAT_TOLERANCE = 1e-9

SUMMARY_COLUMNS = [
    "method_id",
    "route_id",
    "track",
    "engine_scope",
    "denominator_id",
    "timing_denominator",
    "gm_speedup",
    "median_speedup",
    "win_count",
    "tie_count",
    "loss_count",
    "regression_rate_20pct",
    "best_case",
    "worst_case",
    "source_artifact",
    "claim_boundary",
    "notes",
]

DIFF_COLUMNS = [
    "method_id",
    "route_id",
    "column_name",
    "regenerated_value",
    "retained_value",
    "comparison_status",
    "difference",
    "notes",
]


@dataclass(frozen=True)
class RouteSpec:
    method_id: str
    route_id: str
    recompute_mode: str
    note: str


ROUTES = [
    RouteSpec(
        "direct_llm",
        "direct_llm_same_engine_rewrite",
        "per_case",
        "Recomputed from retained canonical case-level exact + timing-success rows.",
    ),
    RouteSpec(
        "direct_llm",
        "direct_llm_execute_repair_1shot",
        "artifact_only",
        "Artifact-only: full 96-row mixed-source timing summary is retained, but only two repair-specific lower-level timing rows are retained.",
    ),
    RouteSpec(
        "sqlglot",
        "sqlglot_optimize_same_dialect",
        "per_case",
        "Recomputed from retained canonical case-level exact63 rows.",
    ),
    RouteSpec(
        "sqlglot",
        "sqlglot_transpile_same_dialect_noop",
        "per_case",
        "Recomputed from retained canonical case-level exact72 rows.",
    ),
    RouteSpec(
        "calcite_hep",
        "calcite_hep_fail_closed_120",
        "per_case",
        "Recomputed from retained canonical case-level 93 exact-row timing packet.",
    ),
    RouteSpec(
        "r_bot",
        "r_bot_same_engine_rewrite",
        "artifact_only",
        "Artifact-only: retained PG15 JSON is bounded appendix evidence and is not the canonical current benchmark metric evidence row.",
    ),
    RouteSpec(
        "sqlglot",
        "sqlglot_combined_same_engine_240",
        "artifact_only",
        "Artifact-only: diagnostic aggregate route-family view, not a single method route.",
    ),
]


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def require_inputs() -> None:
    required = [TABLE6, CANONICAL_CASE_LEVEL, RETAINED_TARGET, *RAW_TIMING_INPUTS]
    missing = [rel(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit("missing retained input artifact(s): " + ", ".join(missing))


def numeric(value: str) -> float | None:
    if value in {"", "NA", "NA_not_retained", "needs_per_case_timing_aggregation"}:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes", "success", "timing_success"}


def row_speedup(row: dict[str, str]) -> float | None:
    retained_ratio = numeric(row.get("speedup_ratio", ""))
    if retained_ratio is not None:
        return retained_ratio

    source = numeric(row.get("source_runtime_ms", "")) or numeric(row.get("median_source_ms", ""))
    rewrite = (
        numeric(row.get("rewrite_runtime_ms", ""))
        or numeric(row.get("generated_runtime_ms", ""))
        or numeric(row.get("median_rewrite_ms", ""))
        or numeric(row.get("median_generated_ms", ""))
    )
    if source is None or rewrite is None or rewrite <= 0:
        return None
    return source / rewrite


def format_best_worst(row: dict[str, str]) -> str:
    speedup = row_speedup(row)
    if speedup is None:
        raise ValueError("cannot format best/worst row without speedup")
    speedup_text = row.get("speedup_ratio") or str(speedup)
    return f"{row['case_id']}|{row['engine']}|{speedup_text}"


def compute_metrics(rows: list[dict[str, str]]) -> dict[str, str]:
    eligible = [
        row
        for row in rows
        if truthy(row.get("timing_success", ""))
        and truthy(row.get("exact_match", "true"))
        and row_speedup(row) is not None
    ]
    if not eligible:
        raise ValueError("no retained exact + timing-success numeric rows")

    speedups = [row_speedup(row) for row in eligible]
    if any(value is None for value in speedups):
        raise ValueError("eligible row lost speedup during aggregation")
    numeric_speedups = [float(value) for value in speedups if value is not None]
    best = max(eligible, key=lambda row: float(row_speedup(row) or 0))
    worst = min(eligible, key=lambda row: float(row_speedup(row) or 0))
    timing_denominator = len(numeric_speedups)
    win_count = sum(value > WIN_THRESHOLD for value in numeric_speedups)
    tie_count = sum(LOSS_THRESHOLD <= value <= WIN_THRESHOLD for value in numeric_speedups)
    loss_count = sum(value < LOSS_THRESHOLD for value in numeric_speedups)
    regression_count = sum(value < REGRESSION_20_THRESHOLD for value in numeric_speedups)

    return {
        "timing_denominator": str(timing_denominator),
        "gm_speedup": str(math.exp(sum(math.log(value) for value in numeric_speedups) / timing_denominator)),
        "median_speedup": str(statistics.median(numeric_speedups)),
        "win_count": str(win_count),
        "tie_count": str(tie_count),
        "loss_count": str(loss_count),
        "regression_rate_20pct": str(regression_count / timing_denominator),
        "best_case": format_best_worst(best),
        "worst_case": format_best_worst(worst),
    }


def retained_by_route(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(row["method_id"], row["route_id"]): row for row in rows}


def regenerate_summary(
    retained_rows: list[dict[str, str]], case_rows: list[dict[str, str]]
) -> tuple[list[dict[str, str]], dict[tuple[str, str], str]]:
    retained = retained_by_route(retained_rows)
    regenerated: list[dict[str, str]] = []
    modes: dict[tuple[str, str], str] = {}

    for spec in ROUTES:
        key = (spec.method_id, spec.route_id)
        if key not in retained:
            raise SystemExit(f"retained target missing route {spec.method_id}/{spec.route_id}")

        row = dict(retained[key])
        modes[key] = spec.recompute_mode

        if spec.recompute_mode == "per_case":
            route_case_rows = [
                case_row
                for case_row in case_rows
                if case_row.get("method_id") == spec.method_id
                and case_row.get("route_id") == spec.route_id
            ]
            metrics = compute_metrics(route_case_rows)
            row.update(metrics)
        elif spec.recompute_mode == "artifact_only":
            # Keep retained values visible but do not claim lower-level recomputation.
            row = dict(retained[key])
        else:
            raise AssertionError(f"unknown recompute mode {spec.recompute_mode}")

        regenerated.append({name: row.get(name, "") for name in SUMMARY_COLUMNS})

    return regenerated, modes


def compare_values(regenerated: str, retained: str, artifact_only: bool) -> tuple[str, str]:
    if artifact_only:
        if regenerated == retained:
            return "artifact_only_match", "0"
        return "conflict_needs_human_review", "artifact_only_value_changed"

    if regenerated == retained:
        return "exact_match", "0"

    left = numeric(regenerated)
    right = numeric(retained)
    if left is not None and right is not None:
        diff = abs(left - right)
        if diff < FLOAT_TOLERANCE:
            return "rounded_match", str(diff)
        return "conflict_needs_human_review", str(diff)

    return "conflict_needs_human_review", "string_mismatch"


def build_diff(
    regenerated_rows: list[dict[str, str]],
    retained_rows: list[dict[str, str]],
    modes: dict[tuple[str, str], str],
) -> list[dict[str, str]]:
    retained = retained_by_route(retained_rows)
    diff_rows: list[dict[str, str]] = []
    notes_by_key = {(spec.method_id, spec.route_id): spec.note for spec in ROUTES}

    for row in regenerated_rows:
        key = (row["method_id"], row["route_id"])
        retained_row = retained.get(key)
        if retained_row is None:
            for column in SUMMARY_COLUMNS:
                diff_rows.append(
                    {
                        "method_id": row["method_id"],
                        "route_id": row["route_id"],
                        "column_name": column,
                        "regenerated_value": row.get(column, ""),
                        "retained_value": "",
                        "comparison_status": "missing_input",
                        "difference": "retained route missing",
                        "notes": notes_by_key.get(key, ""),
                    }
                )
            continue

        artifact_only = modes.get(key) == "artifact_only"
        for column in SUMMARY_COLUMNS:
            status, difference = compare_values(
                row.get(column, ""), retained_row.get(column, ""), artifact_only
            )
            diff_rows.append(
                {
                    "method_id": row["method_id"],
                    "route_id": row["route_id"],
                    "column_name": column,
                    "regenerated_value": row.get(column, ""),
                    "retained_value": retained_row.get(column, ""),
                    "comparison_status": status,
                    "difference": difference,
                    "notes": notes_by_key.get(key, ""),
                }
            )
    return diff_rows


def raw_input_counts() -> list[str]:
    lines: list[str] = []
    for path in RAW_TIMING_INPUTS:
        if path.suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            record_count = len(data.get("records", [])) if isinstance(data, dict) else len(data)
            current_metric = (
                data.get("current_benchmark_metric_evidence", "NA")
                if isinstance(data, dict)
                else "NA"
            )
            lines.append(
                f"- `{rel(path)}`: {record_count} JSON records; current_benchmark_metric_evidence={current_metric}"
            )
        else:
            rows = read_csv(path)
            routes = Counter(row.get("route_id", "") for row in rows)
            route_text = ", ".join(f"{route}={count}" for route, count in sorted(routes.items()))
            lines.append(f"- `{rel(path)}`: {len(rows)} CSV rows; {route_text}")
    return lines


def write_readme(diff_rows: list[dict[str, str]]) -> None:
    counts = Counter(row["comparison_status"] for row in diff_rows)
    recomputed = [f"{spec.method_id}/{spec.route_id}" for spec in ROUTES if spec.recompute_mode == "per_case"]
    artifact_only = [
        f"{spec.method_id}/{spec.route_id}" for spec in ROUTES if spec.recompute_mode == "artifact_only"
    ]

    text = f"""# Speedup Slice Summary Regeneration V1

## Purpose
This static script regenerates `speedup_slice_summary_v1.csv` from retained Common-core v0 timing artifacts and compares the regenerated rows against the retained Round 4 target.

## Inputs Read
- `{rel(TABLE6)}`
- `{rel(CANONICAL_CASE_LEVEL)}`
- `{rel(RETAINED_TARGET)}`
{chr(10).join(raw_input_counts())}

## Outputs Written
- `{rel(OUTPUT_SUMMARY)}`
- `{rel(OUTPUT_DIFF)}`
- `{rel(OUTPUT_README)}`

## Formula Policy
- Eligibility: retained exact + timing-success case-level rows with numeric `speedup_ratio`.
- Speedup ratio: retained `speedup_ratio`; if a future retained row omits it, compute as source median/runtime divided by rewrite median/runtime before aggregation.
- GM speedup: `exp(mean(log(speedup_ratio)))`.
- Median speedup: median over retained eligible `speedup_ratio` values.
- Win/tie/loss: win if `speedup_ratio > 1.05`, tie if `0.95 <= speedup_ratio <= 1.05`, loss if `speedup_ratio < 0.95`.
- Regression@20: `count(speedup_ratio < 0.8) / timing_denominator`.

## Recomputed Routes
{chr(10).join(f'- `{route}`' for route in recomputed)}

## Artifact-Only Routes
{chr(10).join(f'- `{route}`' for route in artifact_only)}

Direct LLM repair remains artifact-only for the full 96-row mixed-source timing slice because only two repair-specific lower-level rows are retained. R-Bot remains artifact-only because the retained PG15 JSON is bounded appendix evidence and is marked `current_benchmark_metric_evidence=false`. SQLGlot combined 240 remains artifact-only because it is a diagnostic route-family aggregate, not a single method route.

## Comparison Summary
- exact_match: {counts.get('exact_match', 0)}
- rounded_match: {counts.get('rounded_match', 0)}
- artifact_only_match: {counts.get('artifact_only_match', 0)}
- conflict_needs_human_review: {counts.get('conflict_needs_human_review', 0)}
- missing_input: {counts.get('missing_input', 0)}

## Boundary
This script does not run database engines, LLM/model calls, verifier tools, PORT9, EXPLAIN collection, or new timing collection. It does not change retained source artifacts, metrics, denominators, taxonomy, registries, case facts, protocol, paper claims, or paper prose.

## Source-of-Truth Writeback Judgment
No source-of-truth writeback is needed if the diff contains no `conflict_needs_human_review` or `missing_input` rows.
"""
    OUTPUT_README.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if regenerated summary conflicts")
    args = parser.parse_args()

    require_inputs()
    retained_rows = read_csv(RETAINED_TARGET)
    case_rows = read_csv(CANONICAL_CASE_LEVEL)
    # These reads are intentional: they ensure the retained raw inputs exist and
    # are included in the readme provenance summary without running any runner.
    _ = read_csv(TABLE6)
    for path in RAW_TIMING_INPUTS:
        if path.suffix == ".csv":
            _ = read_csv(path)
        elif path.suffix == ".json":
            _ = json.loads(path.read_text(encoding="utf-8"))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    regenerated_rows, modes = regenerate_summary(retained_rows, case_rows)
    diff_rows = build_diff(regenerated_rows, retained_rows, modes)
    write_csv(OUTPUT_SUMMARY, SUMMARY_COLUMNS, regenerated_rows)
    write_csv(OUTPUT_DIFF, DIFF_COLUMNS, diff_rows)
    write_readme(diff_rows)

    counts = Counter(row["comparison_status"] for row in diff_rows)
    conflicts = counts.get("conflict_needs_human_review", 0) + counts.get("missing_input", 0)
    print(f"routes rendered: {len(regenerated_rows)}")
    print(f"cells compared: {len(diff_rows)}")
    print(f"exact matches: {counts.get('exact_match', 0)}")
    print(f"rounded matches: {counts.get('rounded_match', 0)}")
    print(f"artifact-only matches: {counts.get('artifact_only_match', 0)}")
    print(f"conflicts: {counts.get('conflict_needs_human_review', 0)}")
    print(f"missing inputs: {counts.get('missing_input', 0)}")
    print(f"output directory: {rel(OUT_DIR)}")

    if args.check and conflicts:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
