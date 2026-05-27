# BASELINE_SMOKE_READINESS_ROLLUP_v0

## 1. Status

This is a tracked scratch readiness rollup for the current baseline smoke route.

This document records the current execution-layer smoke milestone because most machine-generated artifacts live under `reports/baseline_smoke/` and may be git-ignored.

This document is not a formal benchmark protocol artifact and does not change registry, review, or admission state.

## 2. Scope

Covered case sets:

- PG-native 9-case PERF/CONS smoke set:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0013`
  - `PERF_0017`
  - `PERF_0024`
  - `PERF_0033`
  - `PERF_0054`
  - `CONS_0007`
  - `CONS_0012`
- PORT transpile smoke set:
  - `PORT_0004`
  - `PORT_0012`
  - `PORT_0022`

Covered route steps:

- Step 1: P0 controls
- Step 2a: SQLGlot optimize same-dialect
- Step 2b: SQLGlot transpile
- Step 3: Calcite HEP rules
- Step 4a: Direct LLM rewrite
- Step 4b: LLM translate

## 3. Current baseline route progress table

| route step | baseline / method | current smoke state | case scope | result | claim boundary | next action |
|---|---|---|---|---|---|---|
| Step 1 | `NATIVE_IDENTITY` | PG-only execution-layer smoke complete | PG-native 9-case PERF/CONS set | 9 / 9 success | execution-layer smoke only | retain as control route |
| Step 1 | `HUMAN_REFERENCE_POSITIVE` | PG-only execution-layer smoke complete | PG-native 9-case PERF/CONS set | 9 / 9 success | execution-layer smoke only | retain as control route |
| Step 1 | `HARD_NEGATIVE_GUARD` | PG-only execution-layer smoke complete | PG-native 9-case PERF/CONS set | 9 / 9 success | execution-layer smoke only | retain as control route |
| Step 1 | PG control summary | rollup complete | PG-native 9-case PERF/CONS set | `ok=true` | not correctness or speedup scoring | use as baseline control reference |
| Step 2a | `SQLGLOT_OPT_SAME_DIALECT` preflight | complete | PG-native 9-case PERF/CONS set | 9 / 9 parse + generation success | preflight only | keep route open |
| Step 2a | `SQLGLOT_OPT_SAME_DIALECT` PG execution | complete | PG-native 9-case PERF/CONS set | 9 / 9 success | execution-layer only | keep route open |
| Step 2a | SQLGlot-vs-controls summary | rollup complete | PG-native 9-case PERF/CONS set | `ok=true` | row-count observations only, not semantic equivalence or speedup | keep route open |
| Step 2b | `SQLGLOT_TRANSPILE` preflight | complete | `PORT_0004`, `PORT_0012`, `PORT_0022` | 3 / 3 parse + transpile success | preflight only | keep route open |
| Step 2b | `SQLGLOT_TRANSPILE` PG execution | partial | `PORT_0004`, `PORT_0012`, `PORT_0022` | 2 / 3 success | execution-layer only, not translation correctness | inspect `PORT_0012` failure path |
| Step 3 | Calcite HEP readiness audit | complete | first Calcite subset audit scope | tracked audit complete | readiness audit only, not parse or rewrite evidence | retain subset-only interpretation |
| Step 3 | Calcite HEP parse-readiness scaffold | complete | first-subset and PG-native 9-case audit scope | no actual parse/rewrite attempted; first-subset `6` candidate, PG-native-9 `6` first_subset_candidate + `3` maybe_later | readiness scaffold only, not actual Calcite parse/rewrite | preserve as adapter-missing preflight layer |
| Step 4a | `LLM_DIRECT_REWRITE_STRONG` prompt dry-run | complete | PG-native 9-case PERF/CONS set | 9 / 9 ready | prompt-package dry-run only | keep route open |
| Step 4a | `LLM_DIRECT_REWRITE_STRONG` model call | complete | PG-native 9-case PERF/CONS set | 9 / 9 success | model-call canary only | keep route open |
| Step 4a | `LLM_DIRECT_REWRITE_STRONG` SQL extraction | complete | PG-native 9-case PERF/CONS set | 9 / 9 extracted | extraction-layer only | keep route open |
| Step 4a | `LLM_DIRECT_REWRITE_STRONG` PG execution | complete | PG-native 9-case PERF/CONS set | 9 / 9 success | execution-layer only | keep route open |
| Step 4a | LLM 9-case rollup | complete | PG-native 9-case PERF/CONS set | `ok=true`, `total_token_usage=5089` | execution-layer rollup only, not correctness or speedup scoring | preserve as current LLM smoke milestone |
| Step 4b | `LLM_DIRECT_TRANSLATE` prompt dry-run | complete | `PORT_0004`, `PORT_0012`, `PORT_0022` | 3 / 3 ready | prompt-package dry-run only | keep route open |
| Step 4b | `LLM_DIRECT_TRANSLATE` `PORT_0004` canary | complete | clean PORT translate canary subset | model call success, extraction extracted, PG execution success | execution-layer only, not translation correctness | preserve as clean subset evidence |
| Step 4b | `LLM_DIRECT_TRANSLATE` `PORT_0022` canary | complete | clean PORT translate canary subset | model call success, extraction extracted, PG execution success | execution-layer only, not translation correctness | preserve as clean subset evidence |
| Step 4b | `LLM_DIRECT_TRANSLATE` 2-case rollup | complete | `PORT_0004`, `PORT_0022` | clean PORT canary subset 2 / 2 passed; `ok=true`, `total_token_usage=912` | execution-layer rollup only, not translation correctness or speedup scoring | hold `PORT_0012` for failure-analysis comparison |

## 4. Detailed facts by route step

### Step 1 P0 controls

- PG-only 9-case execution-layer smoke completed for the PG-native PERF/CONS set.
- `NATIVE_IDENTITY`: 9 / 9 success.
- `HUMAN_REFERENCE_POSITIVE`: 9 / 9 success.
- `HARD_NEGATIVE_GUARD`: 9 / 9 success.
- PG control summary: `ok=true`.

Interpretation boundary:

- This establishes execution-layer smoke readiness for the control route on the current 9-case PG-native set.
- This does not by itself establish correctness scoring, performance scoring, or admission readiness.

### Step 2a SQLGlot optimize same-dialect

- Preflight completed on the PG-native 9-case PERF/CONS set.
- Parse success: 9 / 9.
- Generation success: 9 / 9.
- PG execution completed: 9 / 9 success.
- SQLGlot-vs-controls summary: `ok=true`.
- SQLGlot row-count matched source on 9 / 9 as a smoke observation only.

Interpretation boundary:

- The row-count match is recorded only as an execution-layer smoke observation.
- It is not a semantic equivalence claim.
- It is not a speedup claim.

### Step 2b SQLGlot transpile

- PORT preflight completed on:
  - `PORT_0004`
  - `PORT_0012`
  - `PORT_0022`
- Parse + transpile success: 3 / 3.
- PORT PG execution: 2 / 3 success.
- Failed case: `PORT_0012`.
- Failure category: `InvalidDatetimeFormat`.
- Failure note: transpiled SQL treated quoted identifier literal `'birthday'` as timestamp input.

Interpretation boundary:

- This is an execution-layer summary only.
- This is not a translation correctness claim.
- This is not a portability correctness claim.

### Step 4a Direct LLM rewrite

- Prompt dry-run: 9 / 9 ready.
- Model call: 9 / 9 success.
- SQL extraction: 9 / 9 extracted.
- PG execution: 9 / 9 success.
- 9-case rollup: `ok=true`.
- Total token usage: `5089`.
- Provider mode used in smoke: OpenAI-compatible third-party endpoint.
- Model label used in smoke: `gpt-5.2`.

Interpretation boundary:

- This is an execution-layer rollup only.
- It is not correctness scoring.
- It is not speedup scoring.
- It is not leaderboard readiness.

### Step 3 Calcite HEP rules

- Readiness audit complete.
- Tracked audit note exists:
  - `docs/_scratch/CALCITE_HEP_READINESS_AUDIT_v0.md`
- No-execution parse-readiness scaffold complete.
- Command added:
  - `python -m scripts.cli baseline-smoke-calcite-readiness`
- First-subset candidate count: `6`.
- PG-native-9 candidate set result:
  - `first_subset_candidate: 6`
  - `maybe_later: 3`
- `maybe_later` cases:
  - `PERF_0013`
  - `PERF_0017`
  - `PERF_0024`
- `parse_attempted_count: 0`
- `rewrite_attempted_count: 0`

Interpretation boundary:

- Calcite remains subset-only.
- Adapter/build path remains missing.
- No actual Calcite parse or rewrite was attempted.
- No Java build was run.
- Calcite is not execution-ready.
- Calcite is not yet a full common-core baseline candidate.

### Step 4b LLM translate

- Prompt dry-run completed on:
  - `PORT_0004`
  - `PORT_0012`
  - `PORT_0022`
- Prompt-package readiness: 3 / 3.
- Source dialects recorded:
  - `PORT_0004`: `mysql`
  - `PORT_0012`: `postgres`
  - `PORT_0022`: `mysql`
- `PORT_0004` end-to-end canary passed:
  - model call: success
  - SQL extraction: extracted
  - PG execution: success
  - row count observation: `1`
  - token usage total: `463`
- `PORT_0022` end-to-end canary passed:
  - model call: success
  - SQL extraction: extracted
  - PG execution: success
  - row count observation: `1`
  - token usage total: `449`
- 2-case LLM translate rollup:
  - command added:
    - `python -m scripts.cli baseline-smoke-llm-translate-rollup`
  - report:
    - `reports/baseline_smoke/llm_direct_translate_2case_rollup_v0.json`
  - `ok=true`
  - `case_count=2`
  - `ok_count=2`
  - `call_and_pg_execution_succeeded_count=2`
  - `pg_execution_success_count=2`
  - `extracted_sql_count=2`
  - `total_token_usage=912`
  - `counts_by_source_dialect={"mysql": 2}`
  - `counts_by_target_dialect={"postgres": 2}`
- `PORT_0012` is held for separate failure-analysis comparison.
- Reason:
  - SQLGlot transpile already exposed an execution-layer failure on `PORT_0012`.
  - It should not be mixed into the clean LLM translate canary subset yet.

Interpretation boundary:

- This is not translation correctness scoring.
- This is not semantic equivalence scoring.
- This is not speedup scoring.
- This is not leaderboard readiness.

## 5. What this does not claim

- No final correctness scoring has been made.
- No speedup scoring has been made.
- No leaderboard claim has been made.
- No common-core admission has been made.
- No registry writeback has been made.
- No formal review update has been made.
- No extended full-run result has been established.

## 6. Known blockers / caveats

- SQLGlot transpile still has one execution-layer failure on `PORT_0012`.
- `PORT_0012` failure category is `InvalidDatetimeFormat`.
- The failure note is that transpiled SQL treated quoted identifier literal `'birthday'` as timestamp input.
- Calcite adapter/build path is missing.
- Calcite remains subset-only and no actual parse/rewrite was attempted.
- LLM pricing snapshot is not frozen.
- The LLM smoke used an OpenAI-compatible third-party endpoint.
- LLM translate currently has only the clean PORT 2-case subset passed.
- `PORT_0012` remains held for failure-analysis comparison on the LLM translate route.
- Generated reports live under `reports/baseline_smoke/` and may be git-ignored.
- PORT is not part of the PG-native same-engine smoke route.
- No MySQL baseline smoke has been run in this readiness rollup.
- No Spark baseline smoke has been run in this readiness rollup.

## 7. Current common-core planning state

- Original preliminary common-core packet: `29`
- Health-gated keep-for-review: `27`
- Human-screened possible additions: `8`
- Next possible human-review slate: `35`
- Pending / not clean: `PERF_0038`
- Extended-oriented: `PERF_0076`
- Formal admission: none
- Registry writeback: none

## 8. Recommended next action

- Create a tracked baseline route status packet / roadmap summarizing Step 1 through Step 4b and the remaining Step 5-9 backlog.
