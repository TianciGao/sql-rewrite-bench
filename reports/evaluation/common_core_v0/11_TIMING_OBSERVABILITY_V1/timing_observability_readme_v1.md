# Timing Observability Readme v1

## Inputs inspected

- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv`
- `reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_missing_data_ledger_v1.csv`
- `reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_existing_values_patch_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/pg_plan_attribution_113_summary_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_failure_exemplar_selection_v1.csv`
- Retained timing ledgers:
  - `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_resolved_01/timing_event_long.csv`
  - `reports/evaluation/common_core_v0/runs/sqlglot_full_per_case_timing_01/timing_event_long.csv`
  - `reports/evaluation/common_core_v0/runs/calcite_hep_93_exact_timing_01/timing_event_long.csv`
  - `reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_timing_event_long.csv`

## Outputs created

- `speedup_slice_summary_v1.csv`
- `speedup_slice_summary_v1.md`
- `method_timing_case_level_v1.csv`
- `selected_plan_observability_frontier_v1.csv`
- `selected_plan_observability_frontier_v1.md`
- `timing_observability_readme_v1.md`

## Timing aggregation rules

- `table6_performance_on_exact_timed_rows_v4.csv` is the canonical route-level speedup source.
- Timing denominators, GM, median, win/tie/loss, Regression@20, and best/worst are copied directly from retained Table 6 rows.
- Missing per-case timing arrays are not recomputed from summaries.
- `sqlglot_combined_same_engine_240` stays an aggregate route-family view rather than a single method row.

## Case-level timing availability

- Full retained per-case timing rows exist for:
  - `direct_llm_same_engine_rewrite` (`94` rows)
  - `sqlglot_transpile_same_dialect_noop` (`72` rows)
  - `sqlglot_optimize_same_dialect` (`63` rows)
  - `calcite_hep_fail_closed_120` (`93` rows after route normalization)
- Repair retains only `2` route-specific new exact timing rows; the full final `96` row summary is mixed-source and therefore also gets a `route_summary_only` availability row.
- `r_bot_same_engine_rewrite` and `sqlglot_combined_same_engine_240` retain route-level summary evidence only in this packet.

## Selected observability aggregation rules

- Preferred frontier source is `table10_plan_attribution_case_study_v6.csv`.
- Delta-class and confidence labels are copied directly from retained selected-plan artifacts.
- Failure exemplar handling comes from `table10_failure_exemplar_selection_v1.csv` and stays separate from the exact-timed attribution denominator.
- No cross-engine or denominator-wide plan attribution is inferred.

## Delta-class and confidence handling

- Selected frontier rows preserve the retained `delta_class` and `confidence` values exactly.
- Wider packet context is retained in `pg_plan_attribution_113_summary_v1.csv`, but this Round 4 frontier table remains selected-case only.

## Known limitations

- Direct LLM repair timing is mixed-source for the full exact denominator; only the two newly repaired rows are route-specific per-case timing artifacts.
- No full-denominator NodeAlignmentCoverage is claimed.
- Failure-side diagnosis is retained, but it is not a plan-attribution success row.
- Bounded prior methods remain bounded appendix evidence.

## Whether source-of-truth writeback is needed

- No. These are evidence-freeze aggregation artifacts only.
