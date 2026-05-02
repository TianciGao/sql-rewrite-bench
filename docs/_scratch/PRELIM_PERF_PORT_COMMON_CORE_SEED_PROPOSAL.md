# Preliminary PERF+PORT Common-Core Seed Proposal

- Status: scratch proposal / human-review packet / not admitted / not registry-backed decision / not registry writeback
- Date: 2026-05-01

## 1. Purpose

This proposal combines governed performance cases and tagged portability cases into a preliminary fair-horizontal-comparison seed.

The intent is to identify a conservative preliminary candidate seed for later human review across:

- performance baselines
- portability baselines
- governed cross-engine comparison stock

This is a proposal only. It is not admitted, not registry writeback, not a common-core promotion, and not a final benchmark-line decision. CONS remains a separate addendum and is not merged into this PERF+PORT proposal. LONGTAIL remains outside this common-core seed discussion.

## 2. Selection Principles

- tri-engine result evidence
- plan evidence
- clear source / positive / negative relation
- provenance clarity
- no known real positive-output mismatch
- taxonomy support where available
- source-family balance
- portability-risk coverage
- avoid heavy case-specific normalization in the seed

## 3. Proposed 24-Case Preliminary Candidate Seed Table

| case_id | pool | source_family | proposed role | evidence/governance status | why included | blocker before final adoption | risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | canonical governed analytical baseline | human review only | low |
| `PERF_0008` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | clean join/report representative | human review only | low |
| `PERF_0013` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | stable join/aggregate denominator | human review only | low |
| `PERF_0017` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | anchor-quality grouped reporting case | human review only | low |
| `PERF_0019` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | outer-join/materialization variety within governed TPC-H | human review only | low |
| `PERF_0022` | performance | TPC-H | complexity_endpoint | staged; tri-engine; case-root result and plan governance present | richer reporting complexity without known mismatch | later plan-semantics review | low |
| `PERF_0024` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | clean correlated-subquery coverage | human review only | low |
| `PERF_0033` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | clean governed TPC-DS starter | human review only | low |
| `PERF_0038` | performance | TPC-DS | complexity_endpoint | staged; tri-engine; case-root result and plan governance present | richer governed TPC-DS structure | human review only | low |
| `PERF_0052` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | compact CTE/decorrelation case | human review only | low |
| `PERF_0054` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | join-reorder coverage with clean evidence | human review only | low |
| `PERF_0056` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | clean decorrelation coverage | human review only | low |
| `PERF_0062` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | straightforward governed analytical case | human review only | low |
| `PERF_0063` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | string-function feature coverage inside governed TPC-DS | human review only | low |
| `PERF_0076` | performance | TPC-DS | complexity_endpoint | staged; tri-engine; case-root result and plan governance present | complexity ceiling without known mismatch | complexity makes final fairness review harder | medium |
| `PORT_0003` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | strongest null/limit portability representative | empty `sql_feature.primary` due taxonomy gap | medium |
| `PORT_0004` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | clean MySQL-reference datetime/type case | human review only | low |
| `PORT_0006` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | clean boolean/type portability denominator | human review only | low |
| `PORT_0012` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | dense PostgreSQL-reference datetime/type case | human review only | low |
| `PORT_0013` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | clean MySQL-reference boolean/type case | human review only | low |
| `PORT_0016` | portability | PARROT | complexity_endpoint | staged; registry-backed; case-root `result_check` and `plan_check` present | date + top-1 + subquery portability coverage | human review only | low |
| `PORT_0022` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | clean datetime/type case on different schema | human review only | low |
| `PORT_0024` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | compact boolean/type denominator | human review only | low |
| `PORT_0025` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | clean top-1 datetime/limit denominator | human review only | low |

## 4. PERF Side Rationale

TPC-H and TPC-DS provide the clean governed performance core for this proposal. Their seed rows already have tri-engine result evidence, case-root plan evidence, stable provenance, and usable taxonomy structure.

The proposed PERF side is intentionally dominated by:

