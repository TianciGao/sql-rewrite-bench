# Direct LLM @40 Same-Engine Execution Triage

## Scope

This is a read-only triage of:

- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/run_results.json`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/execution_command_matrix.csv`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/logs/*.log`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/workspaces/**/result_check.json`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/generation_triage.md`
- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_generation_matrix.csv`
- `reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv`
- `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md`

This is **execution/validity evidence only**. It is **not** timing evidence, speedup evidence, or leaderboard evidence.

## Run Summary

- planned rows: `120`
- ready_to_execute rows: `115`
- blocked rows: `5`
- executed rows: `99`
- execution_failed rows: `16`
- match_exact rows: `94`
- mismatch rows: `5`
- not_checked_execution_failed rows: `16`
- not_checked_preflight_blocked rows: `5`

Generation-side context from [generation_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/generation_triage.md):

- generation_success: `120`
- format_violation: `0`
- generation_failed: `0`

## Status Separation

The recorded rows separate into four materially different buckets and should stay separated in downstream validity reporting:

1. `94` rows: executed and `match_exact`
2. `5` rows: executed and `mismatch`
3. `16` rows: `execution_failed` and therefore `not_checked_execution_failed`
4. `5` rows: `preflight_blocked_missing_artifact` and therefore `not_checked_preflight_blocked`

This separation matters because the failure evidence is mixed:

- LLM-generated SQL dialect/execution failure:
  - `LONGTAIL_0023 / pg`
  - `LONGTAIL_0023 / spark`
  - `PERF_0019 / pg`
  - `PORT_0008 / mysql`
  - `PORT_0012 / mysql`
  - `PORT_0013 / pg`
  - `PORT_0022 / pg`
  - `PORT_0024 / pg`
  - several Spark parse failures on generated SQL
- Package/preflight artifact gap:
  - the `5` blocked PORT rows with missing witness data
- Result mismatch:
  - the `5` mismatch rows listed below
- Portability stress caveat:
  - all `27` PORT rows remain caveated portability-stress rows and must not be folded into ordinary same-engine success claims
- Draft DDL / package limitation:
  - `PERF_0077 / spark`
  - `PORT_0004 / spark`
  - both failed on draft/comment-only Spark DDL package content rather than on generated rewrite semantics alone

## Counts By Pool

| pool | planned_rows | executed | match_exact | mismatch | execution_failed | not_checked_execution_failed | not_executed_preflight_blocked | not_checked_preflight_blocked |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| consistency | 27 | 27 | 24 | 3 | 0 | 0 | 0 | 0 |
| longtail | 18 | 16 | 16 | 0 | 2 | 2 | 0 | 0 |
| performance | 48 | 46 | 45 | 1 | 2 | 2 | 0 | 0 |
| portability | 27 | 10 | 9 | 1 | 12 | 12 | 5 | 5 |

## Counts By Engine

| engine | planned_rows | executed | match_exact | mismatch | execution_failed | not_checked_execution_failed | not_executed_preflight_blocked | not_checked_preflight_blocked |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mysql | 40 | 36 | 34 | 2 | 2 | 2 | 2 | 2 |
| pg | 40 | 33 | 32 | 1 | 6 | 6 | 1 | 1 |
| spark | 40 | 30 | 28 | 2 | 8 | 8 | 2 | 2 |

## Counts By Case

| case_id | planned_rows | executed | match_exact | mismatch | execution_failed | not_checked_execution_failed | not_executed_preflight_blocked | not_checked_preflight_blocked |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CONS_0005 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| CONS_0007 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| CONS_0009 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| CONS_0010 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| CONS_0011 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| CONS_0012 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| CONS_0024 | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 0 |
| CONS_0036 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| CONS_0037 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| LONGTAIL_0011 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| LONGTAIL_0012 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| LONGTAIL_0013 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| LONGTAIL_0022 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| LONGTAIL_0023 | 3 | 1 | 1 | 0 | 2 | 2 | 0 | 0 |
| LONGTAIL_0024 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0006 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0007 | 3 | 3 | 2 | 1 | 0 | 0 | 0 | 0 |
| PERF_0008 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0013 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0017 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0019 | 3 | 2 | 2 | 0 | 1 | 1 | 0 | 0 |
| PERF_0024 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0033 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0034 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0035 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0052 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0054 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0056 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0062 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PERF_0077 | 3 | 2 | 2 | 0 | 1 | 1 | 0 | 0 |
| PERF_0082 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| PORT_0003 | 3 | 1 | 1 | 0 | 0 | 0 | 2 | 2 |
| PORT_0004 | 3 | 1 | 1 | 0 | 1 | 1 | 1 | 1 |
| PORT_0005 | 3 | 1 | 1 | 0 | 0 | 0 | 2 | 2 |
| PORT_0008 | 3 | 1 | 1 | 0 | 2 | 2 | 0 | 0 |
| PORT_0012 | 3 | 1 | 1 | 0 | 2 | 2 | 0 | 0 |
| PORT_0013 | 3 | 1 | 1 | 0 | 2 | 2 | 0 | 0 |
| PORT_0022 | 3 | 1 | 1 | 0 | 2 | 2 | 0 | 0 |
| PORT_0024 | 3 | 2 | 1 | 1 | 1 | 1 | 0 | 0 |
| PORT_0025 | 3 | 1 | 1 | 0 | 2 | 2 | 0 | 0 |

## Exact Mismatch Rows

| case_id | engine | pool | result_check_path |
|---|---|---|---|
| CONS_0024 | mysql | consistency | `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/workspaces/CONS_0024/mysql/direct_llm_same_engine_rewrite/result_check.json` |
| CONS_0024 | pg | consistency | `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/workspaces/CONS_0024/pg/direct_llm_same_engine_rewrite/result_check.json` |
| CONS_0024 | spark | consistency | `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/workspaces/CONS_0024/spark/direct_llm_same_engine_rewrite/result_check.json` |
| PERF_0007 | spark | performance | `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/workspaces/PERF_0007/spark/direct_llm_same_engine_rewrite/result_check.json` |
| PORT_0024 | mysql | portability | `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/workspaces/PORT_0024/mysql/direct_llm_same_engine_rewrite/result_check.json` |

Observed mismatch characteristics:

- all `5/5` mismatch rows were true result mismatches, not sort-only differences
- all `5/5` had `exact_match=false` and `sorted_match=false`
- `CONS_0024` mismatched on all three engines, which suggests a case-level semantic rewrite issue rather than a single-engine parser problem

## Exact Execution-Failed Rows

| case_id | engine | pool | primary bucket | detail |
|---|---|---|---|---|
| LONGTAIL_0023 | pg | longtail | LLM-generated SQL dialect/execution failure | alias `total_links` referenced in `WHERE` |
| LONGTAIL_0023 | spark | longtail | LLM-generated SQL dialect/execution failure | `AnalysisException`, unresolved alias `total_links` |
| PERF_0019 | pg | performance | LLM-generated SQL dialect/execution failure | column alias `c_count` missing in subquery output |
| PERF_0077 | spark | performance | draft DDL / package limitation | Spark schema file was draft/comment-only |
| PORT_0004 | spark | portability | draft DDL / package limitation | Spark schema file was draft/comment-only |
| PORT_0008 | mysql | portability | LLM-generated SQL dialect/execution failure | PostgreSQL-style quoting/casts sent to MySQL |
| PORT_0008 | spark | portability | LLM-generated SQL dialect/execution failure | Spark `ParseException` |
| PORT_0012 | mysql | portability | LLM-generated SQL dialect/execution failure | PostgreSQL-style quoting/casts sent to MySQL |
| PORT_0012 | spark | portability | LLM-generated SQL dialect/execution failure | Spark `ParseException` |
| PORT_0013 | pg | portability | LLM-generated SQL dialect/execution failure | MySQL-style backticks and `DATE_FORMAT(... AS DATETIME)` in PostgreSQL |
| PORT_0013 | spark | portability | LLM-generated SQL dialect/execution failure | Spark `ParseException`; this row was already on the generation watchlist |
| PORT_0022 | pg | portability | LLM-generated SQL dialect/execution failure | MySQL-style backticks and `DATE_FORMAT(... AS DATETIME)` in PostgreSQL |
| PORT_0022 | spark | portability | LLM-generated SQL dialect/execution failure | Spark `ParseException` |
| PORT_0024 | pg | portability | LLM-generated SQL dialect/execution failure | MySQL-style backticks in PostgreSQL |
| PORT_0025 | pg | portability | LLM-generated SQL dialect/execution failure | dialect-incompatible syntax in PostgreSQL |
| PORT_0025 | spark | portability | LLM-generated SQL dialect/execution failure | unsupported Spark datatype `DATETIME` |

## Exact Preflight-Blocked Rows

| case_id | engine | pool | exclusion_reason | missing artifact |
|---|---|---|---|---|
| PORT_0003 | mysql | portability | `missing_witness_data` | `cases/PORT/PORT_0003/validation/mysql_witness_data.sql` |
| PORT_0003 | spark | portability | `missing_witness_data` | `cases/PORT/PORT_0003/validation/spark_witness_data.sql` |
| PORT_0004 | pg | portability | `missing_witness_data` | `cases/PORT/PORT_0004/validation/pg_witness_data.sql` |
| PORT_0005 | mysql | portability | `missing_witness_data` | `cases/PORT/PORT_0005/validation/mysql_witness_data.sql` |
| PORT_0005 | spark | portability | `missing_witness_data` | `cases/PORT/PORT_0005/validation/spark_witness_data.sql` |

## Top Execution Failure Patterns

| pattern | rows | interpretation |
|---|---:|---|
| `other_execution_failure` | 8 | mostly engine-local semantic or dialect failures surfaced as subprocess errors |
| `parse_error` | 7 | Spark parse failures, including draft DDL package issues and dialect-incompatible generated SQL |
| `spark_analysis_exception` | 1 | unresolved-column semantic failure on `LONGTAIL_0023 / spark` |

Representative evidence:

- `LONGTAIL_0023 / spark`: unresolved alias `total_links`
- `LONGTAIL_0023 / pg`: alias `total_links` not visible in `WHERE`
- `PERF_0019 / pg`: alias `c_count` referenced but not produced
- `PERF_0077 / spark`: package DDL file contained draft comments only
- `PORT_0004 / spark`: package DDL file contained draft comments only
- `PORT_0013 / pg`: PostgreSQL rejected MySQL-style backticks
- `PORT_0025 / spark`: Spark rejected `DATETIME`

## PORT-Specific Caveats

All `27` PORT rows should remain explicitly caveated in downstream reporting.

- `5` PORT rows are package/preflight blocked by missing witness data
- `12` PORT rows are execution failures, concentrated in dialect-sensitive PostgreSQL and Spark rows
- `1` PORT row executed but mismatched: `PORT_0024 / mysql`
- several PORT rows carry `controls_native_source_status=skipped` in the execution matrix and should not be reframed as ordinary native-source same-engine rows
- `PORT_0013 / spark` remained a watchlist row from generation triage and then failed at execution
- the evaluation protocol’s denominator-first rule still requires these caveated and failed rows to remain visible rather than being dropped

## Recommendation

Materialize the Direct LLM validity summary next.

Reasoning:

- the execution evidence is now sufficiently complete for denominator-aware validity reporting
- the run already separates `match_exact`, `mismatch`, `execution_failed`, and `preflight_blocked` outcomes cleanly
- the main remaining reporting risk is category collapse, especially if PORT caveats, package limitations, and dialect failures are merged into a single invalid bucket

Constraint for the next summary:

- keep `94` exact matches, `5` mismatches, `16` execution failures, and `5` preflight blocks as distinct outcome classes
- keep PORT caveats explicit
- do not convert this artifact into timing, speedup, or leaderboard language
