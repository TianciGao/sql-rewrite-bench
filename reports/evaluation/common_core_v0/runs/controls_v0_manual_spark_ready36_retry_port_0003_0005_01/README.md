# Spark Ready36 Retry For PORT_0003 And PORT_0005

This directory records a narrow human retry, not a full rerun of `controls_v0_manual_spark_ready36_01`.

Scope:
- `PORT_0003` Spark validation only
- `PORT_0005` Spark validation only

Why the retry was needed:
- the original Spark ready36 run failed on these two cases with `LOCATION_ALREADY_EXISTS`
- `PORT_0003` failed on stale `spark-warehouse/schools`
- `PORT_0005` failed on stale `spark-warehouse/drivers`

What changed before retry:
- the stale Spark managed-table directories were removed manually
- the human then reran:
  - `bash cases/PORT/PORT_0003/validation/run_spark_validation.sh`
  - `bash cases/PORT/PORT_0005/validation/run_spark_validation.sh`

Observed retry outcome:
- both retry commands exited `0`
- the retry stderr logs show Spark startup warnings only
- the retry stderr logs do not show a traceback

Provenance note:
- these retry successes should be merged carefully during later materialization
- the original failure provenance must be preserved alongside this retry provenance rather than overwritten
