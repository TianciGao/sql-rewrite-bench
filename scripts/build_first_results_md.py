#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Dict

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports" / "pilot"
OUT_PATH = ROOT / "docs" / "FIRST_PILOT_RESULTS.md"


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def markdown_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    if not rows:
        return "_No rows available._"

    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row.get(col, "") for col in columns) + " |")
    return "\n".join([header, sep] + body)


def get_summary_value(rows: List[Dict[str, str]], group: str, field: str = "count") -> str:
    for row in rows:
        if row.get("summary_group") == group:
            return row.get(field, "")
    return ""


def build_results_md() -> str:
    summary_rows = read_csv(REPORTS / "admitted_vs_staged_summary_v0.csv")
    case_rows = read_csv(REPORTS / "case_maturity_matrix_v0.csv")
    source_rows = read_csv(REPORTS / "source_to_case_mapping_v0.csv")
    engine_rows = read_csv(REPORTS / "engine_validation_summary_v0.csv")

    total_cases = get_summary_value(summary_rows, "total_repository_cases")
    first_slice_total = get_summary_value(summary_rows, "first_slice_total")
    anchor_count = get_summary_value(summary_rows, "stable_pilot_anchor")
    admitted_count = get_summary_value(summary_rows, "admitted_external_common_core")
    staged_tri_engine_count = get_summary_value(summary_rows, "staged_tri_engine_validated_draft")

    included_case_ids = []
    for row in case_rows:
        if row.get("include_in_first_slice") == "yes":
            included_case_ids.append(row.get("case_id", ""))

    included_case_text = ", ".join(included_case_ids) if included_case_ids else "N/A"

    md = f"""# First Pilot Results

## File role
This file records the **first paper-facing pre-pilot results slice** for the current SQL rewrite benchmark repository.

It is intended to summarize the currently stabilized evidence and provide a first results block for paper drafting.
It does **not** claim full pilot-scale completion.

---

## 1. Current interpretation

The repository now supports a controlled first evaluation slice.
At the current stage:

- total tracked cases: **{total_cases}**
- first-slice cases: **{first_slice_total}**
- stable anchors: **{anchor_count}**
- admitted external common-core cases: **{admitted_count}**
- tri-engine validated staged drafts: **{staged_tri_engine_count}**

The current first-slice cases are:

**{included_case_text}**

This should be interpreted as a **pre-pilot stable reporting slice**, not as a claim of full benchmark completion.

---

## 2. Table 1 — Case maturity summary

{markdown_table(
    summary_rows,
    ["summary_group", "count", "case_ids", "include_in_first_slice", "notes"]
)}

### Interpretation
The current repository already exhibits a non-flat maturity structure:
- four stable pilot anchors,
- admitted external common-core cases,
- and staged drafts with different closure levels.

This supports the benchmark’s structural maturity argument even before full pilot-scale expansion.

---

## 3. Table 2 — Case-level maturity matrix

{markdown_table(
    case_rows,
    [
        "case_id",
        "pool",
        "source_family",
        "current_maturity",
        "validated_engines",
        "admitted_or_staged",
        "include_in_first_slice",
        "notes",
    ],
)}

### Interpretation
The current first-slice inclusion boundary is intentionally conservative.
Only cases with sufficiently stable maturity and engine evidence are included.

---

## 4. Table 3 — Source-to-case materialization map

{markdown_table(
    source_rows,
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
)}

### Interpretation
The benchmark is not being built as a flat SQL union.
Instead, different source families currently play different roles:
- anchors,
- admitted external case lines,
- staged draft lines,
- realism substrate lines,
- and unresolved target-only lines.

---

## 5. Table 4 — Engine-validation summary

{markdown_table(
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
)}

### Interpretation
The first slice is intentionally restricted to cases with strong enough engine evidence.
In particular, the current first slice already includes:
- tri-engine anchors,
- admitted external tri-engine cases,
- and tri-engine validated staged consistency drafts.

This gives the repository meaningful early support for correctness-aware and cross-engine evaluation.

---

## 6. Current strongest takeaways

At the current repository stage, the strongest paper-facing takeaways are:

1. The benchmark already has a meaningful **four-pool structure**.
2. The repository already separates **anchor / admitted / staged** lines.
3. A stable **tri-engine evidence slice** already exists.
4. The consistency line already contains **tri-engine validated staged drafts**, showing that correctness is a first-class benchmark dimension.

---

## 7. Current non-claims

The current results should **not** be interpreted as evidence of:

- full pilot-scale completion,
- full source-universe closure,
- large-scale baseline comparison,
- broad workload curation completion,
- or benchmark expansion readiness.

These remain later-phase goals.

---

## 8. Immediate next step

The next step after this results snapshot should be to use these tables as the basis for:

- the first evaluation subsection draft,
- the first benchmark-characterization subsection,
- and the first appendix-style maturity summary block.

Only after that should the team decide whether to prioritize:
- selected source activation,
- controlled benchmark expansion,
- or baseline-comparison preparation.
"""
    return md


def main() -> int:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(build_results_md(), encoding="utf-8")
    print(f"wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())