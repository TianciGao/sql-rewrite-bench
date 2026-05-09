# Expected Artifacts

## Package outputs

Human-run package outputs should be written under:

- `reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_canary_01/`

Core package-level artifacts:

- `run_results.json`
- `run_event_long.csv`

## Row-level artifacts

For each row:

- `generated/<case_id>/<engine>/calcite_hep_same_engine_rewrite.sql`
- `logs/<case_id>_<engine>.log`
- `row_results/<case_id>/<engine>/result.json`

## Fail-closed behavior

If the wrapper remains PostgreSQL-shaped at output:

- `run_results.json` should record:
  - `status = preflight_failed`
  - `failure_category = target_engine_dialect_not_implemented`
- `run_event_long.csv` should still contain all `6` rows with explicit
  `preflight_blocked` status

The package must not silently reinterpret PostgreSQL-dialect output as MySQL or
Spark same-engine evidence.
