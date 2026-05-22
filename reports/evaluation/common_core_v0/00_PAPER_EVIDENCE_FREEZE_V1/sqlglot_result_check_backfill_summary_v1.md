# SQLGlot Result Check Backfill Summary v1

This is checker backfill only. No timing/LLM/verifier/EXPLAIN run was performed. SQLGlot routes remain separated.

## Table

| route_id | expected_exact_rows_from_table6 | rows_checked | exact_rows_after_backfill | mismatch_rows_after_backfill | source_execution_failed_rows | candidate_execution_failed_rows | blocked_rows | checker_failed_rows | timing_denominator_ready_rows | denominator_status | recommended_next_step | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sqlglot_transpile_same_dialect_noop | 72 | 72 | 72 | 0 | 0 | 0 | 0 | 0 | 72 | timing_ready | Route-separated timing run may proceed on exact rows after backfill. | No-op route backfill is based on the reconstructed 72-row exact frontier. |
| sqlglot_optimize_same_dialect | 65 | 65 | 63 | 0 | 0 | 0 | 0 | 2 | 63 | timing_ready_with_revised_exact_denominator | Route-separated timing run may proceed on exact rows after backfill. | Optimize route includes 56 reconstructed rows plus 9 PORT execution-only rows rechecked here. |

## Notes

- 中文说明：这里补的是逐行 result_check 证据，不是刷新 Table 6 计时结果。
- `sqlglot_combined_same_engine_240` 仍然不是主 timing denominator。
