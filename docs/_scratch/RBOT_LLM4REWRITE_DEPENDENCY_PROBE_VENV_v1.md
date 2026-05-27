# RBOT_LLM4REWRITE_DEPENDENCY_PROBE_VENV_v1

## 0. Purpose And Boundary

This note records an isolated dependency probe for the `LLM4Rewrite` upstream substrate in a temporary Python virtual environment. Packages were installed only into `/tmp/rewritebench_rbot_llm4rewrite_venv`. This was not R-Bot execution, not a model call, not DB execution, not SQLGlot route execution, not index building, and not leaderboard evidence.

## 1. Input Context

- target upstream repo: `curtis-sun/LLM4Rewrite`
- target path: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
- requirements file used: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/requirements.txt`
- target temporary venv path: `/tmp/rewritebench_rbot_llm4rewrite_venv`

Requirements observed:

- `chromadb`
- `llama_index`
- `llama-index-vector-stores-chroma`
- `jsonlines`
- `jpype1`
- `sqlglot`
- `psycopg2`
- `prettytable`
- `scipy`

## 2. Install Result

- `venv_created`: `yes`
- `pip_upgrade_status`: `success`
- `requirements_install_status`: `failed`
- project `.venv` untouched: `yes`

Failure summary:

- the install failed while building `psycopg2`
- blocking error: `pg_config executable not found`
- because the `pip install -r ...` transaction aborted, the isolated venv did not end up with the required import set installed

Relevant failure snippet:

```text
Error: pg_config executable not found.
pg_config is required to build psycopg2 from source.
```

## 3. Import Probe Result

| module | import_success | version | error_summary |
|---|---|---|---|
| `chromadb` | no | n/a | `ModuleNotFoundError: No module named 'chromadb'` |
| `llama_index` | no | n/a | `ModuleNotFoundError: No module named 'llama_index'` |
| `llama_index.core` | no | n/a | `ModuleNotFoundError: No module named 'llama_index'` |
| `llama_index.vector_stores.chroma` | no | n/a | `ModuleNotFoundError: No module named 'llama_index'` |
| `jpype` | no | n/a | `ModuleNotFoundError: No module named 'jpype'` |
| `psycopg2` | no | n/a | `ModuleNotFoundError: No module named 'psycopg2'` |
| `jsonlines` | no | n/a | `ModuleNotFoundError: No module named 'jsonlines'` |
| `sqlglot` | no | n/a | `ModuleNotFoundError: No module named 'sqlglot'` |
| `openai` | no | n/a | `ModuleNotFoundError: No module named 'openai'` |
| `scipy` | no | n/a | `ModuleNotFoundError: No module named 'scipy'` |
| `prettytable` | no | n/a | `ModuleNotFoundError: No module named 'prettytable'` |

Machine-readable probe output was written to:

`/tmp/rewritebench_rbot_llm4rewrite_venv_probe.json`

## 4. Readiness Impact

Previous blocker status for `missing_required_python_imports`:

`still_blocked`

This probe narrowed the blocker from “imports missing in the current environment” to a more specific install-time dependency issue:

- `psycopg2` source build requires `pg_config`
- the upstream requirement set does not currently install cleanly in the isolated probe venv on this machine

## 5. Remaining Blockers Before R-Bot Smoke

- `missing_required_python_imports`
- `psycopg2_build_blocked_by_missing_pg_config`
- `rag_index_not_built_or_pinned`
- `postgres_runtime_not_verified`
- `single_case_runner_not_implemented_or_not_executed`
- `token_cost_logging_path_still_needs_execution_time_validation`

## 6. Recommended Next Step

`fix_dependency_install_issue`

The next step should be to resolve the isolated dependency install failure first, because the current smoke path is still blocked before any RAG/index preflight or execution-time harness step would be meaningful.

## 7. Non-Modification Note

This probe made no model call, no DB execution, no SQLGlot route execution, no R-Bot execution, and no index build. The project `.venv` was not modified. No registry files, review files, rules files, `docs/EXECUTION_STATUS.md`, or case files were changed. The three long-standing taxonomy notes were untouched.
