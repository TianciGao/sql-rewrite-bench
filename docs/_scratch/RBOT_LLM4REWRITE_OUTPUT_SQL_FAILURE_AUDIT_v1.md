# RBOT_LLM4REWRITE_OUTPUT_SQL_FAILURE_AUDIT_v1

## 0. Purpose And Boundary
This is a read-only audit of the missing `output_sql` outcome from the bounded `PERF_0006` R-Bot / LLM4Rewrite smoke. No rerun, model call, DB call, checker, or speedup occurred in this audit.

## 1. Smoke Result Recap
The committed smoke result was:
- `dry_run_passed: true`
- `method_executed: true`
- `generation_status: generation_success`
- `output_sql_extracted: false`
- `failure_category: output_sql_missing`
- `checker_status: not_run`
- `speedup_status: not_run`

Claim boundary remained:
`bounded_1_case_RBot_LLM4Rewrite_generation_smoke_not_leaderboard`

## 2. Artifact Inspection
- `method_stdout.log`: exists. It contains only:
  - `Input Cost: 36.37`
  - Chroma startup debug lines
  - `Matched NL rewrite rules: [...]`
- `method_stderr.log`: exists but is empty.
- `selected_rules.json`: exists, but only shows empty selection artifacts:
  - `available: false`
  - no arranged or rearranged rule sequence
  - no selection rounds
- `retrieval_trace.json`: exists, but only shows:
  - `available: false`
  - empty `retrieved_cases_log_excerpt`
- `token_cost_log.json`: exists and only shows:
  - `available: false`
  - `input_cost: "36.37"`
- `generated_sql.sql`: does not exist
- `checker_candidate_sql.sql`: does not exist

No SQL-like text appeared in stdout or stderr.

## 3. Token / Model-Call Evidence
`token_cost_log.json` does not show token usage, output cost, or any explicit model-consumption counters. It only preserves the upstream `Input Cost` line, which is a database cost-estimation value, not model token usage.

The artifacts do not show a direct OpenAI/model call completing. The human observation that token balance did not visibly change is consistent with the captured artifacts.

## 4. Wrapper Path Analysis
The wrapper in [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py) does call the upstream generation path nominally:
- it builds a runner script
- it imports `init_llms`, `init_docstore`, and `test`
- it calls `test('method_stdout', ...)`

The wrapper expects generated SQL from the upstream log line:
- `Rewrite Execution Results: {...}`
- then extracts `output_sql` from that dict

That extraction pattern matches the upstream contract in `my_rewriter/db_utils.py`, where `execute_rewrite()` logs:
- `Rewrite Execution Results: {used_rules, output_sql, output_cost, time}`

However, the wrapper reuses a fixed run name, `method_stdout`, and the upstream `test()` function in `my_rewriter/test_utils.py` has this guard:

```python
log_filename = f'{LOG_DIR}/{name}.log'
if os.path.exists(log_filename):
    return
```

That means if `method_stdout.log` already exists from an earlier partial attempt, a later invocation returns immediately before retrieval, model generation, and rewrite execution.

## 5. Upstream Output Contract Analysis
In upstream LLM4Rewrite:
- `test_utils.test()` logs input cost, retrieval activity, and then calls `rag_rewrite(...)`
- `rag_rewrite()` eventually calls `execute_rewrite(...)`
- `execute_rewrite()` in `my_rewriter/db_utils.py` computes:
  - `used_rules`
  - `output_sql`
  - `output_cost`
  - `time`
- then logs:
  - `Rewrite Execution Results: { ... }`

So `output_sql` is normally produced by the real rewrite execution path, not by the early rule-matching path alone.

The current wrapper did point at the correct upstream function family, but the reused fixed log name means the upstream runner contract can short-circuit before generation.

## 6. Diagnosis
`upstream_runner_contract_mismatch`

Primary reason:
- the wrapper invokes the nominal upstream path, but it does so through `test(name=...)`
- upstream `test()` treats an existing log file as “already done” and returns early
- the observed artifact set matches an early or partial prior log, not a fresh completed generation pass

This is not best explained as a pure extraction bug because the expected `Rewrite Execution Results` line never appeared in the log at all.

## 7. Recommended Next Step
`implement corrected wrapper to call explicit model-backed generation path`

Least invasive correction:
- stop using a fixed upstream log name that triggers `test()` no-op behavior
- either remove/rotate the target log file before invocation, or call a more explicit upstream generation/rewrite entrypoint that does not silently return on existing logs

## 8. Non-Modification Note
No rerun, model call, DB call, checker, or speedup occurred in this audit. No repo files were changed except this scratch report. No registry, review, rules, or `docs/EXECUTION_STATUS.md` changes occurred.
