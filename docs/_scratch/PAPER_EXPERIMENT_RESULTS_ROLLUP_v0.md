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
- SQLGlot same-dialect now has full 9-case checker-backed consistency:
  - materialized cases `9 / 9`
  - checker consistent `9`
  - inconsistent `0`
  - failed `0`
  - `result_consistency_rate=1.0`
- Direct LLM rewrite now has full 9-case checker-backed consistency:
  - materialized cases `9 / 9`
  - checker consistent `9`
  - inconsistent `0`
  - failed `0`
  - `result_consistency_rate=1.0`
- checker mode for both generated routes:
  - `exact_tsv_report_local`
- row-count match is not semantic correctness

Interpretation:

- the benchmark currently has a strong correctness-control line
- full `9`-case common-core generated-method checker-backed consistency is now closed for SQLGlot and Direct LLM
- correctness-gated generated-method speedup remains a separate step

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
- SQLGlot and Direct LLM now have full 9-case checker-backed consistency
- SQLGlot and Direct LLM now also have correctness-gated PERF-only method speedup summaries from existing reruns
- full benchmark leaderboard promotion remains separate because the current generated-method speedup packet is PERF-only

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
- bounded PG route matrix confirms the same SQLGlot outcome: `2 / 3` PostgreSQL success
- PG reference consistency:
  - executable cases checked: `2`
  - consistent: `0`
  - inconsistent: `2`
  - `PORT_0012` remained blocked because SQLGlot PG execution had already failed

LLM Translate:

- prompt readiness: `3 / 3`
- clean subset execution: `2 / 2`
- passed clean cases:
  - `PORT_0004`
  - `PORT_0022`
- total token usage: `912`
- `PORT_0012` targeted Direct LLM canary command now exists
- latest targeted `PORT_0012` execute-path result:
  - `model_call_status=success`
  - `extraction_status=extracted`
  - `pg_execution_status=success`
  - `row_count=1`
  - `runtime_ms=63`
  - `token_usage_total=480`
- bounded PG route matrix:
  - model call success: `3 / 3`
  - SQL extraction success: `3 / 3`
  - PostgreSQL execution success: `3 / 3`
  - `total_token_usage=1317`
  - `PORT_0012` matrix result:
    - `pg_execution_status=success`
    - `row_count=1`
    - `token_usage_total=455`
- PG reference consistency:
  - executable route cases from existing evidence: `3`
  - checked: `2`
  - consistent: `1`
  - inconsistent: `1`
  - execution failed: `1`
  - checked-record consistency rate: `0.5`
- `PORT_0012` remains holdout failure-analysis / stress case

Interpretation:

- current RQ3 evidence is useful route-status evidence
- the targeted `PORT_0012` Direct LLM follow-up succeeded on PostgreSQL in this one-case stress canary
- the bounded PostgreSQL route matrix now also shows Direct LLM translate succeeded on all three selected PORT cases
- this suggests the targeted LLM path avoided the SQLGlot identifier-literal / datetime failure on `PORT_0012`
- contrast on `PORT_0012` is now explicit:
  - SQLGlot failed on PostgreSQL with `InvalidDatetimeFormat`
  - Direct LLM succeeded on PostgreSQL in both the targeted canary and the bounded PG route matrix
  - PG reference consistency still did not close because the current positive reference SQL failed on PostgreSQL during the LLM exact-TSV check
- exact-TSV reference checking also exposed value mismatches on executable cases:
  - SQLGlot mismatched reference output on both executable cases
  - Direct LLM matched exactly on `PORT_0004` but mismatched on `PORT_0022`
- `PORT_0012` still remains outside the clean denominator unless a separate denominator-expansion decision is taken
- the clean denominator policy may now warrant revisit, but it should not be expanded automatically from this PG-only result
- it is not full PORT closure

## RQ4 Coverage / Failure Slicing

Current remaining gaps:

- taxonomy and failure slicing are not yet fully computed
- formal operator-delta summary / attribution logic remains incomplete
- final correctness-gated generated-method leaderboard still requires explicit promotion / policy beyond the current PERF-only generated-method consistency result
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
- correctness-gated generated-method speedup table
  - SQLGlot PERF-only `GM_Speedup`, `WTL`, `RegressionRate@20%`
  - Direct LLM PERF-only `GM_Speedup`, `WTL`, `RegressionRate@20%`, token column
- bounded portability snapshot table
  - SQLGlot Transpile `3/3 -> 2/3`
  - LLM Translate clean subset `2/2`
  - `PORT_0012` holdout note plus targeted-canary success note

## Non-Claim Boundaries

- no final leaderboard
- no admission decision
- no registry writeback
- no formal review update
- SQLGlot and Direct LLM row-count match is not semantic equivalence
- SQLGlot and Direct LLM generated-method speedup is correctness-gated for PERF-only cases
- SQLGlot and Direct LLM are not admitted into a full benchmark speedup leaderboard because the current runtime packet is PERF-only
- PORT current snapshot is not full portability closure
- current PORT route-matrix evidence is PG-only, not translation correctness, and not a cross-engine matrix
- current PORT translation-consistency evidence is PG-side reference consistency only and uses exact TSV matching

## Recommended Next Use

- decide whether to keep generated-method runtime claims PERF-only for the paper body or add a separate CONS runtime policy decision packet
