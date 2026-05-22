# Materialization Notes

- This package materializes the 4-case manual Spark controls canary into Common-core v0 evaluation tables.
- Route rows are derived from Spark `result_check.json` artifacts where present, not from separate route-specific execution commands.
- `PERF_0006` remained `missing_script` in the manual canary and is therefore kept explicit as skipped/unsupported for all three routes despite a legacy `runs/spark/result_check.json` file existing in the repo.
- `CONS_0007` and `LONGTAIL_0011` use Spark witness-checker fields `source_positive_equal` and `source_negative_different` to derive all three routes.
- `PORT_0012` uses the Spark cross-dialect checker. `human_positive` and `hard_negative` are supported from the checker fields; `native_source` remains explicit as unsupported because the checker does not provide a Spark source-baseline route.
- `controls_summary.csv` is derived directly from `run_event_long.csv`.
- `validation_report.json` passed with `ok=true` and `issue_count=0`.
