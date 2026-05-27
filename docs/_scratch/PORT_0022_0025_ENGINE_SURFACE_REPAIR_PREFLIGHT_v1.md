# PORT_0022_0025_ENGINE_SURFACE_REPAIR_PREFLIGHT_v1

## 0. Purpose And Boundary
- read-only repair preflight
- `PORT_0022` / `PORT_0025` only
- no DB execution
- no checker/speedup
- no `SpeedupTransferRate`
- no script/case/artifact modification

## 1. Prior Diagnostic Recap
The verified failures are engine-surface portability failures, not artifact gaps:
- MySQL fails because the positive rewrite surface is PostgreSQL-style `EXTRACT(YEAR FROM CAST(... AS TIMESTAMP))`
- Spark fails because the source surface is MySQL-style `CAST(... AS DATETIME)` inside `DATE_FORMAT(...)`

Both cases already have PG-side route evidence and target-engine execution artifacts. The current blocker is therefore bounded SQL surface incompatibility at execution time, not missing witness data, missing outputs, or checker contract absence.

## 2. MySQL Rewrite Surface Analysis
| case_id | failing_expression | column_type_context | proposed_mysql_surface | patch_location_recommendation | risk | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `PORT_0022` | `EXTRACT(YEAR FROM CAST(t1.creationdate AS TIMESTAMP)) = 2010` | `creationdate DATETIME` in [ddl_mysql.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/schema/ddl_mysql.sql) | `YEAR(t1.creationdate) = 2010` | generated temporary SQL inside validation script | `medium` | `EXTRACT(YEAR FROM t1.creationdate)` may also work in MySQL, but `YEAR(...)` is the narrower bounded repair. |
| `PORT_0025` | `EXTRACT(YEAR FROM CAST(t2.account_date AS TIMESTAMP)) = 1993` | `account_date DATE` in [ddl_mysql.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/schema/ddl_mysql.sql) | `YEAR(t2.account_date) = 1993` | generated temporary SQL inside validation script | `medium` | The `TIMESTAMP` cast is unnecessary because the MySQL DDL already exposes a date-typed column. |

## 3. Spark Source Surface Analysis
| case_id | failing_expression | column_type_context | proposed_spark_surface | patch_location_recommendation | risk | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `PORT_0022` | `DATE_FORMAT( CAST( \`t1\`.\`creationdate\` AS DATETIME ) , '%Y' ) = '2010'` | `creationdate TIMESTAMP` in [ddl_spark.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/schema/ddl_spark.sql) | `date_format(CAST(\`t1\`.\`creationdate\` AS TIMESTAMP), 'yyyy') = '2010'` | generated temporary SQL inside validation script | `medium` | Spark DDL already uses `TIMESTAMP`, so replacing `DATETIME` with `TIMESTAMP` is semantically aligned and bounded. |
| `PORT_0025` | `DATE_FORMAT( CAST( \`t2\`.\`account_date\` AS DATETIME ) , '%Y' ) = '1993'` | `account_date DATE` in [ddl_spark.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/schema/ddl_spark.sql) | `date_format(CAST(\`t2\`.\`account_date\` AS TIMESTAMP), 'yyyy') = '1993'` | generated temporary SQL inside validation script | `medium` | Spark DDL already exposes a date-compatible column, so this can be normalized without changing case intent. |

## 4. Patch Location Recommendation
Compared options:
- editing canonical case SQL:
  - highest policy risk
  - mixes engine-specific portability fixes into canonical benchmark files
- editing engine-specific rewrite/source files:
  - better than canonical edits, but still changes case-local benchmark artifacts directly
- validation-script generated temp SQL:
  - safest route
  - keeps canonical case files unchanged
  - matches the current pattern where validation scripts already act as engine-specific execution adapters
- wrapper-level adapter normalization:
  - broader than needed for the bounded PORT subset
  - higher spillover risk to unrelated cases

Recommended route:
- `engine_specific_temp_sql_patch_needed`
- implement bounded temporary SQL generation inside the `PORT_0022` / `PORT_0025` MySQL and Spark validation scripts

## 5. Proposed Patch Plan
Exact files to change in the next task:
- [run_mysql_validation.sh](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/validation/run_mysql_validation.sh)
- [run_mysql_validation.sh](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/validation/run_mysql_validation.sh)
- [run_spark_validation.sh](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/validation/run_spark_validation.sh)
- [run_spark_validation.sh](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/validation/run_spark_validation.sh)

Exact temporary artifacts to create if patched:
- `cases/PORT/PORT_0022/runs/mysql/rewrite_pos_01.mysql_normalized.sql`
- `cases/PORT/PORT_0025/runs/mysql/rewrite_pos_01.mysql_normalized.sql`
- `cases/PORT/PORT_0022/runs/spark/source.spark_normalized.sql`
- `cases/PORT/PORT_0025/runs/spark/source.spark_normalized.sql`

Exact rerun scope:
- `PORT_0022` and `PORT_0025` only
- MySQL and Spark validation rerun only
- no PostgreSQL rerun
- no speedup
- no `SpeedupTransferRate`

Expected outputs if successful:
- `cases/PORT/PORT_0022/runs/mysql/result_check.json`
- `cases/PORT/PORT_0022/runs/spark/result_check.json`
- `cases/PORT/PORT_0025/runs/mysql/result_check.json`
- `cases/PORT/PORT_0025/runs/spark/result_check.json`

Rollback / non-overclaim boundary:
- if either engine still fails after bounded temp-SQL normalization, retain the current closure boundary and record the residual target-engine blocker rather than broadening the patch scope or editing canonical case semantics

## 6. Recommended Next Step
- `patch validation scripts to generate engine-specific temp SQL and rerun PORT_0022 / PORT_0025 closure`

## 7. Non-Modification Note
- no DB execution
- no checker/speedup
- no `SpeedupTransferRate`
- no model/API
- no registry/review/rules/`EXECUTION_STATUS` changes
- no case/script/artifact modifications
- taxonomy notes untouched
