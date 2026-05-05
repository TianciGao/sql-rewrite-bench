# LEARNEDREWRITE_LLM4REWRITE_SINGLE_CASE_SMOKE_RUN_PERF_0006_v1

## 0. Purpose And Boundary
This is a bounded LearnedRewrite smoke for `PERF_0006` only.

- temp repacked unsigned jar used
- not leaderboard
- not full prior-method coverage
- not registry writeback
- checker not run
- speedup not run

## 1. Preconditions
- dry-run status: passed
- jar path:
  `/tmp/rewritebench_learnedrewrite_classpath_recovery/LearnedRewrite_repacked_unsigned.jar`
- jar recovery status: recovered temp unsigned jar present and used
- Java/JVM visibility: yes
- PG env visible: yes
- no model/API used: yes

## 2. Execution Summary
- method command:
  `python -m scripts.cli formal-learnedrewrite-llm4rewrite-single-case-run --case PERF_0006`
- method_executed: yes
- generation_status: `generation_success_with_output_sql`
- output_sql_extracted: yes
- generated_sql_path:
  `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v1.sql`
- checker_candidate_sql_path:
  `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/checker_candidate_sql_v1.sql`
- stdout path:
  `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/method_stdout_v1.log`
- stderr path:
  `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/method_stderr_v1.log`
- res/jsonl path:
  `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/res_v1.jsonl`
- failure category: none
- failure summary: none

Important artifact interpretation:
- `output_sql` was captured successfully
- `used_rules` was empty
- `output_cost` was `-1`
- the captured candidate is effectively the source SQL echoed back, with an extra trailing semicolon

## 3. Candidate SQL
Candidate SQL path:

`/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v1.sql`

Excerpt:

```sql
select
	l_returnflag,
	l_linestatus,
	sum(l_quantity) as sum_qty,
	sum(l_extendedprice) as sum_base_price,
	sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
	sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
	avg(l_quantity) as avg_qty,
	avg(l_extendedprice) as avg_price,
	avg(l_discount) as avg_disc,
	count(*) as count_order
from
	lineitem
where
	l_shipdate <= date '1998-08-27'
group by
	l_returnflag,
	l_linestatus
order by
	l_returnflag,
	l_linestatus;
;
```

## 4. Checker / Consistency
- checker_status: `not_run`
- consistency_status: `not_checked`
- checker intentionally not run in this step

## 5. Speedup
- speedup_status: `not_run`

## 6. Claim Boundary
`bounded_1_case_LearnedRewrite_candidate_generation_smoke_not_leaderboard`

This claim boundary is limited to bounded candidate generation and artifact capture. It is not a checker-backed success claim.

## 7. Remaining Blockers / Next Step
Next step:

- PG checker handoff for the generated SQL

But the generated candidate should be treated cautiously because the smoke artifact shows:

- no learned rules were reported as used
- no output cost was produced
- the candidate appears semantically identical to the source text rather than a clear nontrivial rewrite

## 8. Non-Modification Note
- only `PERF_0006` targeted
- no R-Bot
- no model/API
- no checker
- no speedup
- no MySQL/Spark/SQLGlot routes
- no registry/review/rules/EXECUTION_STATUS changes
- no case files changed
- taxonomy notes untouched
