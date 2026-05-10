# Calcite HEP Method Comparison Proposed Row v1

This is a proposed denominator-aware evidence row for later review. It does not
update `method_comparison_summary_v2` in this task.

| field | value |
|---|---|
| `method_id` | `calcite_hep` |
| `route_id` | `calcite_hep_common_core_v0_fail_closed_ledger` |
| `method_family` | `calcite_hep` |
| `evidence_type` | `tri_engine_fail_closed_ledger_preview` |
| `generation_or_route_denominator_id` | `common_core_v0_40_same_engine_120` |
| `execution_or_ready_denominator_id` | `fail_closed_exact_match_ledger_on_common_core_v0_40_same_engine_120` |
| `timing_denominator_id` | `NA_not_computed` |
| `engine_scope` | `tri_engine_same_engine_fail_closed_mixed_evidence` |
| `planned_generation_or_route_rows` | `120` |
| `generated_or_ready_rows` | `96` |
| `executed_rows` | `95` |
| `match_exact_rows` | `93` |
| `timing_success_rows` | `NA_not_computed` |
| `denominator_caveat` | `Retained PG40 route evidence plus bounded non-PG MySQL/Spark expansion and bounded recovery-canary evidence synthesized into a fail-closed 120-row correctness ledger; not a full timing packet and not leaderboard-comparable` |
| `leaderboard_comparable` | `no` |
| `executable_rate` | `0.7917` |
| `result_consistency_rate` | `0.7750` |
| `negative_rejection_rate` | `NA_not_computed` |
| `gm_speedup` | `NA_not_computed` |
| `regression_rate_20pct` | `NA_not_computed` |
| `cross_engine_executable_rate` | `NA_not_computed` |
| `cross_engine_consistency_rate` | `NA_not_computed` |
| `speedup_transfer_rate` | `NA_not_computed` |
| `verifier_support_rate` | `NA_not_computed` |
| `plan_parse_rate` | `NA_not_computed` |
| `node_alignment_coverage` | `NA_not_computed` |
| `attribution_coverage` | `NA_not_computed` |
| `material_regression_rows` | `NA_not_computed` |
| `high_variance_watchlist` | `NA_not_computed` |
| `caveat` | `Proposed paper row only. Treat parser failures, HEP rewrite failures, setup failures, execution failures, and mismatches as non-exact in-denominator rows. The bounded recovery chain lifts the fail-closed ledger from 70/120 to 93/120 but does not make the row timing-backed or leaderboard-comparable. Requires a separate paper-readiness check before canonical table integration.` |
| `source_summary_files` | `reports/evaluation/common_core_v0/calcite_hep_120_fail_closed_synthesis_v1.md; reports/evaluation/common_core_v0/calcite_hep_120_recovery_canary_08_result_card_v1.md; reports/evaluation/common_core_v0/calcite_hep_120_recovery_round2_canary_09_result_card_v1.md; reports/evaluation/common_core_v0/calcite_hep_120_recovery_round4b_numeric_scale_canary_04_result_card_v1.md; reports/evaluation/common_core_v0/calcite_hep_120_recovery_perf0035_canary_03_result_card_v1.md; reports/evaluation/common_core_v0/calcite_hep_validity_summary_v1.md; reports/evaluation/common_core_v0/calcite_hep_speedup_summary_v1.md; reports/evaluation/common_core_v0/calcite_hep_mysql_spark_execution_expansion_result_card_v1.md` |
