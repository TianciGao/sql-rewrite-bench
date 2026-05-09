# Calcite HEP MySQL/Spark Rewrite Canary v2 Plan

## Scope

This package is a bounded **rewrite-only** target-dialect recovery canary for:

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

Identifiers:

- `method_id = calcite_hep`
- `route_id = calcite_hep_same_engine_rewrite`
- `canary_denominator_id = calcite_hep_mysql_spark_canary_02`
- planned rows = `6`

## Goal

Attempt explicit target-engine dialect rendering through a package-local wrapper
instead of stopping at the canary 01 PostgreSQL-shaped output blocker.

## Target dialect policy

The v2 package attempts:

- MySQL rows via `org.apache.calcite.sql.dialect.MysqlSqlDialect.DEFAULT`
- Spark rows via `org.apache.calcite.sql.dialect.SparkSqlDialect.DEFAULT`

The package-local wrapper is the only place where Calcite-version API
compatibility fixes should be applied for this canary.

The package does not:

- use `PostgresqlSqlDialect` for MySQL or Spark same-engine evidence
- use SQLGlot transpilation
- use Hive as a silent Spark substitute

## Output contract

For each row, the human-run package should write:

- `generated/<case_id>/<engine>/calcite_hep_rewrite.sql` if final SQL is
  nonempty
- `logs/<case_id>/<engine>/rewrite.stdout.log`
- `logs/<case_id>/<engine>/rewrite.stderr.log`
- `metadata/<case_id>/<engine>/row_metadata.json`

Package-level outputs:

- `run_event_long.csv`
- `run_results.json`

## Preflight policy

Preflight checks:

- selected source/schema/witness paths exist
- Calcite checkout exists
- package-local wrapper source exists
- wrapper can be compiled against the visible Calcite checkout
- MySQL dialect availability is checked separately
- Spark dialect availability is checked separately

If one engine is unavailable:

- block only that engine
- continue to attempt the other engine if safe

## Boundary

This package is not:

- execution evidence
- correctness evidence
- timing evidence
- speedup evidence
- leaderboard evidence

Existing PG-only Calcite HEP summaries remain canonical until this canary is
human-run and later separately triaged.
