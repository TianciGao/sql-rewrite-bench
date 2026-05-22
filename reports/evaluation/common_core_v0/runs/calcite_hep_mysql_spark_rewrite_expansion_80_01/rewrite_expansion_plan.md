# Calcite HEP MySQL/Spark Rewrite Expansion 80 Plan

## Scope

This package expands the bounded MySQL/Spark rewrite canary to the full frozen
common-core case slate for rewrite-only generation attempts.

Identifiers:

- `method_id = calcite_hep`
- `route_id = calcite_hep_same_engine_rewrite`
- `expansion_denominator_id = calcite_hep_mysql_spark_common_core_v0_80`
- engines: `mysql`, `spark`
- planned rows = `80`

Denominator construction:

- `40` frozen common-core cases from
  `reports/curation/common_core_v0_final_denominator.csv`
- each attempted on `2` engines

## Goal

Produce bounded rewrite-generation evidence only for the full MySQL/Spark
common-core slate, using explicit target-dialect rendering:

- MySQL via `org.apache.calcite.sql.dialect.MysqlSqlDialect`
- Spark via `org.apache.calcite.sql.dialect.SparkSqlDialect`

## Boundary

This package is rewrite-only:

- no SQL execution
- no correctness / result-consistency claim
- no timing
- no speedup
- no leaderboard

It does not create tri-engine `120`-row evidence. It is only the
MySQL/Spark-side rewrite expansion layer.

## Rendering Rules

The package must not:

- use `PostgresqlSqlDialect` for MySQL or Spark rows
- use SQLGlot transpilation
- silently repair the retained decimal precision caveat seen in
  `PERF_0006`

The package may only attempt explicit target-dialect rendering through the
shared package-local canary wrapper source proven in canary v2.

## Status Contract

Per row, `row_status` must be one of:

- `rewrite_success`
- `parser_failed`
- `hep_rewrite_failed`
- `target_dialect_unavailable`
- `rel_to_sql_failed`
- `generated_sql_missing`
- `setup_failed`

Each row must also record:

- `dialect_class_used`
- `rewrite_changed`
- `failure_category`
- `blocker_reason`

Row setup must resolve case-local source SQL with fallback:

- prefer `cases/<POOL>/<CASE>/source.sql`
- if absent, fall back to `cases/<POOL>/<CASE>/source/query.sql`

Schema is required for rewrite:

- MySQL: `cases/<POOL>/<CASE>/schema/ddl_mysql.sql`
- Spark: `cases/<POOL>/<CASE>/schema/ddl_spark.sql`

Witness data is retained as later execution metadata only. Missing witness files
must not block this rewrite-only package; they should be recorded as
`witness_missing_for_later_execution = true` in row metadata instead.

## Artifacts

Package-level:

- `run_results.json`
- `run_event_long.csv`

Row-level:

- generated SQL for successful rows
- stdout / stderr logs for every row
- row metadata for every row

## Shared Wrapper Dependency

To avoid diverging wrapper variants, this package reuses the proven shared
target-dialect wrapper source from:

- `reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_canary_02/wrapper_src/CalciteHepTargetDialectCanary.java`

This package does not modify:

- canonical PG Calcite HEP evidence
- `tools/calcite_hep/CalciteHepRewriteSmoke.java`
- `method_comparison_summary_v2`
