# RBOT_LLM4REWRITE_RAG_INDEX_BUILD_SQLGLOT_SHIM_v1

## 0. Purpose And Boundary

This note records a temp-only `sqlglot` shim RAG/index build retry for the `LLM4Rewrite` substrate. It is not R-Bot execution, not RewriteBench case execution, not DB execution, and not SQLGlot route execution.

## 1. Why Shim Was Needed

The previous temp-only bypass already cleared the LearnedRewrite / JPype import side effect, but the build then failed because copied upstream files expected:

```python
from sqlglot.optimizer.simplify import NONDETERMINISTIC
```

while the installed `sqlglot` in the smoke venv exposes:

- `Simplifier.NONDETERMINISTIC`

instead of a module-level `NONDETERMINISTIC`.

## 2. Temp Patches Applied

Files copied into the temp build root:

- `rag/`
- `knowledge-base/`
- `explain_rule/`
- `my_rewriter/`

Temp build root:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_shim`

Files patched in the copied tree:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_shim/rag/gen_rewrites_from_rules.py`
- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_shim/knowledge-base/rule_cluster_funcs/24.py`
- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_shim/rag/gen_sql_templates.py`

Patch intent:

- patch 1: bypass `my_rewriter.rewrite` import-time JPype / LearnedRewrite jar side effect for RAG-only build
- patch 2: replace module-level `NONDETERMINISTIC` import with:
  - `from sqlglot.optimizer.simplify import Simplifier`
  - `NONDETERMINISTIC = Simplifier.NONDETERMINISTIC`

Modification status:

- upstream clone changed: `no`
- project repo code changed: `no`

## 3. Build Command

Commands run:

```bash
cd /tmp/rewritebench_rbot_llm4rewrite_rag_build_shim/rag && unzip -n stackoverflow-rewrite-embed.zip
cd /tmp/rewritebench_rbot_llm4rewrite_rag_build_shim/rag && PYTHONPATH=/tmp/rewritebench_rbot_llm4rewrite_rag_build_shim /tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python rag_gen.py > /tmp/rewritebench_rbot_llm4rewrite_rag_build_shim/rag_gen_build.log 2>&1; echo $? > /tmp/rewritebench_rbot_llm4rewrite_rag_build_shim/rag_gen_exit_code.txt
```

## 4. Build Result

- `archive_unzipped`: `yes`
- `rag_gen_exit_code`: `1`
- `chroma_db_created`: `no`
- `chroma_db_path`: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_shim/rag/chroma_db`
- `build_log_path`: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_shim/rag_gen_build.log`
- directory size: not available because `chroma_db` was not created
- whether OpenAI/model/embedding API appears to have been called: `no_observed_call_before_llama_index_huggingface_import_failure`
- token/cost availability: `not available`

Observed new failure:

```text
ModuleNotFoundError: No module named 'llama_index.embeddings.huggingface'
```

This means the `sqlglot` shim itself worked well enough to move execution past the previous blocker, but the build still fails before index creation because the installed `llama_index` package set does not provide the import path expected by copied upstream `my_rewriter/config.py`.

## 5. Readiness Impact

- `rag_index_not_built_or_pinned`: `failed_build`
- `learnedrewrite_import_side_effect`: `bypassed_for_rag_only_tmp_build`
- `sqlglot_nondeterministic_mismatch`: `bypassed_for_tmp_build`

The build is still blocked, but on a new dependency-compatibility issue rather than the earlier JPype or `sqlglot` blockers.

## 6. Remaining Blockers Before 1-case R-Bot Smoke

- `rag_index_not_built_or_pinned`
- `upstream_llama_index_huggingface_module_missing`
- `postgres_runtime_not_verified`
- `single_case_runner_not_implemented_or_not_executed`
- `token_cost_logging_path_still_needs_execution_time_validation`

## 7. Recommended Next Step

`fix_new_build_failure`

The immediate next step should be to isolate or satisfy the copied upstream `llama_index.embeddings.huggingface` expectation before moving on to PostgreSQL runtime or the single-case runner.

## 8. Non-Modification Note

This step performed no R-Bot execution, no RewriteBench case execution, no DB execution, and no SQLGlot route execution. The upstream clone was not modified. Project repo code was not modified, aside from this scratch note. No case files, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md` were changed.
