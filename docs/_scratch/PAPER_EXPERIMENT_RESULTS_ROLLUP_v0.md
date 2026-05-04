# PAPER_EXPERIMENT_RESULTS_ROLLUP_v0

## Status

This is a tracked scratch rollup of the current paper-facing formal experiment results.

It consolidates existing formal common-core and PORT results only.

It does not add new execution evidence.

## Input Basis

- `docs/_scratch/PAPER_EXPERIMENT_CURRENT_RESULTS_DASHBOARD_v0.md`
- `docs/_scratch/FORMAL_COMMON_CORE_EXPLORATORY_METHOD_SPEEDUP_APPENDIX_v0.md`
- `docs/_scratch/FORMAL_PORT_CURRENT_RESULTS_SNAPSHOT_v0.md`

## RQ1 Correctness / Validity

Current formal common-core correctness state:

- control routes checker-backed scoring is complete
- `result_consistency_rate_observed_existing_artifacts=1.0`
- `negative_rejection_rate_observed_existing_artifacts=1.0`
- `false_accept_rate_observed_existing_artifacts=0.0`
- SQLGlot same-dialect formal execution is complete with row-count match `9 / 9`
- Direct LLM rewrite formal execution is complete with row-count match `9 / 9`
- SQLGlot and Direct LLM still do not have route-specific checker-backed method consistency
- row-count match is not semantic correctness

Interpretation:

- the benchmark currently has a strong correctness-control line
- generated-method validity remains execution-plus-row-count evidence, not checker-backed closure

## RQ2 Plan Observability And Runtime

Current common-core plan-observability state:

- control plans present and parseable: `9 / 9`
- SQLGlot method plans collected and parseable: `9 / 9`
- Direct LLM method plans collected and parseable: `9 / 9`
- source-positive, source-negative, source-SQLGlot, and source-LLM pair readiness: `9 / 9`
- operator-delta preflight exists from existing plans
- observed top-node changes:
  - source-positive: `2`
  - source-negative: `2`
  - source-SQLGlot: `0`
  - source-LLM: `1`
- attribution is not computed

Current runtime / speedup state:

- `HUMAN_REFERENCE_POSITIVE` PERF-only positive-control speedup is complete
- `case_count=7`
- `GM_Speedup=0.96159127168004`
- `Win/Tie/Loss=1/2/4`
- `RegressionRate@20%=0/7`
- SQLGlot PERF-only exploratory appendix:
  - `GM=0.9709643241218479`
  - `Win/Tie/Loss=1/2/4`
  - `RegressionRate@20%=0/7`
- Direct LLM PERF-only exploratory appendix:
  - `GM=1.0023345046000625`
  - `Win/Tie/Loss=1/5/1`
  - `RegressionRate@20%=0/7`
  - `total_token_usage=4487`

Interpretation:

- positive-control speedup now exists as a bounded formal runtime result
- SQLGlot and Direct LLM runtime appendix results exist, but remain row-count-gated exploratory material only
- correctness-gated generated-method leaderboard speedup remains blocked

## RQ3 Portability

Current bounded PORT status:

- clean denominator:
  - `PORT_0004`
  - `PORT_0022`
- holdout:
  - `PORT_0012`

SQLGlot Transpile:

- preflight parse + transpile: `3 / 3`
- PostgreSQL execution: `2 / 3`
- `PORT_0012` failed with `InvalidDatetimeFormat`

LLM Translate:

- prompt readiness: `3 / 3`
- clean subset execution: `2 / 2`
- passed clean cases:
  - `PORT_0004`
  - `PORT_0022`
- total token usage: `912`
- `PORT_0012` remains holdout failure-analysis / stress case

Interpretation:

- current RQ3 evidence is useful route-status evidence
- it is not full PORT closure

## RQ4 Coverage / Failure Slicing

Current remaining gaps:

- taxonomy and failure slicing are not yet fully computed
- route-specific checker-backed method consistency for SQLGlot is missing
- route-specific checker-backed method consistency for Direct LLM is missing
- formal operator-delta summary / attribution logic remains incomplete
- correctness-gated generated-method speedup leaderboard is not available
- final paper packet consolidation remains incomplete

## Draftable Paper Tables

The following paper-facing tables can now be drafted from existing artifacts:

- control-route correctness table
  - native / human positive / hard negative execution and checker-backed consistency
- common-core generated-method execution table
  - SQLGlot and Direct LLM execution success, row-count observation, token usage for LLM
- plan observability readiness table
  - source / positive / negative / SQLGlot / LLM plan availability and parse readiness
- operator-delta observation table
  - source-positive, source-negative, source-SQLGlot, source-LLM top-node and node-type deltas
- positive-control speedup table
  - HUMAN_REFERENCE_POSITIVE PERF-only `GM_Speedup`, `WTL`, `RegressionRate@20%`
- exploratory appendix speedup table
  - SQLGlot PERF-only row-count-gated appendix
  - Direct LLM PERF-only row-count-gated appendix with token column
- bounded portability snapshot table
  - SQLGlot Transpile `3/3 -> 2/3`
  - LLM Translate clean subset `2/2`
  - `PORT_0012` holdout note

## Non-Claim Boundaries

- no final leaderboard
- no admission decision
- no registry writeback
- no formal review update
- SQLGlot and Direct LLM row-count match is not semantic equivalence
- SQLGlot and Direct LLM appendix speedup is exploratory and row-count-gated only
- SQLGlot and Direct LLM are not admitted into the correctness-gated speedup leaderboard
- PORT current snapshot is not full portability closure

## Recommended Next Use

- use this rollup as the paper-drafting index for current results, while keeping correctness-gated generated-method consistency and final leaderboard language out of scope until those artifacts exist
