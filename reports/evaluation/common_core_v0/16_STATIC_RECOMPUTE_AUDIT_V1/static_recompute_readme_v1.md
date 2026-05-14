# Static Recompute Audit V1 README

## Inputs Inspected
This audit reads Round 15A outputs and retained Common-core v0 denominator, taxonomy, hard-negative, failure-accounting, timing, observability, PORT, verifier, and artifact-map CSV artifacts.

## Outputs Created
The directory contains exactly five audit files: `static_recompute_results_v1.csv`, `static_recompute_mismatches_v1.csv`, `static_recompute_readiness_update_v1.csv`, `static_recompute_summary_v1.md`, and `static_recompute_readme_v1.md`.

## Formulas Used
Integer denominator and outcome counts use direct counts or retained accounting identities. GM speedup is `exp(mean(log(speedup_ratio)))` over exact + timing-success rows. Median speedup is the median retained speedup ratio. Regression@20 is `count(speedup_ratio < 0.8) / timing_denominator`. Taxonomy top tags sort by descending case coverage, then tag name.

## Tolerance / Rounding Policy
Integer counts require exact equality. String-valued retained categories require exact equality. Floating-point values are exact matches when strings match, rounded matches when decimal difference is less than `1e-9`, or when a retained rounded value matches four-decimal rounding.

## What Was Not Recomputed
R-Bot timing, SQLGlot combined 240 timing, and Direct LLM repair mixed-source timing are artifact-only summary rows. SpeedupTransferRate is expected NA because paired target-engine timing is absent. Full NodeAlignmentCoverage is expected NA/future work because only a selected PG frontier is retained. SQLSolver proof/refute verdict split is not recomputed because detailed verdict rows are not retained.

## How To Use Before Submission
Use `static_recompute_results_v1.csv` as the row-level audit ledger, `static_recompute_mismatches_v1.csv` as the narrow erratum queue, and `static_recompute_readiness_update_v1.csv` to decide which metric groups can support the final Section 8 render. If the mismatch file has no data rows, no Round 15B source-of-truth writeback is indicated.
