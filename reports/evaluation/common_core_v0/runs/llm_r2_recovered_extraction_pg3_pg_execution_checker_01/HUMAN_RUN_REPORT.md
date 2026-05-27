# LLM-R2 Recovered-Extraction PG3 PostgreSQL Execution/Checker 01

This run records recovered-route PostgreSQL source/generated execution and exact TSV checker for the PG3 subset only.

Boundary:
- route_id: `llm_r2_recovered_extraction_route_v1`
- cases: `PERF_0006`, `PERF_0013`, `PERF_0024`
- PostgreSQL only
- no timing
- no speedup
- no MySQL
- no Spark
- no PG40
- no full120
- original recovered SQL preserved unchanged; semicolon-normalized execution copy allowed only for execution input

## Per-Case Summary

- `PERF_0006`
  - source_execution_status: `executed`
  - generated_execution_status: `failed`
  - checker_status: `failed`
  - consistency_status: `not_checked`
  - failure_category: `SyntaxError`
  - failure_summary: `语法错误 在 "SELECT" 或附近的
LINE 1: ..._linestatus order by  l_returnflag,  l_linestatus SELECT l_r...
                                                             ^`

- `PERF_0013`
  - source_execution_status: `executed`
  - generated_execution_status: `failed`
  - checker_status: `failed`
  - consistency_status: `not_checked`
  - failure_category: `SyntaxError`
  - failure_summary: `语法错误 在 "SELECT" 或附近的
LINE 1: ... '1' year group by  n_name order by  revenue desc SELECT nat...
                                                             ^`

- `PERF_0024`
  - source_execution_status: `executed`
  - generated_execution_status: `failed`
  - checker_status: `failed`
  - consistency_status: `not_checked`
  - failure_category: `SyntaxError`
  - failure_summary: `语法错误 在 "SELECT" 或附近的
LINE 1: ...key     and n_name = 'BRAZIL' order by     s_name SELECT sup...
                                                             ^`

## Non-Claims

- This run does not create recovered PG9 appendix evidence because all three generated executions would need to exact-match first.
- This run does not change original-route PG9 evidence.
- This run does not claim timing, speedup, MySQL, Spark, PG40, or full120 evidence.
- This run does not update `method_comparison_summary_v2`.
