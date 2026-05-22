# Calcite HEP 120 Recovery PERF_0035 Canary 03 01

This package is a bounded, fail-closed post-90 recovery canary for exactly the
three retained `PERF_0035` rows that remain non-exact after the current
Calcite HEP ledger reached `90/120`.

It is human-run only. Codex must not execute it.

## Scope

- method_id: `calcite_hep`
- route_id: `calcite_hep_same_engine_rewrite`
- denominator_id: `common_core_v0_40_same_engine_120`
- previous fail-closed exact ledger: `90/120`
- planned rows: `3`
- maximum possible ledger after this canary: `93/120`

Rows only:

- `PERF_0035:pg`
- `PERF_0035:mysql`
- `PERF_0035:spark`

## Recovery Boundary

- recovery-canary validity evidence only
- no timing
- no speedup
- no leaderboard
- no full `120`-row comparable claim

## Allowed Repair Only

- package-local final projection removal of the proven trailing helper column
- package-local final projection scale preservation for `avg_monthly_sales`

## Success Rule

A row only counts as recovered if the repaired generated SQL:

1. executes source SQL,
2. executes repaired generated SQL,
3. produces `match_exact` under the unchanged checker,
4. sets `recovered_exact = true`.
