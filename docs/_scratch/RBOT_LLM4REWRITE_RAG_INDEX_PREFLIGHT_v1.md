# RBOT_LLM4REWRITE_RAG_INDEX_PREFLIGHT_v1

## 0. Purpose And Boundary

This is a no-execution RAG/index preflight only for the `LLM4Rewrite` R-Bot substrate. No index was built, no model or embedding API was called, no R-Bot method was run, no database was touched, and no SQLGlot route was executed.

## 1. Current R-Bot State

Current state before index build:

- external substrate found via `LLM4Rewrite`
- adapter preflight complete
- three-case input mapping complete for `PERF_0006`, `PERF_0008`, and `PERF_0033`
- single-case harness created for `PERF_0006`
- upstream Python dependencies are importable in `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- current leading blocker is `rag_index_not_built_or_pinned`

## 2. Knowledge / Rule Asset Inventory

Observed assets:

- knowledge-base path present: `yes`
- rule summary file present: `yes`
- rule function path present: `yes`
- prompt/config assets present: `yes`

Important paths:

- knowledge base root: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base`
- rule summary file: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_summaries_structured.jsonl`
- rule function directory: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/knowledge-base/rule_cluster_funcs`
- RAG module root: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag`
- prompt assets: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/prompts.py` and `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/prompts.py`
- config asset: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/config.py`

Visible counts:

- rule function files: `30`
- structured rule summary files: `1`
- bundled embedding archive files: `1`

Bundled RAG archive:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip`

That archive already contains the JSONL inputs used by `rag_gen.py`, including:

- `stackoverflow-rewrite-query-optimization.jsonl`
- `stackoverflow-rewrite-rules-query-optimization.jsonl`
- `stackoverflow-rewrite-sql-templates-query-optimization.jsonl`
- `stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl`

## 3. Index Build Contract

Build script/function:

- primary build entrypoint: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/rag_gen.py`

Required inputs visible in code and assets:

- `stackoverflow-rewrite-query-optimization.jsonl`
- `stackoverflow-rewrite-rules-query-optimization.jsonl`
- `stackoverflow-rewrite-sql-templates-query-optimization.jsonl`
- `stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl`
- `my_rewriter/config.py`
- `rag/gen_rewrites_from_rules.py`

Required outputs:

- Chroma persistent directory at `./chroma_db` relative to the build working directory
- collection name: `stackoverflow`

Embedding backend:

- default path in `init_llms('')`: `OpenAIEmbedding(model=\"text-embedding-3-small\")`
- alternate path when `model_type` contains `open`: `HuggingFaceEmbedding(model_name='gte-Qwen2-1.5B-instruct', max_length=131072)`

OpenAI/model call requirement:

- `rag_gen.py` can avoid fresh embedding calls only when run with the default empty `--model` path, because it reads bundled embeddings from the archive-backed JSONL files
- however, `init_llms()` still initializes an embedding model object, and the README instructs users to set `OPENAI_API_KEY`
- for the practical upstream path as documented, model/API approval should be treated as required for the build path

External data download requirement:

- not for the RAG build itself, because the StackOverflow-derived embedding archive is already present in the repo clone
- benchmark datasets such as TPC-H / DSB / Calcite are part of later benchmark execution, not part of this index-build preflight

Can output be redirected to `/tmp`:

- `yes`
- `rag_gen.py` hardcodes `chromadb.PersistentClient(path=\"./chroma_db\")`
- that means the output path is controlled by the current working directory
- a future build can be staged by copying or bind-mounting the `rag/` subtree into a `/tmp` work directory and running the script there

Determinism / replayability:

- partially replayable
- bundled JSONL assets and explicit collection name are stable
- output path is fixed relative to cwd
- build reproducibility depends on the embedding/backend path chosen and exact dependency versions

Existing prebuilt index present:

- `no`
- no existing `chroma_db` or other visible prebuilt index directory was found in the clone

## 4. Future Index Build Command Candidate

All commands below are `NOT RUN`.

Candidate future build staging:

```bash
cp -R /tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag /tmp/rewritebench_rbot_llm4rewrite_rag_build/
cd /tmp/rewritebench_rbot_llm4rewrite_rag_build/rag
unzip -n stackoverflow-rewrite-embed.zip
/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python rag_gen.py
```

Optional alternate build candidates from the upstream README, also `NOT RUN`:

```bash
/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python rag_structure.py
/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python rag_semantics.py
```

## 5. Artifact Capture Plan

Future approved build should capture:

- index directory, expected as `/tmp/rewritebench_rbot_llm4rewrite_rag_build/rag/chroma_db`
- build log
- embedding/backend config actually used
- rule asset snapshot reference
- knowledge-base snapshot reference
- token/cost log if any API-backed embedding path is used
- failure log

## 6. Readiness Decision

Decision:

`index_build_ready_if_api_approved`

Reason:

- required knowledge/rule assets are present
- the build script is visible
- the output path can be redirected to `/tmp`
- no missing corpus or rule artifact blocker was found

Approval note:

- human approval for OpenAI/API use on the R-Bot smoke path appears sufficient to cover a future RAG/index build on the same path
- no separate approval appears strictly necessary from the current instruction set
- execution-time token/cost capture should still be recorded if the build is later run

## 7. Remaining Blockers Before 1-case Smoke

- `rag_index_not_built_or_pinned`
- `postgres_runtime_not_verified`
- `single_case_runner_not_implemented_or_not_executed`
- `token_cost_logging_path_still_needs_execution_time_validation`

This preflight resolved the contract uncertainty around the RAG/index build, but it did not remove the fact that the index is still not yet built or pinned.

## 8. Recommended Next Step

`perform_actual_RAG/index_build_in_/tmp`

This is the next logical step because:

- the dependency probe is complete
- the asset inventory is complete
- the build contract is now sufficiently concrete
- PostgreSQL runtime verification and the single-case runner matter after the retrieval artifact exists

## 9. Non-Modification Note

This preflight performed no index build, no model or embedding call, no DB execution, no R-Bot execution, and no SQLGlot route execution. It did not modify the project `.venv`, case files, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md`. The three long-standing taxonomy notes were untouched.
