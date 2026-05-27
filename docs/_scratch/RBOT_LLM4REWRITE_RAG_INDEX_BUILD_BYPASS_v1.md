# RBOT_LLM4REWRITE_RAG_INDEX_BUILD_BYPASS_v1

## 0. Purpose And Boundary

This note records a temp-only bypass build attempt for the `LLM4Rewrite` RAG/index path. It is not R-Bot execution, not RewriteBench case execution, not DB execution, and not SQLGlot route execution.

## 1. Why Bypass Was Needed

The prior tmp build attempt failed before index creation because `rag_gen.py` reached `my_rewriter/rewrite.py` through `rag/gen_rewrites_from_rules.py`, and that module:

- imports `jpype`
- resolves `CalciteRewrite/out/artifacts/LearnedRewrite_jar`
- starts the JVM at import time

That LearnedRewrite Java bridge side effect is not semantically required for vector-index creation, but it blocked the build path before `chroma_db` could be created.

## 2. Temp Patch Applied

Files copied into the temp build root:

- `rag/`
- `knowledge-base/`
- `explain_rule/`
- `my_rewriter/`

Temp build root:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass`

Patched file:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass/rag/gen_rewrites_from_rules.py`

Patch intent:

- avoid importing `my_rewriter.rewrite` at import time
- materialize `NORMAL_RULES` from local `explain_rule/calcite_rewrite_rules_structured.jsonl`
- leave `match_all_rules` and `match_normal_rules` as inert stubs, because they are not used by `rag_gen.py`

Modification status:

- upstream clone changed: `no`
- project repo code changed: `no`

## 3. Build Command

Commands run:

```bash
cd /tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass/rag && unzip -n stackoverflow-rewrite-embed.zip
cd /tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass/rag && PYTHONPATH=/tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass /tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python rag_gen.py > /tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass/rag_gen_build.log 2>&1; echo $? > /tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass/rag_gen_exit_code.txt
```

## 4. Build Result

- `archive_unzipped`: `yes`
- `rag_gen_exit_code`: `1`
- `chroma_db_created`: `no`
- `chroma_db_path`: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass/rag/chroma_db`
- `build_log_path`: `/tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass/rag_gen_build.log`
- directory size: not available because `chroma_db` was not created
- whether OpenAI/model/embedding API appears to have been called: `no_observed_call_before_sqlglot_import_failure`
- token/cost availability: `not available`

Observed new failure:

```text
ImportError: cannot import name 'NONDETERMINISTIC' from 'sqlglot.optimizer.simplify'
```

This indicates the JPype/LearnedRewrite side effect was bypassed successfully, but the build still fails earlier than index creation because one of the copied rule-function files depends on a `sqlglot` API surface that is not present in the currently installed version.

## 5. Readiness Impact

- `rag_index_not_built_or_pinned`: `failed_build`
- `learnedrewrite_import_side_effect`: `bypassed_for_rag_only_tmp_build`

The bypass worked for the original jar/JPype blocker, but the overall tmp build still failed on an upstream rule-function / `sqlglot` compatibility issue.

## 6. Remaining Blockers Before 1-case R-Bot Smoke

- `rag_index_not_built_or_pinned`
- `upstream_rule_function_sqlglot_version_mismatch`
- `postgres_runtime_not_verified`
- `single_case_runner_not_implemented_or_not_executed`
- `token_cost_logging_path_still_needs_execution_time_validation`

## 7. Recommended Next Step

`fix_bypass_build_failure`

The immediate next step should be to isolate or satisfy the upstream `sqlglot` compatibility expectation in the temp-only build path before moving on to PostgreSQL runtime or single-case runner work.

## 8. Non-Modification Note

This step performed no R-Bot execution, no RewriteBench case execution, no DB execution, and no SQLGlot route execution. The upstream clone was not modified. Project repo code was not modified, aside from this scratch note. No case files, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md` were changed.
