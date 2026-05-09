# Calcite HEP 120 Recovery Round-3b MySQL Setup Canary 02 01 Plan

## Purpose

Retry only the two Round-3 MySQL rows that failed on the per-row temporary
database strategy.

## Planned Rows

- `PERF_0062:mysql`
- `LONGTAIL_0013:mysql`

## Retained Failure Being Targeted

Both rows failed before schema load and before exact-match comparison on:

- `DROP DATABASE IF EXISTS ...`

with retained MySQL `ERROR 1044` access-denied evidence.

## Package Change

- use the existing `MYSQL_DATABASE` from `scripts/env_mysql.sh`
- derive row-local cleanup from case-local DDL table names
- drop those tables inside the existing database before schema load
- load schema and witness data
- execute retained Round-3 source and generated SQL
- compare outputs exactly under the unchanged checker
- drop those tables again during cleanup

## Expected Ledger Outcomes

- previous ledger: `84/120`
- `0` recovered => `84/120`
- `1` recovered => `85/120`
- `2` recovered => `86/120`

## Explicit Non-Goals

- no rewrite rerun outside the retained Round-3 generated SQL
- no checker changes
- no numeric normalization
- no timing or speedup
- no paper-table or synthesis update in this task
