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
| Step 5 | LearnedRewrite | not started | future baseline family | no readiness audit yet | unknown readiness | next readiness audit candidate |
| Step 6 | GenRewrite | not started | future baseline family | no readiness audit yet | later-stage candidate; correction-loop and cost questions unresolved | defer until post-audit sequencing |
| Step 7 | R-Bot / LLM-R2 | not started | future baseline family | no readiness audit yet | retrieval/demo/rule-pool assumptions untested | defer until audit scope is defined |
| Step 8 | SlabCity | not started | frontier exception line | no readiness audit yet | frontier exception, not near-term baseline route | defer |
| Step 9 | SQLSolver / VeriEQL support | not started | support / analysis line | no readiness audit yet | support analysis, not main leaderboard route | defer behind main-route audits |

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
- LearnedRewrite has not received a readiness audit.
- GenRewrite still requires correction-loop framing and cost audit before route entry.
- R-Bot / LLM-R2 still requires retrieval/demo/rule-pool readiness audit.
- SlabCity remains a frontier exception line, not a near-term baseline route.
- SQLSolver / VeriEQL support remains a support-analysis line, not a main leaderboard route.

## 6. Remaining Baseline Backlog

- Step 5 LearnedRewrite:
  - not started
  - recommended next readiness audit
- Step 6 GenRewrite:
  - not started
  - later
  - requires correction-loop and cost audit
- Step 7 R-Bot / LLM-R2:
  - not started
  - later
  - requires retrieval/demo/rule pool audit
- Step 8 SlabCity:
  - not started
  - frontier exception
- Step 9 SQLSolver / VeriEQL support:
  - not started
  - support analysis, not main leaderboard

## 7. Recommended Next Action

- Run a LearnedRewrite readiness audit.

## 8. Non-Goals

- No registry writeback.
- No admission decision.
- No leaderboard claim.
- No correctness scoring.
- No speedup scoring.
