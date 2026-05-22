# Calcite HEP MySQL/Spark Execution Expansion Result Card v1

Calcite HEP was extended beyond PostgreSQL with explicit MySQL/Spark
target-dialect rendering. In the bounded non-PG expansion, `60/80`
MySQL/Spark rows produced retained target-dialect SQL. Execution-validity was
run on those `60` rows: `59/60` executed and `49/60` matched exactly. The
remaining rows include `10` exact-output mismatches and `1` Spark setup
artifact. This is bounded execution-validity evidence, not timing, speedup,
leaderboard, or full `120`-row comparable evidence.

## Denominator Table

| Scope | Rows |
|---|---:|
| Full common-core same-engine denominator | `120` |
| Non-PG MySQL/Spark expansion denominator | `80` |
| Rewrite-success denominator used for execution | `60` |
| Executed rows | `59` |
| Exact-match rows | `49` |
| Mismatch rows | `10` |
| Setup-failed rows | `1` |

## By-Engine Summary

- MySQL: planned `28`, executed `28`, match_exact `23`, mismatch `5`, setup_failed `0`
- Spark: planned `32`, executed `31`, match_exact `26`, mismatch `5`, setup_failed `1`

## Failure / Mismatch Summary

- `PERF_0006:mysql`, `PERF_0006:spark`:
  `aggregate_rewrite_precision_decimal_scale_loss`
- `PERF_0035:mysql`, `PERF_0035:spark`:
  `rewrite_output_shape_changed_extra_column_and_scale_loss`
- `PERF_0062:mysql`, `PERF_0062:spark`:
  `numeric_format_scale_loss`
- `LONGTAIL_0012:mysql`, `LONGTAIL_0012:spark`:
  `numeric_format_scale_loss`
- `LONGTAIL_0013:mysql`, `LONGTAIL_0013:spark`:
  `numeric_format_scale_loss`
- `PERF_0077:spark`:
  `schema_setup_artifact_comment_only_ddl_fragment`

## Boundary

- This result should not be read as `120`-row tri-engine leaderboard evidence.
- It should not be used for timing or speedup except on the explicit `49`
  `match_exact` rows.
- It does not change `method_comparison_summary_v2` in this task.
- It is suitable for paper discussion as bounded non-PG Calcite HEP
  feasibility / validity evidence.

## Paper-Safe Wording

`Calcite HEP was extended beyond PostgreSQL with explicit MySQL/Spark target-dialect rendering. In the bounded non-PG expansion, 60/80 MySQL/Spark rows produced retained target-dialect SQL. Execution-validity was run on those 60 rows: 59/60 executed and 49/60 matched exactly. The remaining rows include 10 exact-output mismatches and 1 Spark setup artifact. This is bounded execution-validity evidence, not timing, speedup, leaderboard, or full 120-row comparable evidence.`

## Source Artifacts

- rewrite expansion triage:
  [rewrite_expansion_80_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_rewrite_expansion_80_01/rewrite_expansion_80_triage.md)
- execution expansion triage:
  [execution_expansion_60_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_execution_expansion_60_01/execution_expansion_60_triage.md)
- execution expansion records:
  [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_execution_expansion_60_01/run_results.json)
