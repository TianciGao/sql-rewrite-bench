# Expected Artifacts

## Package outputs

Human-run outputs should be written under:

- `reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_canary_02/`

Core package-level artifacts:

- `run_results.json`
- `run_event_long.csv`

## Row-level artifacts

For each row:

- `generated/<case_id>/<engine>/calcite_hep_rewrite.sql` if final target-engine
  SQL is nonempty
- `logs/<case_id>/<engine>/rewrite.stdout.log`
- `logs/<case_id>/<engine>/rewrite.stderr.log`
- `metadata/<case_id>/<engine>/row_metadata.json`

## Dialect status recording

Each row should record:

- `dialect_class_used`
- `dialect_rendering_status`
- `rewrite_changed`

Allowed `dialect_rendering_status` values:

- `target_dialect_rendered`
- `target_dialect_unavailable`
- `wrapper_compile_failed`
- `parser_failed`
- `hep_rewrite_failed`
- `rendered_sql_missing`

## Fail-closed behavior

If target dialect routing cannot be established safely for an engine:

- block only that engine
- keep the other engine attemptable if safe

The package must not silently reinterpret PostgreSQL-dialect output as MySQL or
Spark same-engine evidence.
