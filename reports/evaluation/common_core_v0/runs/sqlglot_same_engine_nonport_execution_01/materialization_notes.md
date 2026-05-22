# Materialization Notes

This package materializes the non-PORT SQLGlot same-engine execution run as denominator-aware method evidence.

Materialization choices:
- included all `186` planned non-PORT rows
- mapped `executed + exit_code=0` to `status=success`
- mapped `executed + exit_code!=0` to `status=failure`
- mapped `not_executed_generation_failed` to `status=skipped` with `failure_bucket=method_error`
- mapped `noop_generated` to `status=skipped` with `failure_bucket=unsupported`
- set `is_valid_result=false` for every row because this package has execution evidence only and no result-comparison artifact
- set `is_speedup_eligible=false` and filled `speedup_exclusion_reason` for every row because this package has no timing
- excluded all `PORT` rows by design
- did not create `same_engine_leaderboard.csv`

Run validator command:
```bash
python scripts/common_core_v0_validation.py   --manifest reports/evaluation/common_core_v0/runs/sqlglot_same_engine_nonport_execution_01/run_manifest.json   --run-event-long reports/evaluation/common_core_v0/runs/sqlglot_same_engine_nonport_execution_01/run_event_long.csv   --method-case-summary reports/evaluation/common_core_v0/runs/sqlglot_same_engine_nonport_execution_01/method_case_summary.csv   --json
```

Validator exit code: `0`

Validator reported no issues.
