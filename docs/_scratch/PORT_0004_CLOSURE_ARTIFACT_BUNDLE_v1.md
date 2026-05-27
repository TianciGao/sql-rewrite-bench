# PORT_0004_CLOSURE_ARTIFACT_BUNDLE_v1

## 0. Purpose And Boundary
- PORT_0004 closure artifact bundle only
- no DB execution
- no checker
- no speedup
- no SpeedupTransferRate
- no fake results

## 1. Prior Readiness Recap
- `PORT_0004` was artifact-contract blocked
- PG-side route evidence exists
- MySQL/Spark standardized witness artifacts were missing
- `PORT_0022`, `PORT_0025`, and `PORT_0024` are out of scope

## 2. Existing PORT_0004 Artifacts
- `source_sql`: `cases/PORT/PORT_0004/source.sql`
- `ddl_mysql`: `cases/PORT/PORT_0004/schema/ddl_mysql.sql`
- `ddl_pg`: `cases/PORT/PORT_0004/schema/ddl_pg.sql`
- `ddl_spark`: `cases/PORT/PORT_0004/schema/ddl_spark.sql`
- `validation_readme`: `cases/PORT/PORT_0004/validation/README.md`
- `checker_yaml`: `cases/PORT/PORT_0004/validation/checker.yaml`
- `load_witness_mysql`: `cases/PORT/PORT_0004/validation/load_witness_mysql.sql`
- `load_witness_spark`: `cases/PORT/PORT_0004/validation/load_witness_spark.sql`
- `pg_llm_result_check`: `reports/formal_port/result_checks/llm_direct_translate/port_0004.json`
- `pg_sqlglot_result_check`: `reports/formal_port/result_checks/sqlglot_transpile/port_0004.json`

## 3. Created / Verified Standardized Artifacts
| artifact_path | status | derived_from | notes |
| --- | --- | --- | --- |
| cases/PORT/PORT_0004/validation/mysql_witness_data.sql | created | cases/PORT/PORT_0004/validation/load_witness_mysql.sql | standardized deterministic copy of existing MySQL loader draft |
| cases/PORT/PORT_0004/validation/spark_witness_data.sql | created | cases/PORT/PORT_0004/validation/load_witness_spark.sql | standardized deterministic copy of existing Spark loader draft |
| /tmp/rewritebench_port_closure_artifacts/PORT_0004/mysql/future_command_NOT_RUN.txt | created | cases/PORT/PORT_0004/validation/run_mysql_validation.sh | future command manifest, explicitly NOT RUN |
| /tmp/rewritebench_port_closure_artifacts/PORT_0004/spark/future_command_NOT_RUN.txt | created | cases/PORT/PORT_0004/validation/run_spark_validation.sh | future command manifest, explicitly NOT RUN |
| /tmp/rewritebench_port_closure_artifacts/PORT_0004/closure_artifact_paths.json | created | bundle metadata generated in this task | artifact index only, no execution results |
| /tmp/rewritebench_port_closure_artifacts/PORT_0004/DO_NOT_RUN_YET.txt | created | bundle metadata generated in this task | hard stop marker for future execution |

## 4. Future Closure Commands
- MySQL command path: `/tmp/rewritebench_port_closure_artifacts/PORT_0004/mysql/future_command_NOT_RUN.txt`
- MySQL intended command: `bash cases/PORT/PORT_0004/validation/run_mysql_validation.sh`
- MySQL status: `NOT RUN`
- MySQL expected result artifacts: `['cases/PORT/PORT_0004/runs/mysql/source.tsv', 'cases/PORT/PORT_0004/runs/mysql/rewrite_pos_01.tsv', 'cases/PORT/PORT_0004/runs/mysql/result_check.json']`
- Spark command path: `/tmp/rewritebench_port_closure_artifacts/PORT_0004/spark/future_command_NOT_RUN.txt`
- Spark intended command: `bash cases/PORT/PORT_0004/validation/run_spark_validation.sh`
- Spark status: `NOT RUN`
- Spark expected result artifacts: `['cases/PORT/PORT_0004/runs/spark/source.tsv', 'cases/PORT/PORT_0004/runs/spark/rewrite_pos_02_spark.tsv', 'cases/PORT/PORT_0004/runs/spark/result_check.json']`

## 5. Remaining Gaps
- route candidate SQL file path is not discoverable from existing SQLGlot/LLM reports
- actual MySQL execution not run
- actual Spark execution not run
- case-local runs/mysql/result_check.json absent by design because no execution occurred
- case-local runs/spark/result_check.json absent by design because no execution occurred
- SpeedupTransferRate not ready

## 6. Recommended Next Step
- `run PORT_0004 MySQL/Spark closure execution`

## 7. Non-Modification Note
- no DB execution
- no checker/speedup
- no model/API
- no SpeedupTransferRate
- no registry/review/rules/EXECUTION_STATUS changes
- no fake result artifacts
- taxonomy notes untouched
