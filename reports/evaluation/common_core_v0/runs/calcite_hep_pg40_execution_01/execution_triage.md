# Calcite HEP PG40 Execution Triage

This is a read-only triage report for the Calcite HEP PostgreSQL execution run on the frozen `common_core_v0_40_pg40` denominator.

This is execution/validity evidence only. It is not timing or speedup evidence.

## Headline Counts

- planned rows: `40`
- generation_success rows: `29`
- generation_failed rows: `11`
- ready_to_execute rows: `29`
- executed rows: `23`
- execution_failed rows: `6`
- match_exact rows: `21`
- mismatch rows: `2`
- not_checked_execution_failed rows: `6`
- not_checked_generation_failed rows: `11`

## Counts By Pool

- `performance`: generation `{'generation_success': 16}`; execution `{'executed': 16}`; consistency `{'match_exact': 14, 'mismatch': 2}`
- `consistency`: generation `{'generation_success': 9}`; execution `{'executed': 7, 'execution_failed': 2}`; consistency `{'match_exact': 7, 'not_checked_execution_failed': 2}`
- `portability`: generation `{'generation_failed_parse': 7, 'generation_failed_unsupported_sql': 1, 'generation_success': 1}`; execution `{'not_executed_generation_failed': 8, 'execution_failed': 1}`; consistency `{'not_checked_generation_failed': 8, 'not_checked_execution_failed': 1}`
- `longtail`: generation `{'generation_success': 3, 'generation_failed_unsupported_sql': 3}`; execution `{'execution_failed': 3, 'not_executed_generation_failed': 3}`; consistency `{'not_checked_execution_failed': 3, 'not_checked_generation_failed': 3}`

## Counts By Generation Status

- `generation_success`: `29`
- `generation_failed_parse`: `7`
- `generation_failed_unsupported_sql`: `4`

## Counts By Execution Status Observed

- `executed`: `23`
- `execution_failed`: `6`
- `not_executed_generation_failed`: `11`

## Counts By Consistency Check Status

- `match_exact`: `21`
- `mismatch`: `2`
- `not_checked_execution_failed`: `6`
- `not_checked_generation_failed`: `11`

## Generation-failed Rows

