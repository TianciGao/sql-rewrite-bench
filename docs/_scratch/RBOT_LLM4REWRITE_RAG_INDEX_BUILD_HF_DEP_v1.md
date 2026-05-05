# RBOT_LLM4REWRITE_RAG_INDEX_BUILD_HF_DEP_v1

## 0. Purpose And Boundary

This note records a temp-only dependency fix and RAG/index build retry for the `LLM4Rewrite` substrate. It is not R-Bot execution, not RewriteBench case execution, not DB execution, and not leaderboard evidence.

## 1. Dependency Fix

The missing optional dependency was installed into the isolated smoke venv only:

- package installed: `llama-index-embeddings-huggingface`
- package version: `0.7.0`
- venv path: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- import `llama_index.embeddings.huggingface`: `success`
- import `HuggingFaceEmbedding`: `success`
- project `.venv` touched: `no`

Observed runtime impact:

- the isolated `/tmp` smoke venv grew to about `5.4G`
- the optional dependency pulled in a large `sentence-transformers` / `torch` stack

## 2. Temp Patches Reapplied

Temp build root:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_hf`

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

Patch intent:

- avoid importing `my_rewriter.rewrite` and its import-time JPype / LearnedRewrite jar lookup
- map the copied upstream `sqlglot` import to `Simplifier.NONDETERMINISTIC`

Modification status:

- upstream clone changed: `no`
- project repo code changed: `no`

## 3. Build Result

Build command:

```bash
cd /tmp/rewritebench_rbot_llm4rewrite_rag_build_hf/rag && PYTHONPATH=/tmp/rewritebench_rbot_llm4rewrite_rag_build_hf /tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python rag_gen.py > /tmp/rewritebench_rbot_llm4rewrite_rag_build_hf/rag_gen_build.log 2>&1; echo $? > /tmp/rewritebench_rbot_llm4rewrite_rag_build_hf/rag_gen_exit_code.txt
```

Observed result:

- `rag_gen_exit_code`: `1`
- `chroma_db_created`: `no`
- `chroma_db_path`: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_hf/rag/chroma_db`
- `build_log_path`: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_hf/rag_gen_build.log`
- directory size: not available because `chroma_db` was not created
- embedding/model/API call appears to have occurred: `no_observed_call_before_openai_like_import_failure`
- token/cost availability: `not available`

New failure:

```text
ModuleNotFoundError: No module named 'llama_index.llms.openai_like'
```

This means the specific HuggingFace embedding blocker was cleared, but the copied upstream `my_rewriter/config.py` still expects an additional `llama_index` integration module before the RAG build can proceed.

## 4. Readiness Impact

- `upstream_llama_index_huggingface_module_missing`: `resolved`
- `rag_index_not_built_or_pinned`: `failed_build`

The build moved past the prior HuggingFace import blocker, but the RAG/index path is still blocked by another upstream `llama_index` dependency gap.

## 5. Remaining Blockers Before 1-case R-Bot Smoke

- `rag_index_not_built_or_pinned`
- `upstream_llama_index_openai_like_module_missing`
- `postgres_runtime_not_verified`
- `single_case_runner_not_implemented_or_not_executed`
- `token_cost_logging_path_still_needs_execution_time_validation`

## 6. Recommended Next Step

`fix_new_build_failure`

The immediate next step should be to resolve or bypass the copied upstream `llama_index.llms.openai_like` expectation before moving on to PostgreSQL runtime or the single-case runner.

## 7. Non-Modification Note

This step performed no R-Bot execution, no RewriteBench case execution, no DB execution, and no SQLGlot route execution. The upstream clone was not modified. Project repo code was not modified, aside from this scratch note. No case files, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md` were changed.
