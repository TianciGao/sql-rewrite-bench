# BASELINE_ROUTE_STATUS_AND_BACKLOG_v0

## 1. Status

This is a tracked scratch baseline route status and backlog packet.

It summarizes the current execution-layer smoke state across baseline route Steps 1 through 9 and records the immediate backlog posture.

This document is not:

- a registry writeback
- a common-core admission decision
- a leaderboard result
- a correctness scoring artifact
- a speedup scoring artifact
- a formal review update

## 2. Status Table

| step | route / baseline family | current status | scope | result | current interpretation | next posture |
|---|---|---|---|---|---|---|
| Step 1 | Native / Human positive / Hard negative guard | complete | PG-only 9-case PERF/CONS smoke set | execution-layer smoke complete | control route established | retain as smoke control reference |
| Step 2a | SQLGlot optimize same-dialect | complete | PG-only 9-case PERF/CONS smoke set | execution-layer smoke complete | same-dialect SQLGlot route is open | retain as active comparison route |
| Step 2b | SQLGlot transpile | partial | PORT 3-case smoke set | preflight 3 / 3 complete; PG execution 2 / 3 | one execution-layer failure captured on `PORT_0012` | hold for failure analysis, not clean subset closure |
| Step 3 | Calcite HEP rules | readiness-only complete | first-subset and PG-native-9 audit scope | readiness audit complete; parse-readiness scaffold complete | subset-only, adapter missing, no actual parse/rewrite attempted | not execution-ready |
| Step 4a | Direct LLM rewrite | complete | PG-native 9-case PERF/CONS smoke set | model call 9 / 9; extraction 9 / 9; PG execution 9 / 9; `total_token_usage=5089` | execution-layer smoke route complete | retain as current LLM rewrite milestone |
| Step 4b | LLM translate | partial but clean subset passed | PORT smoke route | prompt dry-run 3 / 3; clean PORT canary subset 2 / 2 passed for `PORT_0004` and `PORT_0022`; `total_token_usage=912` | clean subset established; `PORT_0012` held for separate comparison | continue only with bounded failure analysis |
| Step 5 | LearnedRewrite | readiness-only complete | first-subset and PG-native-9 audit scope | readiness audit complete; input-readiness scaffold complete; first-subset `4`, maybe_later `5`; no inference/rewrite/execution attempted | subset-only candidate, artifact stack missing, not execution-ready | execution deferred; use as subset-only candidate after artifact/adapter path exists |
| Step 6 | GenRewrite | readiness-only complete | first-subset and PG-native-9 audit scope | readiness audit complete; input/cost-readiness scaffold complete; first-subset `4`, maybe_later `5`; likely_cost_risk `medium: 6`, `high: 3`; no model/correction/verifier/executor-feedback attempted | frontier appendix / subset-only candidate, control stack missing, not execution-ready | execution deferred until correction-loop, verifier, retry, cost, and prompt/rule policies are frozen |
| Step 7 | R-Bot / LLM-R2 | readiness-only complete | first-subset and PG-native-9 audit scope | readiness audit complete; retrieval-readiness scaffold complete; first-subset `4`, maybe_later `5`; likely_retrieval_cost_risk `medium: 6`, `high: 3`; no execution/model/retrieval/demo-selection/rerank attempted | retrieval-dependent appendix / subset-only candidate, retrieval/demo/rule-pool stack missing, not execution-ready | execution deferred until retrieval corpus, demo/rule pool, contamination policy, rerank policy, and fair comparison contract exist |
| Step 8 | SlabCity | readiness-only complete | frontier exception audit scope | readiness audit complete; conclusion: defer; frontier exception only; no local runner / adapter / CLI / API wrapper; no synthesis engine; no verifier / solver integration; no reproducible service/runtime contract | frontier exception only, not execution-ready | keep deferred until runnable local adapter or reproducible service/runtime contract exists |
| Step 9 | SQLSolver / VeriEQL support | readiness-only complete | support-first and pg-native-9 audit scope | readiness audit complete; support-readiness scaffold complete; `support_candidate: 1`, `maybe: 6`, `exclude: 2`; no solver/database/model execution attempted | support-only / subset-only verifier, not main leaderboard, not execution-ready | use only as bounded support-analysis candidate after solver wrapper, subset policy, timeout policy, and schema/constraint extraction exist |

## 3. Completed Smoke Milestones

