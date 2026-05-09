# Calcite HEP 120 Recovery Round-4b Numeric Scale Canary 04 01

This package is a bounded, fail-closed recovery canary for exactly four rows
that already execute but still fail exact-match because retained generated SQL
does not preserve the source query's engine-specific numeric display scale.

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

- `PERF_0062:pg`
  - preserve output scales `16`, `16`, `16`, `2`
- `PERF_0062:spark`
  - preserve output scales `1`, `6`, `6`, `2`
- `LONGTAIL_0013:pg`
  - preserve output scale `16` for output column `3`
- `LONGTAIL_0013:spark`
  - preserve output scale `1` for output column `3`

## Success Rule

A row only counts as recovered if the repaired generated SQL:

1. executes source SQL,
2. executes generated SQL,
3. produces `match_exact` under the existing checker,
4. sets `recovered_exact = true`.
