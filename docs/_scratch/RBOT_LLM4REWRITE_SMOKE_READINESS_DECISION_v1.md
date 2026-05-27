# RBOT_LLM4REWRITE_SMOKE_READINESS_DECISION_v1

## 0. Purpose And Boundary

This is readiness decision only.

It is not execution.
It is not result evidence.
It is not a leaderboard artifact.
It is not a prior-method result.

## 1. Current R-Bot Status

Current status:

- external substrate found via `LLM4Rewrite`
- adapter preflight created
- `PERF_0006` / `PERF_0008` / `PERF_0033` map cleanly into temporary input-bundle shape
- no R-Bot method execution has occurred
- no model call has occurred
- no DB execution has occurred
- current status: `adapter_preflight_created_not_executed`

## 2. Smoke Candidate

Recommended first smoke case: `PERF_0006`

Why this is the least risky first case:

- it is already part of the first bounded subset carried through the earlier readiness notes
- it has clean source SQL and PostgreSQL DDL available
- it is compact and analytically simple compared with later candidates
- it is a straightforward one-query denominator for validating the single-case harness and output capture path

Boundary for any future attempt:

- denominator must be `1` case only
- PostgreSQL-only
- no speedup in the first smoke unless checker consistency closes first

## 3. Readiness Gate Table

| gate | status | evidence | required action before smoke |
| --- | --- | --- | --- |
| source SQL mapped | `ready` | all three case bundles contain `source.sql`; `rewritebench_case_metadata.json` points to case source paths | none |
| PG schema mapped | `ready` | all three case bundles contain `create_tables.sql`; metadata points to `schema/ddl_pg.sql` | none |
| `output_sql` capture path understood | `ready` | upstream `db_utils.py` logs `Rewrite Execution Results` with `output_sql` | preserve a stable capture file/log path |
| selected-rules/retrieval trace capture path understood | `ready` | upstream `rag_rewrite.py` logs selected rules and rule-arrangement stages | define exact retained artifact paths |
| PostgreSQL runtime available | `blocked` | preflight run note lists `postgres_runtime_not_prepared` | provision one-case PostgreSQL runtime |
| RAG/index assets built or pinned | `blocked` | preflight run note lists `rag_index_not_built_or_pinned` | build or pin the retrieval/index artifacts reproducibly |
| OpenAI/API policy approved | `blocked` | upstream `config.py` defaults to OpenAI-backed embeddings/LLM paths; preflight lists `model_api_policy_unresolved` | approve API/runtime policy or approved alternative backend |
| single-case harness available | `blocked` | upstream runners are benchmark-loop runners; preflight lists `single_case_runner_not_implemented_upstream` | add a minimal single-case harness or equivalent wrapper path |
| token/cost logging plan | `conditional` | upstream paths imply model usage and runtime cost relevance, but RewriteBench-side accounting is not frozen | define token/cost capture format before smoke |
| failure taxonomy mapping | `conditional` | output and traces are visible, but failure normalization is still log-based | map upstream failures into RewriteBench categories |
| artifact output path plan | `ready` | `/tmp` bundle path exists and output-capture contract is documented | keep bounded artifact paths explicit |
| no registry/leaderboard claim policy | `ready` | all preflight notes keep no-execution and no-leaderboard boundaries explicit | retain those boundaries during any smoke |

## 4. Decision

Decision: `conditionally_ready_after_runtime_policy_resolution`

Reason:

- the substrate exists
- the input mapping works for the bounded first subset
- the output capture path is understood
- but runtime, retrieval/index, API policy, and single-case harness remain unresolved hard gates

## 5. Required Before Execution

- environment variables for the chosen runtime path
- API/model policy decision
- PostgreSQL runtime for the one-case denominator
- RAG/index build or pinned artifact set
- single-case harness or equivalent command path
- artifact capture paths for generated SQL and traces
- `output_sql` extraction path
- checker handoff plan
- explicit no registry writeback / no leaderboard claim policy

## 6. Forbidden Claims

Do not claim:

- R-Bot result
- R-Bot leaderboard evidence
- full prior-method coverage
- checker-backed R-Bot result
- speedup result
- registry/admission/common-core promotion

## 7. Recommended Next Step

Recommended next step: resolve API/runtime policy first

Reason:

- without that decision, a single-case harness still cannot be judged against the real allowed execution path
- the current blocked gates are driven more by runtime/policy than by remaining input mapping uncertainty

## 8. Non-Modification Note

No method execution occurred.
No model call occurred.
No DB execution occurred.
No SQLGlot run occurred.
No package install occurred.
No scripts, cases, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md` were modified.
