# PORT_0012_0013_MYSQL_SPARK_CLOSURE_PREFLIGHT_v1

## 0. Purpose And Boundary
- read-only closure preflight
- PORT_0012 / PORT_0013 only
- no DB execution
- no checker/speedup
- no SpeedupTransferRate
- no artifact modification

## 1. Current Snapshot Recap
- PG-side route packet is now closed 6/6
- cross-engine closed subset remains 4/6
- PORT_0012 / PORT_0013 are pending MySQL/Spark closure
- SpeedupTransferRate is not computed

## 2. Artifact Inventory
### PORT_0012
- source SQL: `cases/PORT/PORT_0012/source.sql`
- rewrite SQL: `cases/PORT/PORT_0012/rewrite_pos_01.sql`
- MySQL DDL: `cases/PORT/PORT_0012/schema/ddl_mysql.sql`
- MySQL witness: `cases/PORT/PORT_0012/validation/mysql_witness_data.sql`
- MySQL script: `cases/PORT/PORT_0012/validation/run_mysql_validation.sh`
- Spark DDL: `cases/PORT/PORT_0012/schema/ddl_spark.sql`
- Spark witness: `cases/PORT/PORT_0012/validation/spark_witness_data.sql`
- Spark script: `cases/PORT/PORT_0012/validation/run_spark_validation.sh`
- existing runs/mysql artifacts: `['cases/PORT/PORT_0012/runs/mysql/plans/rewrite_neg_01.json', 'cases/PORT/PORT_0012/runs/mysql/plans/rewrite_pos_01.json', 'cases/PORT/PORT_0012/runs/mysql/rewrite_neg_01.tsv', 'cases/PORT/PORT_0012/runs/mysql/rewrite_pos_01.tsv']`
- existing runs/spark artifacts: `['cases/PORT/PORT_0012/runs/spark/plans/rewrite_neg_01.txt', 'cases/PORT/PORT_0012/runs/spark/plans/rewrite_pos_01.txt', 'cases/PORT/PORT_0012/runs/spark/rewrite_neg_01.tsv', 'cases/PORT/PORT_0012/runs/spark/rewrite_pos_01.tsv']`
- root result_check state: `cases/PORT/PORT_0012/runs/result_check.json`
- PG-route repair artifact: `/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0012/sqlglot_pg_route_patched.sql`

### PORT_0013
- source SQL: `cases/PORT/PORT_0013/source.sql`
- rewrite SQL: `cases/PORT/PORT_0013/rewrite_pos_01.sql`
- MySQL DDL: `cases/PORT/PORT_0013/schema/ddl_mysql.sql`
- MySQL witness: `cases/PORT/PORT_0013/validation/mysql_witness_data.sql`
- MySQL script: `cases/PORT/PORT_0013/validation/run_mysql_validation.sh`
- Spark DDL: `cases/PORT/PORT_0013/schema/ddl_spark.sql`
- Spark witness: `cases/PORT/PORT_0013/validation/spark_witness_data.sql`
- Spark script: `cases/PORT/PORT_0013/validation/run_spark_validation.sh`
- existing runs/mysql artifacts: `['cases/PORT/PORT_0013/runs/mysql/plans/source.json', 'cases/PORT/PORT_0013/runs/mysql/source.tsv']`
- existing runs/spark artifacts: `['cases/PORT/PORT_0013/runs/spark/plans/rewrite_neg_01.txt', 'cases/PORT/PORT_0013/runs/spark/plans/rewrite_pos_01.txt', 'cases/PORT/PORT_0013/runs/spark/rewrite_neg_01.tsv', 'cases/PORT/PORT_0013/runs/spark/rewrite_pos_01.tsv']`
- root result_check state: `cases/PORT/PORT_0013/runs/result_check.json`
- PG-route repair artifact: `/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0013/sqlglot_pg_route_patched.sql`

## 3. Readiness Analysis
| case_id | mysql_artifacts_ready | spark_artifacts_ready | mysql_script_status | spark_script_status | likely_temp_sql_needed | stale_failure_artifacts | readiness_status | blockers | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PORT_0012 | yes | yes | rewrite_only_scaffold_no_result_check_generation | rewrite_only_scaffold_no_result_check_generation | no_new_engine_surface_patch_obvious | no | ready_after_engine_surface_temp_sql_patch | validation_scripts_do_not_emit_engine_local_result_check | patch validation scripts first, then execute |
| PORT_0013 | yes | yes | source_only_scaffold_no_result_check_generation | spark_specific_rewrite_scaffold_no_result_check_generation | no_new_engine_surface_patch_obvious | no | ready_after_engine_surface_temp_sql_patch | validation_scripts_do_not_emit_engine_local_result_check | patch validation scripts first, then execute |

## 4. Execution Boundary If Approved
- cases: `['PORT_0012', 'PORT_0013']`
- engines: `['mysql', 'spark']`
- allowed scripts: `['cases/PORT/PORT_0012/validation/run_mysql_validation.sh', 'cases/PORT/PORT_0012/validation/run_spark_validation.sh', 'cases/PORT/PORT_0013/validation/run_mysql_validation.sh', 'cases/PORT/PORT_0013/validation/run_spark_validation.sh']`
- expected artifacts: `['cases/PORT/PORT_0012/runs/mysql/rewrite_pos_01.tsv', 'cases/PORT/PORT_0012/runs/mysql/rewrite_neg_01.tsv', 'cases/PORT/PORT_0012/runs/spark/rewrite_pos_01.tsv', 'cases/PORT/PORT_0012/runs/spark/rewrite_neg_01.tsv', 'cases/PORT/PORT_0013/runs/mysql/source.tsv', 'cases/PORT/PORT_0013/runs/spark/rewrite_pos_01.tsv', 'cases/PORT/PORT_0013/runs/spark/rewrite_neg_01.tsv', 'engine-local or root-level result_check artifacts after checker invocation']`
- no speedup
- no SpeedupTransferRate
- no PG rerun unless scripts require reference reads only

## 5. Recommended Next Step
- `patch validation scripts first, then execute`

## 6. Non-Modification Note
- no execution
- no DB/checker/speedup
- no SpeedupTransferRate
- no model/API
- no registry/review/rules/EXECUTION_STATUS changes
- taxonomy notes untouched
