# RBOT_LLM4REWRITE_SINGLE_CASE_HARNESS_PREFLIGHT_v1

## 1. Purpose And Boundary

This note records a single-case harness preflight for `PERF_0006` using the upstream `LLM4Rewrite` repository as the candidate R-Bot substrate. This is harness-preflight evidence only. It is not method execution, not result evidence, not leaderboard evidence, and not a prior-method closure claim.

## 2. Human API Policy Decision

Human direction now permits OpenAI/API use for a later R-Bot / LLM4Rewrite smoke path, and token budget is not currently treated as a blocker. This preflight did not call OpenAI or any other model. Token and cost logging remain required if execution later occurs.

## 3. Target Case

Target case: `PERF_0006`

The existing no-execution adapter preflight bundle for `PERF_0006` was verified and reused. The single-case harness preflight then created a separate execution-oriented harness directory under `/tmp` without executing R-Bot, PostgreSQL, or any model-backed step.

## 4. Harness Files Created

Harness root:

`/tmp/rewritebench_rbot_llm4rewrite_single_case_smoke/PERF_0006/`

Files written:

- `source.sql`
- `create_tables.sql`
- `llm4rewrite_single_case_config_stub.py`
- `proposed_future_execute_command.txt`
- `artifact_capture_plan.md`
- `readiness_summary.json`
- `DO_NOT_RUN_YET.txt`

These files define only the single-case harness shape, a non-secret config stub, a proposed future command, and the capture plan needed if a later smoke is approved.

## 5. Environment Readiness

Observed from the no-execution readiness probe:

- `OPENAI_API_KEY` visible: `yes`
- PostgreSQL env visible as a complete set across `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`: `yes`
- `LLM4Rewrite` clone visible under `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`: `yes`

Required import probe results:

- `chromadb`: missing
- `llama_index`: missing
- `jpype`: missing
- `psycopg2`: missing
- `jsonlines`: missing

Current environment conclusion: basic shell/env visibility is present, but Python runtime dependencies for the upstream stack are not yet available in this environment.

## 6. RAG / Index Readiness

Observed from the preflight:

- RAG / knowledge-base assets visible: `yes`
- Chroma / index artifacts already visible: `no`

The harness documents a plausible future index-build step, but this preflight did not build any RAG or Chroma index. Index readiness therefore remains conditional rather than execution-ready.

## 7. PostgreSQL Runtime Readiness

The required PostgreSQL environment variables are visible, which is enough for a no-execution readiness check. No PostgreSQL connection was attempted and no query was executed. Runtime reachability, credentials validity, schema loadability, and upstream DB compatibility remain unverified at this stage.

## 8. Execution Readiness Decision

Current status should now be described as:

`single_case_harness_created_execution_ready_or_blocked_with_exact_reasons`

Machine-readable readiness result for `PERF_0006`:

- `source_sql_found`: `yes`
- `pg_schema_found`: `yes`
- `openai_api_key_visible`: `yes`
- `pg_env_visible`: `yes`
- `llm4rewrite_clone_visible`: `yes`
- `required_python_imports`: `not ready`
- `rag_assets_visible`: `yes`
- `chroma_index_visible`: `no`
- `single_case_harness_created`: `yes`
- `can_execute_next`: `no`

Decision:

The harness exists and the case maps cleanly into a single-case execution shape, but execution readiness is still blocked. The exact current blocker is missing required Python imports for the upstream stack.

## 9. Remaining Blockers

- `missing_required_python_imports`

Additional conditions that remain unresolved even though they are not the current decisive blocker:

- Chroma / retrieval index has not been built or pinned in this environment
- actual PostgreSQL runtime compatibility has not been verified
- no single-case execution run has been attempted

## 10. Exact Next Command If Approved Later

The harness wrote the proposed future command to:

`/tmp/rewritebench_rbot_llm4rewrite_single_case_smoke/PERF_0006/proposed_future_execute_command.txt`

The documented future execution shape is:

```bash
python3 -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-run \
  --case PERF_0006 \
  --bundle /tmp/rewritebench_rbot_llm4rewrite_single_case_smoke/PERF_0006 \
  --database rewritebench_perf_0006 \
  --index hybrid
```

That command has not been implemented or run in this preflight. The file also records the expected prior index-build step and environment assumptions.

## 11. Forbidden Claims

Do not claim any of the following from this preflight:

- an R-Bot result
- checker-backed R-Bot evidence
- speedup evidence
- leaderboard coverage
- full prior-method coverage
- registry, admission, or common-core promotion

## 12. Non-Modification Note

This preflight made no method execution, no model call, no PostgreSQL execution, no MySQL execution, no Spark execution, and no SQLGlot run. It did not modify case files, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md`. The three long-standing taxonomy notes were not touched.

Claim boundary retained:

`single_case_harness_preflight_only_not_rbot_result`
