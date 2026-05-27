# Calcite HEP MySQL/Spark Rewrite Expansion 80

This package prepares a bounded human-run rewrite-only expansion across the full
frozen common-core slate for MySQL and Spark:

- `40` common-core cases
- `2` engines
- planned rows = `80`

## Scope

- `method_id = calcite_hep`
- `route_id = calcite_hep_same_engine_rewrite`
- `expansion_denominator_id = calcite_hep_mysql_spark_common_core_v0_80`

## Boundary

This package is not:

- execution evidence
- correctness evidence
- timing evidence
- speedup evidence
- leaderboard evidence
- tri-engine `120`-row evidence

## Rendering Policy

The package uses explicit target-dialect rendering only:

- MySQL rows use `org.apache.calcite.sql.dialect.MysqlSqlDialect`
- Spark rows use `org.apache.calcite.sql.dialect.SparkSqlDialect`

It does not:

- fall back to `PostgresqlSqlDialect`
- use SQLGlot transpilation
- silently repair the retained decimal precision caveat learned from
  `PERF_0006`

## Shared Wrapper

This package reuses the shared canary v2 target-dialect wrapper source:

- `reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_canary_02/wrapper_src/CalciteHepTargetDialectCanary.java`

That keeps the MySQL/Spark rendering path aligned with the proven 6-row canary
and avoids editing the canonical PG wrapper.

## Path Resolution

Row setup resolves source SQL from the actual case layout:

- prefer `cases/<POOL>/<CASE>/source.sql`
- fall back to `cases/<POOL>/<CASE>/source/query.sql`

Schema remains required for rewrite, but witness files are treated as optional
metadata for a later execution package rather than as a rewrite-time blocker.
