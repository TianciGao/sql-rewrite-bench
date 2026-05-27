# PORT_0012_0013_MYSQL_SPARK_CLOSURE_PATCH_AND_RERUN_v1

## 0. Purpose And Boundary
- PORT_0012 / PORT_0013 only
- MySQL/Spark validation-script patch + rerun
- no PostgreSQL
- no speedup
- no SpeedupTransferRate
- no canonical SQL edits

## 1. Preflight Recap
- PG-side route packet is closed `6/6`
- PORT_0012 / PORT_0013 were pending MySQL/Spark closure
- MySQL/Spark DDL, witness files, validation scripts, and prior run artifacts already existed
- the blocker was missing engine-local `result_check.json` generation in the validation wrappers

## 2. Patch Summary
| file | change made | engine-local result_check generation added | expected output paths | canonical SQL unchanged because |
| --- | --- | --- | --- | --- |
| `cases/PORT/PORT_0012/validation/run_mysql_validation.sh` | preserved existing MySQL rewrite execution, then invoked `check_results.py` into `runs/mysql/result_check.json` when PG + Spark TSV dependencies are present | yes | `runs/mysql/rewrite_pos_01.tsv`, `runs/mysql/rewrite_neg_01.tsv`, `runs/mysql/result_check.json` | the gap was closure-contract emission, not SQL semantics |
| `cases/PORT/PORT_0012/validation/run_spark_validation.sh` | preserved existing Spark rewrite execution, then invoked `check_results.py` into `runs/spark/result_check.json` when PG + MySQL TSV dependencies are present | yes | `runs/spark/rewrite_pos_01.tsv`, `runs/spark/rewrite_neg_01.tsv`, `runs/spark/result_check.json` | the gap was closure-contract emission, not SQL semantics |
| `cases/PORT/PORT_0013/validation/run_mysql_validation.sh` | preserved existing MySQL source execution, then invoked `check_results.py` into `runs/mysql/result_check.json` when PG + Spark TSV dependencies are present | yes | `runs/mysql/source.tsv`, `runs/mysql/result_check.json` | the gap was closure-contract emission, not SQL semantics |
| `cases/PORT/PORT_0013/validation/run_spark_validation.sh` | preserved existing Spark rewrite execution, then invoked `check_results.py` into `runs/spark/result_check.json` when MySQL + PG TSV dependencies are present | yes | `runs/spark/rewrite_pos_01.tsv`, `runs/spark/rewrite_neg_01.tsv`, `runs/spark/result_check.json` | the gap was closure-contract emission, not SQL semantics |

## 3. MySQL Rerun Results
| case_id | command | execution_status | source/candidate TSV paths used or generated | result_check_path | consistency_status | failure_category | failure_summary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PORT_0012` | `bash cases/PORT/PORT_0012/validation/run_mysql_validation.sh` | success | generated `cases/PORT/PORT_0012/runs/mysql/rewrite_pos_01.tsv`, `cases/PORT/PORT_0012/runs/mysql/rewrite_neg_01.tsv`; used existing `cases/PORT/PORT_0012/runs/pg/source.tsv` and `cases/PORT/PORT_0012/runs/spark/*.tsv` for checker | `cases/PORT/PORT_0012/runs/mysql/result_check.json` | consistent / validated | none | none |
| `PORT_0013` | `bash cases/PORT/PORT_0013/validation/run_mysql_validation.sh` | success | generated `cases/PORT/PORT_0013/runs/mysql/source.tsv`; used existing `cases/PORT/PORT_0013/runs/pg/rewrite_pos_01.tsv`, `cases/PORT/PORT_0013/runs/pg/rewrite_neg_01.tsv`, and `cases/PORT/PORT_0013/runs/spark/*.tsv` for checker | `cases/PORT/PORT_0013/runs/mysql/result_check.json` | consistent / validated | none | none |

## 4. Spark Rerun Results
| case_id | command | execution_status | source/candidate TSV paths used or generated | result_check_path | consistency_status | failure_category | failure_summary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PORT_0012` | `bash cases/PORT/PORT_0012/validation/run_spark_validation.sh` | success | regenerated `cases/PORT/PORT_0012/runs/spark/rewrite_pos_01.tsv`, `cases/PORT/PORT_0012/runs/spark/rewrite_neg_01.tsv`; used `cases/PORT/PORT_0012/runs/pg/source.tsv` and `cases/PORT/PORT_0012/runs/mysql/*.tsv` for checker | `cases/PORT/PORT_0012/runs/spark/result_check.json` | consistent / validated | none | none |
| `PORT_0013` | `bash cases/PORT/PORT_0013/validation/run_spark_validation.sh` | success | regenerated `cases/PORT/PORT_0013/runs/spark/rewrite_pos_01.tsv`, `cases/PORT/PORT_0013/runs/spark/rewrite_neg_01.tsv`; used `cases/PORT/PORT_0013/runs/mysql/source.tsv` and `cases/PORT/PORT_0013/runs/pg/*.tsv` for checker | `cases/PORT/PORT_0013/runs/spark/result_check.json` | consistent / validated | none | none |

## 5. Updated Cross-engine Closure Status
- `PORT_0012 mysql_closed = yes`
- `PORT_0012 spark_closed = yes`
- `PORT_0012 cross_engine_closed = yes`
- `PORT_0013 mysql_closed = yes`
- `PORT_0013 spark_closed = yes`
- `PORT_0013 cross_engine_closed = yes`
- updated bounded closed subset: `PORT_0004`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`

## 6. SpeedupTransferRate Status
- `not_computed`
- this task only patched closure-contract emission and reran MySQL/Spark validation
- no speedup or target-engine benefit measurement was run
- no transfer metric is computed here even though bounded cross-engine closure now reaches `6/6`

## 7. Recommended Next Step
- `update PORT cross-engine closure snapshot with PORT_0012 / PORT_0013 results`

## 8. Non-Modification Note
- only PORT_0012 / PORT_0013 were targeted
- no PostgreSQL rerun
- no speedup
- no SpeedupTransferRate
- no model/API
- no registry/review/rules/EXECUTION_STATUS changes
- taxonomy notes untouched
