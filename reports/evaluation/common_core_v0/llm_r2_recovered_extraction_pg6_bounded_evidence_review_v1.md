# LLM-R2 Recovered-Extraction PG6 Bounded Evidence Review v1

This is governance review only.

No LLM-R2 inference, PostgreSQL, checker, timing, speedup, MySQL, or Spark
command was run for this packet.

## Scope

This packet freezes bounded recovered-extraction-route PostgreSQL evidence for
`llm_r2` on 6 Common-core PG rows only:

- `PERF_0008`
- `PERF_0017`
- `PERF_0019`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`

Boundary:

- `route_id = llm_r2_recovered_extraction_route_v1`
- `bounded_recovered_pg_rows = 6`
- `generated_rows = 6`
- `pg_source_executed_rows = 6`
- `pg_generated_executed_rows = 6`
- `exact_match_rows = 6`
- `timing_rows = 0`
- `mysql_rows = 0`
- `spark_rows = 0`
- `full120_evidence = no`
- `leaderboard_comparable = no`

Important separation:

- This is recovered-extraction-route evidence, not original-route evidence.
- The frozen original-route PG9 packet remains unchanged:
  `9/9` generated, `3/9` exact-match, `6/9` `execution_failed`.
- This packet does not merge original-route PG3 and recovered-route PG6 into a
  single recovered PG9 row.
- Recovered PG9 must not be claimed unless `PERF_0006`, `PERF_0013`, and
  `PERF_0024` are separately rerun under the recovered route.

## Evidence Inspected

- [llm_r2_recovered_extraction_perf0008_generation_canary_01](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_perf0008_generation_canary_01)
- [llm_r2_recovered_extraction_perf0008_pg_execution_checker_canary_01](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_perf0008_pg_execution_checker_canary_01)
- [llm_r2_recovered_extraction_pg5_generation_expansion_01](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_pg5_generation_expansion_01)
- [llm_r2_recovered_extraction_pg5_pg_execution_checker_01](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_pg5_pg_execution_checker_01)
- [llm_r2_pg9_bounded_evidence_reconciliation_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.md)
- [llm_r2_extraction_wrapper_recovery_audit_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_extraction_wrapper_recovery_audit_v1.md)
- [llm_r2_recovered_extraction_route_plan_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_recovered_extraction_route_plan_v1.md)
- [llm_r2_recovered_extraction_execute_mode_plan_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_recovered_extraction_execute_mode_plan_v1.md)

## Evidence Rollup

| method_id | route_or_scope | denominator_scope | case_count | generation_attempted_rows | generated_rows | source_executed_rows | generated_executed_rows | exact_match_rows | execution_failed_rows | timing_rows | leaderboard_comparable | paper_table_placement |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `llm_r2` | `llm_r2_recovered_extraction_route_v1` | `common_core_v0_llm_r2_recovered_pg_supported_6` | `6` | `6` | `6` | `6` | `6` | `6` | `0` | `0` | `no` | `bounded_pg_only_appendix_evidence` |

## Per-Case Table

| case_id | engine | generated_status | source_execution_status | generated_execution_status | exact_match | failure_bucket | retained_run_artifact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0008` | `pg` | `generated` | `executed` | `executed` | `true` | `exact_match` | [perf0008 canary pair](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_perf0008_pg_execution_checker_canary_01) | generation came from the single-case recovered-route canary; checker came from the single-case PostgreSQL canary with semicolon-normalized execution copy only |
| `PERF_0017` | `pg` | `generated` | `executed` | `executed` | `true` | `exact_match` | [pg5 checker workspace](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_pg5_pg_execution_checker_01/workspaces/PERF_0017/pg/result_check.json) | recovered-route generation retained separately from original-route PG9 packet |
| `PERF_0019` | `pg` | `generated` | `executed` | `executed` | `true` | `exact_match` | [pg5 checker workspace](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_pg5_pg_execution_checker_01/workspaces/PERF_0019/pg/result_check.json) | recovered-route exact-match retained under PG5 checker run |
| `PERF_0033` | `pg` | `generated` | `executed` | `executed` | `true` | `exact_match` | [pg5 checker workspace](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_pg5_pg_execution_checker_01/workspaces/PERF_0033/pg/result_check.json) | recovered-route exact-match retained under PG5 checker run |
| `PERF_0052` | `pg` | `generated` | `executed` | `executed` | `true` | `exact_match` | [pg5 checker workspace](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_pg5_pg_execution_checker_01/workspaces/PERF_0052/pg/result_check.json) | this row was an original-route malformed CTE-WITH failure but exact-matched under the separate recovered route |
| `PERF_0054` | `pg` | `generated` | `executed` | `executed` | `true` | `exact_match` | [pg5 checker workspace](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_pg5_pg_execution_checker_01/workspaces/PERF_0054/pg/result_check.json) | recovered-route exact-match retained under PG5 checker run |

## Retained Artifact Table

| scope | artifact |
| --- | --- |
| `PERF_0008` generation canary | [generated_sql_schema_native_recovered_extraction_v1.sql](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_perf0008_generation_canary_01/retained_route_artifacts/PERF_0008/generated_sql_schema_native_recovered_extraction_v1.sql) |
| `PERF_0008` checker canary | [checker_result_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_perf0008_pg_execution_checker_canary_01/retained_checker_artifacts/checker_result_v1.json) |
| PG5 generation expansion | [llm_r2_recovered_extraction_pg5_generation_ledger.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_pg5_generation_expansion_01/llm_r2_recovered_extraction_pg5_generation_ledger.csv) |
| PG5 checker run | [llm_r2_recovered_extraction_pg5_pg_execution_checker_ledger.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_pg5_pg_execution_checker_01/llm_r2_recovered_extraction_pg5_pg_execution_checker_ledger.csv) |
| non-timing/non-speedup boundary | [pg5 attestation](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_pg5_pg_execution_checker_01/validation/no_timing_speedup_mysql_spark_full120_attestation.txt) |
| canary boundary | [perf0008 canary attestation](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_recovered_extraction_perf0008_pg_execution_checker_canary_01/validation/no_timing_speedup_mysql_spark_expansion_attestation.txt) |

## Exact-Match Summary

Retained recovered-route evidence supports:

- `6/6` generation attempts
- `6/6` retained generated SQL outputs
- `6/6` PostgreSQL source executions
- `6/6` PostgreSQL generated executions
- `6/6` exact-match checker outcomes

This packet therefore freezes recovered-route PG6 bounded evidence only.

## Non-Claims

- This does not create a leaderboard.
- This does not update `method_comparison_summary_v2`.
- This does not create a full PG40 row.
- This does not create a full `120`-row LLM-R2 row.
- This does not claim recovered PG9 evidence.
- This does not claim MySQL/Spark support.
- This does not claim timing or speedup.
- This does not create a result card or proposed row.
- This does not reinterpret the frozen original-route PG9 packet in place.

## Next Recommended Gate

Human decide whether to preserve LLM-R2 recovered-extraction PG6 as separate
bounded appendix evidence, or authorize recovered-route PG3 reruns before any
broader recovered-route claim.
