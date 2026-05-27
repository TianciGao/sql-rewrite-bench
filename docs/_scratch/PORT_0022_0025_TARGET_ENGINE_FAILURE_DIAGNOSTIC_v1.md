# PORT_0022_0025_TARGET_ENGINE_FAILURE_DIAGNOSTIC_v1

## 0. Purpose And Boundary
- read-only diagnostic
- `PORT_0022` / `PORT_0025` only
- no DB execution
- no checker/speedup
- no `SpeedupTransferRate`
- no script or artifact modification

## 1. Current Snapshot Recap
`PORT_0004` and `PORT_0024` are currently the bounded cross-engine closed subset. `PORT_0022` and `PORT_0025` remain unresolved on target-engine execution surfaces even though PG-side route evidence is already present. `SpeedupTransferRate` remains `not_computed` because the bounded cross-engine denominator is still incomplete and target-engine benefit evidence is not aligned.

## 2. Artifact Inventory
For both cases, the case packages include source SQL, MySQL DDL, Spark DDL, validation witness/load scripts, MySQL/Spark validation scripts, and case-local `runs/mysql` and `runs/spark` directories with failure artifacts. Both cases also have `result_check.json` files for MySQL and Spark, plus engine logs capturing the exact failure surface.

`PORT_0022`:
- source SQL present: [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/source.sql)
- MySQL package present: [ddl_mysql.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/schema/ddl_mysql.sql), validation witness/load files, `runs/mysql/result_check.json`
- Spark package present: [ddl_spark.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/schema/ddl_spark.sql), validation witness/load files, `runs/spark/result_check.json`
- MySQL rewrite artifact/log surface present: `runs/mysql/rewrite_pos_01.log`
- Spark source failure logs present: `runs/spark/load_and_execute.log`, `runs/spark/stderr.log`

`PORT_0025`:
- source SQL present: [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/source.sql)
- MySQL package present: [ddl_mysql.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/schema/ddl_mysql.sql), validation witness/load files, `runs/mysql/result_check.json`
- Spark package present: [ddl_spark.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/schema/ddl_spark.sql), validation witness/load files, `runs/spark/result_check.json`
- MySQL rewrite artifact/log surface present: `runs/mysql/rewrite_pos_01.log`
- Spark source failure logs present: `runs/spark/load_and_execute.log`, `runs/spark/stderr.log`

## 3. PORT_0022 Diagnostic
### MySQL
- classification: `mysql_timestamp_rewrite_surface_failure`
- existing artifacts: `runs/mysql/source.tsv`, `runs/mysql/rewrite_pos_01.log`, `runs/mysql/result_check.json`
- exact failure evidence: MySQL `result_check.json` and rewrite log report `ERROR 1064` near `TIMESTAMP)) = 2010`
- likely root cause: the positive rewrite surface is PostgreSQL-style SQL, specifically `EXTRACT(YEAR FROM CAST(t1.creationdate AS TIMESTAMP)) = 2010`, and that surface is being executed directly in MySQL
- likely minimal fix: bounded MySQL rewrite-surface normalization for year extraction and timestamp casting on the PORT bounded subset
- risk: `medium`

### Spark
- classification: `spark_unsupported_datetime_source_failure`
- existing artifacts: `runs/spark/result_check.json`, `runs/spark/load_and_execute.log`, `runs/spark/stderr.log`
- exact failure evidence: Spark `result_check.json` and logs report `[UNSUPPORTED_DATATYPE] Unsupported data type "DATETIME"` during source execution
- likely root cause: source SQL uses MySQL-oriented `CAST( t1.creationdate AS DATETIME )` inside `DATE_FORMAT(...)`, and Spark rejects that type surface before rewrite execution begins
- likely minimal fix: bounded Spark source-surface normalization away from `DATETIME`
- risk: `medium`

## 4. PORT_0025 Diagnostic
### MySQL
- classification: `mysql_timestamp_rewrite_surface_failure`
- existing artifacts: `runs/mysql/source.tsv`, `runs/mysql/rewrite_pos_01.log`, `runs/mysql/result_check.json`
- exact failure evidence: MySQL `result_check.json` and rewrite log report `ERROR 1064` near `TIMESTAMP)) = 1993`
- likely root cause: the positive rewrite surface again uses PostgreSQL-style `EXTRACT(YEAR FROM CAST(t2.account_date AS TIMESTAMP)) = 1993`, which is not valid MySQL execution surface as written
- likely minimal fix: bounded MySQL rewrite-surface normalization shared with `PORT_0022`
- risk: `medium`

### Spark
- classification: `spark_unsupported_datetime_source_failure`
- existing artifacts: `runs/spark/result_check.json`, `runs/spark/load_and_execute.log`, `runs/spark/stderr.log`
- exact failure evidence: Spark `result_check.json` and logs report `[UNSUPPORTED_DATATYPE] Unsupported data type "DATETIME"` during source execution
- likely root cause: source SQL uses MySQL-oriented `CAST( t2.account_date AS DATETIME )` inside `DATE_FORMAT(...)`, which Spark rejects before it can evaluate the target rewrite
- likely minimal fix: bounded Spark source-surface normalization shared with `PORT_0022`
- risk: `medium`

## 5. Cross-case Pattern
`PORT_0022` and `PORT_0025` share the same split portability pattern:
- MySQL failure surface: PostgreSQL rewrite SQL executed in MySQL
- Spark failure surface: MySQL-style `DATETIME` source SQL executed in Spark

This makes a bounded shared repair path reasonable. The safer grouping is by engine surface rather than by case:
- one MySQL rewrite-surface repair shared across both cases
- one Spark source-surface repair shared across both cases

The MySQL and Spark repairs should still be treated as separate implementation tasks, because they touch different SQL surfaces and carry different regression risks.

## 6. Recommended Fix Plan
Patch both engine surfaces in a bounded way:
- convert the MySQL target rewrite surface away from PostgreSQL `EXTRACT(... AS TIMESTAMP)` execution surface
- convert the Spark source surface away from MySQL `DATETIME` casting

This is the smallest repair plan that addresses the verified failure surfaces without broadening PORT scope or inferring transfer evidence prematurely.

## 7. Recommended Next Step
- `patch both MySQL and Spark surfaces then rerun bounded closure`

## 8. Non-Modification Note
- no execution
- no checker/speedup
- no `SpeedupTransferRate`
- no model/API
- no registry/review/rules/`EXECUTION_STATUS` changes
- no case/script/artifact modifications
- taxonomy notes untouched
