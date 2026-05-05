# RBOT_LLM4REWRITE_ADAPTER_PREFLIGHT_RUN_v1

## 1. Purpose And Boundary

This is no-execution adapter preflight only.

It is not method execution.
It is not a model call.
It is not DB execution.
It is not SQLGlot execution.
It is not leaderboard evidence.
It is not an R-Bot result.

## 2. Cases Mapped

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`

All three cases were mapped against the same upstream substrate:

- target substrate: `R-Bot via LLM4Rewrite`
- upstream repo: `https://github.com/curtis-sun/LLM4Rewrite`

## 3. Temporary Bundles Created

Temporary bundle roots:

- `/tmp/rewritebench_rbot_llm4rewrite_adapter_preflight/PERF_0006`
- `/tmp/rewritebench_rbot_llm4rewrite_adapter_preflight/PERF_0008`
- `/tmp/rewritebench_rbot_llm4rewrite_adapter_preflight/PERF_0033`

Bundle purpose:

- map each RewriteBench case package into a plausible single-case LLM4Rewrite-compatible input shape
- document the expected later runtime command
- document later output capture requirements
- avoid any method, model, or database execution

## 4. Files Written Under /tmp

Each case bundle contains:

- `source.sql`
- `create_tables.sql`
- `rewritebench_case_metadata.json`
- `llm4rewrite_config_stub.py`
- `expected_command.txt`
- `output_capture_contract.md`

## 5. Upstream Contract Observed

Observed upstream contract remained consistent across all three mappings:

- stock runner shape is benchmark-loop oriented, not single-case oriented
- source SQL and schema are dataset-file driven upstream
- PostgreSQL runtime is assumed
- retrieval/index setup is assumed
- `output_sql` capture path is understood from upstream code
- selected-rules and retrieval-trace capture path is understood from upstream logs

## 6. Mapping Result

### PERF_0006

- `source_sql_found`: `yes`
- `pg_schema_found`: `yes`
- `temp_bundle_created`: `yes`
- `config_stub_created`: `yes`
- `expected_command_documented`: `yes`
- `output_capture_contract_documented`: `yes`
- `can_attempt_future_1_case_smoke`: `conditional`

### PERF_0008

- `source_sql_found`: `yes`
- `pg_schema_found`: `yes`
- `temp_bundle_created`: `yes`
- `config_stub_created`: `yes`
- `expected_command_documented`: `yes`
- `output_capture_contract_documented`: `yes`
- `can_attempt_future_1_case_smoke`: `conditional`

### PERF_0033

- `source_sql_found`: `yes`
- `pg_schema_found`: `yes`
- `temp_bundle_created`: `yes`
- `config_stub_created`: `yes`
- `expected_command_documented`: `yes`
- `output_capture_contract_documented`: `yes`
- `can_attempt_future_1_case_smoke`: `conditional`

Shared blockers before smoke:

- `postgres_runtime_not_prepared`
- `rag_index_not_built_or_pinned`
- `model_api_policy_unresolved`
- `single_case_runner_not_implemented_upstream`

## 7. Missing Before Execution

The preflight removed the input-bundle uncertainty for `PERF_0006`, `PERF_0008`, and `PERF_0033`, but the following still remain before any one-case smoke:

- prepare a PostgreSQL runtime for the one-case denominator
- decide whether OpenAI/API execution is allowed for this baseline
- pin or build the retrieval/index artifacts reproducibly
- decide whether to implement a dedicated single-case harness rather than reuse the upstream benchmark-loop runner
- define exact artifact capture for generated SQL, selected rules, retrieval trace, and failures

## 8. Whether Bounded Smoke Is Ready

Current answer for all three cases: `conditional`

Reason:

- the case packages map cleanly into a temporary input-bundle shape
- the upstream runner and output path are understood well enough to continue
- but runtime, retrieval/index, and policy dependencies are still unresolved

Required conclusions:

- this is no-execution adapter preflight only
- no R-Bot result exists yet
- no model call occurred
- no DB execution occurred
- no SQLGlot run occurred
- `PERF_0006`, `PERF_0008`, and `PERF_0033` were only mapped into temporary input-bundle shapes
- R-Bot status may be upgraded only to `adapter_preflight_created_not_executed`
- do not claim runnable result
- do not claim leaderboard coverage

## 9. Recommended Next Step

Recommended next step:

- keep the existing no-execution adapter preflight command as the reusable mapping scaffold
- do not attempt bounded smoke until runtime/data dependencies are explicitly resolved

## 10. Non-Modification Note

No R-Bot or LLM4Rewrite method execution occurred.
No DB execution occurred.
No model call occurred.
No SQLGlot run occurred.
No package install occurred.
No registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were modified.