- Step 1 Native / Human positive / Hard negative guard:
  - PG-only 9-case execution-layer smoke complete.
- Step 2a SQLGlot optimize same-dialect:
  - PG-only 9-case execution-layer smoke complete.
- Step 2b SQLGlot transpile:
  - PORT 3-case preflight complete.
  - PG execution 2 / 3 complete.
  - `PORT_0012` failure captured.
- Step 3 Calcite HEP rules:
  - readiness audit complete.
  - parse-readiness scaffold complete.
  - no actual Calcite parse or rewrite attempted.
- Step 4a Direct LLM rewrite:
  - 9-case execution-layer smoke complete.
  - model call 9 / 9.
  - extraction 9 / 9.
  - PG execution 9 / 9.
  - `total_token_usage=5089`.
- Step 4b LLM translate:
  - prompt dry-run 3 / 3.
  - clean PORT canary subset 2 / 2 passed:
    - `PORT_0004`
    - `PORT_0022`
  - `PORT_0012` held for failure-analysis comparison.
  - `total_token_usage=912`.
- Step 5 LearnedRewrite:
  - readiness audit complete.
  - input-readiness scaffold complete.
  - command added:
    - `python -m scripts.cli baseline-smoke-learnedrewrite-readiness`
  - first-subset candidate count: `4`
  - PG-native-9 result:
    - `first_subset_candidate: 4`
    - `maybe_later: 5`
  - first-subset candidate cases:
    - `PERF_0006`
    - `PERF_0008`
    - `PERF_0033`
    - `PERF_0054`
  - `maybe_later` cases:
    - `PERF_0013`
    - `PERF_0017`
    - `PERF_0024`
    - `CONS_0007`
    - `CONS_0012`
  - `execution_attempted_count: 0`
  - `inference_attempted_count: 0`
  - `rewrite_attempted_count: 0`
  - artifact stack missing.
  - not runnable as a baseline yet.
- Step 6 GenRewrite:
  - readiness audit complete.
  - input/cost-readiness scaffold complete.
  - command added:
    - `python -m scripts.cli baseline-smoke-genrewrite-readiness`
  - first-subset candidate count: `4`
  - PG-native-9 result:
    - `first_subset_candidate: 4`
    - `maybe_later: 5`
  - likely_cost_risk:
    - `medium: 6`
    - `high: 3`
  - first-subset candidate cases:
    - `PERF_0006`
    - `PERF_0008`
    - `PERF_0033`
    - `PERF_0054`
  - `maybe_later` cases:
    - `PERF_0013`
    - `PERF_0017`
    - `PERF_0024`
    - `CONS_0007`
    - `CONS_0012`
  - `execution_attempted_count: 0`
  - `model_call_attempted_count: 0`
  - `correction_loop_attempted_count: 0`
  - `verifier_loop_attempted_count: 0`
  - `executor_feedback_attempted_count: 0`
  - control stack missing.
  - not runnable as a baseline yet.
- Step 7 R-Bot / LLM-R2:
  - readiness audit complete.
  - retrieval-readiness scaffold complete.
  - command added:
    - `python -m scripts.cli baseline-smoke-rbot-llmr2-readiness`
  - first-subset candidate count: `4`
  - PG-native-9 result:
    - `first_subset_candidate: 4`
    - `maybe_later: 5`
  - likely_retrieval_cost_risk:
    - `medium: 6`
    - `high: 3`
  - first-subset candidate cases:
    - `PERF_0006`
    - `PERF_0008`
    - `PERF_0033`
    - `PERF_0054`
  - `maybe_later` cases:
    - `PERF_0013`
    - `PERF_0017`
    - `PERF_0024`
    - `CONS_0007`
    - `CONS_0012`
  - `execution_attempted_count: 0`
  - `model_call_attempted_count: 0`
  - `retrieval_attempted_count: 0`
  - `demo_selection_attempted_count: 0`
  - `rerank_attempted_count: 0`
  - retrieval/demo/rule-pool stack missing.
  - not runnable as a baseline yet.
- Step 8 SlabCity:
  - readiness audit complete.
  - tracked audit note exists:
    - `docs/_scratch/SLABCITY_READINESS_AUDIT_v0.md`
  - recommendation: defer.
  - no execution attempted.
  - no synthesis engine available.
  - no verifier / solver integration available.
  - no local adapter / service contract available.
  - not runnable as a baseline yet.
