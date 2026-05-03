# BASELINE_ROUTE_READINESS_CLOSEOUT_v0

## 1. Status

This is the final tracked scratch closeout packet for the baseline route readiness sweep.

This document consolidates the completed Step 1 through Step 9 baseline route readiness sweep into one tracked scratch summary.

This document is not:

- a registry writeback
- a common-core admission decision
- a formal review update
- a leaderboard result
- correctness scoring
- speedup scoring
- semantic equivalence scoring
- release protocol

## 2. Executive Summary

The current sweep establishes three PG-native execution-layer smoke routes as completed:

- Step 1 P0 controls
- Step 2a SQLGlot same-dialect
- Step 4a Direct LLM rewrite

The current sweep also establishes two runnable but narrower execution-layer lines:

- Step 2b SQLGlot transpile completed first PORT smoke with one captured `PORT_0012` failure
- Step 4b LLM translate completed a clean PORT 2-case canary subset on `PORT_0004` and `PORT_0022`

The remaining routes are not runnable leaderboard baselines in the current repository state:

- Step 3 Calcite HEP is readiness-only and subset-only
- Step 5 LearnedRewrite is readiness-only and subset-only
- Step 6 GenRewrite is readiness-only and frontier appendix / subset-only
- Step 7 R-Bot / LLM-R2 is readiness-only and retrieval-dependent
- Step 8 SlabCity is deferred
- Step 9 SQLSolver / VeriEQL support is support-only and subset-only

No correctness, speedup, leaderboard, admission, or semantic equivalence claim has been made in this closeout.

## 3. Route Status Table

| step | route / baseline | current state | runnable status | result | claim boundary | next posture |
|---|---|---|---|---|---|---|
| Step 1 | Native / Human positive / Hard negative guard | complete | runnable | PG-only 9-case execution-layer smoke complete; Native 9/9; Human positive 9/9; Hard negative 9/9; PG control summary `ok=true` | execution-layer smoke only | retain as control route |
| Step 2a | SQLGlot optimize same-dialect | complete | runnable | PG-only 9-case preflight 9/9; PG execution 9/9; SQLGlot-vs-controls summary `ok=true` | row-count is smoke observation only, not semantic equivalence or speedup | retain as active comparison route |
| Step 2b | SQLGlot transpile | partial | runnable partial | PORT 3-case preflight 3/3; PG execution 2/3; `PORT_0012` failure captured with `InvalidDatetimeFormat` | translation-route execution-layer smoke only, not translation correctness | hold `PORT_0012` for failure analysis |
| Step 3 | Calcite HEP rules | readiness-only complete | not runnable | readiness audit complete; parse-readiness scaffold complete; first-subset `6`; maybe_later `3`; no actual parse/rewrite attempted | readiness-only, subset-only, not execution evidence | execution deferred until adapter/build path exists |
| Step 4a | Direct LLM rewrite | complete | runnable | prompt dry-run 9/9; model call 9/9; extraction 9/9; PG execution 9/9; rollup `ok=true`; `total_token_usage=5089` | execution-layer smoke only, not correctness or speedup | retain as current LLM rewrite milestone |
| Step 4b | LLM translate | clean subset complete | runnable clean subset | prompt dry-run 3/3; clean PORT subset 2/2 passed on `PORT_0004` and `PORT_0022`; rollup `ok=true`; `total_token_usage=912` | not translation correctness | keep `PORT_0012` as holdout failure-analysis path |
| Step 5 | LearnedRewrite | readiness-only complete | not runnable | readiness audit complete; input-readiness scaffold complete; first-subset `4`; maybe_later `5`; no inference/rewrite/execution attempted | subset-only candidate only | execution deferred until artifact/adapter path exists |
| Step 6 | GenRewrite | readiness-only complete | not runnable | readiness audit complete; input/cost-readiness scaffold complete; first_subset_candidate `4`; maybe_later `5`; likely_cost_risk `medium=6`, `high=3`; no model/correction/verifier/executor-feedback attempted | frontier appendix / subset-only only | execution deferred until control stack and policy layer exist |
| Step 7 | R-Bot / LLM-R2 | readiness-only complete | not runnable | readiness audit complete; retrieval-readiness scaffold complete; first_subset_candidate `4`; maybe_later `5`; likely_retrieval_cost_risk `medium=6`, `high=3`; no execution/model/retrieval/demo-selection/rerank attempted | retrieval-dependent appendix / subset-only only | execution deferred until retrieval/demo/rule-pool stack exists |
| Step 8 | SlabCity | audit complete; deferred | not runnable | readiness audit complete; frontier exception only; no runner/adapter/CLI/API wrapper; no synthesis engine; no verifier/solver integration | deferred frontier exception | keep deferred until runnable local adapter or reproducible service contract exists |
| Step 9 | SQLSolver / VeriEQL support | readiness-only complete | not runnable | readiness audit complete; support-readiness scaffold complete; support_candidate `1`; maybe `6`; exclude `2`; no solver/database/model execution attempted | support-only bounded verifier line, not leaderboard or speedup | use only as bounded support-analysis candidate after solver/support path exists |

