This is a retained-artifact preflight only.
No DB/checker/timing/EXPLAIN/LLM/verifier run was performed in this cleanup step.

What this file answers: why some PostgreSQL attribution candidates remain blocked.
Selected cases: none; this is a gap summary for the future EXPLAIN ANALYZE packet.
This does not support full-denominator observability. Claims that must not be made: denominator-wide attribution readiness.

中文说明：这里只做字段规范化与展示一致性清理，不新增实验结论。

| gap_id | scope | current_status | blocking_reason | affected_rows | can_be_fixed_by_aggregation_only | requires_new_execution | priority | recommended_next_step | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pg_attr_gap_01 | direct_llm_execute_repair_1shot | 32_preserved_pg_exact_rows_blocked_for_route_specific_attribution | mixed_source_final_exact_row_without_route_specific_repair_timing_trace | 32 | no | yes | high | keep only the 2 newly repaired PG exact rows in the first route-specific repair attribution run | Preserved rows remain useful for final-outcome accounting but not for route-specific repair attribution. |
| pg_attr_gap_02 | failure_diagnostic_rows | blocked_for_exact_timed_attribution_but_useful_for_failure_observability | failure_diagnostic_row_not_exact_timed | 1 | no | yes | medium | keep the failure exemplar separate from the 20-30-row exact-timed attribution run | This row should strengthen failure-side Table 10 narrative, not the exact-timed attribution pool. |
| pg_attr_gap_03 | main_routes_overall | 113_ready_pg_exact_timed_candidates_available | none_for_ready_rows | 0 | not_applicable | yes | resolved_for_preflight | review and approve a first 24-row EXPLAIN ANALYZE BUFFERS packet | Ready rows already cover all 5 main method routes with PG exact-timed evidence. |
