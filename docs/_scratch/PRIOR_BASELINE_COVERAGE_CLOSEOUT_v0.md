# PRIOR_BASELINE_COVERAGE_CLOSEOUT_v0

## Status

This note closes out prior-baseline coverage for the current experiment state.

It is a documentation-only consolidation of the current audit and bounded evidence packets. It is not a new experiment, not a registry writeback, and not a final leaderboard.

## Boss-Requested Baseline Table

| baseline | current status | denominator / scope | metrics available | claim boundary | why not broader | next action if worth pursuing |
| --- | --- | --- | --- | --- | --- | --- |
| Native / Original SQL | `implemented` | expanded common-core PG `46` | execution, row-count, control reference | control only | not a generated prior method | maintain as control route |
| Human positive | `implemented` | expanded common-core PG `46`; speedup on PERF `7 + 19 + 11 + 4` | execution, checker-backed consistency, speedup | control only | not a learned/generated prior method | maintain as positive control |
| Hard negative | `implemented` | expanded common-core PG `46` | execution, negative rejection | guard only | not a generated prior method | maintain as guard route |
| SQLGlot optimize | `implemented` | common-core PG `43` | execution, checker on seed/common-core slices, seed speedup, failure categories | implemented but capability-bounded | optimizer failures persist on later PERF waves | keep explicit capability-boundary wording |
| SQLGlot no-opt | `implemented` | expanded PERF PG `34` | execution, checker-backed consistency, speedup | separate baseline candidate only | same-dialect no-opt route, not optimize replacement | keep as separate SQLGlot prior baseline |
| Direct LLM rewrite | `implemented_on_expanded_perf_checker_backed_and_speedup_scored` | seed common-core PG `9`; expanded PERF PG `34` | call/extract, PG execution, checker-backed consistency, seed and expanded PERF speedup, token usage | PostgreSQL-only; expanded PERF speedup near-neutral | no broader cross-engine closure, not a strong speedup result | keep wording narrow and checker-backed |
| Calcite HEP | `bounded_checker_backed_and_speedup_scored_subset` | bounded PostgreSQL PERF subset `4`: `PERF_0006`, `PERF_0008`, `PERF_0033`, `PERF_0054` | real-route generation `4/4`, PG checker consistency `4/4`, speedup `4/4`, row-count `4/4`, `GM_Speedup=0.9588741913559858`, `W/T/L=0/3/1`, `RegressionRate@20%=0.0` | bounded 4-case PostgreSQL-only subset; not final baseline | only a clean four-case slice is closed; runtime is near-neutral to mildly negative | stop at bounded subset unless a larger closure is intentionally funded |
| LearnedRewrite | `preflight_only` | readiness subsets only | readiness audit, input-readiness scaffold | no runnable evidence yet | no repo-local adapter, checkpoint, or inference path | leave in backlog unless runnable substrate appears |
| SlabCity | `blocked` | none | readiness audit only | blocked | no local runner or reproducible service/runtime contract | do not pursue until runner/contract exists |
| GenRewrite | `preflight_only` | readiness subsets only | readiness audit, input/cost scaffold | no runnable evidence yet | missing correction/verifier/executor control stack | leave in backlog unless bounded control loop is built |
| R-Bot | `preflight_only` | readiness subsets only | readiness audit, retrieval-readiness scaffold | no runnable evidence yet | missing retrieval corpus, selector, rule pool, rerank path | leave in backlog unless retrieval substrate is built |
| LLM-R2 | `preflight_only` | readiness subsets only | readiness audit, retrieval-readiness scaffold | no runnable evidence yet | missing demonstration selection and rule-application substrate | leave in backlog unless retrieval/demo substrate is built |
| SQLGlot Transpile | `partially_implemented` | PORT PG-side `6` | PG execution, policy/reference consistency, failure analysis | PostgreSQL-side portability only | not cross-engine closure; failures remain on `PORT_0012`, `PORT_0013` | keep as bounded PG-side PORT baseline |
| LLM Translate | `partially_implemented` | PORT PG-side `6` | call, extraction, PG execution, policy/reference consistency, token usage | PostgreSQL-side portability only | no cross-engine closure | keep as bounded PG-side PORT baseline |
| SQLSolver | `not_integrated` | support-first readiness scope | support-readiness audit only | verifier/support line only | no repo-local solver checkout or wrapper | leave as support-only backlog |
| VeriEQL | `bounded_support_canary_evidence` | bounded support canary `CONS_0035` only | empty constraint: `source_positive=non_equivalent`, `source_negative=non_equivalent`; report-local bridge `UNIQUE(EMPNO, DEPTNO)`: constrained `source_positive=timeout`, constrained `source_negative=non_equivalent`; `prove_count=0`; negative refutation evidence present | support/verifier only; not rewrite, not speedup, not final support-table result | positive proof is not closed under the bounded bridge experiment | keep as bounded support evidence with caveat |

## Explicit Baseline Notes

- Calcite HEP is bounded 4-case only, PostgreSQL-only, checker-backed and speedup-scored, and not a final prior baseline.
- VeriEQL is support-canary only on `CONS_0035`; it is not a rewrite baseline and not a speedup baseline.
- LearnedRewrite, GenRewrite, R-Bot, and LLM-R2 still lack runnable substrate, not just polish.
- SlabCity still lacks a local runner or reproducible service contract.
- SQLSolver still lacks a repo-local solver wrapper.

## Current Strength Of Coverage

The current experiment state is materially stronger than before:

- controls are implemented on the expanded packet
- SQLGlot no-opt is execution-backed, checker-backed, and speedup-scored on expanded PERF
- Direct LLM rewrite is execution-backed, checker-backed, and speedup-scored on expanded PERF
- Calcite HEP now has a real bounded generated-method subset with checker and speedup evidence
- VeriEQL now has real bounded verifier/support evidence beyond pure feasibility-only status

But this is still not full prior-method coverage.

## Recommended Final Claim

Recommended closeout wording:

- claim audited prior-baseline coverage
- claim implemented baselines where they are actually implemented
- claim bounded baselines where closure is only on a narrow subset
- claim explicit blocked/readiness-only status for the remaining lines

Do not claim:

- full prior-method coverage
- full runnable coverage across all boss-requested baselines
- final Calcite HEP baseline coverage
- VeriEQL rewrite or speedup coverage

The strongest accurate statement is:

- the current experiment now has audited prior-baseline coverage with a mix of implemented routes, bounded generated-method baselines, bounded verifier/support evidence, and explicitly documented blocked baselines.
