# PORT_0004_MYSQL_SPARK_CLOSURE_EXECUTION_v1

## 0. Purpose And Boundary
- `PORT_0004` only
- MySQL + Spark closure execution
- no speedup
- no SpeedupTransferRate
- no other PORT cases

## 1. Artifact Bundle Recap
- standardized witness files were present before execution:
  - `cases/PORT/PORT_0004/validation/mysql_witness_data.sql`
  - `cases/PORT/PORT_0004/validation/spark_witness_data.sql`
- future command manifests existed under `/tmp/rewritebench_port_closure_artifacts/PORT_0004/` and were previously marked `NOT RUN`
- prior PG-side route evidence already existed in `reports/formal_port/result_checks/sqlglot_transpile/port_0004.json` and `reports/formal_port/result_checks/llm_direct_translate/port_0004.json`
- no fake MySQL/Spark result artifacts existed before this execution attempt

## 2. MySQL Closure Result
- command: `bash cases/PORT/PORT_0004/validation/run_mysql_validation.sh`
- execution_status: `partial_success_output_contract_incomplete`
- result_check path: `cases/PORT/PORT_0004/runs/mysql/result_check.json`
- consistency_status: `unknown`
- source artifact path: `cases/PORT/PORT_0004/runs/mysql/source.tsv`
- candidate artifact path: `cases/PORT/PORT_0004/runs/mysql/rewrite_pos_01.tsv`
- failure_category: `missing_candidate_and_result_check`
- failure_summary: script exited successfully but did not produce `runs/mysql/rewrite_pos_01.tsv` or `runs/mysql/result_check.json`

## 3. Spark Closure Result
- command: `bash cases/PORT/PORT_0004/validation/run_spark_validation.sh`
- execution_status: `failed`
- result_check path: `cases/PORT/PORT_0004/runs/spark/result_check.json`
- consistency_status: `unknown`
- source artifact path: `cases/PORT/PORT_0004/runs/spark/source.tsv`
- candidate artifact path: `cases/PORT/PORT_0004/runs/spark/rewrite_pos_02_spark.tsv`
- failure_category: `spark_table_location_conflict`
- failure_summary: Spark failed with `LOCATION_ALREADY_EXISTS` for `spark_catalog.default.patient` at `spark-warehouse/patient` before producing a new `result_check.json`

## 4. Updated PORT_0004 Closure Status
- `mysql_closed`: `no`
- `spark_closed`: `no`
- `cross_engine_closed`: `no`
- remaining blockers:
  - `mysql_output_contract_incomplete`
  - `spark_table_location_conflict`

## 5. Impact On Transfer Readiness
- `SpeedupTransferRate` remains `not_computed`
- `PORT_0004` does not yet join the cross-engine closed subset because neither engine produced a fresh case-local closure result check in this run
- no transfer metric is computed or implied from this execution attempt

## 6. Recommended Next Step
- `diagnose PORT_0004 MySQL/Spark failures`

## 7. Non-Modification Note
- only `PORT_0004` was targeted
- no speedup
- no SpeedupTransferRate
- no model/API
- no registry/review/rules/EXECUTION_STATUS changes
- taxonomy notes untouched
