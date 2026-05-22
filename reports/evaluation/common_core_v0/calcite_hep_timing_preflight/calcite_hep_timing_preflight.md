# Calcite HEP Timing Preflight

This is a timing-bearing preflight for Calcite HEP on the frozen `common_core_v0_40_pg40` denominator.

It does not run timing, compute speedup, or create any leaderboard artifact.

## Scope

- `denominator_id = common_core_v0_40_pg40`
- `method_id = calcite_hep`
- `route_id = calcite_hep_pg_rewrite`
- planned rows: `40`
- engine: `pg`

## Eligibility Rule

Timing eligibility is defined strictly as:

- `timing_eligible = yes` if and only if `consistency_check_status = match_exact`

Therefore:

- generation_success rows: `29`
- executed rows: `23`
- match_exact rows: `21`
- mismatch rows: `2`
- execution_failed rows: `6`
- generation_failed rows: `11`
- timing_eligible rows: `21`
- speedup_eligible rows: `21`

## Exclusion Breakdown

- `generation_failed`: `11`
- `execution_failed`: `6`
- `mismatch`: `2`

Counts by pool:

- `performance`: `14` eligible, `2` mismatch
- `consistency`: `7` eligible, `2` execution_failed
- `portability`: `0` eligible, `8` generation_failed, `1` execution_failed
- `longtail`: `0` eligible, `3` generation_failed, `3` execution_failed

## Main Caveats

- This is Calcite HEP PostgreSQL-only evidence, not tri-engine evidence.
- `generation_failed` rows remain part of the 40-row denominator and are not silently dropped.
- `execution_failed` rows remain explicit and are not timing-eligible.
- `mismatch` rows were executed but are not consistency-valid and are not timing-eligible.
- `PORT_0024` remains an execution-failed portability row despite generation success.
- The execution triage indicates that most execution failures look like Calcite-generated SQL identifier or PostgreSQL dialect failures rather than timing-runner setup failures.

## Timing Outlook

The later timing run should target exactly the `21` `match_exact` rows:

- `14` performance rows
- `7` consistency rows

No `portability` or `longtail` row is currently timing-eligible.
