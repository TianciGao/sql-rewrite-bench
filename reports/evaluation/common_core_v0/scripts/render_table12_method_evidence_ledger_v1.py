#!/usr/bin/env python3
"""Static renderer for Section 8 Table 12.

This script regenerates the Common-core v0 denominator-aware method evidence
ledger from retained CSV/MD artifacts only. It intentionally does not run any
database, model, verifier, PORT, EXPLAIN, or timing command.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = REPO_ROOT / "reports/evaluation/common_core_v0"

TABLE3_PATH = BASE / "00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv"
CANDIDATE_FAILURE_PATH = BASE / "10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1/candidate_failure_accounting_v1.csv"
SPEEDUP_PATH = BASE / "11_TIMING_OBSERVABILITY_V1/speedup_slice_summary_v1.csv"
PROVENANCE_PATH = BASE / "17_TABLE12_ULTIMATE_PROVENANCE_V1/table12_cell_provenance_v1.csv"
FORMULA_MAP_PATH = BASE / "17_TABLE12_ULTIMATE_PROVENANCE_V1/table12_formula_source_map_v1.csv"
PROVENANCE_SUMMARY_PATH = BASE / "17_TABLE12_ULTIMATE_PROVENANCE_V1/table12_provenance_summary_v1.md"
STATIC_RECOMPUTE_RESULTS_PATH = BASE / "16_STATIC_RECOMPUTE_AUDIT_V1/static_recompute_results_v1.csv"
STATIC_RECOMPUTE_SUMMARY_PATH = BASE / "16_STATIC_RECOMPUTE_AUDIT_V1/static_recompute_summary_v1.md"

OUT_DIR = BASE / "18_TABLE12_REGENERATION_V1"
OUT_CSV = OUT_DIR / "table12_method_evidence_ledger_regenerated_v1.csv"
OUT_MD = OUT_DIR / "table12_method_evidence_ledger_regenerated_v1.md"
OUT_DIFF = OUT_DIR / "table12_regeneration_diff_v1.csv"
OUT_README = OUT_DIR / "table12_regeneration_readme_v1.md"

OLD_DRAFT_VALUES = {"1.0168", "1.0190", "1.0267"}

CSV_COLUMNS = [
    "method_route",
    "method_id",
    "route_id",
    "scope",
    "planned",
    "generated_or_ready",
    "executed",
    "exact",
    "timed",
    "gm_speedup",
    "regression_rate_20pct",
    "placement",
    "denominator_id",
    "source_artifacts",
    "claim_boundary",
    "notes",
]

DIFF_COLUMNS = [
    "method_id",
    "route_id",
    "column_name",
    "regenerated_value",
    "expected_value",
    "comparison_status",
    "source_artifact",
    "notes",
]

TABLE12_COLUMNS = [
    "method / route",
    "scope",
    "planned",
    "generated_or_ready",
    "executed",
    "exact",
    "timed",
    "gm_speedup",
    "regression_rate_20pct",
    "placement",
]

COLUMN_TO_OUTPUT = {
    "method / route": "method_route",
    "scope": "scope",
    "planned": "planned",
    "generated_or_ready": "generated_or_ready",
    "executed": "executed",
    "exact": "exact",
    "timed": "timed",
    "gm_speedup": "gm_speedup",
    "regression_rate_20pct": "regression_rate_20pct",
    "placement": "placement",
}

ROUTE_ORDER = [
    ("direct_llm", "direct_llm_same_engine_rewrite"),
    ("direct_llm", "direct_llm_execute_repair_1shot"),
    ("sqlglot", "sqlglot_optimize_same_dialect"),
    ("sqlglot", "sqlglot_transpile_same_dialect_noop"),
    ("calcite_hep", "calcite_hep_fail_closed_120"),
    ("r_bot", "r_bot_same_engine_rewrite"),
    ("llm_r2", "llm_r2_original_route_bounded_pg9"),
    ("llm_r2", "llm_r2_recovered_extraction_route_v1"),
    ("learnedrewrite", "UNKNOWN_NOT_RECOVERED"),
]

# The Round 17 provenance audit used a normalized LearnedRewrite route id for
# target rows. The paper-facing retained candidate accounting route remains
# UNKNOWN_NOT_RECOVERED.
EXPECTED_ROUTE_ALIASES = {
    ("learnedrewrite", "UNKNOWN_NOT_RECOVERED"): ("learnedrewrite", "learnedrewrite_pg10_bounded"),
}


@dataclass(frozen=True)
class SourceTables:
    table3: dict[tuple[str, str], dict[str, str]]
    candidate_failure: dict[tuple[str, str], dict[str, str]]
    speedup: dict[tuple[str, str], dict[str, str]]
    provenance: dict[tuple[str, str, str], dict[str, str]]
    formula_map_rows: list[dict[str, str]]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"missing required input: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def index_by_route(rows: Iterable[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(r["method_id"], r["route_id"]): r for r in rows}


def load_sources() -> SourceTables:
    required = [
        TABLE3_PATH,
        CANDIDATE_FAILURE_PATH,
        SPEEDUP_PATH,
        PROVENANCE_PATH,
        FORMULA_MAP_PATH,
        PROVENANCE_SUMMARY_PATH,
        STATIC_RECOMPUTE_RESULTS_PATH,
        STATIC_RECOMPUTE_SUMMARY_PATH,
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))

    provenance_rows = read_csv(PROVENANCE_PATH)
    return SourceTables(
        table3=index_by_route(read_csv(TABLE3_PATH)),
        candidate_failure=index_by_route(read_csv(CANDIDATE_FAILURE_PATH)),
        speedup=index_by_route(read_csv(SPEEDUP_PATH)),
        provenance={(r["method_id"], r["route_id"], r["column_name"]): r for r in provenance_rows},
        formula_map_rows=read_csv(FORMULA_MAP_PATH),
    )


def combine_artifacts(*values: str) -> str:
    seen: list[str] = []
    for value in values:
        for part in str(value).split("|"):
            part = part.strip()
            if part and part not in seen:
                seen.append(part)
    return "|".join(seen)


def combine_notes(*values: str) -> str:
    return " ".join(v.strip() for v in values if v and v.strip())


def table3(sources: SourceTables, method_id: str, route_id: str) -> dict[str, str]:
    key = (method_id, route_id)
    if key not in sources.table3:
        raise KeyError(f"missing Table 3 route: {key}")
    return sources.table3[key]


def failure(sources: SourceTables, method_id: str, route_id: str) -> dict[str, str]:
    key = (method_id, route_id)
    if key not in sources.candidate_failure:
        raise KeyError(f"missing candidate failure route: {key}")
    return sources.candidate_failure[key]


def speedup(sources: SourceTables, method_id: str, route_id: str) -> dict[str, str] | None:
    return sources.speedup.get((method_id, route_id))


def build_rows(sources: SourceTables) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    direct = table3(sources, "direct_llm", "direct_llm_same_engine_rewrite")
    direct_speed = speedup(sources, "direct_llm", "direct_llm_same_engine_rewrite")
    assert direct_speed is not None
    rows.append({
        "method_route": "Direct LLM original",
        "method_id": "direct_llm",
        "route_id": "direct_llm_same_engine_rewrite",
        "scope": "tri-engine same-engine",
        "planned": direct["planned_rows"],
        "generated_or_ready": f"{direct['generated_rows']} generated; {direct['ready_rows']} ready",
        "executed": direct["executed_rows"],
        "exact": direct["exact_match_rows"],
        "timed": direct_speed["timing_denominator"],
        "gm_speedup": direct_speed["gm_speedup"],
        "regression_rate_20pct": direct_speed["regression_rate_20pct"],
        "placement": "main same-engine evidence",
        "denominator_id": direct["denominator_id"],
        "source_artifacts": combine_artifacts(str(TABLE3_PATH.relative_to(REPO_ROOT)), direct["source_artifacts"], direct_speed["source_artifact"]),
        "claim_boundary": direct["claim_boundary"],
        "notes": direct["notes"],
    })

    repair = failure(sources, "direct_llm", "direct_llm_execute_repair_1shot")
    repair_speed = speedup(sources, "direct_llm", "direct_llm_execute_repair_1shot")
    assert repair_speed is not None
    rows.append({
        "method_route": "Direct LLM + Repair-1",
        "method_id": "direct_llm",
        "route_id": "direct_llm_execute_repair_1shot",
        "scope": "tri-engine feedback route",
        "planned": repair["planned"],
        "generated_or_ready": f"{repair['generated_or_ready']} generated; {repair['preflight_blocked']} preflight-blocked",
        "executed": repair["executed"],
        "exact": repair["exact"],
        "timed": repair_speed["timing_denominator"],
        "gm_speedup": repair_speed["gm_speedup"],
        "regression_rate_20pct": repair_speed["regression_rate_20pct"],
        "placement": "route-level evidence; mixed-source timing",
        "denominator_id": repair["denominator_id"],
        "source_artifacts": combine_artifacts(str(CANDIDATE_FAILURE_PATH.relative_to(REPO_ROOT)), repair["source_artifact"], repair_speed["source_artifact"]),
        "claim_boundary": combine_notes(repair["claim_boundary"], repair_speed["claim_boundary"]),
        "notes": combine_notes(
            repair["notes"],
            "Executed = exact + mismatch = 97 / 96 + 1; ready_after_preflight / 115 is not executed.",
            repair_speed["notes"],
        ),
    })

    sql_opt = table3(sources, "sqlglot", "sqlglot_optimize_same_dialect")
    sql_opt_failure = failure(sources, "sqlglot", "sqlglot_optimize_same_dialect")
    sql_opt_speed = speedup(sources, "sqlglot", "sqlglot_optimize_same_dialect")
    assert sql_opt_speed is not None
    rows.append({
        "method_route": "SQLGlot optimize",
        "method_id": "sqlglot",
        "route_id": "sqlglot_optimize_same_dialect",
        "scope": "tri-engine route",
        "planned": sql_opt["planned_rows"],
        "generated_or_ready": f"{sql_opt['planned_rows']} attempted; {sql_opt['generated_rows']} generated",
        "executed": sql_opt_failure["executed"],
        "exact": sql_opt["exact_match_rows"],
        "timed": sql_opt_speed["timing_denominator"],
        "gm_speedup": sql_opt_speed["gm_speedup"],
        "regression_rate_20pct": sql_opt_speed["regression_rate_20pct"],
        "placement": "revised exact63 route",
        "denominator_id": sql_opt["denominator_id"],
        "source_artifacts": combine_artifacts(str(TABLE3_PATH.relative_to(REPO_ROOT)), sql_opt["source_artifacts"], sql_opt_failure["source_artifact"], sql_opt_speed["source_artifact"]),
        "claim_boundary": sql_opt["claim_boundary"],
        "notes": combine_notes(sql_opt["notes"], sql_opt_failure["notes"], "Do not use older exact65 / old SQLGlot optimize timing values."),
    })

    noop = table3(sources, "sqlglot", "sqlglot_transpile_same_dialect_noop")
    noop_failure = failure(sources, "sqlglot", "sqlglot_transpile_same_dialect_noop")
    noop_speed = speedup(sources, "sqlglot", "sqlglot_transpile_same_dialect_noop")
    assert noop_speed is not None
    rows.append({
        "method_route": "SQLGlot no-op",
        "method_id": "sqlglot",
        "route_id": "sqlglot_transpile_same_dialect_noop",
        "scope": "tri-engine route",
        "planned": noop["planned_rows"],
        "generated_or_ready": f"{noop['planned_rows']} attempted; {noop['generated_rows']} generated",
        "executed": noop_failure["executed"],
        "exact": noop["exact_match_rows"],
        "timed": noop_speed["timing_denominator"],
        "gm_speedup": noop_speed["gm_speedup"],
        "regression_rate_20pct": noop_speed["regression_rate_20pct"],
        "placement": "no-op / low-transform route",
        "denominator_id": noop["denominator_id"],
        "source_artifacts": combine_artifacts(str(TABLE3_PATH.relative_to(REPO_ROOT)), noop["source_artifacts"], noop_failure["source_artifact"], noop_speed["source_artifact"]),
        "claim_boundary": combine_notes(noop["claim_boundary"], noop_failure["claim_boundary"]),
        "notes": combine_notes(noop["notes"], noop_failure["notes"], f"source-like/no-op count retained: {noop_failure['noop_or_source_like']}."),
    })

    calcite = table3(sources, "calcite_hep", "calcite_hep_fail_closed_120")
    calcite_failure = failure(sources, "calcite_hep", "calcite_hep_fail_closed_120")
    calcite_speed = speedup(sources, "calcite_hep", "calcite_hep_fail_closed_120")
    assert calcite_speed is not None
    rows.append({
        "method_route": "Calcite HEP fail-closed",
        "method_id": "calcite_hep",
        "route_id": "calcite_hep_fail_closed_120",
        "scope": "tri-engine fail-closed route",
        "planned": calcite["planned_rows"],
        "generated_or_ready": "retained route artifacts",
        "executed": calcite_failure["executed"],
        "exact": calcite["exact_match_rows"],
        "timed": calcite_speed["timing_denominator"],
        "gm_speedup": calcite_speed["gm_speedup"],
        "regression_rate_20pct": calcite_speed["regression_rate_20pct"],
        "placement": "correctness-gated timing packet",
        "denominator_id": calcite["denominator_id"],
        "source_artifacts": combine_artifacts(str(TABLE3_PATH.relative_to(REPO_ROOT)), calcite["source_artifacts"], calcite_failure["source_artifact"], calcite_speed["source_artifact"]),
        "claim_boundary": calcite_speed["claim_boundary"],
        "notes": combine_notes(calcite["notes"], calcite_failure["notes"]),
    })

    rbot = failure(sources, "r_bot", "r_bot_same_engine_rewrite")
    rbot_speed = speedup(sources, "r_bot", "r_bot_same_engine_rewrite")
    assert rbot_speed is not None
    rows.append({
        "method_route": "R-Bot",
        "method_id": "r_bot",
        "route_id": "r_bot_same_engine_rewrite",
        "scope": "mixed scope",
        "planned": "formal 120 generation",
        "generated_or_ready": "PG-scoped subsets",
        "executed": "15 PG-only",
        "exact": "15 PG-only",
        "timed": rbot_speed["timing_denominator"],
        "gm_speedup": rbot_speed["gm_speedup"],
        "regression_rate_20pct": rbot_speed["regression_rate_20pct"],
        "placement": "bounded / mixed appendix",
        "denominator_id": rbot["denominator_id"],
        "source_artifacts": combine_artifacts(rbot["source_artifact"], rbot_speed["source_artifact"]),
        "claim_boundary": combine_notes(rbot["claim_boundary"], rbot_speed["claim_boundary"]),
        "notes": combine_notes(rbot["notes"], "Mixed-scope / PG15 bounded appendix; do not force into a full 120 exact/timing row."),
    })

    llm_r2 = failure(sources, "llm_r2", "llm_r2_original_route_bounded_pg9")
    rows.append({
        "method_route": "LLM-R2 original",
        "method_id": "llm_r2",
        "route_id": "llm_r2_original_route_bounded_pg9",
        "scope": "PG-only bounded",
        "planned": llm_r2["planned"],
        "generated_or_ready": llm_r2["generated_or_ready"],
        "executed": "3 exact + 6 execution failed",
        "exact": llm_r2["exact"],
        "timed": "0",
        "gm_speedup": "NA",
        "regression_rate_20pct": "NA",
        "placement": "bounded appendix",
        "denominator_id": llm_r2["denominator_id"],
        "source_artifacts": llm_r2["source_artifact"],
        "claim_boundary": llm_r2["claim_boundary"],
        "notes": llm_r2["notes"],
    })

    recovered = failure(sources, "llm_r2", "llm_r2_recovered_extraction_route_v1")
    rows.append({
        "method_route": "LLM-R2 recovered",
        "method_id": "llm_r2",
        "route_id": "llm_r2_recovered_extraction_route_v1",
        "scope": "PG9 recovery audit",
        "planned": recovered["planned"],
        "generated_or_ready": recovered["generated_or_ready"],
        "executed": recovered["executed"],
        "exact": recovered["exact"],
        "timed": "0",
        "gm_speedup": "NA",
        "regression_rate_20pct": "NA",
        "placement": "PG6 exact recovered subset",
        "denominator_id": recovered["denominator_id"],
        "source_artifacts": recovered["source_artifact"],
        "claim_boundary": recovered["claim_boundary"],
        "notes": combine_notes(recovered["notes"], "PG9 recovery audit / PG6 exact recovered subset; not a standalone PG6 denominator row."),
    })

    learned = failure(sources, "learnedrewrite", "UNKNOWN_NOT_RECOVERED")
    rows.append({
        "method_route": "LearnedRewrite",
        "method_id": "learnedrewrite",
        "route_id": "UNKNOWN_NOT_RECOVERED",
        "scope": "PG10 bounded",
        "planned": learned["planned"],
        "generated_or_ready": learned["generated_or_ready"],
        "executed": learned["executed"],
        "exact": "10 checker-consistent",
        "timed": "NA",
        "gm_speedup": "NA",
        "regression_rate_20pct": "NA",
        "placement": "bounded appendix; 8 source-like/no-op",
        "denominator_id": learned["denominator_id"],
        "source_artifacts": combine_artifacts(learned["source_artifact"], "reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md"),
        "claim_boundary": learned["claim_boundary"],
        "notes": combine_notes(learned["notes"], "8 source-like/no-op rows retained; do not infer missing executed/timing."),
    })

    ordered = {(r["method_id"], r["route_id"]): r for r in rows}
    return [ordered[key] for key in ROUTE_ORDER]


def decimal_diff(a: str, b: str) -> Decimal | None:
    try:
        return abs(Decimal(str(a)) - Decimal(str(b)))
    except (InvalidOperation, ValueError):
        return None


def compare_values(regenerated: str, expected: str, column_name: str) -> str:
    if regenerated == expected:
        if expected == "NA" or expected.startswith("NA_"):
            return "expected_NA_match"
        if column_name in {"scope", "placement", "method / route"}:
            return "artifact_boundary_match"
        return "exact_match"
    diff = decimal_diff(regenerated, expected)
    if diff is not None and diff < Decimal("1e-9"):
        return "rounded_match"
    if expected == "NA" and regenerated.startswith("NA"):
        return "expected_NA_match"
    return "conflict_needs_human_review"


def expected_key(method_id: str, route_id: str, column_name: str) -> tuple[str, str, str]:
    expected_method, expected_route = EXPECTED_ROUTE_ALIASES.get((method_id, route_id), (method_id, route_id))
    return expected_method, expected_route, column_name


def build_diff(rows: list[dict[str, str]], sources: SourceTables) -> list[dict[str, str]]:
    diff_rows: list[dict[str, str]] = []
    for row in rows:
        for column_name in TABLE12_COLUMNS:
            output_column = COLUMN_TO_OUTPUT[column_name]
            regenerated = row[output_column]
            provenance = sources.provenance.get(expected_key(row["method_id"], row["route_id"], column_name))
            if provenance is None:
                diff_rows.append({
                    "method_id": row["method_id"],
                    "route_id": row["route_id"],
                    "column_name": column_name,
                    "regenerated_value": regenerated,
                    "expected_value": "",
                    "comparison_status": "missing_input",
                    "source_artifact": str(PROVENANCE_PATH.relative_to(REPO_ROOT)),
                    "notes": "Missing expected target cell in Table 12 provenance artifact.",
                })
                continue
            expected = provenance["canonical_full_value"]
            status = compare_values(regenerated, expected, column_name)
            diff_rows.append({
                "method_id": row["method_id"],
                "route_id": row["route_id"],
                "column_name": column_name,
                "regenerated_value": regenerated,
                "expected_value": expected,
                "comparison_status": status,
                "source_artifact": provenance["immediate_source_artifact"],
                "notes": provenance["notes"],
            })
    return diff_rows


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_semantic_checks(rows: list[dict[str, str]], sources: SourceTables) -> list[str]:
    by_route = {(r["method_id"], r["route_id"]): r for r in rows}
    checks: list[str] = []

    repair = by_route[("direct_llm", "direct_llm_execute_repair_1shot")]
    repair_failure = failure(sources, "direct_llm", "direct_llm_execute_repair_1shot")
    require(repair["exact"] == "96", "Direct LLM repair exact must be 96")
    require(repair_failure["mismatch"] == "1", "Direct LLM repair mismatch must be retained as 1")
    require(repair["executed"] == "97", "Direct LLM repair executed must be 97")
    require("115" not in repair["executed"], "Direct LLM repair executed must not use ready_after_preflight 115")
    checks.append("Direct LLM + Repair-1 executed = exact + mismatch = 97 / 96 + 1; ready_after_preflight 115 is not executed.")

    sql_opt = by_route[("sqlglot", "sqlglot_optimize_same_dialect")]
    require(sql_opt["exact"] == "63", "SQLGlot optimize exact must be 63")
    require(sql_opt["timed"] == "63", "SQLGlot optimize timed must be 63")
    require(sql_opt["gm_speedup"] == "0.9907164888740984", "SQLGlot optimize GM must be canonical exact63 GM")
    checks.append("SQLGlot optimize uses exact63/timed63 and canonical GM 0.9907164888740984.")

    noop = by_route[("sqlglot", "sqlglot_transpile_same_dialect_noop")]
    require(noop["exact"] == "72", "SQLGlot no-op exact must be 72")
    require(noop["timed"] == "72", "SQLGlot no-op timed must be 72")
    joined_noop = " ".join(noop.values()).lower()
    require("no-op" in joined_noop or "source-like" in joined_noop, "SQLGlot no-op/source-like boundary must remain visible")
    checks.append("SQLGlot no-op preserves exact72/timed72 and source-like/no-op boundary.")

    calcite = by_route[("calcite_hep", "calcite_hep_fail_closed_120")]
    require(calcite["exact"] == "93", "Calcite HEP exact must be 93")
    require(calcite["timed"] == "93", "Calcite HEP timed must be 93")
    require(calcite["gm_speedup"] == "0.995917121478", "Calcite HEP GM must be canonical 93-row GM")
    checks.append("Calcite HEP uses exact93/timed93 and canonical GM 0.995917121478.")

    rbot = by_route[("r_bot", "r_bot_same_engine_rewrite")]
    joined_rbot = " ".join(rbot.values()).lower()
    require("mixed" in joined_rbot and "pg15" in joined_rbot and rbot["exact"] != "120", "R-Bot must remain mixed-scope PG15 bounded appendix evidence")
    checks.append("R-Bot remains mixed-scope / PG15 bounded appendix evidence.")

    recovered = by_route[("llm_r2", "llm_r2_recovered_extraction_route_v1")]
    joined_recovered = " ".join(recovered.values()).lower()
    require(recovered["planned"] == "9", "LLM-R2 recovered planned must be 9")
    require(recovered["exact"] == "6", "LLM-R2 recovered exact must be 6")
    require(recovered["timed"] == "0", "LLM-R2 recovered timed must be 0")
    require("pg9" in joined_recovered and "pg6" in joined_recovered, "LLM-R2 recovered must preserve PG9/PG6 boundary")
    checks.append("LLM-R2 recovered preserves PG9 recovery audit / PG6 exact recovered subset boundary.")

    learned = by_route[("learnedrewrite", "UNKNOWN_NOT_RECOVERED")]
    joined_learned = " ".join(learned.values()).lower()
    require(learned["planned"] == "10", "LearnedRewrite planned must be 10")
    require(learned["exact"] == "10 checker-consistent", "LearnedRewrite exact must be 10 checker-consistent")
    require(learned["executed"] == "NA_not_retained", "LearnedRewrite executed must remain NA_not_retained")
    require(learned["timed"] == "NA" and learned["gm_speedup"] == "NA" and learned["regression_rate_20pct"] == "NA", "LearnedRewrite timing/speedup cells must remain NA")
    require("source-like" in joined_learned or "no-op" in joined_learned, "LearnedRewrite source-like/no-op boundary must remain visible")
    checks.append("LearnedRewrite remains bounded PG10 with 8 source-like/no-op rows and no inferred execution/timing.")

    expected_gms = {
        ("direct_llm", "direct_llm_same_engine_rewrite"): "1.043634242319266",
        ("direct_llm", "direct_llm_execute_repair_1shot"): "1.0430582867389244",
        ("sqlglot", "sqlglot_optimize_same_dialect"): "0.9907164888740984",
        ("sqlglot", "sqlglot_transpile_same_dialect_noop"): "1.000145903000493",
        ("calcite_hep", "calcite_hep_fail_closed_120"): "0.995917121478",
        ("r_bot", "r_bot_same_engine_rewrite"): "0.9218248321470981",
    }
    for key, expected in expected_gms.items():
        require(by_route[key]["gm_speedup"] == expected, f"{key} GM must be {expected}")
    checks.append("All Round 4 canonical GM speedup values are retained.")

    rendered_text = "\n".join(
        ",".join(r[c] for c in ["timed", "gm_speedup", "regression_rate_20pct"])
        for r in rows
    )
    for old in OLD_DRAFT_VALUES:
        require(old not in rendered_text, f"old draft value leaked into regenerated output: {old}")
    checks.append("No obsolete draft GM values appear in regenerated metric cells.")

    return checks


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: str) -> str:
    return str(value).replace("|", "\\\\|")


def write_markdown(rows: list[dict[str, str]], checks: list[str]) -> None:
    headers = [
        "method / route",
        "Scope",
        "Planned",
        "Generated / Ready",
        "Executed",
        "Exact",
        "Timed",
        "GM",
        "Regression@20",
        "Placement",
    ]
    lines = [
        "# Table 12 Method Evidence Ledger Regenerated V1",
        "",
        "## Purpose",
        "Static regeneration of Section 8 Table 12 from retained Common-core v0 artifacts.",
        "",
        "## Regenerated Table 12",
        "|" + "|".join(headers) + "|",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for row in rows:
        lines.append(
            "|"
            + "|".join(
                md_escape(row[col])
                for col in [
                    "method_route",
                    "scope",
                    "planned",
                    "generated_or_ready",
                    "executed",
                    "exact",
                    "timed",
                    "gm_speedup",
                    "regression_rate_20pct",
                    "placement",
                ]
            )
            + "|"
        )

    source_artifacts = sorted({part for row in rows for part in row["source_artifacts"].split("|") if part})
    lines.extend([
        "",
        "## Source Artifacts",
    ])
    lines.extend(f"- `{artifact}`" for artifact in source_artifacts)
    lines.extend([
        "",
        "## Semantic Checks",
    ])
    lines.extend(f"- {check}" for check in checks)
    lines.extend([
        "",
        "## Boundaries",
        "- Direct LLM repair executed is `97`, computed as `96 exact + 1 mismatch`; ready/preflight values are not executed.",
        "- SQLGlot optimize uses the revised exact63 timing row, not older exact65 or old draft GM values.",
        "- R-Bot, LLM-R2, and LearnedRewrite remain bounded appendix evidence.",
        "- Speedup metrics apply only on exact + timing-success rows.",
        "",
        "## Not A Ranked Leaderboard",
        "This regenerated table is not a ranked leaderboard and does not name a winner.",
        "",
    ])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def write_readme() -> None:
    text = f"""# Table 12 Regeneration README V1

