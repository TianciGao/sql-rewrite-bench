# Calcite HEP 120 Recovery Round 2 Canary 09 01

This package is a bounded, fail-closed round-2 recovery canary for nine
low-risk retained Calcite HEP ledger-gap rows.

It is human-run only. Codex must not execute it.

## Scope

- method_id: `calcite_hep`
- route_id: `calcite_hep_same_engine_rewrite`
- denominator_id: `common_core_v0_40_same_engine_120`
- previous fail-closed exact ledger: `75/120`
- planned rows: `9`
- maximum possible ledger after this canary: `84/120`

Target rows only:

- `LONGTAIL_0022:pg`
- `LONGTAIL_0023:pg`
- `LONGTAIL_0024:pg`
- `PERF_0062:mysql`
- `PERF_0062:spark`
- `LONGTAIL_0012:mysql`
- `LONGTAIL_0012:spark`
- `LONGTAIL_0013:mysql`
- `LONGTAIL_0013:spark`

## Recovery families

- PostgreSQL identifier/schema compatibility repair:
  - `LONGTAIL_0022:pg`
  - `LONGTAIL_0023:pg`
  - `LONGTAIL_0024:pg`
- non-PG numeric scale-preservation repair:
  - `PERF_0062:mysql`
  - `PERF_0062:spark`
  - `LONGTAIL_0012:mysql`
  - `LONGTAIL_0012:spark`
  - `LONGTAIL_0013:mysql`
  - `LONGTAIL_0013:spark`

## Boundaries

- No SQLGlot transpilation.
- No PostgreSQL fallback for MySQL or Spark.
- No checker normalization or exact-match relaxation.
- No timing, speedup, or leaderboard artifacts.
- A row only counts as recovered if it reaches retained
  `executed + match_exact + recovered_exact=true`.

## Claim boundary

`calcite_hep_120_recovery_round2_canary_only_not_timing_speedup_or_leaderboard_evidence`
