# Calcite HEP 120 Recovery Round-4 Numeric Scale Canary 04 01

This package is a bounded, fail-closed recovery canary for exactly four rows
that already execute but still fail exact-match because retained generated SQL
does not preserve the source query's fixed numeric display scale.

It is human-run only. Codex must not execute it.

## Scope

- method_id: `calcite_hep`
- route_id: `calcite_hep_same_engine_rewrite`
- denominator_id: `common_core_v0_40_same_engine_120`
- previous fail-closed exact ledger: `86/120`
- planned rows: `4`
- maximum possible ledger after this canary: `90/120`

Rows only:

- `PERF_0062:pg`
- `PERF_0062:spark`
- `LONGTAIL_0013:pg`
- `LONGTAIL_0013:spark`

## Recovery Boundary

- recovery-canary validity evidence only
- no timing
- no speedup
- no leaderboard
- no full `120`-row comparable claim

## What This Package Does

- reuses retained PostgreSQL and Spark generated SQL from prior Calcite HEP runs
- applies only package-local SQL-level final projection numeric scale repair
- keeps the existing PostgreSQL and Spark execution environments
- keeps exact-match checker semantics unchanged
- does not normalize TSV outputs after execution

## Repair Policy

- `PERF_0062:*`
  - preserve output scales `4`, `6`, `6`, `2` in the final projection
- `LONGTAIL_0013:*`
  - preserve output scale `4` for output column `3` only
  - all other output columns remain unchanged

## Success Rule

A row only counts as recovered if the repaired generated SQL:

1. executes source SQL,
2. executes generated SQL,
3. produces `match_exact` under the existing checker,
4. sets `recovered_exact = true`.
