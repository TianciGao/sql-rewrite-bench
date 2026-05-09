# R-Bot PG40 Generation Expansion Triage

## Scope

This is a read-only triage of the completed `r_bot_pg40_generation_expansion_02` run.

It is:

- PostgreSQL-only generation expansion evidence
- denominator-aware against `common_core_v0_40_pg40`
- still linked back to the source generation denominator `common_core_v0_40_same_engine_120`

It is not:

- execution evidence
- validity evidence
- timing evidence
- speedup evidence
- leaderboard evidence
- a replacement for the existing PG7 retained result card

## Summary

- `planned_pg_rows = 40`
- `generated = 15`
- `failed = 25`
- `blocked = 0`
- `unsupported = 0`
- `run_event_long_rows = 40`
- `generated_sql_exists_for_all_generated_rows = true`
- `generated_row_artifact_contract_complete = true`
- `generated_sql_clean_for_all_generated_rows = true`
- `coverage_improved_over_previous_pg7_retained_run = true`

Coverage improvement over the prior PG7 retained run:

- previous retained PG generation rows: `7`
- PG40 expansion generated rows: `15`
- net generated increase: `+8`
- previously blocked PG rows reduced from `31` to `0` in this expansion package

## Generated Rows

- `PERF_0006:pg`
- `PERF_0007:pg`
- `PERF_0008:pg`
- `PERF_0013:pg`
- `PERF_0017:pg`
- `PERF_0024:pg`
- `PERF_0052:pg`
- `PERF_0054:pg`
- `PERF_0062:pg`
- `CONS_0005:pg`
- `CONS_0007:pg`
- `CONS_0009:pg`
- `CONS_0010:pg`
- `CONS_0012:pg`
- `CONS_0036:pg`

## Failed Rows

- `PERF_0019:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PERF_0033:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PERF_0034:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PERF_0035:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PERF_0056:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PERF_0077:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PERF_0082:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `CONS_0011:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `CONS_0024:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `CONS_0037:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PORT_0003:pg`: `output_sql_missing`; `method finished without extractable output_sql`
- `PORT_0004:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PORT_0005:pg`: `output_sql_missing`; `method finished without extractable output_sql`
- `PORT_0008:pg`: `output_sql_missing`; `method finished without extractable output_sql`
- `PORT_0012:pg`: `output_sql_missing`; `method finished without extractable output_sql`
- `PORT_0013:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PORT_0022:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PORT_0024:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `PORT_0025:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `LONGTAIL_0011:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `LONGTAIL_0012:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `LONGTAIL_0013:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `LONGTAIL_0022:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `LONGTAIL_0023:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`
- `LONGTAIL_0024:pg`: `subprocess_nonzero_exit`; `subprocess exited with code 1`

## Counts

Counts by previous generation status class:

- generated:
  - `previously_generated_pg7 = 7`
  - `previously_blocked_pg31 = 8`
  - `previously_failed_pg2 = 0`
- failed:
  - `previously_generated_pg7 = 0`
  - `previously_blocked_pg31 = 23`
  - `previously_failed_pg2 = 2`

Counts by pool:

- overall:
  - `performance = 16`
  - `consistency = 9`
  - `portability = 9`
  - `longtail = 6`
- generated:
  - `performance = 9`
  - `consistency = 6`
  - `portability = 0`
  - `longtail = 0`
- failed:
  - `performance = 7`
  - `consistency = 3`
  - `portability = 9`
  - `longtail = 6`

Failure category distribution for the `25` failed rows:

- `subprocess_nonzero_exit = 21`
- `output_sql_missing = 4`

## Generated Artifact Checks

For all `15` generated rows, the following retained artifacts exist:

- generated SQL
- prompt
- raw response
- selected rules
- retrieval trace
- token-cost metadata
- provider metadata
- row metadata

Artifact-contract status for generated rows: `satisfied`.

## Generated SQL Quality

For all `15` generated rows:

- empty SQL: `false`
- markdown contamination: `false`
- non-SQL output: `false`
- DDL/DML output: `false`
- multi-statement output: `false`

All retained generated SQL files are single-statement query outputs under this triage check.

## Execution Handoff

Execution/validity package creation is recommended next, but only for these `15` generated PG rows:

- `PERF_0006:pg`
- `PERF_0007:pg`
- `PERF_0008:pg`
- `PERF_0013:pg`
- `PERF_0017:pg`
- `PERF_0024:pg`
- `PERF_0052:pg`
- `PERF_0054:pg`
- `PERF_0062:pg`
- `CONS_0005:pg`
- `CONS_0007:pg`
- `CONS_0009:pg`
- `CONS_0010:pg`
- `CONS_0012:pg`
- `CONS_0036:pg`

Failed rows remain explicit generation outcomes and are not execution candidates yet.

## Bottom Line

The PG40 expansion run materially improved recovered PostgreSQL generation coverage from `7` to `15` rows and eliminated the prior blocked-PG bucket inside this package. The retained evidence remains generation-only. No PG40 validity, timing, speedup, or leaderboard claim should be made from this run alone.
