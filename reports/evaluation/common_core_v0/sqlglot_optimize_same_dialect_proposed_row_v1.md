# SQLGlot Optimize Same-Dialect Proposed Row v1

This is a proposed paper-facing denominator-aware route row for later review.
It does not update `method_comparison_summary_v2` in this task.

| field | value |
|---|---|
| `method_id` | `sqlglot` |
| `route_id` | `sqlglot_optimize_same_dialect` |
| `method_family` | `sqlglot` |
| `evidence_type` | `route_level_same_engine_preview` |
| `generation_or_route_denominator_id` | `common_core_v0_40_same_engine_120_optimize_route` |
| `execution_or_ready_denominator_id` | `attempted_75_on_optimize_route` |
| `timing_denominator_id` | `timing_success_65_on_optimize_route` |
| `engine_scope` | `tri_engine_same_engine` |
| `planned_generation_or_route_rows` | `120` |
| `generated_or_ready_rows` | `75` |
| `executed_rows` | `65` |
| `match_exact_rows` | `65` |
| `timing_success_rows` | `65` |
| `denominator_caveat` | `Single SQLGlot same-engine route only; not cross-dialect portability evidence and not a full SQLGlot method-family aggregate row` |
| `leaderboard_comparable` | `no` |
| `executable_rate` | `0.5417` |
| `result_consistency_rate` | `0.5417` |
| `negative_rejection_rate` | `NA_not_computed` |
| `gm_speedup` | `1.0168` |
| `regression_rate_20pct` | `0.0615` |
| `cross_engine_executable_rate` | `NA_not_computed` |
| `cross_engine_consistency_rate` | `NA_not_computed` |
| `speedup_transfer_rate` | `NA_not_computed` |
| `verifier_support_rate` | `NA_not_computed` |
| `plan_parse_rate` | `NA_not_computed` |
| `node_alignment_coverage` | `NA_not_computed` |
| `attribution_coverage` | `NA_not_computed` |
| `material_regression_rows` | `NA_not_computed` |
| `high_variance_watchlist` | `NA_not_computed` |
| `caveat` | `Proposed paper row only. SQLGlot optimize_same_dialect is a same-engine route-level evidence row. It is denominator-aware route evidence, not cross-dialect portability evidence, not a full SQLGlot method-family aggregate, and not a leaderboard-comparable scalar unless retained timing/speedup evidence explicitly supports that boundary. Unsupported, failed, and no-op rows remain explicit in denominator accounting.` |
| `source_summary_files` | `reports/evaluation/common_core_v0/sqlglot_paper_route_audit_v1.md; reports/evaluation/common_core_v0/sqlglot_validity_summary_v1.md; reports/evaluation/common_core_v0/sqlglot_speedup_summary_v1.md; reports/evaluation/common_core_v0/method_comparison_summary_v2.md` |
