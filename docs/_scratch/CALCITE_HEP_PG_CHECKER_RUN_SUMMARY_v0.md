# CALCITE_HEP_PG_CHECKER_RUN_SUMMARY_v0

## Status

This note records PostgreSQL-only execution and exact-TSV checker results for the Calcite HEP real-route 4-case PERF subset:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

Explicit boundary:

- PostgreSQL-only
- checker-backed only
- no speedup
- not final Calcite HEP baseline
- not a claim that Calcite HEP is fully implemented

## Commands Run

1. `python -m py_compile scripts/cli.py`
2. `python -m scripts.cli formal-calcite-hep-pg-checker-run`
3. `export PGPASSWORD='123456'`
4. `source scripts/env_postgres.sh`
5. `python -m scripts.cli formal-calcite-hep-pg-checker-run --case-id PERF_0006 --execute`
6. `python -m json.tool reports/formal_expansion/calcite_hep_pg_checker_run_v0.json >/dev/null`
7. `python -m json.tool reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0006.json >/dev/null`
8. `python -m scripts.cli formal-calcite-hep-pg-checker-run --execute`
9. `python -m json.tool reports/formal_expansion/calcite_hep_pg_checker_run_v0.json >/dev/null`

Operational note:

- PostgreSQL execution required running outside the sandbox to reach the PostgreSQL host.

## Canary Result

Canary case:

- `PERF_0006`

Canary outcome:

- source PG execution: success
- candidate PG execution: success
- source row count: `2`
- candidate row count: `2`
- row-count match: yes
- exact TSV byte equality: no
- checker status: `inconsistent`

Canary interpretation:

- the PostgreSQL execution path closed end-to-end for both source and Calcite candidate SQL
- the first real checker result was not exact-equal, so widening to the full 4-case subset was necessary

## Full 4-Case Result

Final full-subset outcome:

- `case_count:` `4`
- `executed_count:` `4`
- `source_execution_success_count:` `4`
- `candidate_execution_success_count:` `4`
- `checker_consistent_count:` `3`
- `checker_inconsistent_count:` `1`
- `checker_failed_count:` `0`
- `result_consistency_rate:` `0.75`
- `row_count_match_count:` `4`
- `row_count_mismatch_count:` `0`
- `failure_categories:` none

Per-case result:

| case_id | source exec | candidate exec | source rows | candidate rows | row-count equal | byte equal | checker status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | success | success | `2` | `2` | yes | no | `inconsistent` |
| `PERF_0008` | success | success | `1` | `1` | yes | yes | `consistent` |
| `PERF_0033` | success | success | `1` | `1` | yes | yes | `consistent` |
| `PERF_0054` | success | success | `1` | `1` | yes | yes | `consistent` |

Materialized outputs written under the allowed report-local paths:

- source TSVs: `reports/formal_expansion/result_materialization/calcite_hep/source/*.tsv`
- candidate TSVs: `reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/*.tsv`
- checker JSONs: `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/*.json`
- run summary JSON: `reports/formal_expansion/calcite_hep_pg_checker_run_v0.json`

## Inconsistent Case

Inconsistent case:

- `PERF_0006`

Observed failure shape:

- row counts still match: `2` vs `2`
- exact TSV bytes do not match
- the diff is in decimal-valued output columns, not missing or extra rows

Observed TSV diff characteristics for `PERF_0006`:

- source contains higher-precision decimal text such as `15.0000000000000000`, `150.0000000000000000`, and `0.07500000000000000000`
- Calcite candidate emits shorter or rounded values such as `15.00`, `150.00`, and `0.08`

Interpretation:

- the checker failure is not a row-count failure
- the mismatch is consistent with Calcite rewrite / PostgreSQL evaluation changing exact rendered numeric results in at least one derived expression
- this subset is therefore not yet checker-clean enough to treat as a baseline candidate

## What This Proves

- the Calcite HEP real-route subset now has PostgreSQL execution closure on all four clean PERF cases
- exact-TSV checker artifacts can be produced for the Calcite candidate route
- three of the four cases are checker-consistent under exact TSV

## What This Does Not Prove

- this is not speedup-scored
- this is not a final Calcite HEP baseline
- this does not establish correctness closure for the full subset because `PERF_0006` remains inconsistent

## Next Action

Because the full 4-case run is only `3/4` exact-TSV consistent, the next step should be:

- investigate and fix the `PERF_0006` numeric mismatch before any speedup or stronger baseline framing
