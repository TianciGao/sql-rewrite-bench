# Calcite HEP 120 Recovery PERF_0035 Canary 03 Result Card v1

This is a bounded recovery result card for the retained `PERF_0035`-only
Calcite HEP post-90 canary.

## Headline

After a bounded `PERF_0035` recovery canary targeting a proven internal
helper-column projection artifact and numeric-scale rendering defects, the
fail-closed exact-match ledger improved from `90/120` to `93/120`. Three
additional rows recovered exact-match validity evidence. The recovered rows
reflect package-local final projection repair under unchanged exact-match
semantics, unchanged checker policy, and unchanged denominator scope. This
remains bounded execution-validity evidence, not timing, speedup, leaderboard,
or full `120`-row comparable evidence.

## Scope

- method_id: `calcite_hep`
- route_id: `calcite_hep_same_engine_rewrite`
- denominator_id: `common_core_v0_40_same_engine_120`
- previous_fail_closed_exact_ledger: `90/120`
- planned_rows: `3`
- maximum_possible_ledger_after_this_canary: `93/120`

Recovered rows:

- `PERF_0035:pg`
- `PERF_0035:mysql`
- `PERF_0035:spark`

## Retained Result

- executed: `3/3`
- match_exact: `3/3`
- recovered_exact_count: `3`
- new_fail_closed_exact_ledger: `93/120`
- timing_denominator_id: `NA_not_computed`
- leaderboard_comparable: `no`

For audit clarity:

- `run_event_long.csv` does not expose a standalone `exact_match` column
- exact-match validity here is derived from `consistency_status=match_exact`,
  `recovered_exact=True`, and `recovered_exact_count=3`
