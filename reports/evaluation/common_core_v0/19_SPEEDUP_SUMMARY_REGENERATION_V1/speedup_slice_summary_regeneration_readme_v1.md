# Speedup Slice Summary Regeneration V1

## Purpose
This static script regenerates `speedup_slice_summary_v1.csv` from retained Common-core v0 timing artifacts and compares the regenerated rows against the retained Round 4 target.

## Inputs Read
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv`
- `reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/method_timing_case_level_v1.csv`
- `reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/speedup_slice_summary_v1.csv`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_resolved_01/timing_event_long.csv`: 94 CSV rows; direct_llm_same_engine_rewrite=94
- `reports/evaluation/common_core_v0/runs/sqlglot_full_per_case_timing_01/timing_event_long.csv`: 135 CSV rows; sqlglot_optimize_same_dialect=63, sqlglot_transpile_same_dialect_noop=72
- `reports/evaluation/common_core_v0/runs/calcite_hep_93_exact_timing_01/timing_event_long.csv`: 93 CSV rows; calcite_hep_pg_rewrite=21, calcite_hep_same_engine_rewrite=72
- `reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_timing_event_long.csv`: 2 CSV rows; direct_llm_execute_repair_1shot=2
- `reports/evaluation/common_core_v0/runs/r_bot_pg15_timing_expansion_02/run_results.json`: 15 JSON records; current_benchmark_metric_evidence=False

## Outputs Written
- `reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/speedup_slice_summary_regenerated_v1.csv`
- `reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/speedup_slice_summary_regeneration_diff_v1.csv`
- `reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/speedup_slice_summary_regeneration_readme_v1.md`

## Formula Policy
- Eligibility: retained exact + timing-success case-level rows with numeric `speedup_ratio`.
- Speedup ratio: retained `speedup_ratio`; if a future retained row omits it, compute as source median/runtime divided by rewrite median/runtime before aggregation.
- GM speedup: `exp(mean(log(speedup_ratio)))`.
- Median speedup: median over retained eligible `speedup_ratio` values.
- Win/tie/loss: win if `speedup_ratio > 1.05`, tie if `0.95 <= speedup_ratio <= 1.05`, loss if `speedup_ratio < 0.95`.
- Regression@20: `count(speedup_ratio < 0.8) / timing_denominator`.

## Recomputed Routes
- `direct_llm/direct_llm_same_engine_rewrite`
- `sqlglot/sqlglot_optimize_same_dialect`
- `sqlglot/sqlglot_transpile_same_dialect_noop`
- `calcite_hep/calcite_hep_fail_closed_120`

## Artifact-Only Routes
- `direct_llm/direct_llm_execute_repair_1shot`
- `r_bot/r_bot_same_engine_rewrite`
- `sqlglot/sqlglot_combined_same_engine_240`

Direct LLM repair remains artifact-only for the full 96-row mixed-source timing slice because only two repair-specific lower-level rows are retained. R-Bot remains artifact-only because the retained PG15 JSON is bounded appendix evidence and is marked `current_benchmark_metric_evidence=false`. SQLGlot combined 240 remains artifact-only because it is a diagnostic route-family aggregate, not a single method route.

## Comparison Summary
- exact_match: 64
- rounded_match: 4
- artifact_only_match: 51
- conflict_needs_human_review: 0
- missing_input: 0

## Boundary
This script does not run database engines, LLM/model calls, verifier tools, PORT9, EXPLAIN collection, or new timing collection. It does not change retained source artifacts, metrics, denominators, taxonomy, registries, case facts, protocol, paper claims, or paper prose.

## Source-of-Truth Writeback Judgment
No source-of-truth writeback is needed if the diff contains no `conflict_needs_human_review` or `missing_input` rows.
