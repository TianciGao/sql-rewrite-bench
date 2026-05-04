# EXPANDED_PERF_DIRECT_LLM_SPEEDUP_RUN_SUMMARY_v0

## Status

This note records the current expanded PERF Direct LLM speedup runtime/scoring attempt for:

- `reports/formal_expansion/expanded_perf_direct_llm_speedup_run_v0.json`

Result status:

- dry-run command completed
- canary execute attempted on `PERF_0007`
- canary did not succeed
- full 34-case execute was not started
- canary diagnostics were improved to capture full subprocess context

## Scope

- denominator: expanded PERF `34`
- route: `LLM_DIRECT_REWRITE_STRONG`
- engine: PostgreSQL only
- token usage carried from prior Direct LLM run: `29414`

Runtime policy configured in the command:

- `warmup_count=1`
- `repeat_count=5`
- `statement_timeout_ms=30000`
- `primary_statistic=median`
- `tie_threshold=0.05`
- `regression_threshold=1.2`

## Commands run

- `python -m py_compile scripts/cli.py`
- `python -m scripts.cli formal-expanded-perf-direct-llm-speedup-run`
- `source scripts/env_postgres.sh && python -m scripts.cli formal-expanded-perf-direct-llm-speedup-run --case-id PERF_0007 --execute`
- `python -m json.tool reports/formal_expansion/expanded_perf_direct_llm_speedup_run_v0.json >/dev/null`

The full execute step was skipped because the canary execute did not succeed.

## Dry-run result

- status: `ok=true`
- denominator surfaced: `34`
- execute mode: dry-run by default
- candidate SQL source: prior Direct LLM run report `extracted_sql_text`
- no model calls
- no runtime repeats executed in dry-run mode

## Canary result

Canary command:

- `source scripts/env_postgres.sh && python -m scripts.cli formal-expanded-perf-direct-llm-speedup-run --case-id PERF_0007 --execute`

Canary outcome:

- case count: `1`
- executed count: `1`
- success count: `0`
- failed count: `1`
- failed case: `PERF_0007`
- failure category: `RuntimeError`
- reported error text now captured in full:
  - `validation schema check failed: returncode=2; stdout=''; stderr='psql: error: \n'; validation_schema='perf_0007_validation'; command='psql -X -v ON_ERROR_STOP=1 -q -A -t -c \\'SELECT to_regnamespace(\\'"'"'perf_0007_validation\\'"'"')\\''`

Interpretation:

- the execute path did not clear the single-case PostgreSQL runtime canary
- because the canary failed, the full 34-case speedup runtime/scoring step was not run
- the failure happens before source SQL or candidate SQL runtime measurement

## Diagnosis

Comparison against the existing speedup runners:

- `formal-batch2a-speedup-run`
- `formal-batch3a-speedup-run`
- `formal-batch3b-perf-speedup-run`

All three existing runners use the same `psycopg.connect(...)` execution path:

- validate schema with `SELECT to_regnamespace(...)`
- set `search_path` to `<case>_validation, public`
- execute source SQL and candidate SQL inside PostgreSQL
- collect warmup and repeat runtimes in Python

Expanded Direct LLM speedup now also:

- reads candidate SQL from `extracted_sql_text` in `reports/formal_expansion/expanded_perf_direct_llm_run_v0.json`
- uses the same target validation schema convention
- sets the same runtime policy

However, in this environment, both attempted Python-side PostgreSQL execution paths fail:

- `psycopg.connect(...)` fails with `OperationalError: connection is bad: no error details available`
- nested `psql` subprocess execution from inside Python fails with `returncode=2` and `stderr='psql: error: \n'`

Best current diagnosis:

- PostgreSQL connectivity is available from the top-level shell in this workspace
- but PostgreSQL client access from inside the Python process is failing before query execution
- this appears to be an environment/runtime boundary issue rather than a Direct LLM SQL issue, because the failure occurs at the validation-schema check step before any source/candidate runtime loop starts

## Full run result

- status: not run
- reason: canary execute failed
- final report path currently reflects the latest dry-run state, not a completed full execute result

## Metrics

No successful runtime/scoring result was produced, so the following remain unavailable for the expanded 34-case execute:

- `GM_Speedup`
- `W/T/L`
- `RegressionRate@20%`
- `source_median_runtime_ms`
- `candidate_median_runtime_ms`

Current dry-run report fields remain:

- `GM_Speedup=null`
- `win_count=0`
- `tie_count=0`
- `loss_count=0`
- `regression_20pct_rate=null`
- `row_count_match_count=0`

## Row-count match summary

- canary execute row-count match: not reached
- full 34-case row-count match summary: not available

## Failures

- `PERF_0007`: execute canary failed before runtime/scoring closure

No additional expanded PERF cases were executed after the canary failure.

## Boundaries

- no model calls
- PostgreSQL-only
- expanded PERF only
- not a final leaderboard
- no registry changes
- no `docs/EXECUTION_STATUS.md` changes
- no formal review changes
- no case file changes
- no taxonomy calibration note changes
