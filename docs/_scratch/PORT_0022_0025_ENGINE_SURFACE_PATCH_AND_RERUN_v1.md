# PORT_0022_0025_ENGINE_SURFACE_PATCH_AND_RERUN_v1

## 0. Purpose And Boundary
- `PORT_0022` / `PORT_0025` only
- MySQL/Spark validation-script temp SQL patch + rerun
- no PostgreSQL
- no speedup
- no `SpeedupTransferRate`
- no canonical SQL edits

## 1. Preflight Recap
The bounded failures were engine-surface mismatches:
- MySQL rewrite-surface failure on PostgreSQL-style `EXTRACT(YEAR FROM CAST(... AS TIMESTAMP))`
- Spark source-surface failure on MySQL-style `CAST(... AS DATETIME)` inside `DATE_FORMAT(...)`

The selected repair strategy was to keep canonical case SQL unchanged and generate engine-specific temporary SQL inside the validation scripts only.

## 2. Patch Summary
| file | temp SQL generated | exact transformation | output path | why canonical case SQL was not modified |
| --- | --- | --- | --- | --- |
| [run_mysql_validation.sh](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/validation/run_mysql_validation.sh) | yes | `EXTRACT(YEAR FROM CAST(t1.creationdate AS TIMESTAMP))` -> `YEAR(t1.creationdate)` | `cases/PORT/PORT_0022/runs/mysql/rewrite_pos_01.mysql_normalized.sql` | The failure is MySQL execution surface only; canonical `rewrite_pos_01.sql` remains the benchmark artifact. |
| [run_mysql_validation.sh](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/validation/run_mysql_validation.sh) | yes | `EXTRACT(YEAR FROM CAST(t2.account_date AS TIMESTAMP))` -> `YEAR(t2.account_date)` | `cases/PORT/PORT_0025/runs/mysql/rewrite_pos_01.mysql_normalized.sql` | Same bounded MySQL-only execution repair. |
| [run_spark_validation.sh](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/validation/run_spark_validation.sh) | yes | `CAST(\`t1\`.\`creationdate\` AS DATETIME), '%Y'` -> `CAST(\`t1\`.\`creationdate\` AS TIMESTAMP), 'yyyy'` | `cases/PORT/PORT_0022/runs/spark/source.spark_normalized.sql` | The failure is Spark source-surface only; canonical `source.sql` stays unchanged. |
| [run_spark_validation.sh](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/validation/run_spark_validation.sh) | yes | `CAST(\`t2\`.\`account_date\` AS DATETIME), '%Y'` -> `CAST(\`t2\`.\`account_date\` AS TIMESTAMP), 'yyyy'` | `cases/PORT/PORT_0025/runs/spark/source.spark_normalized.sql` | Same bounded Spark-only execution repair. |

The patched MySQL scripts now:
- execute canonical `source.sql`
- generate normalized temporary MySQL rewrite SQL for positive and negative rewrites
- execute those normalized rewrites
- emit checker JSON when the full TSV contract exists

The patched Spark scripts now:
- generate normalized temporary Spark source SQL
- execute that normalized source SQL
- execute canonical positive and negative rewrites
- emit checker JSON and mirror it into the MySQL run directory when the full TSV contract exists

## 3. MySQL Rerun Results
| case_id | command | temp_sql_path | execution_status | result_check_path | consistency_status | failure_category | failure_summary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PORT_0022` | `bash cases/PORT/PORT_0022/validation/run_mysql_validation.sh` | `cases/PORT/PORT_0022/runs/mysql/rewrite_pos_01.mysql_normalized.sql` | `success` | `cases/PORT/PORT_0022/runs/mysql/result_check.json` | `validated` | `none` | checker confirms MySQL source matches PG positive and Spark positive, and differs from both negatives |
| `PORT_0025` | `bash cases/PORT/PORT_0025/validation/run_mysql_validation.sh` | `cases/PORT/PORT_0025/runs/mysql/rewrite_pos_01.mysql_normalized.sql` | `success` | `cases/PORT/PORT_0025/runs/mysql/result_check.json` | `validated` | `none` | checker confirms MySQL source matches PG positive and Spark positive, and differs from both negatives |

## 4. Spark Rerun Results
| case_id | command | temp_sql_path | execution_status | result_check_path | consistency_status | failure_category | failure_summary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PORT_0022` | `bash cases/PORT/PORT_0022/validation/run_spark_validation.sh` | `cases/PORT/PORT_0022/runs/spark/source.spark_normalized.sql` | `success` | `cases/PORT/PORT_0022/runs/spark/result_check.json` | `validated` | `none` | normalized Spark source executed, Spark positive matched MySQL source, Spark negative differed |
| `PORT_0025` | `bash cases/PORT/PORT_0025/validation/run_spark_validation.sh` | `cases/PORT/PORT_0025/runs/spark/source.spark_normalized.sql` | `success` | `cases/PORT/PORT_0025/runs/spark/result_check.json` | `validated` | `none` | normalized Spark source executed, Spark positive matched MySQL source, Spark negative differed |

## 5. Updated Cross-engine Closure Status
- `PORT_0022 mysql_closed = yes`
- `PORT_0022 spark_closed = yes`
- `PORT_0022 cross_engine_closed = yes`
- `PORT_0025 mysql_closed = yes`
- `PORT_0025 spark_closed = yes`
- `PORT_0025 cross_engine_closed = yes`

Updated bounded closed subset:
- `PORT_0004`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

## 6. SpeedupTransferRate Status
`SpeedupTransferRate` remains `not_computed`.

Even though bounded cross-engine closure improved, transfer metrics are still not ready here because:
- this task closed execution/consistency surfaces only
- no speedup or benefit measurements were run
- the broader aligned transfer denominator still remains incomplete because `PORT_0012` and `PORT_0013` are still PG-route/dialect blocked

## 7. Recommended Next Step
- `update PORT cross-engine closure snapshot with PORT_0022 / PORT_0025 results`

## 8. Non-Modification Note
- only `PORT_0022` / `PORT_0025` targeted
- no PostgreSQL
- no speedup
- no `SpeedupTransferRate`
- no model/API
- no registry/review/rules/`EXECUTION_STATUS` changes
- taxonomy notes untouched
