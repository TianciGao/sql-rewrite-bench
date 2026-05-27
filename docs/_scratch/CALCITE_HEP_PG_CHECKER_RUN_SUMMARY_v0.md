# CALCITE_HEP_PG_CHECKER_RUN_SUMMARY_v0

## Status

This note records the post-fix bounded 4-case Calcite HEP real-route generation and PostgreSQL checker rerun for:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

Explicit boundary:

- PostgreSQL-only
- checker-backed only
- no speedup yet
- not final Calcite HEP baseline
- not a claim that Calcite HEP is fully implemented

## Commands Run

1. `python -m py_compile scripts/cli.py`
2. `python -m scripts.cli formal-calcite-hep-real-route-canary --case-id PERF_0006 --case-id PERF_0008 --case-id PERF_0033 --case-id PERF_0054 --execute`
3. `python -m json.tool reports/formal_expansion/calcite_hep_real_route_canary_v0.json >/dev/null`
4. `export PGPASSWORD='123456'`
5. `source scripts/env_postgres.sh`
6. `python -m scripts.cli formal-calcite-hep-pg-checker-run --execute`
7. `python -m json.tool reports/formal_expansion/calcite_hep_pg_checker_run_v0.json >/dev/null`
8. `python -m json.tool reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0006.json >/dev/null`
9. `python -m json.tool reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0008.json >/dev/null`
10. `python -m json.tool reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0033.json >/dev/null`
11. `python -m json.tool reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0054.json >/dev/null`

Operational note:

- PostgreSQL execution required running outside the sandbox to reach the PostgreSQL host.

## 4-Case Real-Route Result

Generation result on the bounded subset:

- `case_count:` `4`
- `real_route_success_count:` `4/4`
- `parse_success_count:` `4/4`
- `validation_success_count:` `4/4`
- `sql_to_rel_success_count:` `4/4`
- `hep_planner_success_count:` `4/4`
- `rel_to_sql_success_count:` `4/4`
- `emit_success_count:` `4/4`
- `emitted_sql_mode_distribution:` `calcite_rel_to_sql=4`

Interpretation:

- all four cases still close the intended real Calcite route after the `PERF_0006` AVG precision fix
- no passthrough fallback was used

## 4-Case Checker Result

Post-fix PostgreSQL checker result on the same bounded subset:

- `case_count:` `4`
- `executed_count:` `4`
- `source_execution_success_count:` `4`
- `candidate_execution_success_count:` `4`
- `checker_consistent_count:` `4`
- `checker_inconsistent_count:` `0`
- `checker_failed_count:` `0`
- `result_consistency_rate:` `1.0`
- `row_count_match_count:` `4`
- `row_count_mismatch_count:` `0`
- `failure_categories:` none

Per-case result:

| case_id | source exec | candidate exec | source rows | candidate rows | row-count equal | byte equal | checker status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | success | success | `2` | `2` | yes | yes | `consistent` |
| `PERF_0008` | success | success | `1` | `1` | yes | yes | `consistent` |
| `PERF_0033` | success | success | `1` | `1` | yes | yes | `consistent` |
| `PERF_0054` | success | success | `1` | `1` | yes | yes | `consistent` |

## Interpretation

What this now proves:

- Calcite HEP is checker-backed on the bounded 4-case clean PERF subset
- PostgreSQL execution closure exists for both source and Calcite candidate SQL on all four cases
- the earlier `PERF_0006` AVG precision mismatch is cleared in the bounded subset

What this still does not prove:

- no speedup result has been run
- no final baseline claim should be made
- this remains a bounded PostgreSQL-only subset result

## Materialized Artifacts

Artifacts written under the allowed report-local paths:

- source TSVs: `reports/formal_expansion/result_materialization/calcite_hep/source/*.tsv`
- candidate TSVs: `reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/*.tsv`
- checker JSONs: `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/*.json`
- real-route report: `reports/formal_expansion/calcite_hep_real_route_canary_v0.json`
- checker run report: `reports/formal_expansion/calcite_hep_pg_checker_run_v0.json`

## Next Action

Because the bounded 4-case subset is now `4/4` checker-consistent, the next step should be:

- run Calcite HEP speedup preflight

Still out of scope here:

- speedup execution
- final baseline claim
