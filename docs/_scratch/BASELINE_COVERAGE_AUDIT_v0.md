# BASELINE_COVERAGE_AUDIT_v0

## Status

This is a tracked baseline coverage audit for the current expanded experiment state.

It is a coverage/status audit only. It is not a new experiment, not a registry writeback, and not a leaderboard artifact.

## Executive Summary

The current baseline stack splits into five practical groups:

- implemented control routes:
  - Native / Original SQL
  - Human positive rewrite
  - Hard negative guard
- implemented SQLGlot routes:
  - SQLGlot optimize
  - SQLGlot no-opt / same-dialect transpile
- implemented LLM routes:
  - Direct LLM rewrite
- partially implemented PORT routes:
  - SQLGlot Transpile
  - LLM Translate
- readiness-only baselines:
  - Calcite HEP
  - LearnedRewrite
  - GenRewrite
  - R-Bot
  - LLM-R2
- blocked / not-integrated support lines:
  - SlabCity
  - SQLSolver
  - VeriEQL

Current status counts:

- `implemented`: `6`
- `partially_implemented`: `2`
- `preflight_only`: `5`
- `not_integrated`: `2`
- `blocked`: `1`

## Coverage Table

| baseline family | current status | current denominator | metrics available | main blockers / caveats |
|---|---|---|---|---|
| Native / Original SQL | `implemented` | expanded common-core PG `46` | execution, row-count, control reference | control only |
| Human positive rewrite | `implemented` | expanded common-core PG `46`; speedup on PERF `7 + 19 + 11 + 4` | execution, checker-backed consistency, speedup | control only |
| Hard negative guard | `implemented` | expanded common-core PG `46` | execution, negative rejection | guard only |
| SQLGlot optimize | `implemented` | common-core PG `43` | execution, seed checker, seed speedup, failure categories | persistent `OptimizeError` boundary on later PERF waves |
| SQLGlot no-opt / same-dialect transpile | `implemented` | expanded PERF PG `34` | execution, checker-backed consistency, speedup | separate baseline candidate only |
| Direct LLM rewrite | `implemented_on_expanded_perf_checker_backed` | seed common-core PG `9`; expanded PERF PG `34` | call/extract/PG execution, checker-backed consistency on expanded PERF, seed speedup, token usage | remaining missing piece: expanded PERF speedup |
| SQLGlot Transpile | `partially_implemented` | PORT PG-side `6` | PG execution, policy/reference consistency, failure analysis | PG-side failures on `PORT_0012`, `PORT_0013` |
| LLM Translate | `partially_implemented` | PORT PG-side `6` | call, extraction, PG execution, policy/reference consistency, token usage | PG-only bounded slice, not cross-engine closure |
| Calcite HEP | `preflight_only` | readiness subsets | readiness audit, subset recommendations | no runnable adapter/build path |
| LearnedRewrite | `preflight_only` | readiness subsets | readiness audit, input-readiness scaffold | artifact and inference path missing |
| SlabCity | `blocked` | none | readiness audit | no local runner / service contract |
| GenRewrite | `preflight_only` | readiness subsets | readiness audit, input/cost scaffold | correction/verifier loop missing |
| R-Bot | `preflight_only` | readiness subsets | readiness audit, retrieval-readiness scaffold | retrieval stack missing |
| LLM-R2 | `preflight_only` | readiness subsets | readiness audit, retrieval-readiness scaffold | retrieval stack missing |
| SQLSolver | `not_integrated` | support-first readiness scope | support-readiness audit | no runner / solver wrapper |
| VeriEQL | `not_integrated` | support-first readiness scope | support-readiness audit | no runner / subset/timeout policy |

## Main audit conclusions

- Controls are fully integrated across the current expanded common-core packet.
- `SQLGLOT_OPT_SAME_DIALECT` is implemented, but its expanded PERF denominator is not uniformly closed because the optimizer boundary persists.
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` is now the strongest expanded PERF generated-method baseline after the controls:
  - execution-backed
  - checker-backed
  - speedup-scored
- Direct LLM rewrite is now closed on expanded PERF as a PostgreSQL-only checker-backed route.
- Direct LLM rewrite still does not have expanded PERF speedup evidence.
- SQLGlot Transpile and LLM Translate are both real bounded PORT baselines, but only on PostgreSQL-side evidence.
- Calcite HEP, LearnedRewrite, GenRewrite, R-Bot, LLM-R2, SQLSolver, and VeriEQL remain backlog or support lines rather than active paper-denominator baselines.

## Recommended next actions by family

- Direct LLM rewrite:
  - keep checker-backed PostgreSQL wording explicit
  - next missing piece is expanded PERF speedup
- SQLGlot optimize:
  - keep explicit capability-boundary language
- SQLGlot no-opt:
  - keep as separate baseline candidate, not optimize replacement
- PORT translation routes:
  - keep bounded PostgreSQL-side framing
- non-integrated families:
  - leave them in readiness/support backlog unless a runnable adapter path appears quickly

## Claim boundaries

- no model execution
- no SQL execution
- no checker execution
- no new metrics beyond current tracked evidence
- not a leaderboard artifact
- not a registry writeback
- not a formal review update
