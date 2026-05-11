# Final Timing Summary

| method_id | route_id | denominator_id | planned_rows | final_exact_rows | timing_scope | timing_attempted_rows | timing_success_rows | timing_failed_rows | median_speedup | gm_speedup | win_count | tie_count | loss_count | regression_20pct_count | regression_rate_20pct | best_case_id | best_case_engine | best_case_speedup | worst_case_id | worst_case_engine | worst_case_speedup | claim_boundary | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| direct_llm | direct_llm_execute_repair_1shot | common_core_v0_40_same_engine_120 | 120 | 96 | mixed_source_timing_full_final_exact_rows | 96 | 96 | 0 | 1.009402551073825 | 1.0430582867389244 | 23 | 67 | 6 | 4 | 0.041666666666666664 | CONS_0012 | pg | 1.707530829371433 | PERF_0007 | pg | 0.6948993689766564 | Timing is mixed-source only if the retained 94 original exact timing rows are merged with newly repaired exact-row timing. | GM speedup and Regression@20 are computed only on timing_success rows. |

Timing claims depend on the actual timing scope.
