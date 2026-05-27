# EXPANDED_PERF_DIRECT_LLM_RUN_SCAFFOLD_SUMMARY_v0

## Scope

- Command: `python -m scripts.cli formal-expanded-perf-direct-llm-run`
- Benchmark line: expanded PERF Direct LLM rewrite
- Registered 34-case packet size remains unchanged
- Route: `LLM_DIRECT_REWRITE_STRONG`
- Engine scope in this scaffold: PostgreSQL only
- This turn executed only the canary case `PERF_0007`

## Command registration status

- Command registration remains ok: `yes`
- Registered in `scripts/cli.py`: `yes`
- Supported options remain:
  - `--case-id CASE_ID` repeatable
  - `--execute`
  - `--output reports/formal_expansion/expanded_perf_direct_llm_run_v0.json`
- Default mode: dry-run

## Behavior update completed

- Report-local source materialization path now used:
  - `reports/formal_expansion/result_materialization/expanded_perf/source/perf_0007.tsv`
- Report-local candidate materialization path now used:
  - `reports/formal_expansion/result_materialization/expanded_perf/llm_direct_rewrite/perf_0007.tsv`
- Report-local checker JSON now written:
  - `reports/formal_expansion/result_checks/expanded_perf/llm_direct_rewrite/perf_0007.json`
- Checker mode: `exact_tsv_report_local`
- Main report claim boundary now:
  - `expanded_perf_direct_llm_pg_checker_not_speedup_not_final_leaderboard`

## Dry-run result

- Command run:
  - `python -m scripts.cli formal-expanded-perf-direct-llm-run --case-id PERF_0007`
- Result: `ok=true`
- Selected case count: `1`
- `PERF_0007` dry-run status: `ready_for_execute`
- Report path: `reports/formal_expansion/expanded_perf_direct_llm_run_v0.json`

## PERF_0007 canary result

- Command run:
  - `source scripts/env_postgres.sh && python -m scripts.cli formal-expanded-perf-direct-llm-run --case-id PERF_0007 --execute`
- Result: `ok=true`
- PERF_0007 canary model call status: `success`
- PERF_0007 extraction status: `extracted`
- PERF_0007 source execution status: `success`
- PERF_0007 candidate execution status: `success`
- PERF_0007 checker status: `consistent`
- Source row count: `1`
- Candidate row count: `1`
- Row count equal: `true`
- Byte equal: `true`
- Search path after set: `perf_0007_validation, public`

## Summary fields now present

- Existing fields retained:
  - `call_success_count`
  - `execution_success_count`
  - `env_status`
  - `token_usage_total_if_available`
- Checker-backed fields now present:
  - `model_call_success_count`
  - `extraction_success_count`
  - `source_execution_success_count`
  - `candidate_execution_success_count`
  - `checker_consistent_count`
  - `checker_inconsistent_count`
  - `checker_failed_count`
  - `result_consistency_rate`
  - `row_count_match_count`
  - `row_count_mismatch_count`
  - `total_token_usage`
  - `token_per_consistent_rewrite`

## Token usage

- Input tokens: `432`
- Output tokens: `88`
- Total token usage: `520`
- Token per consistent rewrite: `520.0`

## Readiness

- Checker-backed canary path status: `ready`
- Full 34-case checker-backed expanded PERF run readiness: `yes`
- Readiness basis:
  - command registration remains ok
  - dry-run path is healthy
  - single-case source materialization succeeded
  - single-case candidate materialization succeeded
  - single-case checker JSON succeeded
  - summary JSON and checker JSON both validated with `python -m json.tool`

## Boundaries

- No registry file changed
- `docs/EXECUTION_STATUS.md` not changed
- No formal review file changed
- No taxonomy calibration note touched
- No full 34-case execution was run
- Only the single requested canary case `PERF_0007` was executed