- Step 9 SQLSolver / VeriEQL support:
  - readiness audit complete.
  - tracked audit note exists:
    - `docs/_scratch/SQLSOLVER_VERIEQL_SUPPORT_READINESS_AUDIT_v0.md`
  - support-readiness scaffold complete.
  - command added:
    - `python -m scripts.cli baseline-smoke-sqlsolver-verieql-readiness`
  - `support_candidate: 1`
  - `maybe: 6`
  - `exclude_from_first_support_scaffold: 2`
  - support_candidate case:
    - `CONS_0007`
  - maybe cases:
    - `PERF_0006`
    - `PERF_0008`
    - `PERF_0024`
    - `PERF_0033`
    - `PERF_0054`
    - `CONS_0012`
  - excluded cases:
    - `PERF_0013`
    - `PERF_0017`
  - `equivalence_execution_attempted_count: 0`
  - `support_analysis_attempted_count: 0`
  - no solver/database/model execution attempted.
  - not runnable as support verifier yet.

## 4. Claim Boundaries

- No correctness scoring has been made.
- No semantic equivalence scoring has been made.
- No speedup scoring has been made.
- No leaderboard claim has been made.
- No common-core admission has been made.
- No registry writeback has been made.
- No formal review status has changed.
- Generated reports under `reports/baseline_smoke/` remain execution artifacts, not formal protocol.

## 5. Remaining Blockers

- `PORT_0012` remains the open SQLGlot transpile execution-layer failure case.
- Calcite HEP rules remain subset-only.
- Calcite adapter/build path is still missing.
- No actual Calcite parse or rewrite has been attempted.
- LLM translate has only a clean 2-case PORT subset passed so far.
- `PORT_0012` remains held out of the clean LLM translate subset pending failure-analysis comparison.
- LearnedRewrite readiness audit and input-readiness scaffold are complete, but execution is blocked by missing adapter/checkpoints/inference path/dependency file/artifact path.
- GenRewrite readiness audit and input/cost-readiness scaffold are complete, but execution is blocked by missing correction-loop implementation, verifier/executor-feedback loop, n-best/rerank path, retry/correction-round budget, frozen prompt/rule library, and cost policy.
- R-Bot / LLM-R2 readiness audit and retrieval-readiness scaffold are complete, but execution is blocked by missing retrieval corpus/index, demo pool, rule pool, rerank policy, embedding/vector path, demo/retrieval count policy, contamination policy, and fair comparison contract.
- SlabCity readiness audit is complete, but it remains deferred because there is no local runner, adapter, CLI/API wrapper, synthesis engine, verifier/solver integration, or reproducible service/runtime contract.
- SQLSolver / VeriEQL readiness audit and support-readiness scaffold are complete, but execution is blocked by missing SQLSolver/VeriEQL runners, SMT/Z3/CVC5 wrapper, symbolic equivalence checker, schema/constraint extraction path, timeout/subset policy, and local reproducible solver artifact path.

## 6. Remaining Baseline Backlog

- Step 5 LearnedRewrite:
  - readiness audit complete
  - input-readiness scaffold complete
  - execution deferred
  - subset-only candidate
  - future work requires artifact/adapter path
- Step 6 GenRewrite:
  - readiness audit complete
  - input/cost-readiness scaffold complete
  - execution deferred
  - frontier appendix / subset-only candidate
  - future work requires correction-loop, verifier, retry, cost, and prompt/rule policies
- Step 7 R-Bot / LLM-R2:
  - readiness audit complete
  - retrieval-readiness scaffold complete
  - execution deferred
  - retrieval-dependent appendix / subset-only candidate
  - future work requires retrieval corpus, demo/rule pool, contamination policy, rerank policy, and fair comparison contract
- Step 8 SlabCity:
  - readiness audit complete
  - deferred
  - frontier exception only
  - future work requires runnable local adapter or reproducible service/runtime contract
- Step 9 SQLSolver / VeriEQL support:
  - readiness audit complete
  - support-readiness scaffold complete
  - support-only / subset-only verifier
  - execution deferred
  - future work requires solver wrappers, subset policy, timeout policy, schema/constraint extraction, and reproducible artifact path

## 7. Recommended Next Action

- Create a final baseline route readiness closeout packet.

## 8. Non-Goals

- No registry writeback.
- No admission decision.
- No leaderboard claim.
- No correctness scoring.
- No speedup scoring.
