# R-Bot PG7 Execution Triage

## Scope

This triage covers only the retained execution/validity evidence for the seven PostgreSQL rows that were generated in the formal `@120` generation run and then admitted to the PG7 execution package.

Boundary: this is execution/validity evidence only. It is not timing, speedup, or leaderboard evidence.

## Summary

- Planned execution rows: `7`
- Executed rows: `7`
- Execution-failed rows: `0`
- `match_exact` rows: `7`
- `mismatch` rows: `0`
- PostgreSQL preflight check exit code: `0`
- `result_check.json` exists for all 7 rows: `yes`
- `source.tsv` exists for all 7 rows: `yes`
- `generated.tsv` exists for all 7 rows: `yes`

## Row-Level Status

- `PERF_0006:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0008:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0013:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0017:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0024:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0052:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present
- `PERF_0054:pg`: `executed`, `match_exact`, `result_check.json` present, `source.tsv` present, `generated.tsv` present

## Artifact Coverage

For each of the seven executed rows, the retained workspace contains:

- `source.sql`
- `generated.sql`
- `ddl_pg.sql`
- `pg_witness_data.sql`
- `source.tsv`
- `generated.tsv`
- `result_check.json`

For each of the seven executed rows, retained stdout/stderr logs are also present under `reports/evaluation/common_core_v0/runs/r_bot_pg7_execution_01/logs/`.

## Timing Boundary

Timing may proceed only for these seven rows:

- `PERF_0006:pg`
- `PERF_0008:pg`
- `PERF_0013:pg`
- `PERF_0017:pg`
- `PERF_0024:pg`
- `PERF_0052:pg`
- `PERF_0054:pg`

This triage does not establish timing, speedup, or leaderboard evidence. It only establishes that the retained PG7 execution package records seven executed rows and seven exact output matches.
