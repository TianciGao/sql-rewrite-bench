# Materialization Notes

- This package materializes the 4-case manual PG/MySQL controls canary into Common-core v0 evaluation tables.
- Route rows are derived from case-local `result_check.json` artifacts, not from separate route-specific execution commands.
- `PERF_0006`, `CONS_0007`, and `LONGTAIL_0011` provide engine-local witness evidence for all three control routes on `pg` and `mysql`.
- `PORT_0012` uses a draft `cross_dialect_reference` checker. Materialized rows keep `pg native_source`, `mysql human_positive`, and `mysql hard_negative` as supported; the unsupported route/engine combinations remain explicit as skipped rows.
- `controls_summary.csv` is derived directly from `run_event_long.csv`.
- `validation_report.json` passed with `ok=true` and `issue_count=0`.
