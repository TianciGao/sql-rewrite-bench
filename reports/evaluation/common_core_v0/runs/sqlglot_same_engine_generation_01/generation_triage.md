# SQLGlot Generation-Only Triage

## Headline

- total rows: `240`
- generated count: `203`
- failed count: `37`
- no-op count: `37`

Validator-style boundary reminder:
- this package is generation-only
- no database execution occurred
- no result-consistency, executability, speedup, or regression claim is made here

## Counts By Route

- `sqlglot_optimize_same_dialect`: `120` rows
- `sqlglot_transpile_same_dialect_noop`: `120` rows

Failure split by route:
- `sqlglot_optimize_same_dialect`: `32` failed
- `sqlglot_transpile_same_dialect_noop`: `5` failed

## Counts By Engine

- `pg`: `80` total, `19` failed, `9` no-op
- `mysql`: `80` total, `9` failed, `14` no-op
- `spark`: `80` total, `9` failed, `14` no-op

## Counts By Pool

- `performance`: `96` total, `24` failed, `9` no-op
- `consistency`: `54` total, `3` failed, `6` no-op
- `portability`: `54` total, `10` failed, `22` no-op
- `longtail`: `36` total, `0` failed, `0` no-op

## Failure Concentration

Failures are concentrated in:
- `sqlglot_optimize_same_dialect`, not the same-dialect transpile/no-op route
- `performance` and `portability` cases, not consistency/longtail
- `pg` most strongly, then `mysql` and `spark`

Pattern breakdown:
- `optimizer_unresolved_column`: `27`
- `dialect_function_argument_unsupported`: `0`
- `other`: `10`

Interpretation:
- unresolved-column failures look like SQLGlot optimizer scope/binding limits on more complex TPC-H/TPC-DS and some PORT queries
- `ToChar(..., format)` failures indicate dialect-function rendering gaps, concentrated in MySQL/Spark portability-style rows
- failures do not look concentrated in `CONS` or `LONGTAIL`
- failures are not primarily a PORT-only phenomenon, but PORT should still remain a separate execution pass because of explicit same-engine caveats in the preflight

## Top Failure Messages

