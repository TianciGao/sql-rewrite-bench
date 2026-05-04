# CALCITE_HEP_PG_CHECKER_RUN_SUMMARY_v0

## Status

This note now reflects two bounded facts about the Calcite HEP PostgreSQL checker lane:

- the earlier 4-case checker run closed PostgreSQL execution on all four clean PERF cases
- after the targeted `PERF_0006` AVG precision fix, the `PERF_0006` checker canary is now exact-TSV consistent

Explicit boundary:

- PostgreSQL-only
- checker-backed only
- no speedup
- not final Calcite HEP baseline
- not a claim that Calcite HEP is fully implemented

## Historical 4-Case Run

Historical full-subset result before the `PERF_0006` fix:

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

Historical inconsistent case:

- `PERF_0006`

## Fixed Canary

Bounded rerun performed after the AVG precision fix:

- `python -m scripts.cli formal-calcite-hep-real-route-canary --case-id PERF_0006 --execute`
- `python -m scripts.cli formal-calcite-hep-pg-checker-run --case-id PERF_0006 --execute`

Fixed `PERF_0006` canary result:

- source PG execution: success
- candidate PG execution: success
- source row count: `2`
- candidate row count: `2`
- row-count match: yes
- exact TSV byte equality: yes
- checker status: `consistent`
- emitted SQL mode: `calcite_rel_to_sql`

Interpretation:

- the targeted AVG precision fix cleared the only known checker inconsistency on the clean PERF subset
- the previously failing `avg_disc` path is now checker-consistent on `PERF_0006`

## Current Reading

What is now true:

- `PERF_0006` is checker-clean under the bounded canary rerun
- the prior `3/4` checker result is stale with respect to `PERF_0006`
- a fresh full 4-case PostgreSQL checker rerun is now appropriate

What has not been rerun yet in this step:

- the full 4-case checker summary after the `PERF_0006` fix

So the strongest current statement is:

- `PERF_0006` recovery succeeded
- full 4-case checker-clean recovery is now plausible and should be verified with a bounded 4-case rerun

## Materialized Artifacts

Current `PERF_0006` checker artifact paths:

- source TSV: `reports/formal_expansion/result_materialization/calcite_hep/source/perf_0006.tsv`
- candidate TSV: `reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0006.tsv`
- checker JSON: `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0006.json`
- checker run report: `reports/formal_expansion/calcite_hep_pg_checker_run_v0.json`

## Next Action

Because the repaired `PERF_0006` canary is now exact-TSV consistent, the next step should be:

- rerun the bounded 4-case PostgreSQL checker subset

Still out of scope here:

- speedup
- final baseline claim
