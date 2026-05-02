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

## 3. Original 24-Case Preliminary Candidate Seed Table

This table preserves the original preliminary PERF+PORT main-seed proposal.
It should not be read as the current clean health-gated common-core review denominator.

Current scratch-packet count language after human caveat review:

- original preliminary PERF+PORT main seed: `24`
- health-gated PERF+PORT keep-for-review count: `22`
- pending / not clean within PERF+PORT: `PERF_0038`
- extended-oriented within PERF+PORT: `PERF_0076`
- original total preliminary packet: `29`
- health-gated total keep-for-review count: `27`
- CONS addendum retained: `5`

| case_id | pool | source_family | proposed role | evidence/governance status | why included | blocker before final adoption | risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | canonical governed analytical baseline | human review only | low |
| `PERF_0008` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | clean join/report representative | human review only | low |
| `PERF_0013` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | stable join/aggregate denominator | human review only | low |
| `PERF_0017` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | anchor-quality grouped reporting case | human review only | low |
| `PERF_0019` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | outer-join/materialization variety within governed TPC-H | human review only | low |
| `PERF_0022` | performance | TPC-H | complexity_endpoint | staged; tri-engine; case-root result and plan governance present | richer reporting complexity without known mismatch | taxonomy / metadata cleanup needed, especially incomplete or empty `sql_feature.primary` and stale TODO-style metadata | low |
| `PERF_0024` | performance | TPC-H | performance_baseline | staged; tri-engine; case-root result and plan governance present | clean correlated-subquery coverage | human review only | low |
| `PERF_0033` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | clean governed TPC-DS starter | human review only | low |
| `PERF_0038` | performance | TPC-DS | complexity_endpoint | staged; tri-engine; case-root result and plan governance present | richer governed TPC-DS structure | pending / not clean for now; positive rewrite is effectively identical to source, so it should not currently count as a clean common-core candidate and may be reconsidered only if a real positive rewrite is added later | medium |
| `PERF_0052` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | compact CTE/decorrelation case | human review only | low |
| `PERF_0054` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | join-reorder coverage with clean evidence | human review only | low |
| `PERF_0056` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | clean decorrelation coverage | human review only | low |
| `PERF_0062` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | straightforward governed analytical case | human review only | low |
| `PERF_0063` | performance | TPC-DS | performance_baseline | staged; tri-engine; case-root result and plan governance present | string-function feature coverage inside governed TPC-DS | human review only | low |
| `PERF_0076` | performance | TPC-DS | complexity_endpoint | staged; tri-engine; case-root result and plan governance present | complexity ceiling without known mismatch | no longer counted in the clean health-gated common-core review denominator; retain as extended / characterization material because fairness is harder while plan-observability and failure-analysis value remain strong | medium |
| `PORT_0003` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | strongest null/limit portability representative | `sql_feature.primary` taxonomy exception must be resolved or explicitly documented | medium |
| `PORT_0004` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | clean MySQL-reference datetime/type case | human review only | low |
| `PORT_0006` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | clean boolean/type portability denominator | human review only | low |
| `PORT_0012` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | dense PostgreSQL-reference datetime/type case | human review only | low |
| `PORT_0013` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | clean MySQL-reference boolean/type case | human review only | low |
| `PORT_0016` | portability | PARROT | complexity_endpoint | staged; registry-backed; case-root `result_check` and `plan_check` present | date + top-1 + subquery portability coverage | complex portability endpoint; human review should check portability interpretation fairness | medium |
| `PORT_0022` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | clean datetime/type case on different schema | human review only | low |
| `PORT_0024` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | compact boolean/type denominator | human review only | low |
| `PORT_0025` | portability | PARROT | portability_baseline | staged; registry-backed; case-root `result_check` and `plan_check` present | clean top-1 datetime/limit denominator | human review only | low |

## 4. PERF Side Rationale

TPC-H and TPC-DS provide the clean governed performance core for this proposal. Their seed rows already have tri-engine result evidence, case-root plan evidence, stable provenance, and usable taxonomy structure.

The proposed PERF side is intentionally dominated by:

- governed TPC-H baselines
- governed TPC-DS baselines
- a small number of complexity endpoints

After human caveat review, two PERF rows should now be interpreted more narrowly:

- `PERF_0038` remains pending / not clean and should not currently count as a clean common-core candidate because its positive rewrite is effectively identical to source.
- `PERF_0076` should no longer be counted in the clean health-gated common-core review denominator and should instead remain visible as extended / characterization material for plan-observability and failure analysis.

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

`PORT_0003` should be kept with an explicit caveat. It remains a strong null/limit portability representative, but its `sql_feature.primary` list is empty because the current taxonomy does not provide a clean tag for that flat top-k portability shape. That taxonomy exception should be resolved or explicitly documented rather than overwritten with a weak substitute tag.

`PORT_0016` should remain in the review packet as a complex portability endpoint, with explicit human attention on portability interpretation fairness rather than being treated as a simple denominator case.

