# Calcite HEP MySQL/Spark Canary Result Card v1

This is bounded canary evidence, not a full MySQL/Spark evaluation.

## Scope

- `method_id = calcite_hep`
- `route_id = calcite_hep_same_engine_rewrite`
- cases: `PERF_0006`, `PERF_0007`, `CONS_0005`
- engines: `MySQL`, `Spark`
- planned rows = `6`

## Rewrite Canary v2

The bounded target-dialect rewrite canary produced:

- target-dialect SQL generated = `6 / 6`
- MySQL target-dialect rewrite = `3 / 3`
- Spark target-dialect rewrite = `3 / 3`

Dialect classes used:

- `org.apache.calcite.sql.dialect.MysqlSqlDialect`
- `org.apache.calcite.sql.dialect.SparkSqlDialect`

## Execution / Validity Canary

The bounded execution canary produced:

- executed = `6 / 6`
- match_exact = `4 / 6`
- mismatch = `2 / 6`

Mismatch rows:

- `PERF_0006:mysql`
- `PERF_0006:spark`

## Mismatch Root Cause

Best retained root-cause classification:

- `aggregate_rewrite_precision_decimal_scale_loss`

The generated AVG-like aggregate rewrite introduced `DECIMAL(15,0)` scale loss,
causing `avg_disc = 0.075000` in the source result to become `avg_disc = 0` in
the generated result. That is a semantic mismatch, not just output formatting.

## Boundary

- no timing was computed
- no speedup was computed
- `method_comparison_summary_v2` remains unchanged
- this does not create leaderboard-comparable evidence

If timing is ever attempted, it should use only the explicit `match_exact_4`
denominator:

- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

## Paper-Safe Wording

`Calcite HEP was extended in a bounded MySQL/Spark canary with explicit target-dialect rendering. The canary generated 6/6 target-dialect SQL candidates and all 6 executed, but only 4/6 matched exactly. The two mismatches were both PERF_0006 and were caused by aggregate rewrite precision / decimal scale loss. Therefore this is useful boundary evidence, but not full MySQL/Spark correctness, timing, speedup, or leaderboard evidence.`

## Source Artifacts

- rewrite triage:
  [rewrite_canary_v2_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_canary_02/rewrite_canary_v2_triage.md)
- execution triage:
  [execution_canary_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_execution_canary_02/execution_canary_triage.md)
- execution records:
  [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_execution_canary_02/run_results.json)
