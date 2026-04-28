# Validation Draft Notes

`PORT_0004` has not been validated yet.

This directory now contains draft executable-looking validation scaffolding:

- `load_witness_pg.sql`
- `load_witness_mysql.sql`
- `load_witness_spark.sql`
- `run_pg_validation.sh`
- `run_mysql_validation.sh`
- `run_spark_validation.sh`
- `check_results.py`

A later validation task should:

1. review the witness rows against the portability claim,
2. confirm the draft DDLs are acceptable for each engine,
3. run the per-engine scripts manually in a prepared shell,
4. inspect the generated `runs/<engine>/` outputs,
5. treat any success as draft evidence only until registry writeback is explicitly requested.

No engine commands have been run for this draft package in the current task.
