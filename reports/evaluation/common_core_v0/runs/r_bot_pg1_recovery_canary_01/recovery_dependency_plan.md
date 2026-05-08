# R-Bot PG1 Recovery Dependency Plan

This document is a recovery-planning artifact only for the `R-Bot` `PERF_0006 / pg` canary.

It does not run R-Bot, call an API, install packages, execute SQL, or create current benchmark evidence.

## Scope

- `method_id = r_bot`
- `route_id = r_bot_pg_rewrite`
- `case_id = PERF_0006`
- `engine = pg`
- current package:
  [r_bot_pg1_recovery_canary_01](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/README.md)

## Current Readout

Observed from the canary run artifacts:

- `OPENAI_API_KEY` was not visible
- the repo-local smoke preflight could not import:
  - `chromadb`
  - `jpype`
  - `jsonlines`
  - `llama_index`
  - `psycopg2`
- the dry-run scaffold did find:
  - `/tmp` `LLM4Rewrite` clone
  - `/tmp` smoke venv
  - `/tmp` RAG index location
  - repo-local single-case harness artifacts
- the row stayed blocked because policy and substrate freeze are still incomplete

## Headline Diagnosis

There are two different environments in play, and they must not be conflated.

### Repo current Python

The repo-local CLI preflight `formal-rbot-llm4rewrite-single-case-smoke-preflight` uses the current interpreter and checks `safe_module_available(...)` there. In the observed run, that interpreter did not have the required modules.

Interpretation:

- the repo current Python is suitable for control-plane preflight
- it is not currently a complete data-plane execution substrate for `R-Bot`

### `/tmp` smoke venv

Scratch evidence shows a separate smoke venv exists at:

- `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`

That venv already had successful import probes for the required stack in earlier dependency notes, including working versions for `chromadb`, `jpype`, `jsonlines`, `llama_index`-family modules, and `psycopg2`.

Interpretation:

- the actual `R-Bot` recovery path is expected to run in the `/tmp` smoke venv, not in repo `.venv`
- the repo-local preflight should be treated as a readiness gate, not proof that repo `.venv` is the right execution substrate

## Missing Dependencies

Missing in the observed current interpreter:

- `OPENAI_API_KEY`
- Python imports:
  - `chromadb`
  - `jpype`
  - `jsonlines`
  - `llama_index`
  - `psycopg2`

Additional integration modules are also likely required by the copied upstream substrate, based on the scratch audits:

- `llama_index.vector_stores.chroma`
- `llama_index.embeddings.openai`
- `llama_index.embeddings.huggingface`
- `llama_index.llms.openai`
- `llama_index.llms.openai_like`

So the dependency gap is not just the five top-level imports shown in `run_results.json`.

## Exact Package Mapping

The practical pip package mapping is:

| import / capability | pip package name | version signal |
|---|---|---|
| `chromadb` | `chromadb` | `1.5.9` observed in `/tmp` smoke probe |
| `jpype` | `jpype1` | `1.7.0` observed in `/tmp` smoke probe |
| `jsonlines` | `jsonlines` | version not captured in current notes |
| `psycopg2` | `psycopg2-binary` for smoke recovery | `2.9.12` observed in `/tmp` smoke probe |
| `sqlglot` helper path | `sqlglot` | `30.7.0` observed in `/tmp` smoke probe |
| `prettytable` helper path | `prettytable` | `3.17.0` observed in `/tmp` smoke probe |
| `scipy` helper path | `scipy` | `1.17.1` observed in `/tmp` smoke probe |
| OpenAI SDK path | `openai` | `2.34.0` observed in `/tmp` smoke probe |
| `llama_index.core` namespace | `llama-index-core` | `0.14.21` observed in `/tmp` smoke probe |
| `llama_index.vector_stores.chroma` | `llama-index-vector-stores-chroma` | import success observed |
| `llama_index.embeddings.openai` | `llama-index-embeddings-openai` | inferred from scratch import audits |
| `llama_index.embeddings.huggingface` | `llama-index-embeddings-huggingface` | inferred from scratch import audits |
| `llama_index.llms.openai` | `llama-index-llms-openai` | inferred from upstream config path |
| `llama_index.llms.openai_like` | `llama-index-llms-openai-like` | import success observed in scratch note |

Important boundary:

- the upstream `requirements.txt` still lists `psycopg2`
- the recovery-safe smoke probe replaced that with `psycopg2-binary` in `/tmp` only, to bypass the `pg_config` build blocker
- that substitution is acceptable for smoke recovery planning, but should stay explicit

## Where These Dependencies Belong

Expected home for execution-time dependencies:

- primary expectation: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- not yet justified as a required startup dependency for repo `.venv`

Reason:

