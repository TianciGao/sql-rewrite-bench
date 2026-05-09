# Calcite HEP MySQL/Spark Rewrite Canary 01

This package is a bounded human-run **rewrite-only canary** for six rows:

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

## Important boundary

This package is not:

- a full MySQL/Spark evaluation
- execution evidence
- timing evidence
- speedup evidence
- leaderboard evidence

## Current expected behavior

The visible Java wrapper still renders through `PostgresqlSqlDialect`. Because
of that, this package is intentionally fail-closed:

- it keeps MySQL and Spark labels explicit
- it does not silently treat PG-shaped SQL as same-engine MySQL/Spark output
- if the wrapper remains PostgreSQL-shaped, the runner records explicit blocked
  status and stops before row attempts

## Environment

Expected local inputs:

- repo root checkout
- visible Calcite checkout at:
  - `$CALCITE_CHECKOUT_ROOT`
- wrapper source at:
  - `tools/calcite_hep/CalciteHepRewriteSmoke.java`

The runner does not execute SQL and does not use witness data for execution.
