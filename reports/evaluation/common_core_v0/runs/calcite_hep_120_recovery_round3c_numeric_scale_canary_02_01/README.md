# Calcite HEP 120 Recovery Round-3c Numeric Scale Canary 02 01

This package is a bounded, fail-closed recovery canary for exactly two MySQL
rows that already execute but still fail exact-match because retained generated
SQL loses decimal display scale.

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
- applies only package-local SQL-level numeric-scale preservation repair
- keeps the existing `MYSQL_DATABASE`
- performs explicit per-row table cleanup before and after each row
- keeps exact-match checker semantics unchanged
- does not normalize TSV outputs after execution

## Repair Policy

- `PERF_0062:mysql`
  - preserve output scales `4`, `6`, `6`, `2` in the final projection
- `LONGTAIL_0013:mysql`
  - preserve output scale `4` for output column `3` only
  - all other output columns remain unchanged

## Success Rule

A row only counts as recovered if the repaired generated SQL:

1. executes source SQL,
2. executes generated SQL,
3. produces `match_exact` under the existing checker,
4. sets `recovered_exact = true`.