- governed TPC-H baselines
- governed TPC-DS baselines
- a small number of complexity endpoints

This preliminary candidate seed is intentionally limited to governed PERF cases only. Real-schema bridge value from JOB/IMDB is preserved below as provisional follow-on material rather than being folded into the main 24-case seed now.

## 5. Provisional JOB/IMDB Bridge Candidates

These cases have real-schema bridge value and should remain visible in the human-review packet, but they should stay outside the main seed until JOB/IMDB current-generation governance is backfilled.

| case_id | source_family | provisional role | current evidence status | why not in main seed yet | risk |
| --- | --- | --- | --- | --- | --- |
| `PERF_0077` | JOB/IMDB | real_schema_bridge | tri-engine evidence in review-prep and registry; no current-generation case-root governance | strongest early real-schema bridge candidate, but current registry facts remain `benchmark_line=not_assessed` and `admission_status=not_assessed` | medium |
| `PERF_0082` | JOB/IMDB | real_schema_bridge | tri-engine evidence in review-prep and registry; no current-generation case-root governance | useful second bridge case with join/materialize value, but still outside the governed current-generation PERF set | medium |

## 6. PORT Side Rationale

PORT contributes the portability denominator that PERF alone cannot provide. The proposed PORT rows are chosen to keep the set interpretable, registry-backed, and evidence-complete while still covering both PostgreSQL-reference and MySQL-reference directions.

The selected PORT cases jointly cover:

- `datetime_semantics_gap`
- `type_semantics_gap`
- `boolean_semantics_gap`
- `null_semantics_gap`
- `limit_fetch_gap`
- `identifier_quoting`

`PORT_0003` should be kept with an explicit caveat. It remains a strong null/limit portability representative, but its `sql_feature.primary` list is empty because the current taxonomy does not provide a clean tag for that flat top-k portability shape. That is a taxonomy gap, not a reason to overwrite the case with a weak substitute tag.

## 7. Explicit Exclusions

- `PERF_0071`–`PERF_0075`: excluded because real positive-output mismatch is still unresolved
- `PORT_0007`: excluded because it is not registry-backed and lacks current evidence closure
- LONGTAIL: excluded because it is extended-oriented for now
- CONS: kept as a separate addendum and not merged into this PERF+PORT proposal
- unregistered failed packages: excluded from this proposal

Additional caveats for human review:

- `PERF_0077` and `PERF_0082` have real-schema bridge value, but they should remain provisional until JOB/IMDB current-generation governance is backfilled.
- `PORT_0003` remains in the seed despite empty `sql_feature.primary`; this is treated as a taxonomy gap, not a case defect.
- `PERF_0071`–`PERF_0075` remain excluded due real positive-output mismatch.
- `PORT_0007` remains excluded due lack of registry-backed current evidence.
- LONGTAIL remains excluded from the common-core seed.
- CONS remains a separate addendum and is not merged into the main seed here.

## 8. Extended Set Pointer

The following groups should remain outside this preliminary seed and instead be treated as extended-oriented material:

- PERF normalization-heavy TPC-DS cases
- provisional JOB/IMDB realism-stress and bridge cases pending governance backfill
- PORT portability-stress cases that are valuable but not clean enough for the seed
- LONGTAIL and CONS later as extended characterization lines after taxonomy and governance normalization

This proposal is therefore not trying to absorb all strong cases into one denominator. It is intentionally conservative.

## 9. Open Blockers

- JOB/IMDB current-generation governance backfill
- PORT taxonomy gaps for flat top-k / grouped-order cases
- formal human review
- plan semantics not formally reviewed
- no admission decision yet

## 10. Recommended Next Step

Do not update registry yet.

If the team wants real-schema bridge cases in the seed, the recommended next action is a small JOB/IMDB governance backfill feasibility-to-execution step focused on current-generation case-root result and plan governance for a narrow bridge batch.

Otherwise, wait for human review of this proposal and keep it as a scratch proposal only.
