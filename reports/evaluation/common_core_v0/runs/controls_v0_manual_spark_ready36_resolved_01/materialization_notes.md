# Materialization Notes

- This package materializes a resolved Spark ready36 controls subset for Common-core v0.
- It includes all `36` cases marked `ready_for_manual_spark_validation` in the Spark coverage audit.
- The four `artifact_reuse_only` performance cases are intentionally excluded.
- Performance, consistency, and longtail rows are derived from Spark result-check evidence such as `source_positive_equal` and `source_negative_different` or equivalent legacy Spark fields.
- Portability rows are derived only from route combinations supported by the cross-dialect checker; `native_source` remains explicit as `skipped` / `unsupported` for portability cases.
- `PORT_0003` and `PORT_0005` originally failed in `controls_v0_manual_spark_ready36_01` because of Spark `LOCATION_ALREADY_EXISTS` against stale `spark-warehouse` directories.
- This resolved package uses the targeted retry success records from `controls_v0_manual_spark_ready36_retry_port_0003_0005_01` for those two cases.
- Original failure provenance and retry provenance are both preserved in the resolved row notes and artifact paths.
- `controls_summary.csv` is derived directly from `run_event_long.csv`.
- `validation_report.json` passed with `ok=true` and `issue_count=0`.