- `OptimizeError: Column 'l_orderkey' could not be resolved. Line: 12, Col: 11`: `3`
- `OptimizeError: Column 'n_name' could not be resolved. Line: 12, Col: 7`: `3`
- `OptimizeError: Column 'c_custkey' could not be resolved. Line: 12, Col: 13`: `3`
- `OptimizeError: Column 'c_custkey' could not be resolved. Line: 17, Col: 21`: `3`
- `OptimizeError: Column 's_name' could not be resolved. Line: 6, Col: 10`: `3`
- `OptimizeError: Column 'sr_customer_sk' could not be resolved. Line: 8, Col: 22`: `3`
- `OptimizeError: Column 'ss_ext_sales_price' could not be resolved. Line: 10, Col: 26`: `3`
- `OptimizeError: Column 'ss_quantity' could not be resolved. Line: 5, Col: 22`: `3`
- `OptimizeError: Column 'empno' could not be resolved. Line: 1, Col: 12`: `3`
- `ParseError: Expected END after CASE. Line 5, Col: 32.
  
-- draft-only / not validated
-- source dialect: mysql_like_candidate
SELECT CAST( SUM( CASE WHEN `[4msex[0m` = 'F' THEN 1 ELSE 0 END ) AS DOUBLE ) * 100 / COUNT( `id` ) FROM `patient` WHERE `diagnosis` = 'RA`: `2`
- `ParseError: Expecting ). Line 1, Col: 21.
  SELECT CAST( SUM( `[4mt2[0m`.`gender` = 'F' ) AS DOUBLE ) * 100 / COUNT( `t2`.`client_id` ) FROM `district` AS `t1` INNER JOIN`: `2`
- `ParseError: Expecting ). Line 1, Col: 23.
  SELECT CAST( COUNT( `[4mt1[0m`.`id` ) AS DOUBLE ) / 12 FROM `postlinks` AS `t1` INNER JOIN `posts` AS `t2` ON `t1`.`postid` = `t2`: `2`
- `ParseError: Expected END after CASE. Line 1, Col: 39.
  SELECT CAST( SUM( CASE WHEN `[4mistextless[0m` = 0 AND `isstoryspotlight` = 1 THEN 1 ELSE 0 END ) AS DOUBLE ) * 100 / COUNT( `id` ) FROM `cards``: `2`
- `ParseError: Invalid expression / Unexpected token. Line 1, Col: 11.
  SELECT `t1[4m`[0m.`account_id` FROM `loan` AS `t1` INNER JOIN `account` AS `t2` ON `t1`.`account_id` = `t2`.`account_`: `2`

## Failed Rows By Case / Engine / Route

- `PERF_0008` / `pg` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'l_orderkey' could not be resolved. Line: 12, Col: 11`
- `PERF_0008` / `mysql` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'l_orderkey' could not be resolved. Line: 12, Col: 11`
- `PERF_0008` / `spark` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'l_orderkey' could not be resolved. Line: 12, Col: 11`
- `PERF_0013` / `pg` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'n_name' could not be resolved. Line: 12, Col: 7`
- `PERF_0013` / `mysql` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'n_name' could not be resolved. Line: 12, Col: 7`
- `PERF_0013` / `spark` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'n_name' could not be resolved. Line: 12, Col: 7`
- `PERF_0017` / `pg` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'c_custkey' could not be resolved. Line: 12, Col: 13`
- `PERF_0017` / `mysql` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'c_custkey' could not be resolved. Line: 12, Col: 13`
- `PERF_0017` / `spark` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'c_custkey' could not be resolved. Line: 12, Col: 13`
- `PERF_0019` / `pg` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'c_custkey' could not be resolved. Line: 17, Col: 21`
- `PERF_0019` / `mysql` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'c_custkey' could not be resolved. Line: 17, Col: 21`
- `PERF_0019` / `spark` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'c_custkey' could not be resolved. Line: 17, Col: 21`
- `PERF_0024` / `pg` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 's_name' could not be resolved. Line: 6, Col: 10`
- `PERF_0024` / `mysql` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 's_name' could not be resolved. Line: 6, Col: 10`
- `PERF_0024` / `spark` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 's_name' could not be resolved. Line: 6, Col: 10`
- `PERF_0052` / `pg` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'sr_customer_sk' could not be resolved. Line: 8, Col: 22`
- `PERF_0052` / `mysql` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'sr_customer_sk' could not be resolved. Line: 8, Col: 22`
- `PERF_0052` / `spark` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'sr_customer_sk' could not be resolved. Line: 8, Col: 22`
- `PERF_0054` / `pg` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'ss_ext_sales_price' could not be resolved. Line: 10, Col: 26`
- `PERF_0054` / `mysql` / `sqlglot_optimize_same_dialect`: `OptimizeError: Column 'ss_ext_sales_price' could not be resolved. Line: 10, Col: 26`

## No-op Rows By Case / Engine / Route

- `PERF_0007` / `pg` / `sqlglot_transpile_same_dialect_noop`
- `PERF_0007` / `mysql` / `sqlglot_transpile_same_dialect_noop`
- `PERF_0007` / `spark` / `sqlglot_transpile_same_dialect_noop`
- `PERF_0033` / `pg` / `sqlglot_transpile_same_dialect_noop`
- `PERF_0033` / `mysql` / `sqlglot_transpile_same_dialect_noop`
- `PERF_0033` / `spark` / `sqlglot_transpile_same_dialect_noop`
- `PERF_0054` / `pg` / `sqlglot_transpile_same_dialect_noop`
- `PERF_0054` / `mysql` / `sqlglot_transpile_same_dialect_noop`
- `PERF_0054` / `spark` / `sqlglot_transpile_same_dialect_noop`
- `CONS_0036` / `pg` / `sqlglot_transpile_same_dialect_noop`
- `CONS_0036` / `mysql` / `sqlglot_transpile_same_dialect_noop`
- `CONS_0036` / `spark` / `sqlglot_transpile_same_dialect_noop`
- `CONS_0037` / `pg` / `sqlglot_transpile_same_dialect_noop`
- `CONS_0037` / `mysql` / `sqlglot_transpile_same_dialect_noop`
- `CONS_0037` / `spark` / `sqlglot_transpile_same_dialect_noop`
- `PORT_0003` / `pg` / `sqlglot_transpile_same_dialect_noop`
- `PORT_0003` / `mysql` / `sqlglot_transpile_same_dialect_noop`
- `PORT_0003` / `spark` / `sqlglot_transpile_same_dialect_noop`
- `PORT_0004` / `mysql` / `sqlglot_transpile_same_dialect_noop`
- `PORT_0004` / `spark` / `sqlglot_transpile_same_dialect_noop`

## No-op Interpretation

`is_noop_output=yes` is expected in many `sqlglot_transpile_same_dialect_noop` rows. That route is intentionally a same-dialect parse/print boundary check, so no-op outputs should remain explicit rather than being treated as missing work.

The no-op rows should remain visible in later execution planning because:
- they confirm parse/generate coverage without overclaiming optimization
- they are useful as boundary controls for execution canaries
- they should not be mixed with optimizer-generated rewrites when judging rewrite novelty

## Recommended Next Execution Canary

Recommended first execution subset:
- start with non-PORT, tri-engine rows that had `generation_success` on both routes and already have strong fresh controls evidence
- preferred seed subset:
- CONS_0007 pg/mysql/spark optimize+transpile
- CONS_0012 pg/mysql/spark optimize+transpile
- PERF_0033 pg/mysql/spark optimize+transpile
- PERF_0054 pg/mysql/spark optimize+transpile

Why this subset first:
- it avoids the explicit PORT same-engine caveat slice
- it avoids optimizer-generation failures that are already known from this canary
- it gives a clean first comparison between `sqlglot_optimize_same_dialect` and `sqlglot_transpile_same_dialect_noop`

Rows that should remain explicit in later materialization, not dropped:
- all `generation_failed` optimizer rows
- all `is_noop_output=yes` transpile/no-op rows
- all PORT rows, even when generation succeeded, because generation success does not imply same-engine executability or consistency under the PORT caveat policy

PORT recommendation:
- keep `PORT` rows out of the first execution canary
- run PORT as a separate pass after a non-PORT same-engine canary succeeds
- in that separate pass, preserve explicit unsupported / caveat framing rather than treating generation success as execution readiness
