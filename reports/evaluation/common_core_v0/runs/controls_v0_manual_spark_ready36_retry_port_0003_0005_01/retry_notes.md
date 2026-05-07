# Retry Notes

## Original Failure

This retry package is anchored to the original run:
- `reports/evaluation/common_core_v0/runs/controls_v0_manual_spark_ready36_01/`

The original failures were:
- `PORT_0003`: `SparkRuntimeException [LOCATION_ALREADY_EXISTS]` for managed-table location `spark-warehouse/schools`
- `PORT_0005`: `SparkRuntimeException [LOCATION_ALREADY_EXISTS]` for managed-table location `spark-warehouse/drivers`

These were infrastructure / local Spark warehouse state failures, not SQL semantic mismatches.

## Manual Remediation

Before retry, the human manually removed only the stale Spark warehouse directories:
- `spark-warehouse/schools`
- `spark-warehouse/drivers`

No case files or registry files were modified as part of this recording step.

## Retry Evidence

Retried commands:
- `bash cases/PORT/PORT_0003/validation/run_spark_validation.sh`
- `bash cases/PORT/PORT_0005/validation/run_spark_validation.sh`

Observed retry results:
- both commands exited `0`
- retry stdout shows Spark environment startup
- retry stderr shows Spark warnings only
- no traceback appears in the retry stderr logs

## Materialization Guidance

When these retries are folded into a later Spark materialization pass:
- preserve the original `controls_v0_manual_spark_ready36_01` failure provenance
- preserve this retry package as separate recovery provenance
- do not collapse the history into a misleading “always succeeded” story
