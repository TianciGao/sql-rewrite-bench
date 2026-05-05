# RBOT_LLM4REWRITE_RAG_INDEX_BUILD_OPENAI_LIKE_DEP_v1

## 0. Purpose And Boundary

This note records a temp-only dependency fix and RAG/index build retry for the `LLM4Rewrite` substrate. It is not R-Bot execution, not RewriteBench case execution, not DB execution, and not leaderboard evidence.

## 1. Dependency Fix

The missing optional dependency was installed into the isolated smoke venv only:

- package installed: `llama-index-llms-openai-like`
- package version: `0.7.2`
- venv path: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- import `llama_index.llms.openai_like`: `success`
- import `OpenAILike`: `success`
- project `.venv` touched: `no`

## 2. Temp Patches Reapplied

Temp build root:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like`

Copied into the temp build root:

- `rag/`
- `knowledge-base/`
- `explain_rule/`
- `my_rewriter/`

Temp-only patches applied in the copied tree:

- LearnedRewrite / JPype bypass in `rag/gen_rewrites_from_rules.py`
- `sqlglot` `NONDETERMINISTIC` shim in:
  - `knowledge-base/rule_cluster_funcs/24.py`
  - `rag/gen_sql_templates.py`

Modification status:

- upstream clone changed: `no`
- project repo code changed: `no`

## 3. Build Result

Build command:

```bash
cd /tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag && PYTHONPATH=/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like /tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python rag_gen.py > /tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_build.log 2>&1; echo $? > /tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_exit_code.txt
```

Observed result:

- `rag_gen_exit_code`: `0`
- `chroma_db_created`: `yes`
- `chroma_db_path`: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- `build_log_path`: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_build.log`
- directory size: about `204M`
- whether embedding/model/API call appears to have occurred: `no observed external API call from log review; local embedding workload was observed`
- token/cost availability: `not available`

Observed artifacts:

- `chroma.sqlite3`
- HNSW index files under a generated UUID subdirectory

The build log shows local progress bars and final corpus counts:

- `Q&A Count: 2091`
- `SQL Count: 2910`
- `Node Count: 5459`

## 4. Readiness Impact

- `upstream_llama_index_openai_like_module_missing`: `resolved`
- `rag_index_not_built_or_pinned`: `resolved_for_tmp_smoke`

The temp-only RAG/index build is now complete enough for `/tmp` smoke purposes.

## 5. Remaining Blockers Before 1-case R-Bot Smoke

- `postgres_runtime_not_verified`
- `single_case_runner_not_implemented_or_not_executed`
- `token_cost_logging_path_still_needs_execution_time_validation`

## 6. Recommended Next Step

`verify_PostgreSQL_runtime_for_PERF_0006`

The RAG/index blocker is cleared for temp smoke, so the next gating item should be PostgreSQL runtime verification for the target case before attempting any single-case method execution.

## 7. Non-Modification Note

This step performed no R-Bot execution, no RewriteBench case execution, no DB execution, and no SQLGlot route execution. The upstream clone was not modified. Project repo code was not modified, aside from this scratch note. No case files, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md` were changed.
