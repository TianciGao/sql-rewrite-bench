# Direct LLM Same-Engine Proposed Row v1

This is a proposed paper-facing denominator-aware route row for later review.
It does not update `method_comparison_summary_v2` in this task.

| field | value |
|---|---|
| `method_id` | `direct_llm` |
| `route_id` | `direct_llm_same_engine_rewrite` |
| `method_family` | `direct_llm` |
| `evidence_type` | `route_summary` |
| `generation_or_route_denominator_id` | `common_core_v0_40` |
| `execution_or_ready_denominator_id` | `ready_to_execute_115` |
| `timing_denominator_id` | `timing_success_94_on_common_core_v0_40` |
| `engine_scope` | `tri_engine_same_engine` |
| `planned_generation_or_route_rows` | `120` |
| `generated_or_ready_rows` | `115` |
| `executed_rows` | `99` |
| `match_exact_rows` | `94` |
| `timing_success_rows` | `94` |
| `denominator_caveat` | `Single-route same-engine packet on 120 planned rows; timing is valid only on the retained timing_success_94_on_common_core_v0_40 subset; unsupported, blocked, failed, and mismatched rows remain explicit in denominator accounting` |
| `leaderboard_comparable` | `no` |
| `executable_rate` | `0.8250` |
| `result_consistency_rate` | `0.7833` |
| `negative_rejection_rate` | `NA_not_computed` |
| `gm_speedup` | `1.0436` |
| `regression_rate_20pct` | `0.0319` |
| `cross_engine_executable_rate` | `NA_not_computed` |
| `cross_engine_consistency_rate` | `NA_not_computed` |
| `speedup_transfer_rate` | `NA_not_computed` |
| `verifier_support_rate` | `NA_not_computed` |
| `plan_parse_rate` | `NA_not_computed` |
| `node_alignment_coverage` | `NA_not_computed` |
| `attribution_coverage` | `NA_not_computed` |
| `material_regression_rows` | `NA_not_computed` |
| `high_variance_watchlist` | `NA_not_computed` |
| `caveat` | `Proposed paper row only. This is same-engine Direct LLM rewrite evidence. It is denominator-aware evidence, not a final ranked leaderboard scalar, and not cross-dialect portability evidence. GM speedup is timing-denominator scoped. Unsupported, blocked, failed, and mismatch rows remain explicit in denominator accounting. Direct LLM has strong retained same-engine evidence, but this proposed row does not promote it into canonical status.` |
| `source_summary_files` | `reports/evaluation/common_core_v0/direct_llm_validity_summary_v1.md; reports/evaluation/common_core_v0/direct_llm_validity_summary_v1.csv; reports/evaluation/common_core_v0/direct_llm_speedup_summary_v1.md; reports/evaluation/common_core_v0/direct_llm_speedup_summary_v1.csv; reports/evaluation/common_core_v0/method_comparison_summary_v2.md` |
