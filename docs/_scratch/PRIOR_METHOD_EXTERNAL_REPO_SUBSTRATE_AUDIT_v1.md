# PRIOR_METHOD_EXTERNAL_REPO_SUBSTRATE_AUDIT_v1

## 0. Purpose And Boundary

This is an external substrate audit only.

It is not implementation.
It is not execution.
It is not a runnable-baseline claim.
It is not a registry writeback.
It is not a leaderboard artifact.

No method, database, model, or SQLGlot route was executed during this audit.

## 1. Executive Summary

Two newly found upstream repositories were inspected as candidate runnable substrates for boss-requested prior methods:

- `https://github.com/curtis-sun/LLM4Rewrite`
- `https://github.com/DAMO-NLP-SG/LLM-R2`

Current high-level conclusion:

- `LLM4Rewrite` is a real upstream substrate candidate and clearly maps to `R-Bot`.
- `LLM4Rewrite` also contains a bundled `LearnedRewrite` bridge and jar artifact, but that path still requires local audit and RewriteBench-specific adaptation before any bounded smoke.
- `LLM-R2` resolves on `git ls-remote`, but shallow clone did not complete successfully in this environment, so its code tree could not be inspected locally.

## 2. Repository Findings

### 2.1 `curtis-sun/LLM4Rewrite`

| field | finding |
| --- | --- |
| URL | `https://github.com/curtis-sun/LLM4Rewrite` |
| `git ls-remote` | success |
| default branch | `main` |
| latest commit hash | `c9c90e5d7867888c3aaba86e4fc9e6d48f53b375` |
| license file present | `yes` |
| README present | `yes` |
| requirements/environment files present | `requirements.txt` present |
| runnable entrypoints found | `my_rewriter/test.sh`, `test_tpch.sh`, `test_dsb.sh`, `test_calcite.sh`, `test.py`, `test_learned_rewrite.py`, `test_llm_only.py` |
| dataset requirements | explicit `TPC-H`, `DSB`, and `Calcite` datasets plus six PostgreSQL databases |
| model/API requirements | `OpenAI` API path present; also `OpenAILike` and `HuggingFaceEmbedding` config paths |
| DB/runtime requirements | Ubuntu 22.04, PostgreSQL 14.13, Python 3.10, OpenJDK 17, JPype, Calcite jar path |
| retrieval/demo/rule assets present | `rag/`, `knowledge-base/`, `rule_cluster_summaries_structured.jsonl`, `rule_cluster_funcs/`, `stackoverflow-rewrite-embed.zip`, prompt files, rewrite-rule jsonl files |
| output SQL path visible | `yes`; code writes `output_sql` in `test_learned_rewrite.py`, and bundled Java `LearnedRewriter.java` emits `output_sql` |
| maps to | primary: `R-Bot`; secondary embedded path: `LearnedRewrite`; not `LLM-R2` |
| current classification | `runnable_after_adapter_possible` |

Specific checks:

- Does it implement `R-Bot`?
  - yes; README title is `R-Bot: An LLM-based Query Rewrite System`
- Does it include `rag` / knowledge-base / rule files?
  - yes
- Does it include `my_rewriter/test.sh` or equivalent runner?
  - yes
- Does it require OpenAI API?
  - yes for the main documented path
- Does it require TPC-H / DSB / Calcite databases?
  - yes, explicitly
- Does it output rewritten SQL in logs or files?
  - yes in code path via `output_sql`; runtime result files are generated during execution rather than bundled
- Does it include any `LearnedRewrite` runner or only logs?
  - it includes a real `test_learned_rewrite.py` runner plus `CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`, not only logs

Exact missing pieces before a RewriteBench bounded smoke:

- freeze and audit the runtime/dependency contract locally
- decide whether OpenAI-based execution is allowed, or whether only the non-OpenAI open-model path is admissible
- confirm whether the bundled `LearnedRewrite.jar` is source-consistent and reproducible enough to treat as upstream substrate rather than only a packaged artifact
- define a RewriteBench adapter from case package to the repo input contract
- define a PostgreSQL-only bounded denominator that does not assume TPC-H/DSB/Calcite benchmark setup
- separate `R-Bot` evidence from the embedded `LearnedRewrite` path so the two baselines are not conflated
- define artifact capture for generated SQL, selected rules, retrieval trace, and failure modes