- the current repository phase does not allow silently turning local-LLM-style prior-method dependencies into a repo-wide startup contract
- the observed `R-Bot` substrate is external and scratch-backed
- the repo-local CLI only needs to orchestrate and document the substrate, not absorb all upstream runtime dependencies into the benchmark’s default environment

## Version Confidence

### Versions we can infer with high confidence

From scratch dependency probes:

- `chromadb==1.5.9`
- `jpype1==1.7.0`
- `psycopg2-binary==2.9.12`
- `sqlglot==30.7.0`
- `openai==2.34.0`
- `prettytable==3.17.0`
- `scipy==1.17.1`
- `llama-index-core==0.14.21`

### Versions we cannot fully pin from current evidence

The current notes do not fully pin versions for:

- `jsonlines`
- `llama-index-vector-stores-chroma`
- `llama-index-embeddings-openai`
- `llama-index-embeddings-huggingface`
- `llama-index-llms-openai`
- `llama-index-llms-openai-like`

So the proposed requirements file should distinguish:

- observed versions
- inferred package names without exact version locks

## Substrate State

### Retrieval corpus/index

Current status:

- retrieval corpus: `partial_tmp_only`
- retrieval index: `partial_tmp_only`

What that means:

- the upstream `LLM4Rewrite` clone and RAG assets are visible under `/tmp`
- the current canary does not prove a repo-pinned, frozen Common-core retrieval substrate
- current evidence depends on scratch paths like:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite`
  - `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
  - `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`

### How to pin the retrieval substrate for current Common-core

Before actual current-denominator generation is allowed, pin:

1. the upstream clone identity
   - repo URL
   - commit SHA
   - local snapshot root
2. the knowledge-base inputs
   - `rule_cluster_summaries_structured.jsonl`
   - rule function directory snapshot
   - bundled `stackoverflow-rewrite-embed.zip`
3. the built index
   - exact `chroma_db` directory origin
   - build working directory
   - build command
   - dependency snapshot used
4. a machine-readable manifest
   - path list
   - file sizes or hashes
   - collection name
   - embedding/backend mode actually used

Recommended pinning boundary:

- move from unnamed `/tmp` scratch assumptions to a documented frozen snapshot manifest
- current evidence should not rely on “whatever index happened to exist in `/tmp`”

## Demo Selection Policy Freeze

Current status:

- `not_frozen`

Before actual current evidence is allowed, define and freeze:

1. eligible retrieval corpus scope
   - what documents/rules may be retrieved
2. deterministic selection rule
   - top-k
   - ranking path
   - tie-breaker
   - any seed or deterministic ordering contract
3. prompt/demo template
   - exact system/user template used by the upstream runner or wrapper
4. case isolation rule
   - no hand-curated per-case demo swaps after looking at target outcomes
5. artifact capture
   - selected rules JSON
   - retrieval trace JSON
   - prompt/policy snapshot reference

## Contamination Guard Definition

Current status:

- `not_available`

For current evidence, the contamination guard should minimally state:

1. no target-case answer leakage
   - no known gold rewrite for `PERF_0006` or any frozen denominator row inside the retrieval corpus or demos
2. no benchmark-local generated candidates in the retrieval index
   - do not index outputs from RewriteBench method runs back into the corpus
3. no post-hoc demo tuning
   - after inspecting a case failure, do not mutate the demo set for that row without declaring a new experiment line
4. substrate provenance must be recorded
   - upstream source
   - snapshot/commit
   - build date
   - manifest

## Preconditions Before `RBOT_CANARY_ALLOW_ACTUAL_RUN=1`

The canary should remain blocked until all of the following are true:

1. `OPENAI_API_KEY` is visible in the same shell that launches the human-run script.
2. The `/tmp` smoke venv is present and passes an import probe for the required Python modules.
3. The exact RAG/index snapshot is pinned by manifest, not only inferred from `/tmp`.
4. The prompt/demo selection policy is frozen and written down.
5. The contamination guard is frozen and written down.
6. The upstream clone identity and commit are recorded.
7. The artifact contract is frozen for:
   - generated SQL
   - selected rules
   - retrieval trace
   - token/cost log
   - failure taxonomy
8. The run is declared as current Common-core evidence rather than historical smoke.

If any item above is still missing, `RBOT_CANARY_ALLOW_ACTUAL_RUN=1` should not produce current evidence.

## Recommended Next Step

Do not attempt actual PG1 generation yet.

Recommended next step:

1. freeze the substrate manifest
2. freeze demo policy and contamination guard
3. confirm the `/tmp` smoke venv dependency set through a non-mutating probe policy
4. only then allow a one-case actual generation canary

Current recommendation: `not_yet_ready_for_actual_generation`
