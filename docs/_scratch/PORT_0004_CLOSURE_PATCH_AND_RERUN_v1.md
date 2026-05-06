# PORT_0004_CLOSURE_PATCH_AND_RERUN_v1

## 0. Purpose And Boundary
- `PORT_0004` only
- MySQL/Spark validation script patch + rerun
- no speedup
- no `SpeedupTransferRate`
- no other PORT cases

## 1. Prior Failure Recap
- MySQL script contract was incomplete
- Spark script was not idempotent
- `cross_engine_closed` was previously `false`

## 2. Patch Summary
### MySQL
- files changed:
  - `cases/PORT/PORT_0004/validation/run_mysql_validation.sh`
- candidate execution step added: `no`
- result_check generation step added: `yes`
- output paths:
  - source TSV: `cases/PORT/PORT_0004/runs/mysql/source.tsv`
  - result check: `cases/PORT/PORT_0004/runs/mysql/result_check.json`
- notes:
  - `PORT_0004` treats MySQL as the source-reference engine
  - no MySQL-specific positive rewrite SQL exists in the case package, so the patch did not invent a fake `rewrite_pos_01.tsv`
  - instead, the script now emits the package checker JSON when the full MySQL/PG/Spark TSV set exists

### Spark
- files changed:
  - `cases/PORT/PORT_0004/validation/run_spark_validation.sh`
- cleanup/idempotency strategy:
  - isolate Spark warehouse under `cases/PORT/PORT_0004/runs/spark/warehouse`
  - drop and recreate a case-local validation database before DDL/load
- output paths:
  - positive TSV: `cases/PORT/PORT_0004/runs/spark/rewrite_pos_02_spark.tsv`
  - negative TSV: `cases/PORT/PORT_0004/runs/spark/rewrite_neg_02_spark.tsv`
  - result check: `cases/PORT/PORT_0004/runs/spark/result_check.json`

## 3. MySQL Rerun Result
- command: `bash cases/PORT/PORT_0004/validation/run_mysql_validation.sh`
- execution_status: `success`
- source artifact path: `cases/PORT/PORT_0004/runs/mysql/source.tsv`
- candidate artifact path: `not_applicable_source_reference_engine`
- result_check path: `cases/PORT/PORT_0004/runs/mysql/result_check.json`
- consistency_status: `consistent`
- failure_category: `none`
- failure_summary: ``

## 4. Spark Rerun Result
- command: `bash cases/PORT/PORT_0004/validation/run_spark_validation.sh`
- execution_status: `success`
- source artifact path: `not_applicable_target_rewrite_engine`
- candidate artifact path: `cases/PORT/PORT_0004/runs/spark/rewrite_pos_02_spark.tsv`
- result_check path: `cases/PORT/PORT_0004/runs/spark/result_check.json`
- consistency_status: `consistent`
- failure_category: `none`
- failure_summary: ``

## 5. Updated PORT_0004 Closure Status
- `mysql_closed`: `yes`
- `spark_closed`: `yes`
- `cross_engine_closed`: `yes`
- remaining blockers: `[]`

## 6. Impact On Transfer Readiness
- `SpeedupTransferRate` remains `not_computed`
- `PORT_0004` now joins the bounded cross-engine closed subset
- no transfer metric is computed here

## 7. Recommended Next Step
- `update PORT cross-engine closure snapshot with PORT_0004 result`

## 8. Non-Modification Note
- only `PORT_0004` targeted
- no speedup
- no `SpeedupTransferRate`
- no model/API
- no registry/review/rules/EXECUTION_STATUS changes
- taxonomy notes untouched