## 4. Runnable / Execution-Smoke Routes

### Step 1 P0 controls

- PG-only 9-case execution-layer smoke is complete.
- `NATIVE_IDENTITY`: 9 / 9 success.
- `HUMAN_REFERENCE_POSITIVE`: 9 / 9 success.
- `HARD_NEGATIVE_GUARD`: 9 / 9 success.
- PG control summary: `ok=true`.

Interpretation:

- this is a completed execution-layer smoke control route
- this is not correctness scoring or speedup scoring

### Step 2a SQLGlot same-dialect

- PG-only 9-case preflight completed: 9 / 9.
- PG-only 9-case execution completed: 9 / 9.
- SQLGlot-vs-controls summary: `ok=true`.
- row-count match is recorded only as a smoke observation.

Interpretation:

- this is a completed execution-layer smoke comparison route
- this is not a semantic equivalence claim
- this is not a speedup claim

### Step 2b SQLGlot transpile

- PORT 3-case preflight completed: 3 / 3.
- PG execution completed: 2 / 3.
- `PORT_0012` failure was captured.
- failure category: `InvalidDatetimeFormat`.

Interpretation:

- this is a partial execution-layer smoke route
- this is not a translation correctness claim
- `PORT_0012` remains a bounded failure-analysis path

### Step 4a Direct LLM rewrite

- prompt dry-run: 9 / 9 ready
- model call: 9 / 9 success
- SQL extraction: 9 / 9 extracted
- PG execution: 9 / 9 success
- rollup: `ok=true`
- `total_token_usage=5089`

Interpretation:

- this is a completed execution-layer smoke LLM rewrite route
- this is not correctness scoring
- this is not speedup scoring

### Step 4b LLM translate

- prompt dry-run completed: 3 / 3
- clean PORT canary subset passed: 2 / 2
- clean passed cases:
  - `PORT_0004`
  - `PORT_0022`
- 2-case rollup: `ok=true`
- `total_token_usage=912`
- `PORT_0012` remains held for failure-analysis comparison

Interpretation:

- this is a clean subset execution-layer smoke route
- this is not a translation correctness claim
- the clean 2-case subset should not be conflated with full PORT closure

## 5. Readiness-Only / Deferred / Support Routes

### Step 3 Calcite HEP

- readiness audit complete
- tracked audit note:
  - `docs/_scratch/CALCITE_HEP_READINESS_AUDIT_v0.md`
- parse-readiness scaffold complete
- command:
  - `python -m scripts.cli baseline-smoke-calcite-readiness`
- first-subset candidate count: `6`
- maybe_later count: `3`
- no actual Calcite parse or rewrite attempted
- role: subset-only readiness line
- blocker summary:
  - adapter missing
  - build path missing
  - no actual parse/rewrite path

### Step 5 LearnedRewrite

- readiness audit complete
- tracked audit note:
  - `docs/_scratch/LEARNED_REWRITE_READINESS_AUDIT_v0.md`
- input-readiness scaffold complete
- command:
  - `python -m scripts.cli baseline-smoke-learnedrewrite-readiness`
- first-subset candidate count: `4`
- maybe_later count: `5`
- no inference / rewrite / execution attempted
- role: subset-only candidate
- blocker summary:
  - artifact stack missing
  - adapter missing
  - no inference path

### Step 6 GenRewrite

- readiness audit complete
- tracked audit note:
  - `docs/_scratch/GENREWRITE_READINESS_AUDIT_v0.md`
- input/cost-readiness scaffold complete
- command:
  - `python -m scripts.cli baseline-smoke-genrewrite-readiness`
- first_subset_candidate: `4`
- maybe_later: `5`
- likely_cost_risk:
  - `medium=6`
  - `high=3`
- no model / correction / verifier / executor-feedback attempted
- role: frontier appendix / subset-only candidate
- blocker summary:
  - correction-loop stack missing
  - verifier/executor-feedback path missing
  - prompt/rule and retry/cost policy layer missing

