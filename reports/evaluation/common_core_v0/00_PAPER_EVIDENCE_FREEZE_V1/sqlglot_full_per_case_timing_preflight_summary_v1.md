# SQLGlot Full Per-Case Timing Preflight Summary v1

This is preflight only. No DB/checker/timing/LLM/verifier/EXPLAIN run was performed.

SQLGlot routes remain route-separated. `sqlglot_combined_same_engine_240` is not a main timing denominator.

## Table

| route_id | denominator_id | route_planned_rows | expected_exact_rows_from_table6 | reconstructed_exact_rows | timing_ready_rows | blocked_rows | missing_source_sql_rows | missing_candidate_sql_rows | missing_schema_rows | missing_result_check_rows | preflight_status | recommended_next_step | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sqlglot_transpile_same_dialect_noop | common_core_v0_40_same_engine_120 | 120 | 72 | 72 | 0 | 72 | 0 | 0 | 0 | 72 | blocked_missing_required_artifacts | Recover retained row-level result_check or equivalent exact-match artifact before any timing run. | Row identities are reconstructable, but exact-match evidence is not retained at row level. |
| sqlglot_optimize_same_dialect | common_core_v0_40_same_engine_120 | 120 | 65 | 56 | 0 | 56 | 0 | 0 | 0 | 56 | blocked_exact_denominator_not_reconstructed | Recover row-level exact-evidence packet for missing route rows before any timing run. | Current retained row-level artifacts reconstruct fewer exact rows than the paper-facing aggregate count. |
| aggregate_summary_only | aggregate_summary_only | 240 | 137 | 128 | 0 | 128 | 0 | 0 | 0 | 128 | aggregate_summary_only | Keep SQLGlot routes separated; do not use sqlglot_combined_same_engine_240 as a main timing denominator. | Diagnostic aggregate only; not a main route-specific timing denominator. |

## Interpretation Notes

- 中文说明：`noop` 路线的 72 行可以逐行重建，但还不能直接批准计时。
- `optimize` 路线当前只能重建 56 行；与 Table 6 的 65 行 aggregate 分母还有 9 行差距。
- 下一步应先补回 exact-match retained artifacts，再考虑真正的 route-separated timing run。
