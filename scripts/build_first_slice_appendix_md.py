#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Dict

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports" / "pilot"
OUT_PATH = ROOT / "docs" / "FIRST_SLICE_APPENDIX.md"


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


def filter_rows(rows: List[Dict[str, str]], key: str, value: str) -> List[Dict[str, str]]:
    return [row for row in rows if row.get(key) == value]


def build_appendix_md() -> str:
    case_rows = read_csv(REPORTS / "case_maturity_matrix_v0.csv")
    source_rows = read_csv(REPORTS / "source_to_case_mapping_v0.csv")
    summary_rows = read_csv(REPORTS / "admitted_vs_staged_summary_v0.csv")
    engine_rows = read_csv(REPORTS / "engine_validation_summary_v0.csv")
    inclusion_rows = read_csv(REPORTS / "first_slice_inclusion_summary_v0.csv")

    included_rows = filter_rows(inclusion_rows, "included_in_first_slice", "yes")
    excluded_rows = filter_rows(inclusion_rows, "included_in_first_slice", "no")

    md = f"""# First Slice Appendix

## File role
This appendix summarizes the current **first-slice pre-pilot case subset** and its immediate exclusions.

It is intended to provide:
- a compact appendix-ready maturity summary,
- a clear included / excluded case boundary,
- and a stable reference block for early paper drafting.

This appendix does **not** claim full pilot completion.

---

## 1. Appendix summary table

{markdown_table(
    summary_rows,
    ["summary_group", "count", "case_ids", "include_in_first_slice", "notes"]
)}

---

## 2. Included first-slice cases

{markdown_table(
    included_rows,
    [
        "case_id",
        "pool",
        "source_family",
        "included_in_first_slice",
        "reason_for_inclusion_or_exclusion",
        "current_gap_if_excluded",
        "notes",
    ],
)}

### Interpretation
These cases are included because they form the most stable currently available slice across:
- all four pools,
- stable anchors,
- admitted external cases,
- and tri-engine validated staged consistency drafts.

---

## 3. Excluded first-slice cases

{markdown_table(
    excluded_rows,
    [
        "case_id",
        "pool",
        "source_family",
        "included_in_first_slice",
        "reason_for_inclusion_or_exclusion",
        "current_gap_if_excluded",
        "notes",
    ],
)}

### Interpretation
These cases are currently excluded not because they are unimportant, but because:
- engine closure remains incomplete,
- or the line is intentionally kept partial in the current phase.

---

## 4. Engine-validation appendix table

{markdown_table(
    engine_rows,
    [
        "case_id",
        "pool",
        "postgres_validated",
        "mysql_validated",
        "spark_validated",
        "result_artifacts_present",
        "plan_artifacts_present",
        "current_status",
    ],
)}

### Interpretation
The first slice is intentionally restricted to cases with sufficiently stable engine evidence and artifact completeness.

---

## 5. Source-to-case appendix table

{markdown_table(
    source_rows,
    [
        "source_family",
        "current_source_status",
        "materialized_cases",
        "current_line_interpretation",
        "first_slice_usage",
    ],
)}

### Interpretation
This table highlights that the benchmark is already organized through source-family roles rather than simple flat query accumulation.

---

## 6. Case-maturity appendix table

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
    ],
)}

### Interpretation
The appendix maturity table makes the repository boundary explicit:
- some cases are already stable enough for early reporting,
- while others remain intentionally staged.

---

## 7. Recommended current use

This appendix is most useful for:
- early appendix drafting,
- evaluation-section support,
- and explicit explanation of first-slice inclusion boundaries.

It should not be used to imply:
- full pilot-scale readiness,
- complete source-universe closure,
- or broad baseline-comparison readiness.
"""
    return md


def main() -> int:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(build_appendix_md(), encoding="utf-8")
    print(f"wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())