## Inputs Read
- `{TABLE3_PATH.relative_to(REPO_ROOT)}`
- `{CANDIDATE_FAILURE_PATH.relative_to(REPO_ROOT)}`
- `{SPEEDUP_PATH.relative_to(REPO_ROOT)}`
- `{PROVENANCE_PATH.relative_to(REPO_ROOT)}`
- `{FORMULA_MAP_PATH.relative_to(REPO_ROOT)}`
- `{PROVENANCE_SUMMARY_PATH.relative_to(REPO_ROOT)}`
- `{STATIC_RECOMPUTE_RESULTS_PATH.relative_to(REPO_ROOT)}`
- `{STATIC_RECOMPUTE_SUMMARY_PATH.relative_to(REPO_ROOT)}`

## Outputs Written
- `{OUT_CSV.relative_to(REPO_ROOT)}`
- `{OUT_MD.relative_to(REPO_ROOT)}`
- `{OUT_DIFF.relative_to(REPO_ROOT)}`
- `{OUT_README.relative_to(REPO_ROOT)}`

## Exact Command
`python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check`

## Formulas / Column Logic
`planned`, `executed`, and `exact` are copied from retained route evidence or candidate failure semantics. `generated_or_ready` preserves route-specific wording and does not conflate ready/preflight state with executed. `timed`, `gm_speedup`, and `regression_rate_20pct` are copied from retained timing slices. GM speedup is defined by the retained audits as `exp(mean(log(speedup_ratio)))`, and Regression@20 as `count(speedup_ratio < 0.8) / timing_denominator`.

