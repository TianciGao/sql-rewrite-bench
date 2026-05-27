# SQLGlot Same-Engine Execution Canary Triage

## Headline

- total method rows: `18`
- success count: `10`
- failure count: `8`

## Failure Counts By Engine

- `pg`: `1`
- `mysql`: `6`
- `spark`: `1`

## Failure Counts By Route

- `sqlglot_optimize_same_dialect`: `5`
- `sqlglot_transpile_same_dialect_noop`: `3`

## Failure Counts By Case

- `PERF_0006`: `2`
- `CONS_0007`: `4`
- `LONGTAIL_0011`: `2`

## Top Error Messages

- `MySQL access denied before database setup`: `6`
- `注意:  递归删除 表 ccv0_sqlglot_cons_0007_sqlglot_optimize_same_dialect.tmp_emps`: `1`
- `Generated SQL contains unresolved nested qualifier e2.e1.commission`: `1`

## Triage Split

Failure class counts:
- `mysql_runner_or_auth_setup_failure`: `6`
- `generated_sql_execution_failure`: `1`
- `other_execution_failure`: `1`

### MySQL Diagnosis

The MySQL failures look like runner/schema/setup failures, not generated SQL failures.

Evidence:
- every failed MySQL row dies at the initial `mysql -e "DROP DATABASE ...; CREATE DATABASE ..."` step
- stderr is the same in all six failed MySQL rows: `ERROR 1045 (28000): Access denied for user 'tianci_gao'@'localhost' (using password: NO)`
- that means the canary never reached schema load, witness-data load, source execution, or generated SQL execution on MySQL

### CONS_0007 Optimize Diagnosis

`CONS_0007` optimize failure is a SQLGlot-generated SQL issue, not an execution harness issue.

Evidence:
- PostgreSQL optimize row ran schema setup, witness load, and source SQL successfully before failing on the generated SQL file
- PostgreSQL stderr shows an invalid correlated reference involving `e2.e1.commission`
- Spark optimize row fails with the same semantic shape: unresolved nested qualifier `e2.e1.commission`
- the transpile/no-op route for `CONS_0007` succeeds on PostgreSQL and Spark, which argues against a generic harness failure for that case

## Failed Rows By Case / Engine / Route

- `PERF_0006` / `mysql` / `sqlglot_optimize_same_dialect`: `MySQL access denied before database setup`
- `PERF_0006` / `mysql` / `sqlglot_transpile_same_dialect_noop`: `MySQL access denied before database setup`
- `CONS_0007` / `pg` / `sqlglot_optimize_same_dialect`: `注意:  递归删除 表 ccv0_sqlglot_cons_0007_sqlglot_optimize_same_dialect.tmp_emps`
- `CONS_0007` / `mysql` / `sqlglot_optimize_same_dialect`: `MySQL access denied before database setup`
- `CONS_0007` / `mysql` / `sqlglot_transpile_same_dialect_noop`: `MySQL access denied before database setup`
- `CONS_0007` / `spark` / `sqlglot_optimize_same_dialect`: `Generated SQL contains unresolved nested qualifier e2.e1.commission`
- `LONGTAIL_0011` / `mysql` / `sqlglot_optimize_same_dialect`: `MySQL access denied before database setup`
- `LONGTAIL_0011` / `mysql` / `sqlglot_transpile_same_dialect_noop`: `MySQL access denied before database setup`

## Recommendation

- A. fix MySQL runner and rerun this canary: yes
- B. keep MySQL failures explicit and proceed to PG/Spark subset: yes
- C. inspect generated SQL before rerun: yes
- D. do not expand to @40 yet: yes

Interpretation:
- fix the MySQL runner/auth setup first, because the current MySQL failures are pre-SQL harness failures
- keep the existing MySQL failures explicit in reporting rather than hiding them
- inspect the optimizer-generated SQL for `CONS_0007` before rerunning optimize on broader scope
- do not expand to `@40` yet, because this canary still mixes one clear harness failure class with one clear generated-SQL failure class

## Next-Step Shape

Recommended immediate next step:
1. fix MySQL credential/bootstrap handling in the run-local MySQL runner
2. inspect and patch or gate the SQLGlot optimize route for `CONS_0007`
3. rerun this same 3-case canary
4. only after that, consider a PG/Spark-only broader non-PORT execution slice
