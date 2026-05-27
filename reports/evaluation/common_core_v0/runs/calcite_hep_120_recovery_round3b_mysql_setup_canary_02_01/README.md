# Calcite HEP 120 Recovery Round-3b MySQL Setup Canary 02 01

This package is a bounded, fail-closed recovery canary for only the two MySQL
rows that failed in Round-3 during MySQL setup, before any exact-match
comparison.

It is human-run only. Codex must not execute it.

## Scope

- method_id: `calcite_hep`
- route_id: `calcite_hep_same_engine_rewrite`
- denominator_id: `common_core_v0_40_same_engine_120`
- previous fail-closed exact ledger: `84/120`
- planned rows: `2`
- maximum possible ledger after this canary: `86/120`

Rows only:

- `PERF_0062:mysql`
- `LONGTAIL_0013:mysql`

## Recovery Boundary

- recovery-canary validity evidence only
- no timing
- no speedup
- no leaderboard
- no full `120`-row comparable claim

## What This Package Does

- reuses the retained Round-3 generated MySQL target-dialect SQL
- avoids the Round-3 `CREATE/DROP DATABASE` strategy
- uses the existing `MYSQL_DATABASE`
- performs safe per-row table cleanup before and after each row
  - `PERF_0062:mysql`:
    `store_sales`, `store`, `customer_demographics`, `household_demographics`, `customer_address`, `date_dim`
  - `LONGTAIL_0013:mysql`:
    `Users`, `Posts`, `Votes`, `Badges`
- keeps exact-match checker semantics unchanged

## Success Rule

A row only counts as recovered if the retained Round-3 generated SQL:

1. executes source SQL,
2. executes generated SQL,
3. produces `match_exact` under the existing checker,
4. sets `recovered_exact = true`.
