# Materialization Notes

This package materializes the PORT SQLGlot same-engine execution run as denominator-aware method evidence after resolving two package witness gaps.

Materialization choices:
- included all `54` planned PORT rows
- used the original PORT run for `7` executed successes, `9` `noop_generated` rows, and `36` `skipped_unsupported` rows
- replaced the two original PostgreSQL optimize package-witness-gap failures with the successful retry rows from `sqlglot_same_engine_port_retry_pg_witness_01`
- preserved carry-forward notes that `PORT_0003 / pg / sqlglot_optimize_same_dialect` and `PORT_0005 / pg / sqlglot_optimize_same_dialect` originally failed before generated-SQL execution because `pg_witness_data.sql` was missing
- mapped `executed + exit_code=0` to `status=success`
- mapped `noop_generated` to `status=skipped` with `failure_bucket=unsupported`
- mapped `skipped_unsupported` to `status=skipped` with `failure_bucket=unsupported`
- set `is_valid_result=false` for every row because this package has execution evidence only and no result-comparison artifact
- set `is_speedup_eligible=false` and filled `speedup_exclusion_reason` for every row because this package has no timing
- did not create `same_engine_leaderboard.csv`

Retry provenance:
- original gap files:
  - `cases/PORT/PORT_0003/validation/pg_witness_data.sql`
  - `cases/PORT/PORT_0005/validation/pg_witness_data.sql`
- retry package:
  - `reports/evaluation/common_core_v0/runs/sqlglot_same_engine_port_retry_pg_witness_01/run_results.json`

Run validator command:
```bash
python scripts/common_core_v0_validation.py   --manifest reports/evaluation/common_core_v0/runs/sqlglot_same_engine_port_execution_resolved_01/run_manifest.json   --run-event-long reports/evaluation/common_core_v0/runs/sqlglot_same_engine_port_execution_resolved_01/run_event_long.csv   --method-case-summary reports/evaluation/common_core_v0/runs/sqlglot_same_engine_port_execution_resolved_01/method_case_summary.csv   --json
```
