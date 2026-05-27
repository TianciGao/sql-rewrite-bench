# Repair Result Summary

| method_id | route_id | denominator_id | planned_rows | original_exact_rows | non_exact_frontier_rows | repair_ready_rows | repair_blocked_rows | repair_llm_call_success_rows | repair_output_accepted_rows | repair_executed_rows | repair_exact_rows | exact_gain_over_original | final_exact_rows | final_exact_rate | final_non_exact_rows | final_execution_failed_rows | final_mismatch_rows | final_extraction_failed_rows | final_blocked_rows | claim_boundary | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| direct_llm | direct_llm_execute_repair_1shot | common_core_v0_40_same_engine_120 | 120 | 94 | 26 | 21 | 5 | 21 | 21 | 21 | 2 | 2 | 96 | 0.8 | 24 | 18 | 1 | 0 | 5 | Feedback-aware extension of Direct LLM only; not a replacement and not a final ranked leaderboard. | Blocked rows remain visible and unrepaired. |

This run is a feedback-aware protocol baseline only.