## What This Script Does Not Do
It does not run databases, LLM/model calls, verifier experiments, PORT9 experiments, EXPLAIN, timing collection, benchmark case generation, or retained source artifact regeneration.

## Known Limitations
This is a Table 12 render entrypoint only. It does not regenerate `table3_same_engine_method_evidence_v3.csv`, `candidate_failure_accounting_v1.csv`, or `speedup_slice_summary_v1.csv`.

## Source-Of-Truth Writeback Judgment
No source-of-truth writeback is needed. This script hardens reproducible rendering without changing retained values, denominators, taxonomy, case facts, protocol, or paper claims.
"""
    OUT_README.write_text(text, encoding="utf-8")


def render(check: bool) -> int:
    sources = load_sources()
    rows = build_rows(sources)
    checks = run_semantic_checks(rows, sources)
    diff_rows = build_diff(rows, sources)
    bad = [r for r in diff_rows if r["comparison_status"] in {"conflict_needs_human_review", "missing_input"}]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUT_CSV, CSV_COLUMNS, rows)
    write_csv(OUT_DIFF, DIFF_COLUMNS, diff_rows)
    write_markdown(rows, checks)
    write_readme()

    # Guard against stale draft values in rendered metric cells.
    emitted = "\n".join(
        row[column]
        for row in rows
        for column in ["timed", "gm_speedup", "regression_rate_20pct"]
    )
    leaked = sorted(old for old in OLD_DRAFT_VALUES if old in emitted)
    if leaked:
        raise AssertionError("old draft values leaked into outputs: " + ", ".join(leaked))

    counts = Counter(r["comparison_status"] for r in diff_rows)
    print(f"rows rendered: {len(rows)}")
    print(f"cells compared: {len(diff_rows)}")
    print(f"exact matches: {counts.get('exact_match', 0)}")
    print(f"rounded matches: {counts.get('rounded_match', 0)}")
    print(f"expected NA matches: {counts.get('expected_NA_match', 0)}")
    print(f"artifact boundary matches: {counts.get('artifact_boundary_match', 0)}")
    print(f"conflicts: {len(bad)}")
    print(f"output directory: {OUT_DIR.relative_to(REPO_ROOT)}")

    if check and bad:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if regenerated cells conflict with provenance targets")
    args = parser.parse_args(argv)
    try:
        return render(check=args.check)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