## 7. Explicit Exclusions

- `PERF_0071`–`PERF_0075`: excluded because real positive-output mismatch is still unresolved
- `PERF_0038`: remains pending / not clean and should not currently count as a clean common-core candidate until a real positive rewrite exists
- `PERF_0076`: no longer counted in the clean health-gated common-core review denominator and retained as extended / characterization material
- `PORT_0007`: excluded because it is not registry-backed and lacks current evidence closure
- LONGTAIL: excluded because it is extended-oriented for now
- CONS: kept as a separate addendum and not merged into this PERF+PORT proposal
- unregistered failed packages: excluded from this proposal

Additional caveats for human review:

- `PERF_0077` and `PERF_0082` have real-schema bridge value, but they should remain provisional until JOB/IMDB current-generation governance is backfilled.
- `PERF_0022` remains in the review packet, but taxonomy / metadata cleanup is still needed, especially around incomplete or empty `sql_feature.primary` and stale TODO-style metadata.
- `PORT_0003` remains in the seed despite empty `sql_feature.primary`; this taxonomy exception should be resolved or explicitly documented.
- `PORT_0016` remains in the seed as a complex portability endpoint and should receive explicit human review for portability interpretation fairness.
- `PERF_0071`–`PERF_0075` remain excluded due real positive-output mismatch.
- `PORT_0007` remains excluded due lack of registry-backed current evidence.
- LONGTAIL remains excluded from the common-core seed.
- CONS remains a separate addendum and is not merged into the main seed here.

## 8. Extended Set Pointer

The following groups should remain outside this preliminary seed and instead be treated as extended-oriented material:

- PERF normalization-heavy TPC-DS cases
- `PERF_0076` as extended / characterization material for plan-observability and failure analysis rather than a clean common-core denominator case
- provisional JOB/IMDB realism-stress and bridge cases pending governance backfill
- PORT portability-stress cases that are valuable but not clean enough for the seed
- LONGTAIL and CONS later as extended characterization lines after taxonomy and governance normalization

This proposal is therefore not trying to absorb all strong cases into one denominator. It is intentionally conservative.

## 9. Open Blockers

- JOB/IMDB current-generation governance backfill
- PORT taxonomy gaps for flat top-k / grouped-order cases
- `PERF_0038` still needs a real positive rewrite before it can be treated as a clean common-core candidate
- `PERF_0022` still needs taxonomy / metadata cleanup
- formal human review
- plan semantics not formally reviewed
- no admission decision yet

## 10. Possible Expansion Slate After Health Gate

This section records a human-screened possible expansion slate for later review after the health-gated review pass.
It does not change the current clean health-gated packet.
It is not admission, not promotion, not registry writeback, and not a final common-core decision.

Current count language:

- current health-gated keep-for-review count: `27`
- human-screened possible additions for later review: `8`
- next possible human-review slate: `35`

Human-screened possible additions for later review:

- PORT possible additions:
  - `PORT_0014`
  - `PORT_0018`
  - `PORT_0023`
  - `PORT_0028`
  - `PORT_0017`
- PERF possible additions:
  - `PERF_0009`
  - `PERF_0012`
  - `PERF_0014`
- CONS: none
- LONGTAIL: none

Interpretation notes:

- These are human-screened possible additions for later review only; they are not admitted, not promoted, not registry writeback, and not final common-core.
- Strong candidates within this slate:
  - `PORT_0014`
  - `PORT_0023`
  - `PERF_0009`
  - `PERF_0012`
  - `PERF_0014`
- Caveat candidates within this slate:
  - `PORT_0018`: `sql_feature.primary` is empty, so a taxonomy exception or tag fix is still needed
  - `PORT_0028`: expression-heavy; acceptable, but it should carry an explicit caveat
  - `PORT_0017`: useful for structural diversity, but it should carry an expression / column-normalization caveat
- The proposed PORT additions improve portability-risk and query-shape coverage, but all of them remain `PARROT`-derived, so they do not solve source-family concentration.
- `PORT_0005` remains a backup / possible candidate and is not part of the first 8-case slate.
- The proposed PERF additions should be interpreted as selective, evidence-strong TPC-H additions rather than a broad PERF expansion.
- CONS is not expanded because the current 5-case semantic addendum should remain compact for now.
- LONGTAIL is not actively added to common-core at this stage.

## 11. Recommended Next Step

Do not update registry yet.

Do not treat the possible expansion slate as admitted, promoted, or final common-core.

The next step is human review of:

1. the `27` health-gated keep-for-review candidates,
2. the `8` human-screened possible additions for later review,
3. the remaining caveats around `PERF_0038`, `PERF_0076`, `PERF_0022`, `PORT_0003`, and `PORT_0016`.

Only after that human review should the team decide whether to promote this scratch material into a formal review packet.

JOB/IMDB bridge backfill is not the current recommended next action and should remain deferred unless separately decided later.
