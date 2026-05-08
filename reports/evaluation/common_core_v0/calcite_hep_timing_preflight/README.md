# Calcite HEP Timing Preflight

This directory prepares the timing-bearing PostgreSQL-only speedup experiment for Calcite HEP on `common_core_v0_40_pg40`.

It is a preflight package only.

## Scope

- `method_id = calcite_hep`
- `route_id = calcite_hep_pg_rewrite`
- `denominator_id = common_core_v0_40_pg40`
- planned rows: `40`
- timing_eligible rows: `21`
- speedup_eligible rows: `21`

## Eligibility Contract

Only `match_exact` rows are timing-eligible.

Therefore:

- `21` rows are timing-eligible
- `19` rows are not timing-eligible and remain explicit in the matrix with exclusion reasons

## Files

- `calcite_hep_timing_preflight.md`
- `calcite_hep_timing_candidate_matrix.csv`
- `calcite_hep_timing_run_plan.json`

## Boundaries

- no timing is run here
- no speedup is computed here
- no leaderboard is created here
