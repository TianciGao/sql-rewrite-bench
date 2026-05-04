# PAPER_EXPERIMENT_CURRENT_RESULTS_DASHBOARD_v0

## Status

This is the current paper-facing experiment dashboard for the formal benchmark packet under the current pilot governance boundary.

It summarizes the current state of the formal common-core and PORT artifact stack without claiming final leaderboard closure.

## Current Results Table

| area | execution status | executable / ready rate | row-count / plan observation | checker-backed consistency status | token usage | speedup status | claim boundary |
|---|---|---:|---|---|---:|---|---|
| control routes | complete | `1.0` executable across native / human positive / hard negative | execution and control-route scoring complete | complete from existing checker artifacts | n/a | HUMAN_REFERENCE_POSITIVE PERF-only positive-control speedup complete: `GM_Speedup=0.96159127168004`, `WTL=1/2/4`, `RegressionRate@20%=0/7` | positive-control speedup only, not full leaderboard |
| SQLGlot same-dialect | complete | `1.0` parse, generation, execution | row-count match `9 / 9`; method plans `9 / 9`; plan parse `9 / 9` | PERF-only checker-backed consistency now computed: `7 / 7`, `rate=1.0`; full 9-case common-core still not closed | n/a | exploratory PERF-only appendix complete: `GM=0.9709643241218479`, `WTL=1/2/4`, `RegressionRate@20%=0/7` | PERF-only checker-backed consistency plus exploratory speedup appendix; not full leaderboard |
| Direct LLM rewrite | complete from existing reports | `1.0` call, extraction, PG execution | row-count match `9 / 9`; method plans `9 / 9`; plan parse `9 / 9` | PERF-only checker-backed consistency now computed: `7 / 7`, `rate=1.0`; full 9-case common-core still not closed | `5089` total formalized token usage | exploratory PERF-only appendix complete: `GM=1.0023345046000625`, `WTL=1/5/1`, `RegressionRate@20%=0/7` | PERF-only checker-backed consistency plus exploratory speedup appendix; not full leaderboard |
| PORT SQLGlot Transpile | partial | preflight `3 / 3`, PG execution `2 / 3` | `PORT_0012` failed `InvalidDatetimeFormat` | not computed | n/a | not computed | not PORT closure |
| PORT LLM Translate | partial clean subset | prompt `3 / 3`, clean subset `2 / 2` | `PORT_0004` and `PORT_0022` passed; `PORT_0012` held out | not computed | `912` | not computed | clean subset only, not full denominator |

## RQ1 Correctness / Validity

- control routes checker-backed scoring is complete
- `result_consistency_rate_observed_existing_artifacts=1.0`
- `negative_rejection_rate_observed_existing_artifacts=1.0`
- `false_accept_rate_observed_existing_artifacts=0.0`
- SQLGlot now has PERF-only checker-backed consistency from report-local materialization: `7 / 7`, `rate=1.0`
- Direct LLM now has PERF-only checker-backed consistency from report-local materialization: `7 / 7`, `rate=1.0`
- SQLGlot and Direct LLM still do not have full 9-case common-core generated-method checker-backed consistency because `CONS_0007` and `CONS_0012` remain outside this PERF-only run
- row-count match is not semantic correctness
- SQLGlot and Direct LLM exploratory appendix speedup now exists for PERF-only cases, but it remains row-count-gated and not correctness-gated

## RQ2 Plan Observability

- control plans present and parseable: `9 / 9`
- SQLGlot method plans collected and parseable: `9 / 9`
- Direct LLM method plans collected and parseable: `9 / 9`
- source-positive, source-negative, source-SQLGlot, and source-LLM pair readiness: `9 / 9`
- operator-delta preflight is complete from existing plans
- attribution is not computed
- HUMAN_REFERENCE_POSITIVE PERF-only positive-control speedup is complete:
  `GM_Speedup=0.96159127168004`, `Win/Tie/Loss=1/2/4`, `RegressionRate@20%=0/7`
- SQLGlot PERF-only exploratory appendix:
  `GM=0.9709643241218479`, `Win/Tie/Loss=1/2/4`, `RegressionRate@20%=0/7`
- Direct LLM PERF-only exploratory appendix:
  `GM=1.0023345046000625`, `Win/Tie/Loss=1/5/1`, `RegressionRate@20%=0/7`, `token_usage=4487`
- SQLGlot and Direct LLM still remain blocked from correctness-gated leaderboard scoring

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
- SQLGlot / Direct LLM exploratory PERF-only speedup appendix
- method plan collection
- plan parse summary
- plan operator-delta preflight
- runtime observation snapshot
- PORT current results snapshot

## Missing Pieces

- SQLGlot full 9-case generated-method checker-backed consistency
- Direct LLM full 9-case generated-method checker-backed consistency
- formal operator-delta summary / attribution logic
- final paper packet consolidation

## Recommended Next Primary Action

- decide whether to build route-specific checker-backed consistency artifacts or keep SQLGlot and Direct LLM speedup in appendix only

## Claim Boundaries

- no final leaderboard
- HUMAN_REFERENCE_POSITIVE speedup is positive-control only
- SQLGlot and Direct LLM appendix speedup is exploratory and row-count-gated only
- SQLGlot and Direct LLM speedup are not admitted into the correctness-gated leaderboard
- no admission
- no registry writeback
