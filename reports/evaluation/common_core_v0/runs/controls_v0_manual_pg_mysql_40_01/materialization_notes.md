# Materialization Notes

- This package materializes the successful 40-case manual PG/MySQL controls run into Common-core v0 evaluation tables.
- Route rows are derived from case-local `result_check.json` artifacts, not from separate route-specific execution commands.
- Performance, consistency, and longtail cases use engine-local checker fields `source_positive_equal` and `source_negative_different` to derive all three routes on `pg` and `mysql`.
- Portability cases use top-level cross-dialect checker artifacts under `cases/PORT/<case>/runs/result_check.json`.
- Portability rows are marked `success` only for the route/engine combinations actually supported by the cross-dialect reference direction; the remaining combinations are kept explicit as `skipped` rows.
- `controls_summary.csv` is derived directly from `run_event_long.csv`.
- `validation_report.json` passed with `ok=true` and `issue_count=0`.