### Step 7 R-Bot / LLM-R2

- readiness audit complete
- tracked audit note:
  - `docs/_scratch/RBOT_LLMR2_READINESS_AUDIT_v0.md`
- retrieval-readiness scaffold complete
- command:
  - `python -m scripts.cli baseline-smoke-rbot-llmr2-readiness`
- first_subset_candidate: `4`
- maybe_later: `5`
- likely_retrieval_cost_risk:
  - `medium=6`
  - `high=3`
- no execution / model / retrieval / demo-selection / rerank attempted
- role: retrieval-dependent appendix / subset-only candidate
- blocker summary:
  - retrieval corpus/index missing
  - demo/rule pool missing
  - contamination/fair-comparison policy missing

### Step 8 SlabCity

- readiness audit complete
- tracked audit note:
  - `docs/_scratch/SLABCITY_READINESS_AUDIT_v0.md`
- conclusion: defer
- no execution attempted
- role: deferred frontier exception only
- blocker summary:
  - no local runner
  - no adapter
  - no CLI/API wrapper
  - no synthesis engine
  - no verifier / solver integration
  - no reproducible service/runtime contract

### Step 9 SQLSolver / VeriEQL support

- readiness audit complete
- tracked audit note:
  - `docs/_scratch/SQLSOLVER_VERIEQL_SUPPORT_READINESS_AUDIT_v0.md`
- support-readiness scaffold complete
- command:
  - `python -m scripts.cli baseline-smoke-sqlsolver-verieql-readiness`
- support_candidate: `1`
- maybe: `6`
- exclude_from_first_support_scaffold: `2`
- no solver / database / model execution attempted
- role: support-only / subset-only verifier
- blocker summary:
  - no SQLSolver runner
  - no VeriEQL runner
  - no SMT / Z3 / CVC5 wrapper
  - no symbolic equivalence checker
  - no schema / constraint extraction path
  - no timeout / subset policy implementation
  - no local reproducible solver artifact path

## 6. Current Runnable vs Non-Runnable Classification

| category | routes |
|---|---|
| Runnable execution-layer smoke complete | Step 1 P0 controls; Step 2a SQLGlot same-dialect; Step 4a Direct LLM rewrite |
| Runnable partial / clean subset | Step 2b SQLGlot transpile; Step 4b LLM translate |
| Readiness scaffold only | Step 3 Calcite HEP; Step 5 LearnedRewrite; Step 6 GenRewrite; Step 7 R-Bot / LLM-R2; Step 9 SQLSolver / VeriEQL support |
| Deferred | Step 8 SlabCity |

## 7. Remaining Blockers

- Step 2b / Step 4b:
  - `PORT_0012` remains the active failure-analysis path
- Step 3 Calcite HEP:
  - Calcite adapter/build path is missing
- Step 5 LearnedRewrite:
  - LearnedRewrite artifact stack and adapter path are missing
- Step 6 GenRewrite:
  - correction-loop / verifier / cost-control stack is missing
- Step 7 R-Bot / LLM-R2:
  - retrieval / demo / rule-pool stack is missing
- Step 8 SlabCity:
  - local adapter or reproducible service/runtime contract is missing
- Step 9 SQLSolver / VeriEQL support:
  - solver wrapper / subset policy / timeout policy / schema-constraint path is missing

## 8. Claim Boundaries

- no correctness scoring
- no semantic equivalence scoring
- no speedup scoring
- no leaderboard claim
- no common-core admission
- no registry writeback
- no formal review update
- reports under `reports/baseline_smoke/` are execution artifacts, not formal protocol

## 9. Recommended Next Engineering Actions

1. Primary next action:
   - Create a `PORT_0012` failure-analysis packet comparing the SQLGlot transpile failure path and the LLM translate holdout path.
2. Secondary:
   - Decide whether to promote any smoke results into a formal baseline protocol draft.
3. Secondary:
   - Decide whether to keep readiness scaffolds as permanent CLI commands or move some to docs-only.
4. Secondary:
   - Defer execution of Step 3 / Step 5 / Step 6 / Step 7 / Step 8 / Step 9 until the missing adapters, artifacts, or contracts exist.

## 10. Non-Goals

- no registry writeback
- no admission decision
- no formal review update
- no leaderboard
- no correctness claim
- no speedup claim

## 11. Verification / Non-Modification Note

- only this closeout document was created
- no database workloads were run
- no LLM calls were made
- no dependency installs or downloads were performed
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
