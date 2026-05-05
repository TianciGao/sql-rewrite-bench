# RBOT_LLM4REWRITE_ADAPTER_PREFLIGHT_RUN_v1

## 1. Purpose And Boundary

This is no-execution adapter preflight only.

It is not method execution.
It is not a model call.
It is not DB execution.
It is not SQLGlot execution.
It is not leaderboard evidence.
It is not an R-Bot result.

## 2. Case Mapped

- case_id: `PERF_0006`
- pool: `performance`
- target substrate: `R-Bot via LLM4Rewrite`
- upstream repo: `https://github.com/curtis-sun/LLM4Rewrite`

## 3. Temporary Bundle Created

Temporary bundle root:

- `/tmp/rewritebench_rbot_llm4rewrite_adapter_preflight/PERF_0006`

Bundle purpose:

- map one RewriteBench case package into a plausible single-case LLM4Rewrite-compatible input shape
- document the expected later runtime command
- document later output capture requirements
- avoid any method, model, or database execution

## 4. Files Written Under /tmp

- `/tmp/rewritebench_rbot_llm4rewrite_adapter_preflight/PERF_0006/source.sql`
- `/tmp/rewritebench_rbot_llm4rewrite_adapter_preflight/PERF_0006/create_tables.sql`
- `/tmp/rewritebench_rbot_llm4rewrite_adapter_preflight/PERF_0006/rewritebench_case_metadata.json`
- `/tmp/rewritebench_rbot_llm4rewrite_adapter_preflight/PERF_0006/llm4rewrite_config_stub.py`
- `/tmp/rewritebench_rbot_llm4rewrite_adapter_preflight/PERF_0006/expected_command.txt`
- `/tmp/rewritebench_rbot_llm4rewrite_adapter_preflight/PERF_0006/output_capture_contract.md`

## 5. Upstream Contract Observed

Observed upstream contract remained consistent with the earlier audit:

- stock runner shape is benchmark-loop oriented, not single-case oriented
- source SQL and schema are dataset-file driven upstream
- PostgreSQL runtime is assumed
- retrieval/index setup is assumed
- `output_sql` capture path is understood from upstream code
- selected-rules and retrieval-trace capture path is understood from upstream logs

## 6. Mapping Result

- `source_sql_found`: `yes`
- `pg_schema_found`: `yes`
- `temp_bundle_created`: `yes`
- `config_stub_created`: `yes`
- `expected_command_documented`: `yes`
- `output_capture_contract_documented`: `yes`
- `can_attempt_future_1_case_smoke`: `conditional`

Blockers before smoke:

- `postgres_runtime_not_prepared`
- `rag_index_not_built_or_pinned`
- `model_api_policy_unresolved`
- `single_case_runner_not_implemented_upstream`

## 7. Missing Before Execution

The preflight removed the input-bundle uncertainty for `PERF_0006`, but the following still remain before any one-case smoke:

- prepare a PostgreSQL runtime for the one-case denominator
- decide whether OpenAI/API execution is allowed for this baseline
- pin or build the retrieval/index artifacts reproducibly
- decide whether to implement a dedicated single-case harness rather than reuse the upstream benchmark-loop runner
- define exact artifact capture for generated SQL, selected rules, retrieval trace, and failures

## 8. Whether Bounded Smoke Is Ready

Current answer: `conditional`

Reason:

- the case package maps cleanly into a temporary input-bundle shape
- the upstream runner and output path are understood well enough to continue
- but runtime, retrieval/index, and policy dependencies are still unresolved

Required conclusion:

- `PERF_0006` was only mapped into a temporary input-bundle shape
- no R-Bot result exists yet
- R-Bot status may be upgraded only to `adapter_preflight_created_not_executed`
- do not claim runnable result
- do not claim leaderboard coverage

## 9. Recommended Next Step

Recommended next step:

- implement a no-execution adapter scaffold/preflight command for additional first-subset cases only if the same temporary-bundle mapping remains clean

Practical note:

- for actual execution readiness, runtime/data dependencies still need to be acquired first

## 10. Non-Modification Note

No R-Bot or LLM4Rewrite method execution occurred.
No DB execution occurred.
No model call occurred.
No SQLGlot run occurred.
No package install occurred.
No registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were modified.
