# Common-core v0 40 Same-Engine 120 Route Contract v1

This is a reviewable Stage-0 rerun contract draft for the
`common_core_v0_40_same_engine_120` campaign.

It is not a final leaderboard.
It does not update `method_comparison_summary_v2`.
It does not change checker policy, denominator policy, or benchmark admission
status.

## Scope

Track A rerun target in this draft is:

- same-engine rewrite only
- `40` common-core cases
- `3` same-engine targets per case: PostgreSQL / MySQL / Spark
- expected total: `120` planned rows
- denominator family: `common_core_v0_40_same_engine_120`

The case list is frozen by:

- [common_core_v0_final_denominator.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/curation/common_core_v0_final_denominator.csv)

## Methods In Scope

The following methods are in Track A rerun scope for Stage-0 planning:

- `direct_llm_same_engine_rewrite`
- `sqlglot_optimize_same_dialect`
- `sqlglot_transpile_same_dialect_noop`
- `calcite_hep`
- `r_bot`
- `learnedrewrite`
- `llm_r2`

Interpretation:

- some methods already have retained same-engine `120` route evidence
- some methods require scaffold recovery before a new same-engine `120` rerun
- some methods currently support correctness-only or PG-oriented evidence and
  therefore remain denominator-aware but not timing-closed

## Methods Excluded From Rewrite Rerun Scope For Now

The following methods are excluded from the Track A rewrite rerun campaign in
this draft:

- `sqlsolver`
- `verieql`

Reason:

- both are currently treated as support or verifier methods
- neither should be mixed into rewrite rerun rows unless later separately
  reclassified under explicit review

## Portability Track Exclusion

The following routes are excluded from Track A same-engine rerun scope:

- `sqlglot_cross_dialect_transpile`
- `llm_translate`

Reason:

- these are Track C portability routes
- they are not same-engine rewrite rows
- their denominators, claims, and timing semantics are not the same as Track A

## Route Distinctions That Must Remain Explicit

### SQLGlot

- `sqlglot_optimize_same_dialect` and
  `sqlglot_transpile_same_dialect_noop` are retained route-specific `120` rows
- they are not automatically method-family aggregate evidence
- a route-level rerun, if later approved, must preserve route identity and
  route-specific denominator labels

### Calcite HEP

- `calcite_hep` currently has retained `120`-row correctness evidence through a
  fail-closed ledger
- it does not currently have a full `120`-row timing packet
- any future rerun contract must keep correctness-only and timing-eligible
  layers separate until a timing policy is explicitly closed

### R-Bot

- `r_bot` currently has PG-oriented subset evidence and bounded non-PG boundary
  evidence only
- it is in scope for planning because a same-engine `120` generation package
  exists, but it is not yet `120`-ready

### LearnedRewrite and LLM-R2

- both remain bounded prior-method PG-only evidence today
- neither may be treated as tri-engine same-engine `120` evidence in this
  contract draft
- both require route or runner scaffold recovery before a later rerun stage

## Stage-0 Contract Output

This draft is intended to freeze only:

- denominator selection
- case expansion into `120` planned rows
- method in-scope versus out-of-scope boundaries
- route identity boundaries
- failure-accounting contract prerequisites

It does not authorize:

- database execution
- SQL generation
- execution checking
- timing measurement
- speedup reporting
- leaderboard publication

## Review Boundary

This contract remains reviewable by a human before it becomes any
source-of-truth rerun instruction.

Until reviewed:

- retained evidence remains the only valid evidence source
- proposed rerun scope remains planning-only
- `leaderboard_comparable` remains unchanged for all methods
