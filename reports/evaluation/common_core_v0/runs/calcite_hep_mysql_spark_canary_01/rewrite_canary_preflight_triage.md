# Calcite HEP MySQL/Spark Rewrite Canary Preflight Triage

This is a read-only triage for the retained `calcite_hep_mysql_spark_canary_01`
preflight result. It is preflight evidence only. It is not rewrite success
evidence, not execution evidence, not correctness evidence, and not timing or
speedup evidence.

## Headline Status

- planned rows = `6`
- preflight_blocked rows = `6`
- rewrite_attempted rows = `0`
- generated / rewrite_success rows = `0`
- status = `preflight_failed`
- failure_category = `target_engine_dialect_not_implemented`

## Exact Blocker

Blocked category:

- `target_engine_dialect_not_implemented`

Blocked reason:

- visible `CalciteHepRewriteSmoke.java` renders with
  `PostgresqlSqlDialect` and does not expose `MysqlSqlDialect` or
  `SparkSqlDialect` output routing

Observed retained wrapper state:

- `wrapper_has_mysql_renderer = false`
- `wrapper_has_spark_renderer = false`
- `wrapper_uses_postgresql_dialect = true`

## What This Is Not

- not broad MySQL/Spark artifact absence
- not MySQL/Spark execution failure
- not correctness = `0`
- not timing evidence
- not speedup evidence

The selected canary cases already have retained same-engine source, schema, and
witness artifacts for both MySQL and Spark. The blocker occurs before any
rewrite attempt because the current visible wrapper does not provide target
engine dialect rendering for those engines.

## Why The Canary Stopped

The retained canary package is fail-closed by design. It refuses to count
PostgreSQL-shaped output as same-engine MySQL or Spark rewrite evidence.

Current visible behavior:

- parse path may accept non-PG input paths for the selected canary rows
- output path still routes through `PostgresqlSqlDialect`
- no visible `MysqlSqlDialect` renderer is exposed
- no visible `SparkSqlDialect` renderer is exposed

So the package correctly stops at preflight instead of silently generating
PG-shaped SQL under MySQL or Spark labels.

## Row-Level Outcome

All six planned rows were blocked at the same package-level preflight:

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

There is no row-level variation here. The blocker is uniform and package-level.

## Current Evidence Boundary

Current Calcite HEP retained benchmark evidence remains PostgreSQL-only:

- validity summary:
  [calcite_hep_validity_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_validity_summary_v1.md)
- speedup summary:
  [calcite_hep_speedup_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_speedup_summary_v1.md)
- denominator-aware comparison ledger:
  [method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md)

That PG-only status should remain unchanged from this canary preflight result.

## Recommended Next Step

Another bounded patch is justified only if there is an explicit decision to
implement target-engine dialect routing in a separate MySQL/Spark canary v2.

That would require a deliberate wrapper or adapter change that can:

- render MySQL-labeled rows through a MySQL target dialect path
- render Spark-labeled rows through a Spark target dialect path
- keep engine labels explicit
- avoid silently reusing PostgreSQL-shaped output as same-engine evidence

Without that explicit routing change, the correct action is to leave the canary
blocked and keep `method_comparison_summary_v2` unchanged.
