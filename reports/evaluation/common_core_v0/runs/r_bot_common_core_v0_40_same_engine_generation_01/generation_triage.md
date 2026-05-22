# R-Bot Formal @120 Generation Triage

## Scope

This is a read-only triage of the completed formal R-Bot same-engine generation package.
It is generation evidence only.
It is not execution, validity, timing, speedup, or leaderboard evidence.

## Summary

- `planned_rows = 120`
- `generated = 7`
- `failed = 2`
- `blocked = 31`
- `unsupported = 80`
- `counts_by_engine = {'pg': 40, 'mysql': 40, 'spark': 40}`
- `counts_by_pool = {'performance': 48, 'consistency': 27, 'portability': 27, 'longtail': 18}`
- `run_event_long_rows = 120`
- `generated_sql_exists_for_all_generated_rows = true`
- `generated_row_artifact_contract_complete = true`
- `failed_row_artifact_contract_complete = true`
- `blocked_row_artifact_contract_complete = true`
- `unsupported_row_artifact_contract_complete = true`
- `generated_sql_clean_for_all_generated_rows = true`

## Generated Rows

- `PERF_0006:pg`
- `PERF_0008:pg`
- `PERF_0013:pg`
- `PERF_0017:pg`
- `PERF_0024:pg`
- `PERF_0052:pg`
- `PERF_0054:pg`

## Failed Rows

- `PERF_0019:pg`: `subprocess_nonzero_exit`; smoke subprocess exited with code 1
- `PERF_0033:pg`: `subprocess_nonzero_exit`; smoke subprocess exited with code 1

## Blocked Rows

- `PERF_0007:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PERF_0034:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PERF_0035:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PERF_0056:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PERF_0062:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PERF_0077:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PERF_0082:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `CONS_0005:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `CONS_0007:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `CONS_0009:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `CONS_0010:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `CONS_0011:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `CONS_0012:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `CONS_0024:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `CONS_0036:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `CONS_0037:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PORT_0003:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PORT_0004:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PORT_0005:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PORT_0008:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PORT_0012:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PORT_0013:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PORT_0022:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PORT_0024:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `PORT_0025:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `LONGTAIL_0011:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `LONGTAIL_0012:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `LONGTAIL_0013:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `LONGTAIL_0022:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `LONGTAIL_0023:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.
- `LONGTAIL_0024:pg`: Recovered committed PG runner currently hard-codes a supported-case subset in scripts/cli.py formal-rbot-llm4rewrite-single-case-smoke-run; keep row explicit and blocked until runner support expands.

## Unsupported Rows

- `PERF_0006:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0006:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0007:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0007:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0008:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0008:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0013:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0013:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0017:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0017:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0019:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0019:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0024:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0024:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0033:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0033:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0034:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0034:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0035:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0035:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0052:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0052:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0054:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0054:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0056:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0056:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0062:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0062:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0077:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0077:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0082:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PERF_0082:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0005:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0005:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0007:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0007:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0009:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0009:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0010:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0010:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0011:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0011:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0012:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0012:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0024:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0024:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0036:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0036:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0037:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `CONS_0037:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0003:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0003:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0004:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0004:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0005:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0005:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0008:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0008:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0012:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0012:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0013:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0013:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0022:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0022:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0024:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0024:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0025:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `PORT_0025:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0011:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0011:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0012:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0012:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0013:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0013:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0022:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0022:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0023:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0023:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0024:mysql`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.
- `LONGTAIL_0024:spark`: Recovered committed R-Bot runner path is PG-only; same-engine mysql/spark generation path is not recovered in committed CLI and must remain explicit, not dropped.

## Generated Artifact Checks

- `PERF_0006:pg`: generated_sql=true, prompt=true, raw_response=true, selected_rules=true, retrieval_trace=true, token_cost_provider=true, environment_snapshot=true, row_metadata=true
- `PERF_0008:pg`: generated_sql=true, prompt=true, raw_response=true, selected_rules=true, retrieval_trace=true, token_cost_provider=true, environment_snapshot=true, row_metadata=true
- `PERF_0013:pg`: generated_sql=true, prompt=true, raw_response=true, selected_rules=true, retrieval_trace=true, token_cost_provider=true, environment_snapshot=true, row_metadata=true
- `PERF_0017:pg`: generated_sql=true, prompt=true, raw_response=true, selected_rules=true, retrieval_trace=true, token_cost_provider=true, environment_snapshot=true, row_metadata=true
- `PERF_0024:pg`: generated_sql=true, prompt=true, raw_response=true, selected_rules=true, retrieval_trace=true, token_cost_provider=true, environment_snapshot=true, row_metadata=true
- `PERF_0052:pg`: generated_sql=true, prompt=true, raw_response=true, selected_rules=true, retrieval_trace=true, token_cost_provider=true, environment_snapshot=true, row_metadata=true
- `PERF_0054:pg`: generated_sql=true, prompt=true, raw_response=true, selected_rules=true, retrieval_trace=true, token_cost_provider=true, environment_snapshot=true, row_metadata=true

## Generated SQL Quality

- `PERF_0006:pg`: empty=false, markdown_contaminated=false, non_sql=false, ddl_or_dml=false, multi_statement=false, statement_count=1
- `PERF_0008:pg`: empty=false, markdown_contaminated=false, non_sql=false, ddl_or_dml=false, multi_statement=false, statement_count=1
- `PERF_0013:pg`: empty=false, markdown_contaminated=false, non_sql=false, ddl_or_dml=false, multi_statement=false, statement_count=1
- `PERF_0017:pg`: empty=false, markdown_contaminated=false, non_sql=false, ddl_or_dml=false, multi_statement=false, statement_count=1
- `PERF_0024:pg`: empty=false, markdown_contaminated=false, non_sql=false, ddl_or_dml=false, multi_statement=false, statement_count=1
- `PERF_0052:pg`: empty=false, markdown_contaminated=false, non_sql=false, ddl_or_dml=false, multi_statement=false, statement_count=1
- `PERF_0054:pg`: empty=false, markdown_contaminated=false, non_sql=false, ddl_or_dml=false, multi_statement=false, statement_count=1

## Artifact-Contract Assessment

- Generated rows satisfy the retained artifact expectations: `yes`.
- Failed rows satisfy the retained failure-path artifact expectations: `yes`.
- Blocked rows satisfy the retained blocked-row artifact expectations: `yes`.
- Unsupported rows satisfy the retained unsupported-row artifact expectations: `yes`.
- `run_event_long.csv` preserves all `120` denominator rows explicitly: `yes`.

## Execution Handoff Boundary

- Execution/validity may proceed only on the generated rows listed above.
- Failed, blocked, and unsupported rows are denominator-visible generation outcomes and are not execution candidates in the current handoff.
- This triage does not authorize timing, speedup, or leaderboard computation.

## Bottom Line

The formal generation package retained denominator-aware outputs for all `120` rows, with `7` generated PG rows, `2` failed PG rows, `31` blocked PG rows, and `80` unsupported mysql/spark rows. Only the `7` generated rows should move into the next execution/validity package.
