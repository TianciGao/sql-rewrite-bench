# Calcite HEP MySQL/Spark Rewrite Canary Plan

## Purpose

This package is a bounded **rewrite-only canary** for testing whether the
current Calcite HEP wrapper can safely move beyond the retained PostgreSQL-only
baseline.

It is not a full MySQL/Spark evaluation and it does not modify the canonical
PG-only Calcite HEP evidence.

## Scope

- `method_id = calcite_hep`
- `route_id = calcite_hep_same_engine_rewrite`
- `canary_denominator_id = calcite_hep_mysql_spark_canary_01`
- engines: `mysql`, `spark`
- cases:
  - `PERF_0006`
  - `PERF_0007`
  - `CONS_0005`
- planned rows: `6`

## Why these rows

- all six selected rows have same-engine schema files
- all six selected rows have same-engine witness-data files
- the cases already exist in the common-core denominator and provide a bounded
  probe for non-PG route feasibility

## Current blocker model

The visible wrapper is still PostgreSQL-shaped at output:

- parser path uses `Lex.MYSQL`
- rendering path uses `PostgresqlSqlDialect`

Because of that, the canary runner must fail closed unless a non-PG-safe
rendering route is visible.

## Planned preflight

The shell runner checks:

1. selected `source.sql` files exist
2. selected same-engine schema files exist
3. selected same-engine witness-data files exist
4. wrapper source exists
5. Calcite checkout exists
6. wrapper source still uses `PostgresqlSqlDialect`

If the output dialect remains PostgreSQL-shaped, the package writes explicit
blocked status for all six rows and stops before wrapper row attempts.

## Claim boundary

This package can only produce:

- rewrite-canary feasibility evidence

It cannot support:

- execution validity claims
- timing or speedup claims
- leaderboard claims
- method comparison updates

## Safe next decision boundary

- if preflight blocks on PostgreSQL-shaped rendering, the next step is a
  separate adapter/design discussion, not a silent same-engine claim
- if a later wrapper explicitly supports MySQL or Spark rendering, a fresh
  canary package can be created or patched for real row attempts
