# R-Bot PG15 Execution Expansion Triage

## Scope

This triage covers only the retained execution/validity evidence for the
fifteen PostgreSQL rows generated in `r_bot_pg40_generation_expansion_02` and
then admitted to the PG15 execution expansion package.

Boundary: this is execution/validity evidence only. It is not timing, speedup,
or leaderboard evidence.

The `25` failed PG generation rows remain explicit generation outcomes in the
PG40 generation denominator and are not silently dropped by this execution
subset.

## Summary

- Planned execution rows: `15`
- Executed rows: `15`
- Execution-failed rows: `0`
- `match_exact` rows: `15`
- `mismatch` rows: `0`
- PostgreSQL preflight check exit code: `0`
- `result_check.json` exists for all 15 rows: `yes`
- `source.tsv` exists for all 15 rows: `yes`
- `generated.tsv` exists for all 15 rows: `yes`

## Row-Level Status

- `PERF_0006:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0007:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0008:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0013:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0017:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0024:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0052:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0054:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0062:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `CONS_0005:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `CONS_0007:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `CONS_0009:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `CONS_0010:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `CONS_0012:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `CONS_0036:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present

## Artifact Coverage

For each of the fifteen executed rows, the retained workspace contains:

- `source.sql`
- `generated.sql`
- `ddl_pg.sql`
- `pg_witness_data.sql`
- `source.tsv`
- `generated.tsv`
- `result_check.json`

For each of the fifteen executed rows, retained stdout/stderr logs are also
present under
`reports/evaluation/common_core_v0/runs/r_bot_pg15_execution_expansion_02/logs/`.

## Comparison Against Previous PG7 Execution Evidence

Relative to the retained PG7 execution package:

- previous PG7 planned rows: `7`
- previous PG7 executed rows: `7`
- previous PG7 `match_exact` rows: `7`
- current PG15 planned rows: `15`
- current PG15 executed rows: `15`
- current PG15 `match_exact` rows: `15`

This means the retained exact-match execution evidence expanded from `7` PG rows
to `15` PG rows in the expansion path, without changing the earlier PG7 record.

## Timing Boundary

Timing may proceed only for these fifteen rows:

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

This triage does not establish timing, speedup, or leaderboard evidence. It
only establishes that the retained PG15 execution package records fifteen
executed rows and fifteen exact output matches.
