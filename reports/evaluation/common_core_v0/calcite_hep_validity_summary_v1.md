# Calcite HEP Validity Summary v1

This is a Calcite HEP PostgreSQL-only validity and execution summary for the frozen `common_core_v0_40_pg40` denominator.

It is validity/execution evidence only. It does not include timing, speedup, or leaderboard claims.

## Scope

- `denominator_id = common_core_v0_40_pg40`
- `method_id = calcite_hep`
- `route_id = calcite_hep_pg_rewrite`
- planned rows: `40`

## Headline Counts

- generation_success rows: `29`
- generation_failed rows: `11`
- ready_to_execute rows: `29`
- executed rows: `23`
- execution_failed rows: `6`
- match_exact rows: `21`
- mismatch rows: `2`

## Rates

- generation_success_rate over planned: `72.50%` (`29 / 40`)
- executable_rate over planned: `57.50%` (`23 / 40`)
- executable_rate over ready_to_execute: `79.31%` (`23 / 29`)
- result_consistency_rate over planned: `52.50%` (`21 / 40`)
- result_consistency_rate over executed: `91.30%` (`21 / 23`)
- result_consistency_rate over ready_to_execute: `72.41%` (`21 / 29`)
- generation_failed_rate over planned: `27.50%` (`11 / 40`)
- execution_failed_rate over planned: `15.00%` (`6 / 40`)
- execution_failed_rate over ready_to_execute: `20.69%` (`6 / 29`)
- mismatch_rate over executed: `8.70%` (`2 / 23`)
- mismatch_rate over ready_to_execute: `6.90%` (`2 / 29`)

## Breakdown By Pool

- `performance`: planned `16`, match_exact `14`, mismatch `2`, execution_failed `0`, not_executed_generation_failed `0`
- `consistency`: planned `9`, match_exact `7`, mismatch `0`, execution_failed `2`, not_executed_generation_failed `0`
- `portability`: planned `9`, match_exact `0`, mismatch `0`, execution_failed `1`, not_executed_generation_failed `8`
- `longtail`: planned `6`, match_exact `0`, mismatch `0`, execution_failed `3`, not_executed_generation_failed `3`

## Breakdown By Outcome Class

- `match_exact`: `21`
- `mismatch`: `2`
- `execution_failed`: `6`
- `not_executed_generation_failed`: `11`

## Interpretation

- `generation_failed` rows are Calcite generation, parser, or schema-ingestion failures and remain part of the 40-row denominator.
- `execution_failed` rows are Calcite-generated SQL execution failures on PostgreSQL unless the execution triage explicitly indicates otherwise.
- `mismatch` rows were executed but are not consistency-valid and are not timing-eligible.
- `match_exact` rows are the later timing-eligible set.
- This summary is Calcite HEP PG-only validity/execution evidence, not timing or speedup evidence.
- It should not be compared directly to SQLGlot or Direct LLM in a final leaderboard at this stage.
