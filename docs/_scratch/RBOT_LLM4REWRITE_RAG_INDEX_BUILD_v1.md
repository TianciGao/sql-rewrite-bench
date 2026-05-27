# RBOT_LLM4REWRITE_RAG_INDEX_BUILD_v1

## 0. Purpose And Boundary

This note records only an attempted RAG/index build artifact creation step for the `LLM4Rewrite` R-Bot substrate. It is not R-Bot execution, not RewriteBench case execution, not DB execution, and not leaderboard evidence.

## 1. Build Inputs

- source rag dir: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag`
- temp build dir: `/tmp/rewritebench_rbot_llm4rewrite_rag_build/rag`
- venv path: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- bundled archive path: `/tmp/rewritebench_rbot_llm4rewrite_rag_build/rag/stackoverflow-rewrite-embed.zip`
- `OPENAI_API_KEY` visible: `yes`

## 2. Build Command

Commands actually run:

```bash
cd /tmp/rewritebench_rbot_llm4rewrite_rag_build/rag && unzip -n stackoverflow-rewrite-embed.zip
cd /tmp/rewritebench_rbot_llm4rewrite_rag_build/rag && /tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python rag_gen.py > /tmp/rewritebench_rbot_llm4rewrite_rag_build/rag_gen_build.log 2>&1; echo $? > /tmp/rewritebench_rbot_llm4rewrite_rag_build/rag_gen_exit_code.txt
cd /tmp/rewritebench_rbot_llm4rewrite_rag_build/rag && PYTHONPATH=/tmp/rewritebench_prior_method_audit/LLM4Rewrite /tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python rag_gen.py > /tmp/rewritebench_rbot_llm4rewrite_rag_build/rag_gen_build.log 2>&1; echo $? > /tmp/rewritebench_rbot_llm4rewrite_rag_build/rag_gen_exit_code.txt
```

The second command was a controlled retry after the first failed because the staged `rag/` subtree could not import `my_rewriter`.

## 3. Build Result

- `archive_unzipped`: `yes`
- `rag_gen_exit_code`: `1`
- `build_log_path`: `/tmp/rewritebench_rbot_llm4rewrite_rag_build/rag_gen_build.log`
- `chroma_db_created`: `no`
- `chroma_db_path`: `/tmp/rewritebench_rbot_llm4rewrite_rag_build/rag/chroma_db`
- file counts / directory size: no `chroma_db` directory exists, so size is not available
- embedding/backend observed: upstream default path still points to `OpenAIEmbedding("text-embedding-3-small")`, but execution failed before index creation
- whether API/model call appears to have occurred: `no_observed_call_before_upstream_import_failure`
- token/cost fields: not available

Observed failure:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'CalciteRewrite/out/artifacts/LearnedRewrite_jar'
```

That failure occurred during upstream import/setup, before any visible `chroma_db` output was created.

## 4. Artifact Capture

- build log path: `/tmp/rewritebench_rbot_llm4rewrite_rag_build/rag_gen_build.log`
- chroma_db path: `/tmp/rewritebench_rbot_llm4rewrite_rag_build/rag/chroma_db`
- source asset snapshot path: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag`
- build summary JSON path: `/tmp/rewritebench_rbot_llm4rewrite_rag_index_build_summary.json`

## 5. Readiness Impact

Blocker `rag_index_not_built_or_pinned` status:

`failed_build`

This attempt did not produce a usable tmp index artifact. It also exposed a new concrete upstream blocker:

- `upstream_calcite_learnedrewrite_jar_dependency_missing`

## 6. Remaining Blockers Before 1-case R-Bot Smoke

- `rag_index_not_built_or_pinned`
- `upstream_calcite_learnedrewrite_jar_dependency_missing`
- `postgres_runtime_not_verified`
- `single_case_runner_not_implemented_or_not_executed`
- `token_cost_logging_path_still_needs_execution_time_validation`

## 7. Recommended Next Step

`fix_RAG/index_build_failure`

The immediate next step should be to isolate or bypass the unexpected upstream Calcite/LearnedRewrite jar dependency in the index build path before moving on to PostgreSQL runtime or single-case runner work.

## 8. Non-Modification Note

This step performed no R-Bot execution, no RewriteBench case execution, no DB execution, and no SQLGlot route execution. No case files, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md` were modified. The project `.venv` was untouched.
