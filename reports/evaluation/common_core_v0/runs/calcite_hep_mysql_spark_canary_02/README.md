# Calcite HEP MySQL/Spark Rewrite Canary 02

This package is a bounded human-run **rewrite-only** target-dialect recovery
canary for six rows:

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

## Why this exists

Canary 01 stopped at preflight because the visible shared wrapper rendered only
through `PostgresqlSqlDialect`.

Canary 02 avoids modifying the canonical PG wrapper and instead uses a
package-local Java wrapper source that attempts explicit target-engine dialect
rendering through:

- `MysqlSqlDialect.DEFAULT`
- `SparkSqlDialect.DEFAULT`

## Important boundary

This package is not:

- full MySQL/Spark evaluation
- execution evidence
- correctness evidence
- timing evidence
- speedup evidence
- leaderboard evidence

## Fail-closed rules

- MySQL rows must not silently render through PostgreSQL dialect output.
- Spark rows must not silently render through PostgreSQL dialect output.
- Hive-like fallback is not used silently for Spark.
- If one engine lacks safe target-dialect routing, only that engine is blocked.

## Runtime expectations

Expected local inputs:

- repo root checkout
- visible Calcite checkout at:
  - `$CALCITE_CHECKOUT_ROOT`
- package-local wrapper source at:
  - `reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_canary_02/wrapper_src/CalciteHepTargetDialectCanary.java`

The runner does not execute SQL and uses witness data paths as retained metadata
only.
