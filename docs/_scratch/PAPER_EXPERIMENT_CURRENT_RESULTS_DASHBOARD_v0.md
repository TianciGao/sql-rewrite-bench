# PAPER_EXPERIMENT_CURRENT_RESULTS_DASHBOARD_v0

## Status

This is the current paper-facing experiment dashboard for the formal benchmark packet under the current pilot governance boundary.

It summarizes the current state of the formal common-core and PORT artifact stack without claiming final leaderboard closure.

## Current Results Table

| area | execution status | executable / ready rate | row-count / plan observation | checker-backed consistency status | token usage | speedup status | claim boundary |
|---|---|---:|---|---|---:|---|---|
| control routes | complete | `1.0` executable across native / human positive / hard negative | execution and control-route scoring complete | complete from existing checker artifacts | n/a | HUMAN_REFERENCE_POSITIVE PERF-only positive-control speedup complete: `GM_Speedup=0.96159127168004`, `WTL=1/2/4`, `RegressionRate@20%=0/7` | positive-control speedup only, not full leaderboard |
| SQLGlot same-dialect | complete | `1.0` parse, generation, execution | row-count match `9 / 9`; method plans `9 / 9`; plan parse `9 / 9` | `not_computed_checker_required` | n/a | not computed | row-count match is not semantic correctness |
| Direct LLM rewrite | complete from existing reports | `1.0` call, extraction, PG execution | row-count match `9 / 9`; method plans `9 / 9`; plan parse `9 / 9` | `not_computed_checker_required` | `5089` total formalized token usage | not computed | read-existing-reports formalization only, not semantic correctness |
| PORT SQLGlot Transpile | partial | preflight `3 / 3`, PG execution `2 / 3` | `PORT_0012` failed `InvalidDatetimeFormat` | not computed | n/a | not computed | not PORT closure |
| PORT LLM Translate | partial clean subset | prompt `3 / 3`, clean subset `2 / 2` | `PORT_0004` and `PORT_0022` passed; `PORT_0012` held out | not computed | `912` | not computed | clean subset only, not full denominator |

## RQ1 Correctness / Validity

- control routes checker-backed scoring is complete
- `result_consistency_rate_observed_existing_artifacts=1.0`
- `negative_rejection_rate_observed_existing_artifacts=1.0`
- `false_accept_rate_observed_existing_artifacts=0.0`
- SQLGlot execution and row-count observation are complete, but method checker-backed consistency is not computed
- Direct LLM execution and row-count observation are complete, but method checker-backed consistency is not computed
- row-count match is not semantic correctness

## RQ2 Plan Observability

- control plans present and parseable: `9 / 9`
- SQLGlot method plans collected and parseable: `9 / 9`
- Direct LLM method plans collected and parseable: `9 / 9`
- source-positive, source-negative, source-SQLGlot, and source-LLM pair readiness: `9 / 9`
- operator-delta preflight is complete from existing plans
- attribution is not computed
- HUMAN_REFERENCE_POSITIVE PERF-only positive-control speedup is complete:
  `GM_Speedup=0.96159127168004`, `Win/Tie/Loss=1/2/4`, `RegressionRate@20%=0/7`
- SQLGlot and Direct LLM speedup remain blocked from correctness-gated leaderboard scoring

Observed operator-delta highlights:

- source-SQLGlot top-node changes: `0`
- source-LLM top-node changes: `1`
- source-positive top-node changes: `2`
- source-negative top-node changes: `2`

## RQ3 Portability

- SQLGlot Transpile:
  preflight `3 / 3`, PG execution `2 / 3`
- `PORT_0012` failed with `InvalidDatetimeFormat`
- LLM Translate:
  prompt readiness `3 / 3`, clean subset `2 / 2`, total token usage `912`
- `PORT_0012` remains holdout failure-analysis / stress case

## RQ4 Coverage / Failure Slicing

- not yet fully computed
- taxonomy and failure slicing remain future work

## Completed Formal Artifacts

- control execution and scoring
- HUMAN_REFERENCE_POSITIVE PERF-only formal speedup run
- SQLGlot same-dialect execution and scoring snapshot
- Direct LLM rewrite execution and scoring snapshot
- method plan collection
- plan parse summary
- plan operator-delta preflight
- runtime observation snapshot
- PORT current results snapshot

## Missing Pieces

- SQLGlot method checker-backed consistency
- Direct LLM method checker-backed consistency
- exploratory SQLGlot / Direct LLM row-count-gated speedup appendix
- formal operator-delta summary / attribution logic
- final paper packet consolidation

## Recommended Next Primary Action

- implement the exploratory SQLGlot / Direct LLM PERF-only row-count-gated speedup appendix while keeping those routes out of the correctness-gated leaderboard

## Claim Boundaries

- no final leaderboard
- HUMAN_REFERENCE_POSITIVE speedup is positive-control only
- SQLGlot and Direct LLM speedup are not admitted into the correctness-gated leaderboard
- no admission
- no registry writeback