- `PORT_0003`
- `PORT_0004`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0025`
- `LONGTAIL_0022`
- `LONGTAIL_0023`
- `LONGTAIL_0024`

## Execution-failed Rows

- `CONS_0036`: `calcite_generated_identifier_casing_failure`
  stderr signal: `注意:  模式 "ccv0_calcite_hep_cons_0036" 不存在 错误:  关系 "DEPT" 不存在 LINE 2: FROM "DEPT"              ^ 注意:  递归删除 表 ccv0_calcite_hep_cons_0036.dept Traceback (most recent call last):   File "<stdin>", line 138, in run_pg_row   File "/usr/lib/python3.12/subprocess.py", line 571, in run     raise CalledProcessError(retcode, process.args, subprocess.CalledProcessError: Command '['psql', '-v', 'ON_ERROR_STOP=1', '-X', '-q', '-c', 'SET search_path TO ccv0_calcite_hep_cons_0036;', '-c', 'COPY (SELECT "NAME", C`
- `CONS_0037`: `calcite_generated_identifier_casing_failure`
  stderr signal: `注意:  模式 "ccv0_calcite_hep_cons_0037" 不存在 错误:  关系 "EMP" 不存在 LINE 2: FROM "EMP"              ^ 注意:  串联删除2个其它对象 DETAIL:  递归删除 表 ccv0_calcite_hep_cons_0037.emp 递归删除 表 ccv0_calcite_hep_cons_0037.dept Traceback (most recent call last):   File "<stdin>", line 138, in run_pg_row   File "/usr/lib/python3.12/subprocess.py", line 571, in run     raise CalledProcessError(retcode, process.args, subprocess.CalledProcessError: Command '['psql', '-v', 'ON_ERROR_STOP=1', '-X', '-q', '-c', 'SET search_path TO ccv`
- `PORT_0024`: `pg_dialect_or_quoting_failure`
  stderr signal: `注意:  模式 "ccv0_calcite_hep_port_0024" 不存在 错误:  语法错误 在 "=" 或附近的 LINE 1: COPY (SELECT CAST( SUM( CASE WHEN `istextless` = 0 AND `isst...                                                        ^ 注意:  递归删除 表 ccv0_calcite_hep_port_0024.cards Traceback (most recent call last):   File "<stdin>", line 129, in run_pg_row   File "/usr/lib/python3.12/subprocess.py", line 571, in run     raise CalledProcessError(retcode, process.args, subprocess.CalledProcessError: Command '['psql', '-v', 'ON_ERROR_STOP=1', `
- `LONGTAIL_0011`: `calcite_generated_identifier_casing_failure`
  stderr signal: `注意:  模式 "ccv0_calcite_hep_longtail_0011" 不存在 错误:  关系 "Posts" 不存在 LINE 3: FROM "Posts"              ^ 注意:  串联删除2个其它对象 DETAIL:  递归删除 表 ccv0_calcite_hep_longtail_0011.users 递归删除 表 ccv0_calcite_hep_longtail_0011.posts Traceback (most recent call last):   File "<stdin>", line 138, in run_pg_row   File "/usr/lib/python3.12/subprocess.py", line 571, in run     raise CalledProcessError(retcode, process.args, subprocess.CalledProcessError: Command '['psql', '-v', 'ON_ERROR_STOP=1', '-X', '-q', '-c', 'SET`
- `LONGTAIL_0012`: `calcite_generated_identifier_casing_failure`
  stderr signal: `注意:  模式 "ccv0_calcite_hep_longtail_0012" 不存在 错误:  关系 "Users" 不存在 LINE 3: FROM "Users"              ^ 注意:  串联删除3个其它对象 DETAIL:  递归删除 表 ccv0_calcite_hep_longtail_0012.users 递归删除 表 ccv0_calcite_hep_longtail_0012.posts 递归删除 表 ccv0_calcite_hep_longtail_0012.votes Traceback (most recent call last):   File "<stdin>", line 138, in run_pg_row   File "/usr/lib/python3.12/subprocess.py", line 571, in run     raise CalledProcessError(retcode, process.args, subprocess.CalledProcessError: Command '['psql', '-v`
- `LONGTAIL_0013`: `calcite_generated_identifier_casing_failure`
  stderr signal: `注意:  模式 "ccv0_calcite_hep_longtail_0013" 不存在 错误:  关系 "Users" 不存在 LINE 3: FROM "Users"              ^ 注意:  串联删除4个其它对象 DETAIL:  递归删除 表 ccv0_calcite_hep_longtail_0013.users 递归删除 表 ccv0_calcite_hep_longtail_0013.posts 递归删除 表 ccv0_calcite_hep_longtail_0013.votes 递归删除 表 ccv0_calcite_hep_longtail_0013.badges Traceback (most recent call last):   File "<stdin>", line 138, in run_pg_row   File "/usr/lib/python3.12/subprocess.py", line 571, in run     raise CalledProcessError(retcode, process.args, subproc`

## Mismatch Rows

- `PERF_0035`
- `PERF_0062`

## Top Execution Failure Patterns

- `CONS_0036`, `CONS_0037`, `LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013` fail because generated SQL refers to quoted upper-case relation names such as `"DEPT"`, `"EMP"`, `"Posts"`, and `"Users"`, while PostgreSQL folds unquoted table creation names to lower-case. This looks like a Calcite-generated SQL identifier/casing failure rather than a database setup gap.
- `PORT_0024` fails with PostgreSQL syntax error near backtick-quoted identifiers. This looks like a generated SQL PG dialect failure, not a witness-loading failure.
- No dominant evidence points to package-level schema/witness setup failure among the six execution-failed rows; the failures are concentrated in generated SQL portability-to-PG issues.

## Interpretation

- The `11` generation-failed rows remain denominator rows and are explicitly preserved as `not_executed_generation_failed`.
- The `6` execution-failed rows should be treated as method/execution failures, primarily Calcite-generated SQL failures against PostgreSQL semantics or dialect.
- `PERF_0035` and `PERF_0062` executed but produced mismatched outputs; they should remain `mismatch` and are not timing-eligible.
- `PORT_0024` should remain an execution failure even though it passed generation.

## Recommendation

- Materialize the Calcite HEP PG40 validity summary next.
- Keep `match_exact`, `mismatch`, `execution_failed`, and `not_executed_generation_failed` as separate outcome classes in that summary.
- Do not admit the two mismatch rows into any timing-eligible set.
