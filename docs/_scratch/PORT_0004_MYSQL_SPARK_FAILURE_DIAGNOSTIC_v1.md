# PORT_0004_MYSQL_SPARK_FAILURE_DIAGNOSTIC_v1

## 0. Purpose And Boundary
- read-only diagnostic
- `PORT_0004` only
- no DB execution
- no checker/speedup
- no `SpeedupTransferRate`
- no script or artifact modification

## 1. Prior Closure Attempt Recap
- MySQL ended in `partial_success_output_contract_incomplete`
- `cases/PORT/PORT_0004/runs/mysql/source.tsv` and `cases/PORT/PORT_0004/runs/mysql/plans/source.json` were produced
- `cases/PORT/PORT_0004/runs/mysql/rewrite_pos_01.tsv` and `cases/PORT/PORT_0004/runs/mysql/result_check.json` were not produced
- Spark failed with `LOCATION_ALREADY_EXISTS` for `spark_catalog.default.patient` at `spark-warehouse/patient`
- `cross_engine_closed` remains `false`

## 2. Artifact Inventory
### MySQL
- present:
  - `cases/PORT/PORT_0004/runs/mysql/source.tsv`
  - `cases/PORT/PORT_0004/runs/mysql/plans/source.json`
- expected but missing:
  - `cases/PORT/PORT_0004/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0004/runs/mysql/result_check.json`
- no case-local MySQL stdout/stderr log artifact was found

### Spark
- present:
  - `cases/PORT/PORT_0004/runs/spark/rewrite_pos_02_spark.tsv`
  - `cases/PORT/PORT_0004/runs/spark/rewrite_neg_02_spark.tsv`
  - `cases/PORT/PORT_0004/runs/spark/plans/rewrite_pos_02_spark.txt`
  - `cases/PORT/PORT_0004/runs/spark/plans/rewrite_neg_02_spark.txt`
- expected but missing:
  - `cases/PORT/PORT_0004/runs/spark/source.tsv`
  - `cases/PORT/PORT_0004/runs/spark/result_check.json`
- warehouse-path evidence exists:
  - `spark-warehouse/patient`

## 3. MySQL Diagnostic
- classification: `mysql_script_contract_incomplete`
- evidence:
  - `run_mysql_validation.sh` loads `schema/ddl_mysql.sql` and `validation/load_witness_mysql.sql`
  - the script runs only `source.sql` to `runs/mysql/source.tsv`
  - the script contains no `rewrite_pos_01.sql` or `rewrite_neg_01.sql` execution step
  - the script contains no `result_check.json` creation or `check_results.py` invocation
  - `validation/README.md` explicitly describes `check_results.py` as a later separate step after MySQL, PostgreSQL, and Spark TSV generation
  - `check_results.py` expects the MySQL source TSV plus PG/Spark TSVs; it does not imply a MySQL candidate TSV
- conclusion:
  - the failure is not a route candidate path typo inside the script
  - the script exited successfully because it completed its narrow source-reference job
  - the closure execution wrapper expected a fuller closure packet than the script is designed to emit
- likely minimal fix:
  - patch the MySQL closure output contract so either:
    - the closure runner stops expecting `runs/mysql/rewrite_pos_01.tsv` and `runs/mysql/result_check.json` from `run_mysql_validation.sh` alone, or
    - the MySQL-side closure flow explicitly adds the separate checker step after the PG/Spark TSVs exist
- risk: `medium`

## 4. Spark Diagnostic
- classification: `spark_script_not_idempotent`
- evidence:
  - `run_spark_validation.sh` executes `ddl_spark.sql` statements directly via `spark.sql(...)`
  - the script contains no `DROP TABLE` or `DROP DATABASE` cleanup logic
  - the script does not isolate execution into a unique temp database or warehouse location
  - `spark-warehouse/patient` exists in the repo root
  - the observed failure was `LOCATION_ALREADY_EXISTS` for `spark_catalog.default.patient`
- conclusion:
  - this is an environment cleanup/idempotency problem, not a result-checker problem
  - a rerun without cleanup is likely to fail again on the same warehouse location
- likely minimal fix:
  - patch the Spark validation path to make setup idempotent, preferably by:
    - using an isolated temp database/location, or
    - adding explicit cleanup before create
- risk: `medium`

## 5. Recommended Fix Plan
- split the repair into two targeted tasks
- MySQL task:
  - align the closure runner and/or script contract with the actual cross-dialect workflow
  - ensure `result_check.json` is created only after the full TSV set exists
- Spark task:
  - add cleanup/idempotency around the managed `patient` table or isolate the warehouse location
- rerun closure only after both fixes land

## 6. Recommended Next Step
- `patch both PORT_0004 MySQL output contract and Spark cleanup, then rerun closure`

## 7. Non-Modification Note
- no DB execution
- no checker/speedup
- no `SpeedupTransferRate`
- no model/API
- no registry/review/rules/EXECUTION_STATUS changes
- no case/script/artifact modifications
- taxonomy notes untouched