### 2.2 `DAMO-NLP-SG/LLM-R2`

| field | finding |
| --- | --- |
| URL | `https://github.com/DAMO-NLP-SG/LLM-R2` |
| `git ls-remote` | success |
| default branch | `main` |
| latest commit hash | `91ba530b45b1353d6d2cc45d816dfefc34dbad92` |
| license file present | `unknown`; clone did not complete |
| README present | `unknown`; clone did not complete |
| requirements/environment files present | `unknown`; clone did not complete |
| runnable entrypoints found | `unknown`; clone did not complete |
| dataset requirements | `unknown`; clone did not complete |
| model/API requirements | `unknown`; clone did not complete |
| DB/runtime requirements | `unknown`; clone did not complete |
| retrieval/demo/rule assets present | `unknown`; clone did not complete |
| output SQL path visible | `unknown`; clone did not complete |
| maps to | likely `LLM-R2`, but local substrate audit could not verify file-level contracts |
| current classification | `acquired_candidate_needs_local_audit` |

Specific checks:

- Does the repo exist and clone?
  - repo exists
  - `git ls-remote` succeeded
  - shallow clone did not complete successfully in this environment
- Does it include demo pool / rule library / rule applier?
  - unknown from this audit because source files were not inspectable locally
- Does it include contrastive model code or checkpoints?
  - unknown
- Does it include runnable scripts?
  - unknown
- Does it require API model calls?
  - unknown
- Does it output rewritten SQL?
  - unknown
- Does it include benchmark data or preprocessing scripts?
  - unknown

Clone failure observed during retry:

- `fatal: could not open '/tmp/rewritebench_prior_method_audit/LLM-R2/.git/objects/pack/tmp_pack_814zeH' for reading: No such file or directory`
- `fatal: fetch-pack: invalid index-pack output`

Exact missing pieces before a RewriteBench bounded smoke:

- one successful local source checkout for inspection
- README and license inspection
- runnable entrypoint identification
- demo/rule/retrieval substrate confirmation
- model/checkpoint/API contract confirmation
- input/output SQL contract confirmation
- benchmark/preprocessing dependency confirmation
- RewriteBench adapter boundary and artifact-capture policy

## 3. Mapping Back To Boss-requested Baselines

### `LLM4Rewrite`

- strongest mapping: `R-Bot`
- secondary embedded path: `LearnedRewrite`
- not evidence for `LLM-R2`

Interpretation:

- this repo materially changes the `R-Bot` status from pure acquisition-blocker abstraction to a concrete upstream candidate with visible code, assets, and runners
- it does not by itself close `R-Bot` for RewriteBench because bounded local adapter work, runtime freeze, and policy decisions still remain
- it also suggests that `LearnedRewrite` may be partially obtainable through this repo bundle, but that needs a separate local audit because the embedded jar and Java wrapper are not yet validated as a clean standalone upstream baseline path

### `LLM-R2`

- likely maps to `LLM-R2`
- current audit did not reach a file-level substrate conclusion because the clone did not complete

Interpretation:

- this repo should be treated as a real upstream candidate rather than a purely hypothetical line
- but the current evidence is still insufficient to upgrade it to `runnable_after_adapter_possible`

## 4. Provisional Classification Summary

| repo | provisional classification | why |
| --- | --- | --- |
| `curtis-sun/LLM4Rewrite` | `runnable_after_adapter_possible` | code, README, license, requirements, RAG assets, runners, PostgreSQL runtime assumptions, and `output_sql` path are all visible |
| `DAMO-NLP-SG/LLM-R2` | `acquired_candidate_needs_local_audit` | upstream ref resolves, but local clone did not complete, so runnable substrate claims remain unverified |

## 5. Non-Modification Note

No DB was run.
No model was called.
No SQLGlot route was run.
No benchmark method was executed.
No external code was added to the project repo.
No registry, review, rules, `docs/EXECUTION_STATUS.md`, case files, reports, or scripts were modified.
